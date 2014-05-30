from tribal.util import const
from sqlalchemy import and_
from sqlalchemy import desc
from sqlalchemy import asc
from sqlalchemy import or_

class QueryExtend():
    
    def __init__(self, cls, result, ** kw):
        self.cls = cls
        self.result = result
        self.kw = kw

    def query(self, queryType, queryList):
        (cls, result, kw) = (self.cls, self.result, self.kw)
        def getQueryKw():
            queryDict = {}
            for i in queryList:
                if isinstance(i, list) or isinstance(i, tuple):
                    if len(i) == 3:
                        value = (kw.get(i[1], ''), kw.get(i[2], ''))
                    else:
                        value = kw.get(i[0], kw.get(i[1], ''))
                    if value:
                        queryDict.update({i[0]:value})
                elif isinstance(i, str) or isinstance(v, unicode):
                    value = kw.get(i, '')
                    if value:
                        queryDict.update({i:value})
            return queryDict

        if queryType == const.QUERY_TYPE_LIKE:
            for k, v in getQueryKw().iteritems():
                result = result.filter(getattr(cls, k).ilike('%%%s%%' % v))
        elif queryType == const.QUERY_TYPE_EQ:
            for k, v in getQueryKw().iteritems():
                result = result.filter(getattr(cls, k) == v)
        elif queryType == const.QUERY_TYPE_IN:
            for k, v in getQueryKw().iteritems():
                if isinstance(v, str) or isinstance(v, unicode):
                    result = result.filter(getattr(cls, k).in_([int(i) for i in v.split(',')]))
                else:
                    result = result.filter(getattr(cls, k).in_(v))
        elif queryType == const.QUERY_TYPE_NOT_IN:
            for k, v in getQueryKw().iteritems():
                if isinstance(v, str) or isinstance(v, unicode):
                    result = result.filter(~ getattr(cls, k).in_([int(i) for i in v.split(',')]))
                else:
                    result = result.filter(~ getattr(cls, k).in_(v))
        elif queryType == const.QUERY_TYPE_DATE:
            for k, v in getQueryKw().iteritems():
                if len(v) == 2 and v[0]:
                    result = result.filter(getattr(cls, k) >= dt.strptime(v[0] + "00:00:00", "%Y-%m-%d%H:%M:%S"))
                if len(v) == 2 and v[1]:
                    result = result.filter(getattr(cls, k) <= dt.strptime(v[1] + "23:59:59", "%Y-%m-%d%H:%M:%S"))
        elif queryType == const.QUERY_TYPE_ORDER_BY:
            asc_orders = [v for k, v in getQueryKw().iteritems()]
            for i in asc_orders:
                (_asc, _order) = i.split('-')
                if _asc == 'asc':
                    result = result.order_by(asc(getattr(cls, _order)))
                else:
                    result = result.order_by(desc(getattr(cls, _order)))
        result = result.filter(cls.active==0)
        self.result = result
        return result
