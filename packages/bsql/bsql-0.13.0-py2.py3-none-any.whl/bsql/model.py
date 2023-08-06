
DEBUG = True

import logging
LOG = logging.getLogger(__name__)

import datetime
import datetime, re, sys
from bl.id import random_id
from bl.dict import Dict
from bl.string import String
from bxml.xml import XML, etree
from bxml.builder import Builder

from .record import Record
from .recordset import RecordSet

class Model(Record):
    """abstract base class for database models to inherit from, holds shared functionality.

    # -- Use an in-memory sqlite3 database for testing: --
    >>> from bsql.database import Database
    >>> db = Database()
    >>> db.execute("create table model_test (id integer primary key autoincrement, name varchar)")

    # -- Example usage: --
    >>> class Temp(Model):                      # set up a temporary model
    ...     relation = 'model_test'
    ...     pk = ['id']
    ...
    >>> t = Temp(db)                            # new instance
    >>> t.name = 'something temporary'          # set an attribute
    >>> t.insert()                              # insert a new record
    >>> t                                       # values are reloaded from the insert
    {'id': 1, 'name': 'something temporary'}
    >>> t.name = "another thing"                # edit an attribute
    >>> t.commit()                              # update the record in the database
    >>> t
    {'id': 1, 'name': 'another thing'}
    >>> t1 = t.select_one(id=t.id)              # get the full record
    >>> t1
    {'id': 1, 'name': 'another thing'}
    >>> t2 = Temp(db)
    >>> t2.name = 'thing 2'
    >>> t2.insert()
    >>> ts = t.select(); len(ts)                # there are two records
    2
    >>> ts = t.select(name='thing 2')
    >>> len(ts)                                 # only one such record
    1
    >>> t1.delete()                             # delete a record
    >>> ts = t.select(); len(ts)                # there is now one record
    1

    -- The rest is teardown: --
    >>> db.execute("drop table model_test")
    """

    relation = None     # the database relation with which this model deals primarily
    pk = ['id']         # fields that make up the primary key of a record
                        #   is there a way to do this by introspection at instance init?
    where = None        # only include records that match this where clause.
                        #   often used to have multiple classes in one table (i.e., single-table inheritance)

    def __init__(self, db, **args):
        Record.__init__(self, db, **args)
        if self.relation is None: 
            self.__dict__['relation'] = String(self.__class__.__name__).identifier().lower() + 's'

    def to_one(self, other_class, self_key=None, other_key=None, to_fields=['*'], 
                     update=False, cache_field=None, orderby=None, **kwargs):
        """returns a record based on the fk fields in this relation."""
        # make sure we have a valid record
        for k in self.pk:
            if self.get(k) is None: return None
        
        if self_key is None: 
            self_key = ["%s_%s" % (other_class.__name__.lower(), fk) for fk in other_class.pk]
        if other_key is None: other_key = other_class.pk
        if cache_field is None: cache_field = other_class.__name__

        for k in self_key:
            if self.get(k) is None: return None

        if update==True or self.__dict__.get(cache_field)==None:
            # get the record from the db
            wherelist = []
            if self.where is not None: 
                wherelist += [self.where]
            fields = list(zip(self_key, other_key))
            for field in fields:
                wherelist.append("%s=%s" % (field[1], self.quote(self[field[0]])))
            wherecl = " and ".join(wherelist)
            attr = ','.join(to_fields)
            if orderby is not None:
                selexpr = """other_class(self.db).select_one(attr="%s", where="%s", orderby="%s", **kwargs)""" % (attr, wherecl, orderby)
            else:
                selexpr = """other_class(self.db).select_one(attr="%s", where="%s", **kwargs)""" % (attr, wherecl)
            self.__dict__[cache_field] = eval(selexpr)
        return self.__dict__[cache_field]

    def to_many(self, other_class, 
                self_key=None, other_key=None, update=False, cache_field=None, 
                orderby=None, where=None, **kwargs):
        """return a set of records from a foreign class that key to this instance."""
        # make sure we have a valid record
        for k in self.pk:
            if self.get(k) is None: return RecordSet()
        
        if self_key is None: self_key = self.pk
        if other_key is None: 
            other_key = ["%s_%s" % (self.__class__.__name__.lower(), fk) for fk in self.pk]
        if cache_field is None: cache_field = other_class.__name__

        for k in self_key:
            if self.get(k) is None: return RecordSet()

        if update==True or self.__dict__.get(cache_field)==None:
            # get the records from the database, however many there are
            wherelist = []
            if self.where is not None: wherelist += [self.where]
            fields = list(zip(self_key, other_key))
            for field in fields:
                wherelist.append(" %s=%s " % (field[1], self.quote(self[field[0]])))
            wherecl = " and ".join(wherelist)
            if where not in ['', None]: 
                LOG.debug("where = %r" % where)
                wherecl += " and %s " % where
            if orderby is not None:
                selexpr = """other_class(self.db).select(where="%s", orderby="%s", **kwargs)""" % (wherecl, orderby)
            else:
                selexpr = """other_class(self.db).select(where="%s", **kwargs)""" % (wherecl)
            self.__dict__[cache_field] = eval(selexpr) or RecordSet()
        rs = RecordSet()
        for r in self.__dict__[cache_field] or []:
            rs.append(r)
        return rs

    def to_many_through(self, other_class, through_relation, through_fields, 
                        self_key=None, other_key=None, to_fields=['*'], 
                        also_select=[], cache_field=None, update=False, 
                        orderby=None, where=None, limit=None, offset=0, **kwargs):
        """return a set of records from a foreign class that key to this instance, 
        through a relationship table."""
        # make sure we have a valid record
        for k in self.pk:
            if self.get(k) is None: return RecordSet()
        
        if self_key is None: self_key = self.pk
        if other_key is None: 
            other_key = other_class.pk
        if cache_field is None: cache_field = other_class.__name__
        
        for k in self_key:
            if self.get(k) is None: return RecordSet()

        if update==True or self.__dict__.get(cache_field)==None:
            # add the relation names to the field names in each field list -- avoid ambiguity in the query
            self_key = ["%s.%s" % (self.relation, field) for field in self_key]
            other_key = ["%s.%s" % (other_class.relation, field) for field in other_key]
            through_fields = ["%s.%s" % (through_relation, field) for field in through_fields]

            # create lists for the inner joins
            onself = [" %s=%s " % field for field in zip(self_key, through_fields)]                      # uses the first set of fields in through_fields
            onforeign = [" %s=%s " % field for field in zip(other_key, through_fields[len(onself):])]  # uses the rest of the fields in through_fields

            # build the query
            sql = "select " + ", ".join(["%s.%s" % (other_class.relation, field) for field in to_fields])
            if type(also_select)==list and len(also_select) > 0:
                sql += ", " + ', '.join(also_select)
            elif type(also_select)==str and len(also_select)> 0:
                sql += ', ' + also_select
            sql+= " from %s" % other_class.relation
            sql+= "\n inner join %s on %s" % (through_relation, " and ".join(onforeign))
            sql+= "\n inner join %s on %s" % (self.relation, " and ".join(onself))
            sql+= "\n where %s" % " and ".join(["%s=%s" % (field, self.quote(self[field.split('.')[1]])) for field in self_key])
            if where not in ['', None]: 
                sql += " and %s " % where
            if orderby in ['', None]: orderby = ",".join(other_class.pk)
            sql += "\n order by %s" % orderby            
            if limit not in [0, None]: sql += " limit %d" % int(limit)
            if offset != 0 and type(offset) == int:
                sql += " offset %d " % offset
            
            # select and cache the data
            self.__dict__[cache_field] = self.db.select(sql, Record=other_class)
        rs = RecordSet()
        for r in self.__dict__[cache_field] or RecordSet():
            rs.append(r)
        return rs

    def prepare_query(self, attr='*', from_expr=None, where="", vals=None, orderby="", limit=None, offset=0, **kwargs):
        if from_expr is None: from_expr = self.relation
        if vals is None: vals = []
        if limit not in [0, None] and self.db.servername() == 'sqlserver':
            sql = "select top %d %s from %s" % (limit, attr, from_expr)
        else:
            sql = "select %s from %s" % (attr, from_expr)
        if where not in ["", None] or len(kwargs)>0: 
            wheresql, wherevals = self.where_from_args(where, **kwargs)
            if wheresql != "":
                sql += " where " + wheresql
                vals += wherevals

        if orderby not in ["", None]:
            sql += """ order by %s """ % orderby
        elif len(self.pk) > 0:       # default to using pk for orderby
            sql += """ order by %s """ % ', '.join(self.pk)
        if limit not in [0, None] and self.db.servername() != 'sqlserver': 
            sql += " limit %d" % int(limit)

        if offset != 0:
            if type(offset) == int:
                sql += " offset %d " % offset
            elif type(offset) in [str, str] and re.match("[0-9]+", offset) is not None:
                sql += " offset %s " % offset
        return sql, vals

    def selectgen(self, attr='*', from_expr=None, where="", vals=None, orderby="", limit=None, offset=0, cursor=None, **kwargs):
        """select records from relation"""
        sql, vals = self.prepare_query(attr=attr, from_expr=from_expr, where=where, vals=vals, orderby=orderby, limit=limit, offset=offset, **kwargs)
        results = self.db.selectgen(sql, vals=vals, Record=self.__class__, cursor=cursor)
        for result in results:
            result.after_select()
            yield result

    def select(self, attr='*', from_expr=None, where="", vals=None, orderby="", limit=None, offset=0, cursor=None, **kwargs):
        """select records from relation"""
        sql, vals = self.prepare_query(attr=attr, from_expr=from_expr, where=where, vals=vals, orderby=orderby, limit=limit, offset=offset, **kwargs)
        records = self.db.selectgen(sql, vals=vals, Record=self.__class__, cursor=cursor)
        results = RecordSet()
        for result in records:
            result.after_select()
            results.append(result)
        return results

    def select_one(self, attr='*', from_expr=None, where="", vals=None, orderby="", offset=0, cursor=None, **kwargs):
        """select one record from relation"""
        results = self.selectgen(attr=attr, from_expr=from_expr, where=where, vals=vals, orderby=orderby, limit=1, offset=offset, **kwargs)
        try:
            result = results.__next__()
        except StopIteration:
            result = None
        return result

    def select_as_dict(self, attr='*', from_expr=None, where="", vals=None, orderby="", cursor=None, **kwargs):
        """returns the SELECT results as a dict, with the keys being tuples of the model's pk."""
        records = self.select(attr=attr, from_expr=from_expr, where=where, vals=vals, orderby=orderby, cursor=cursor, **kwargs)
        d = Dict()
        for record in records:
            d[record.pk_as_tuple()] = record
        return d
            
    def where_from_args(self, where=None, **kwargs):
        wherelist=[]
        wherevals = []
        if where!='' and where is not None: wherelist.append(where)
        for k in kwargs:
            wherelist.append("%s=%%s" % k)
            wherevals.append(kwargs[k])
        wheresql = " and ".join(wherelist)
        return  wheresql, wherevals

    def pk_as_tuple(self):
        """return a tuple with the values of self.pk -- can be used as a dict key."""
        key=()  
        for k in self.pk:
            key = key + (self[k],)
        return key

    def execute(self, sql, vals=None, cursor=None):
        return self.db.execute(sql, vals=vals, cursor=cursor)

    def exists(self, cursor=None):
        return self.select_one(cursor=cursor, 
            **{k:self[k] for k in self.pk}) is not None

    def insert(self, reload=True, cursor=None, **kwargs):
        """insert the current instance into its relation."""
        for k in list(kwargs.keys()): self[k] = kwargs[k]
        self.before_insert_or_update()
        self.before_insert()
        keys = self.keys()
        vals = self.values()
        if 'sqlite' in self.db.servername().lower():
            vals_markers = ["?" for v in vals]
        else:
            vals_markers = ["%s" for v in vals]
        q = "insert into %s (%s) values (%s)" % (
                self.relation, ','.join(keys), ','.join(vals_markers))
        if 'postgres' in self.db.servername().lower(): 
            q += " returning *"
            d = self.db.select_one(q, vals=vals, cursor=cursor)
        else:
            d = self.db.execute(q, vals=vals, cursor=cursor)
        if reload==True:
            if 'sqlite' in self.db.servername().lower():
                d = self.db.select_one("select * from %s where ROWID=last_insert_rowid()" % self.relation)
            elif 'postgres' not in self.db.servername().lower() \
            and None not in [self.get(k) for k in self.pk]:    # local pk is filled
                whereargs = {}
                for k in self.pk:
                    whereargs[k] = self.get(k)
                wherecl, wherevals = self.where_from_args(**whereargs)
                d = self.db.select_one("select * from %s where %s" % (self.relation, wherecl), vals=wherevals)
            for k in list((d or {}).keys()): self[k] = d[k]
        if cursor is None:
            self.db.commit()
        self.after_insert()
        self.after_insert_or_update()

    def insert_safe(self, cursor=None, **args):
        try:
            self.insert(**args)
        except:
            return sys.exc_info()[1].args[0]        

    def insert_if_none(self, reload=True, cursor=None):
        """insert the current instance if it's not there."""
        if self.select_one(cursor=cursor, **self) is None:
            return self.insert(reload=reload)

    def reload(self, **kwargs):
        """reload the current instance from the database."""
        al = []
        if kwargs != {}:
            d = kwargs
            for k in list(d.keys()):
                al.append("%s=%s" % (k, self.quote(d[k])))
        else:
            for k in self.pk:
                al.append("%s=%s" % (k, self.quote(self[k])))
        i = self.select_one(where=" and ".join(al))
        if i is not None:
            for k in list(i.keys()):
                self[k] = i[k]
        else:
            del(self)

    def commit(self, reload=True, fields=[], cursor=None, **kwargs):
        """update this instance's record in its relation."""

        self.before_insert_or_update()
        self.before_update()

        # start with the list of fields 
        if fields==[]:
            keys = self.keys()
        else:
            keys = fields
        vals = [self[k] for k in keys]

        # merge keys & values from kwargs
        for k, v in kwargs.items():
            if k not in keys:
                keys.append(k)
                vals.append(v)
            else:
                i = keys.index(k)
                vals[i] = v

        # make attribute list
        al = []
        for k in keys:
            al.append("%s=%%s" % (k))

        # join pk to indicate which record to update.
        pl = []
        for k in self.pk:
            pl.append("%s=%%s" % (k))
            vals.append(self[k])
        where = ' and '.join(pl)

        # perform the update
        sql = "update %s set %s where %s" % (self.relation, ', '.join(al), where)
        self.db.execute(sql, vals=vals, cursor=cursor)

        # update the local instance
        for i in range(len(keys)):
            self[keys[i]] = vals[i]

        self.after_update()
        self.after_insert_or_update()
        if reload==True: self.reload()

    def commit_safe(self, cursor=None, **args):
        try:
            self.commit(cursor=cursor, **args)
        except:
            return sys.exc_info()[1].args[0]        

    def insert_or_update(self, reload=True, cursor=None, **kwargs):
        pksel = {k:self.get(k) for k in self.pk}
        if None not in pksel.values() and self.select_one(**pksel) is not None:
            self.commit(reload=reload, cursor=cursor, **kwargs)
        else:
            self.insert(reload=reload, cursor=cursor, **kwargs)

    def delete(self, where=None, vals=None, cursor=None):
        """delete the current instance from its relation -- must be up-to-date to do w/o where clause."""
        self.before_delete()
        if vals is None: vals = []
        if where==None:
            where, addvals = self.where_from_args(**{k:self[k] for k in self.pk})
            vals += addvals
        self.db.execute("delete from %s where %s" % (self.relation, where), vals=vals, cursor=cursor)
        for k in list(self.keys()):
            self.pop(k)
        self.after_delete()
        del(self)

    def delete_safe(self, where=None, vals=None, cursor=None, **args):
        try:
            self.delete(where=where, vals=vals, cursor=cursor, **args)
        except:
            return sys.exc_info()[1].args[0]

    def quote(self, attr):
        return self.db.quote(attr)

    # overloadable methods serve as callbacks in the CRUD operations
    
    def before_insert_or_update(self): pass    
    def after_insert_or_update(self): pass    
    def before_insert(self): pass    
    def after_insert(self): pass    
    def before_update(self): pass    
    def after_update(self): pass    
    def before_delete(self): pass        
    def after_delete(self): pass
    def after_select(self): pass

    # import 

    @classmethod
    def from_element(Class, db, element):
        """convert an (xml) element into an instance. Rules:
        * The element attributes are primary key values
        * The element children tags are keys, texts are values
        """
        record = Class(db, **element.attrib)
        for ch in [ch for ch in element.xpath("*") if ch.text not in [None, '']]:
            tag = re.sub("^\{[^\}]*\}", "", ch.tag)
            record[tag] = ch.text
        return record

    @classmethod
    def xml(Class, record, builder=None):
        if builder is None: builder = Builder()._
        elem = builder(Class.relation, **{k:str(record[k]) for k in Class.pk})
        for k in [k for k in record.keys() if k not in Class.pk]:
            elem.append(builder(k, str(record[k] or '')))
        return elem
        
    @classmethod
    def xml_set(Class, recordset, builder=None):
        if builder is None: builder = Builder()._
        root = builder(Class.relation + '-set')
        for record in recordset: 
            root.append(Class.xml(record, builder=builder))
        return root




if __name__ == "__main__":
    import doctest
    doctest.testmod()
