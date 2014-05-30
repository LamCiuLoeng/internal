# -*- coding: utf-8 -*-

from tribal.model import *

__all__ = ["getCutNo"]

def getCutNo():
    headers = DBSession.query(TRBHeaderPO).all()
    
    return headers