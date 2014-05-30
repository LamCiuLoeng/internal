# -*- coding: utf-8 -*-
"""The application's model objects"""
from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

# Global session manager: DBSession() returns the Thread-local
# session object appropriate for the current web request.


#===============================================================================
# test by cl
#===============================================================================
import sqlalchemy
from datetime import date, datetime as dt
from sqlalchemy.orm.session import SessionExtension
from sqlalchemy.orm import attributes, object_mapper

DB_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

class LogSessionExtension(SessionExtension):
    def before_flush(self, session, flush_context, instances):
        print "_^" * 30
        print "Come into my log session extension"
        print "_*" * 30
        log = []
        for obj in session.dirty:
            obj_mapper = object_mapper(obj)
            obj_state = attributes.instance_state(obj)
            for om in obj_mapper.iterate_to_root():
                for obj_col in om.local_table.c:
                    try:
                        prop = obj_mapper.get_property_by_column(obj_col)
                    except UnmappedColumnError:
                        continue

                    try:
                        need2log = obj_col.info["auto_log"]
                    except:
                        continue
                    else:
                        if not need2log : continue

                    if prop.key not in obj_state.dict:
                        getattr(obj, prop.key)

                    history = attributes.get_history(obj, prop.key)
                    if not history.has_changes():continue

                    a, u, d = history

                    if d:
                        attr_old_value = d[0]
                    elif u:
                        attr_old_value = u[0]
                    else:
                        attr_old_value = ""

                    attr_new_value = a[0] or ""

                    if not self._isUpdateReally(obj_col, attr_old_value, attr_new_value) : continue
                    _old, _new = self._2string(obj_col, attr_old_value, attr_new_value)
                    log.append((obj_col.info.get("field_name", prop.key), _old, _new))
        if log :

            print log


    def _isUpdateReally(self, col, old_value, new_value):
        if not old_value and not new_value : return False

        if not (old_value and new_value) : return True

        if isinstance(col.type, sqlalchemy.types.Integer): return old_value == int(new_value)

        if isinstance(col.type, sqlalchemy.types.Float): return old_value == float(new_value)

        if isinstance(col.type, (sqlalchemy.types.Unicode, sqlalchemy.types.String)): return unicode(old_value) == unicode(new_value)

        if isinstance(col.type, (sqlalchemy.types.Date, sqlalchemy.types.DateTime)) : return old_value == dt.strptime(new_value, DB_DATE_FORMAT)

#        if isinstance(prop.type, sqlalchemy.types.Boolean) : return old_value == bool(new_value)
        return False

    def _2string(self, col, old_value, new_value):
        if isinstance(col.type, sqlalchemy.types.Integer): return (old_value or '', new_value or '')

        if isinstance(col.type, sqlalchemy.types.Float): return (old_value or '', new_value or '')

        if isinstance(col.type, (sqlalchemy.types.Unicode, sqlalchemy.types.String)): return (old_value or "", new_value or "")

        if isinstance(col.type, (sqlalchemy.types.Date, sqlalchemy.types.DateTime)) :
            _o = "" if not old_value else old_value.strftime(DB_DATE_FORMAT)
            _n = new_value or ""
            return (_o, _n)

        return (old_value, new_value)





# maker = sessionmaker(autoflush = True, autocommit = False,
#                     extension = [ LogSessionExtension(), ZopeTransactionExtension(), ])
maker = sessionmaker(autoflush = True, autocommit = False,
                     extension = ZopeTransactionExtension())
DBSession = scoped_session(maker)

# Base class for all of our model classes: By default, the data model is
# defined with SQLAlchemy's declarative extension, but if you need more
# control, you can switch to the traditional method.
DeclarativeBase = declarative_base()

# There are two convenient ways for you to spare some typing.
# You can have a query property on all your model classes by doing this:
# DeclarativeBase.query = DBSession.query_property()
# Or you can use a session-aware mapper as it was used in TurboGears 1:
# DeclarativeBase = declarative_base(mapper=DBSession.mapper)

# Global metadata.
# The default metadata is the one from the declarative base.
metadata = DeclarativeBase.metadata

# If you have multiple databases with overlapping table names, you'll need a
# metadata for each database. Feel free to rename 'metadata2'.
# metadata2 = MetaData()

#####
# Generally you will not want to define your table's mappers, and data objects
# here in __init__ but will want to create modules them in the model directory
# and import them at the bottom of this file.
#
######

def init_model(engine):
    """Call me before using any of the tables or classes in the model."""
    engine.dialect.supports_sane_rowcount = False
    DBSession.configure(bind = engine)
    # If you are using reflection to introspect your database and create
    # table objects for you, your tables must be defined and mapped inside
    # the init_model function, so that the engine is available if you
    # use the model outside tg2, you need to make sure this is called before
    # you use the model.

    #
    # See the following example:

    # global t_reflected

    # t_reflected = Table("Reflected", metadata,
    #    autoload=True, autoload_with=engine)

    # mapper(Reflected, t_reflected)

# Import your model modules here.
from tribal.model.auth import User, Group, Permission
from tribal.model.sportsware import *
from tribal.model.orsay import *
from tribal.model.orchestra import *
from tribal.model.sample import *
# from tribal.model.pei import *
from tribal.model.sysutil import *
from tribal.model.dba import *
from tribal.model.bby import *
from tribal.model.tag import *
# from tribal.model.cabelas import *
from tribal.model.lemmi import *
from tribal.model.tmw import *
from tribal.model.mglobalpack import *
from tribal.model.prepress import *
