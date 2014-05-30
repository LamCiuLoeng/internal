# -*- coding: utf-8 -*-
'''
Created on 2012-2-1

@author: cl.lam
'''
from urlparse import urlparse
from functools import wraps
from tg import session,request

__all__ = ['paginate_addition']

class paginate_addition(object):
    def __init__(self,path):
        self.path = path
        
    def __call__(self,f):
        @wraps(f)
        def wrapper(s,**kw):
            if urlparse(request.referer or '').path != self.path:
                try:
                    kw = session['xkw']
                    request.paginate_page = session['xpage']
                    request.paginate_params = kw
                except:
                    pass
            else:
                session['xkw'] = kw
                session['xpage'] = request.paginate_page
                session.save()
            return f(s,**kw)
        return wrapper

