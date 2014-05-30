import traceback
from datetime import datetime as dt
from sqlalchemy.sql import *
from tribal.model import *
import tribal.model as db

__all__ = ["getMaxVersion", "assignJobNo", "getMaster", "getPackagingFormat", "getComponent"]

def getMaxVersion():
    try:
        return DBSession.query(func.max(BBYWorkflowConfig.version)).scalar() or 1
    except:
        traceback.print_exc()
    return 1


def assignJobNo(id):
    return "JN%s%.5d" % (dt.now().strftime("%Y%m%d"), id)


def getMaster(name):
    master = getattr(db, name)
    return DBSession.query(master).filter(master.active == 0).order_by(master.name).all()

def getPackagingFormat():
    return DBSession.query(BBYPackagingFormat).filter(BBYPackagingFormat.active == 0).filter(BBYPackagingFormat.is_component < 2).order_by(BBYPackagingFormat.name).all()

def getComponent():
    return DBSession.query(BBYPackagingFormat).filter(BBYPackagingFormat.active == 0).filter(BBYPackagingFormat.is_component != 1).order_by(BBYPackagingFormat.name).all()
