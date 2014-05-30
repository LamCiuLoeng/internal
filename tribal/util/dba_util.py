# -*- coding: utf-8 -*-
from tribal.model import *
from dateutil import rrule
import datetime

def returnQty(itemId, orderId):
    try:
        orderDetail = DBSession.query(DBAOrderDetail) \
                    .filter(DBAOrderDetail.header_id==orderId) \
                    .filter(DBAOrderDetail.item_id == itemId).first()
        if orderDetail:
            return dict(
                        commited_qty=orderDetail.commited_qty,
                        input_commited_qty=orderDetail.input_commited_qty,
                        forecast_qty=orderDetail.forecast_qty,
                        input_forecast_qty=orderDetail.input_forecast_qty)
        else:
            return dict(
                        commited_qty='',
                        input_commited_qty='',
                        forecast_qty='',
                        input_forecast_qty='')
    except:
        return dict(
                    commited_qty='',
                    input_commited_qty='',
                    forecast_qty='',
                    input_forecast_qty='')



def nextMonth(d):
    mo = d.month
    yr = d.year
    mo += 1
    if mo > 12:
        mo = 1
        yr += 1
    return datetime.date(yr, mo, 1).strftime('%b/%Y')


def returnCatId(cat_name):
    try:
        cat_id = DBSession.query(DBAItemCategory.id).filter(
                        and_(DBAItemCategory.active==0,
                            DBAItemCategory.__table__.c.name.op('ilike')("%%%s%%" %cat_name))
                        ).first()
        return cat_id[0]
    except:
        return None



def workdays(start, end, holidays=0, days_off=None):
    if days_off is None:
        days_off = 5, 6              # 默认：周六和周日
    workdays = [x for x in range(7) if x not in days_off]
    days = rrule.rrule(rrule.DAILY, dtstart=start, until=end, byweekday=workdays)
    return days.count( ) - holidays 