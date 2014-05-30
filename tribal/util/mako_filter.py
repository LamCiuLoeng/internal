# -*- coding: utf-8 -*-
import json
import traceback
from datetime import datetime as dt
import urllib


__all__ = ["b", "pd", "pt", "tp", "cd", "jd", "ue", ]

b = lambda v:"&nbsp;" if not v or v == 'Null' else v
pd = lambda v, len = 10:"&nbsp;" if not v else str(v)[0:len]
pt = lambda v, len = 19:"&nbsp;" if not v else str(v)[0:len]

jd = lambda v : json.dumps(v)
jl = lambda v : json.loads(v)


def tp(v):
    if not v : return "&nbsp;"
    return "<span class='tooltip' title='%s'>%s</span>" % (v, v)

# cound the day
def cd(v):
    try:
        return (dt.now() - v).days
    except:
        traceback.print_exc()
        return ""

def ue(v):
    try:
        return urllib.unquote(v)
    except:
        return v

