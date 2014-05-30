# -*- coding: utf-8 -*-
from datetime import datetime as dt
from tg import config
from tgscheduler import start_scheduler
from tgscheduler.scheduler import add_interval_task, add_monthly_task, add_weekday_task

from tribal.model import *
from tribal.util.common import sendEmail

from sqlalchemy.sql import *
from tribal.util.oracle_helper import *
import transaction

__all__ = ["dbaEmailNotify"]

def dbaEmailNotify():
    start_scheduler()

    #add_monthly_task(action = _emailNotifyOn18th, monthdays = (18,), timeonday = (9, 30)) #send on 9:30AM on every month's 18
    #add_monthly_task(action = _emailNotifyOn20th, monthdays = (20,), timeonday = (9, 30)) #send on 9:30AM on every month's 20
    #add_monthly_task(action = _emailNotifyOn23rd, monthdays = (23,), timeonday = (9, 30)) #send on 9:30AM on every month's 23
    #add_monthly_task(action = _emailNotifyOn25th, monthdays = (25,), timeonday = (9, 30)) #send on 9:30AM on every month's 25
    
    add_weekday_task(action=_getDeliveryDate, weekdays=range(1,8), timeonday=(23, 59))
    
    #add_interval_task(action=_getDeliveryDate, interval = 60*3)

#    add_interval_task(action = _emailNotifyOn13rd, interval = 60*3)
#
#    add_interval_task(action = _emailNotifyOn15th, interval = 60*3)


#: get erp Delivery Date
def _getDeliveryDate():
    orders = DBSession.query(DBAOrderInfo).filter(
                            and_(DBAOrderInfo.active==0,
                            DBAOrderInfo.delivery_date==None
                            )).order_by(DBAOrderInfo.id).all()
    if orders:
        pos = "\'%s\'" % "\',\'".join([o.po.strip().upper() for o in orders])

        sql = '''
            select UPPER(tsh.CUST_PO_NO), min(tdrh.DELIVERY_DATE) DR_DATE from t_sales_contract_hdr tsh, t_delivery_request_hdr tdrh 
            where tsh.COMPANY_CODE in ('RPACEU', 'RPACPACKEU') and UPPER(tsh.CUST_PO_NO) in (%s)   
            and tsh.SALES_CONTRACT_NO=tdrh.SO_NO(+) 
            group by UPPER(tsh.CUST_PO_NO)
        ''' % pos

        try:
            db_conn = createConnection()
            cursor = db_conn.cursor()
            cursor.execute(str(sql))
            result = cursor.fetchall()
            result_dict = {}
            for row in result:
                result_dict[row[0]] = row[1]
            for order in orders:
                delivery_date = result_dict.get(order.po.strip().upper(), '')
                if delivery_date:
                    order.delivery_date = delivery_date.date()
            
        except:
            traceback.print_exc()
        else:
            transaction.commit() 
        finally:
            cursor.close()


###################################
# DIM (5-25)
###################################
def _emailNotifyOn23rd():
    send_from = "r-track@r-pac.com"
    cc_to = config.get("dba_notify_email_cc", "").split(";")
    subject = "r-track(DIM) Online Ordering Reminder for DBA vendors"
    text = ["Dear Customers,", "\n",
          "Please kindly note that r-track(DIM) online ordering system will be closed on %s 25. If you would like to place or revise the orders, please log in the system as soon as possible. Otherwise, the delivery will not be on time next month." % dt.now().strftime("%B"),
          "If you have any difficulties on online ordering, please do not hesitate to contact our Account Executive." , "\n",
          "Thanks for your orders.", "\n",
          "Please do not reply this email.",
          ]

    for email_address in _getAllEmail():
        if email_address : sendEmail(send_from, email_address, subject, "\n".join(text), cc_to)


def _emailNotifyOn25th():
    send_from = "r-track@r-pac.com"
    cc_to = config.get("dba_notify_email_cc", "").split(";")
    subject = "r-track(DIM) Online Ordering Closing for DBA vendors"
    text = ["Dear Customers,", "\n",
          "Please kindly note that r-track(DIM) online ordering system will be closed today in mid-night 12:00 (HK time). No online ordering can be done on tomorrow.",
          "If you would like to place or revise the orders, please log in the system today. Otherwise, the delivery will not be on time next month.",
          "If you have any difficulties on online ordering, please do not hesitate to contact our Account Executive." , "\n",
          "Thanks for your orders.", "\n",
          "Please do not reply this email.",
          ]

    for email_address in _getAllEmail():
        if email_address : sendEmail(send_from, email_address, subject, "\n".join(text), cc_to)


###################################
# PLAYTEX / WONDERBRA / SHOCK ABSORBER (5-20)
###################################
def _emailNotifyOn18th():
    send_from = "r-track@r-pac.com"
    cc_to = config.get("dba_notify_email_cc", "").split(";")
    subject = "r-track(PLAYTEX / WONDERBRA / SHOCK ABSORBER) Online Ordering Reminder for DBA vendors"
    text = ["Dear Customers,", "\n",
          "Please kindly note that r-track(PLAYTEX / WONDERBRA / SHOCK ABSORBER) online ordering system will be closed on %s 20. If you would like to place or revise the orders, please log in the system as soon as possible. Otherwise, the delivery will not be on time next month." % dt.now().strftime("%B"),
          "If you have any difficulties on online ordering, please do not hesitate to contact our Account Executive." , "\n",
          "Thanks for your orders.", "\n",
          "Please do not reply this email.",
          ]

    for email_address in _getAllEmail():
        if email_address : sendEmail(send_from, email_address, subject, "\n".join(text), cc_to)


def _emailNotifyOn20th():
    send_from = "r-track@r-pac.com"
    cc_to = config.get("dba_notify_email_cc", "").split(";")
    subject = "r-track(PLAYTEX / WONDERBRA / SHOCK ABSORBER) Online Ordering Closing for DBA vendors"
    text = ["Dear Customers,", "\n",
          "Please kindly note that r-track(PLAYTEX / WONDERBRA / SHOCK ABSORBER) online ordering system will be closed today in mid-night 12:00 (HK time). No online ordering can be done on tomorrow.",
          "If you would like to place or revise the orders, please log in the system today. Otherwise, the delivery will not be on time next month.",
          "If you have any difficulties on online ordering, please do not hesitate to contact our Account Executive." , "\n",
          "Thanks for your orders.", "\n",
          "Please do not reply this email.",
          ]

    for email_address in _getAllEmail():
        if email_address : sendEmail(send_from, email_address, subject, "\n".join(text), cc_to)

def _getAllEmail():
    result = []
    for c in DBSession.query(DBACustomer).filter(DBACustomer.active == 0).all():
        if c.email_address:
            result.append([e.strip() for e in c.email_address.split("/") if e.strip()])

    return result
