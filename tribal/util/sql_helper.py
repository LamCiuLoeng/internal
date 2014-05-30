# -*- coding: utf-8 -*-
import json, traceback
from datetime import datetime as dt, date
import sqlalchemy.types as types
from sqlalchemy.types import Integer, Unicode, TypeDecorator, TypeEngine, MutableType

__all__ = ["CheckBoxCol", 'MultiTextCol', "MultiDateCol", "JSONCol", ]

class CheckBoxCol(types.TypeDecorator):
    impl = types.Unicode

    def process_bind_param(self, value, dialect):
        if not value : return None
        if isinstance(value, basestring) : return value
        if type(value) == list : return "|".join(sorted(value))  # make sure the same value save the same
        return None

    def process_result_value(self, value, dialect):
        if not value : return None
        return value.split("|")

    def compare_values(self, x, y):  # x new value, y come from copy value]
        if x is None and y is None : return True
        if x is None or y is None : return False

        if isinstance(x, basestring) : x = [x]
        if isinstance(y, basestring) : x = [y]

        tmp_x = sorted(x)
        tmp_y = sorted(y)

        return tmp_x == tmp_y


class MultiTextCol(types.TypeDecorator):
    impl = types.Text

    def process_bind_param(self, value, dialect):
        if not value : return None
        if isinstance(value, basestring) : return value
        if type(value) == list : return ','.join(value)  # make sure the same value save the same
        return None

    def process_result_value(self, value, dialect):
        return value.strip('{}') if value else None


class MultiDateCol(types.TypeDecorator):
    impl = types.Unicode

    _date_format = "%Y-%m-%d"

    def process_bind_param(self, value, dialect):
        if not value : return None
        if isinstance(value, basestring) : return value
        if type(value) == list : return "|".join(value)
        return None

    def process_result_value(self, value, dialect):
        if not value : return None
        return map(lambda v:dt.strptime(v, self._date_format), value.split("|"))


class JSONCol(MutableType, types.TypeDecorator):
    impl = types.Unicode

    def process_bind_param(self, value, dialect):
        if value is None: return None
        return json.dumps(value, ensure_ascii = False)

    def process_result_value(self, value, dialect):
        try:
            return json.loads(str(value))
        except:
#            traceback.print_exc()
            return None

    def compare_values(self, x, y):  # x new value, y come from copy value
        return x == y

    def is_mutable(self): return True

    def copy_value(self, value):
        return None

