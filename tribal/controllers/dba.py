# -*- coding: utf-8 -*-

import os, shutil, traceback, random
from datetime import datetime as dt, date
import time
# turbogears imports
from tg import expose
from tg import redirect, validate, flash, config
from tg.decorators import *

# third party imports
#from pylons.i18n import ugettext as _
from repoze.what import predicates, authorize
from repoze.what.predicates import not_anonymous, in_group, has_permission

# project specific imports
from tribal.lib.base import BaseController
#from tribal.model import DBSession, metadata
from tribal.model import *
from sqlalchemy.sql import *

from tribal.util.common import *
from tribal.util.excel_helper import *
from tribal.util.dba_util import returnCatId, workdays

from tribal.widgets import *
from tribal.widgets.dba import *
from tribal.widgets.master import *


class DBAController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    allow_only=authorize.not_anonymous()

    @expose('tribal.templates.dba.index')
    @paginate('collections', items_per_page = 20)
    @tabFocus(tab_type = "main")
    def index(self, **kw):
        ####category: DIM
        kw.setdefault('category_id', returnCatId('DIM'))
        #####
        add_items=[]
        id_list = []
        input_add_qty_list = {}
        add_qty_list = {}
        input_forecast_qty_list = {}
        forecast_qty_list = {}
        customer=''
        if request.identity["user"].groups and request.identity["user"].groups[0].dba_profiles:
                customer = request.identity["user"].groups[0].dba_profiles[0].customer

        if kw.get('old_ids', ''):
            id_list = kw.get('old_ids', '').split('_')
            input_add_qty = kw.get('h_input_add_qty', '').split('_')
            add_qty = kw.get('h_add_qty', '').split('_')
            input_forecast_qty = kw.get('h_input_forecast_qty', '').split('_')
            forecast_qty = kw.get('h_forecast_qty', '').split('_')

            for index, id in enumerate(id_list):
                input_add_qty_list.setdefault(id, input_add_qty[index])
                add_qty_list.setdefault(id, add_qty[index])
                input_forecast_qty_list.setdefault(id, input_forecast_qty[index])
                forecast_qty_list.setdefault(id, forecast_qty[index])

        if kw.get('ids', ''):
            """
            if not in_group("Admin") and not in_group("DBA_AE"):
                day = int(dt.now().day)
                if day < 5 or day > 25:
                    flash('Only allowed to place the orders between 5th–25th each month!', "warn")
                    redirect("/dba/index")
            """
            add_items = DBAItem.find_by(** {'in_ids':kw.get('ids', [])})
            
                
        result_items = DBAItem.find_by(**kw)

        if result_items and customer:
            result_items = [i for i in result_items if i in customer.items]
        return dict(
                    kw = kw,
                    item_search_form = item_search_form,
                    add_items = add_items,
                    customer = customer,
                    hidden_po = kw.get('hidden_po', ''),
                    hidden_sob = kw.get('hidden_sob', ''),
                    collections = result_items,
                    id_list = id_list,
                    input_add_qty_list = input_add_qty_list,
                    add_qty_list = add_qty_list,
                    input_forecast_qty_list = input_forecast_qty_list,
                    forecast_qty_list = forecast_qty_list
                    )

    @expose('tribal.templates.dba.order_form_update')
    @paginate('collections', items_per_page = 20)
    @tabFocus(tab_type = "main")
    def updateOrder(self, **kw):
        (flag, id)=rpacDecrypt(kw.get("code", ""))
        if not flag:
            flash("Please don't access the resource illegally!")
            redirect("/dba/search")

        """
        if not in_group("Admin") and not in_group("DBA_AE"):
            day = int(dt.now().day)
            if day < 5 or day > 25:
                flash('Only allowed to revise the orders between 5th–25th each month!', "warn")
                redirect("/dba/viewOrder?code=%s" % kw.get("code", ""))
        """
        order=getOr404(DBAOrderInfo, id)

        if order.active==1:
            flash("The Order has been canceled!", "warn")
            redirect("/dba/search")
        elif len(order.details)<1:
            flash("There's no detail related to this order!", "warn")
            redirect("/dba/search")

        kw.setdefault('category_id', returnCatId('DIM'))
        add_items=[]
        id_list = []
        input_add_qty_list = {}
        add_qty_list = {}
        input_forecast_qty_list = {}
        forecast_qty_list = {}

        customer=''
        customer=order.customer

        if kw.get('old_ids', ''):
            id_list = kw.get('old_ids', '').split('_')
            input_add_qty = kw.get('h_input_add_qty', '').split('_')
            add_qty = kw.get('h_add_qty', '').split('_')
            input_forecast_qty = kw.get('h_input_forecast_qty', '').split('_')
            forecast_qty = kw.get('h_forecast_qty', '').split('_')

            for index, id in enumerate(id_list):
                input_add_qty_list.setdefault(id, input_add_qty[index])
                add_qty_list.setdefault(id, add_qty[index])
                input_forecast_qty_list.setdefault(id, input_forecast_qty[index])
                forecast_qty_list.setdefault(id, forecast_qty[index])


        """
        if kw.get('a', '') and not kw.get('ids', ''):
            add_items=[d.item for d in order.details if 0==d.active]
            kw['ids']=','.join([str(d.item.id) for d in order.details if 0==d.active])
        el"""
        add_items=[d.item for d in order.details if 0==d.active]
        if kw.get('ids', ''):
            add_items=DBAItem.find_by(** {'in_ids':kw.get('ids', '')})
        else:
            add_items = []

        return dict(
                    kw = kw,
                    item_search_form = item_search_form,
                    add_items = add_items,
                    customer = customer,
                    hidden_po = order.po,
                    hidden_sob = kw.get('hidden_sob', order.sob),
                    collections = DBAItem.find_by(**kw),
                    order = order,
                    id_list = id_list,
                    input_add_qty_list = input_add_qty_list,
                    add_qty_list = add_qty_list,
                    input_forecast_qty_list = input_forecast_qty_list,
                    forecast_qty_list = forecast_qty_list
                    )

    @expose()
    def save_updateOrder(self, **kw):
        #print kw
        orderId=kw.get('orderId', '')
        id_list=self._returnList(kw.get('add_id', []))
        copy_id_list=id_list
        id_list=[int(id) for id in id_list]
        input_qty_list=self._returnList(kw.get('input_add_qty', []))
        qty_list=self._returnList(kw.get('add_qty', []))
        input_forecast_qty_list=self._returnList(kw.get('input_forecast_qty', []))
        forecast_qty_list=self._returnList(kw.get('forecast_qty', []))
        DBSession.begin(subtransactions = True)
        try:
            order=DBSession.query(DBAOrderInfo).get(orderId)
            order.bill_to=kw.get('bill_to', '')
            order.ship_to=kw.get('ship_to', '')
            order.sob = kw.get('sob', '').strip()
            #order.update_by_id = request.identity["user"].user_id
            order.update_time = dt.now()
            is_special = False
            if kw.get('ship_date', False):
                order.ship_date = kw.get('ship_date', '')
                if workdays(date.today(), date(*time.strptime(order.ship_date, '%Y-%m-%d')[:3]))-2 < 15:
                    is_special = True
            DBSession.flush()
            details=[d for d in order.details if 0==d.active]
            #orderDetail_list=[]

            if len(details)>0:
                for index, d in enumerate(details):
                    if d.item_id in id_list:
                        details[index].commited_qty=int(qty_list[id_list.index(d.item_id)])
                        details[index].forecast_qty=int(forecast_qty_list[id_list.index(d.item_id)])
                        details[index].input_commited_qty=int(input_qty_list[id_list.index(d.item_id)])
                        details[index].input_forecast_qty=int(input_forecast_qty_list[id_list.index(d.item_id)])
                        log = DBALog(order=order, order_detail=d)
                        log.action_type = u'update'
                        log.remark = u'%s Order is revised for %spcs;' % (Date2Text(order.update_time, '%d-%b-%Y'), qty_list[id_list.index(d.item_id)])
                        DBSession.add(log)
                        del qty_list[id_list.index(d.item_id)]
                        del forecast_qty_list[id_list.index(d.item_id)]
                        del input_qty_list[id_list.index(d.item_id)]
                        del input_forecast_qty_list[id_list.index(d.item_id)]
                        id_list.remove(d.item_id)
                    else:
                        details[index].active=1
                        log = DBALog(order=order, order_detail=d)
                        log.action_type = u'delete'
                        log.remark = u'%s Order is revised for cancel item %s ;' % (Date2Text(order.update_time, '%d-%b-%Y'), details[index].item.item_code)
                        DBSession.add(log)

                #print id_list
                if id_list:
                    for index, id in enumerate(id_list):
                        orderDetail=DBAOrderDetail(header = order)
                        orderDetail.commited_qty=int(qty_list[index])
                        orderDetail.forecast_qty=int(forecast_qty_list[index])
                        orderDetail.input_commited_qty=int(input_qty_list[index])
                        orderDetail.input_forecast_qty=int(input_forecast_qty_list[index])
                        orderDetail.item_id=int(id)
                        DBSession.add(orderDetail)
                        DBSession.flush()
                        log = DBALog(order=order, order_detail=orderDetail)
                        log.action_type = u'insert'
                        log.remark = u'%s Order is placed for %spcs;' % (Date2Text(order.update_time, '%d-%b-%Y'), qty_list[index])
                        DBSession.add(log)
                        #orderDetail_list.append(orderDetail)
                    #DBSession.add_all(orderDetail_list)
                DBSession.commit()
                send_to = [e.strip() for e in order.customer.email_address.split("/") if e.strip()]
                self._emailOrderCompleted(order.po, send_to)
                if is_special: #Send the email to EU office and HK office
                    self._emailUrgentRequest(order.po, request.identity["user"].user_name, kw.get('ship_date', ''),
                                        Date2Text(dt.now(), '%Y-%m-%d'))
        except:
            traceback.print_exc()
            DBSession.rollback()
            flash("The service is not avaiable now,please try it later or contact the system administator.", "warn")
            raise
        else:
            if is_special:
                flash('This order will be considered as "special request" and the requested delivery date will have to be validated by r-pac.',
                    status = "warn")
            else:
                flash("The order has been updated successfully!")
            redirect("/dba/viewOrder?code=%s"%rpacEncrypt(order.id))
        redirect("/dba/index")



    @expose()
    def cancelOrder(self, **kw):
        try:
            order=getOr404(DBAOrderInfo, kw.get("orderId", ""))
            if order:
                DBSession.begin(subtransactions = True)
                order.active=1
                if order.details:
                    for d in order.details:
                        if 0==d.active:
                            d.active=1
                DBSession.commit()

        except:
            traceback.print_exc()
            DBSession.rollback()
            flash("Cancel Order fail!")
            redirect("/dba/updateOrder?a=u&code=%s"%rpacEncrypt(kw.get("orderId", "")))
        else:
            flash("The order has been canceled successfully!")
            redirect("/dba/search")


    @expose()
    def saveOrder(self, **kw):
        #print kw
        customer_id=''
        if request.identity["user"].groups and request.identity["user"].groups[0].dba_profiles:
                customer_id=request.identity["user"].groups[0].dba_profiles[0].customer.id
        po=kw.get('po', '').strip()
        sob=kw.get('sob', '').strip()
        id_list=self._returnList(kw.get('add_id', []))
        input_qty_list=self._returnList(kw.get('input_add_qty', []))
        qty_list=self._returnList(kw.get('add_qty', []))
        input_forecast_qty_list=self._returnList(kw.get('input_forecast_qty', []))
        forecast_qty_list=self._returnList(kw.get('forecast_qty', []))
        DBSession.begin(subtransactions = True)
        try:
            if customer_id and po and id_list and qty_list and forecast_qty_list:
                order=DBAOrderInfo()
                order.po=po
                order.sob=sob
                order.customer_id=int(customer_id)
                order.bill_to=kw.get('bill_to', '')
                order.ship_to=kw.get('ship_to', '')
                is_special = False
                if kw.get('ship_date', False):
                    order.ship_date = kw.get('ship_date', '')
                    if workdays(date.today(), date(*time.strptime(order.ship_date, '%Y-%m-%d')[:3]))-2 < 15:
                        is_special = True
                DBSession.add(order)
                DBSession.flush()
                orderDetail_list=[]
                for index, id in enumerate(id_list):
                    orderDetail=DBAOrderDetail(header = order)
                    orderDetail.input_commited_qty=int(input_qty_list[index])
                    orderDetail.commited_qty=int(qty_list[index])
                    orderDetail.input_forecast_qty=int(input_forecast_qty_list[index])
                    orderDetail.forecast_qty=int(forecast_qty_list[index])
                    orderDetail.item_id=int(id)
                    orderDetail_list.append(orderDetail)
                DBSession.add_all(orderDetail_list)
                DBSession.flush()
                #log
                if order and order.details:
                    details = order.details
                    for d in details:
                        log = DBALog(order=order, order_detail=d)
                        log.action_type = u'insert'
                        log.remark = u'%s Order is placed for %spcs;' % (Date2Text(order.create_time, '%d-%b-%Y'), d.commited_qty)
                        DBSession.add(log)
                    
                DBSession.commit()
            else:
                raise
        except:
            traceback.print_exc()
            DBSession.rollback()
            flash("The service is not avaiable now,please try it later or contact the system administator.", "warn")
            raise
        else:
            send_to = [e.strip() for e in order.customer.email_address.split("/") if e.strip()]
            self._emailOrderCompleted(po, send_to)
            if is_special:
                flash('This order will be considered as "special request" and the requested delivery date will have to be validated by r-pac.',
                    status = "warn")
                # Send the email to EU office and HK office
                self._emailUrgentRequest(po, request.identity["user"].user_name, kw.get('ship_date', ''),
                                        Date2Text(dt.now(), '%Y-%m-%d'))
            """
            else:
                flash("Your order will be available for delivery around mid of %s. \
            If any inconvenience with this ready date please contact Hong Kong Account Executive." % dt.now().strftime('%B'), status = "warn")
            """
            redirect("/dba/viewOrder?code=%s"%rpacEncrypt(order.id))
        redirect("/dba/index")



    @expose('tribal.templates.dba.order_form_view')
    @paginate('orderDetails', items_per_page = 20)
    @tabFocus(tab_type = "view")
    def viewOrder(self, **kw):
        (flag, id)=rpacDecrypt(kw.get("code", ""))
        if not flag:
            flash("Please don't access the resource illegally!")
            redirect("/dba/search")

        order=getOr404(DBAOrderInfo, id)

        if order.active==1:
            flash("The Order has been canceled!", "warn")
            redirect("/dba/search")
        elif len(order.details)<1 :
            flash("There's no detail related to this order!", "warn")
            redirect("/dba/search")

        return dict(order = order,
                    orderDetails = [d for d in order.details if 0==d.active],
                    ids = ','.join([str(d.item_id) for d in order.details if 0==d.active])
                    )


    @expose('tribal.templates.dba.search')
    @paginate('collections', items_per_page = 20)
    @tabFocus(tab_type = "view")
    def search(self, **kw):
        try:
            search_form=order_view_form

            if kw:
                kw.setdefault('category_id', returnCatId('DIM'))
                result=self._query_result(kw)

                return dict(search_form = search_form, collections = result, values = kw)
            else:
                return dict(search_form = search_form, collections = [], values = {})
        except:
            flash("The service is not avaiable now,please try it later.", status = "warn")
            traceback.print_exc()
            redirect("/dba/index")

    def _query_result(self, kw):
        try:
            conditions=[]
            if kw.get("customerPO", False):
                conditions.append(DBAOrderInfo.po==kw["customerPO"].strip())

            if kw.get("sob", False):
                conditions.append(DBAOrderInfo.sob==kw["sob"].strip())

            if kw.get("orderStartDate", False) and kw.get("orderEndDate", False):
                b_date=dt.strptime(kw.get("orderStartDate", '2009-12-1200:00:00')+"00:00:00", "%Y-%m-%d%H:%M:%S")
                e_date=dt.strptime(kw.get("orderEndDate", '2009-12-1200:00:00')+"23:59:59", "%Y-%m-%d%H:%M:%S")
                conditions.append(DBAOrderInfo.create_time>=b_date)
                conditions.append(DBAOrderInfo.create_time<=e_date)
            elif kw.get("orderStartDate", False):
                b_date=dt.strptime(kw.get("orderStartDate", '2009-12-1200:00:00')+"00:00:00", "%Y-%m-%d%H:%M:%S")
                conditions.append(DBAOrderInfo.create_time>=b_date)
            elif kw.get("orderEndDate", False):
                e_date=dt.strptime(kw.get("orderEndDate", '2009-12-1200:00:00')+"23:59:59", "%Y-%m-%d%H:%M:%S")
                conditions.append(DBAOrderInfo.create_time<=e_date)

            if kw.get("shipStartDate", False) and kw.get("shipEndDate", False):
                b_date=date(*time.strptime(kw.get("shipStartDate", '2009-12-12'), '%Y-%m-%d')[:3])
                e_date=date(*time.strptime(kw.get("shipEndDate", '2009-12-12'), '%Y-%m-%d')[:3])
                conditions.append(DBAOrderInfo.ship_date>=b_date)
                conditions.append(DBAOrderInfo.ship_date<=e_date)
            elif kw.get("shipStartDate", False):
                b_date=date(*time.strptime(kw.get("shipStartDate", '2009-12-12'), '%Y-%m-%d')[:3])
                conditions.append(DBAOrderInfo.ship_date>=b_date)
            elif kw.get("shipEndDate", False):
                e_date=date(*time.strptime(kw.get("shipEndDate", '2009-12-12'), '%Y-%m-%d')[:3])
                conditions.append(DBAOrderInfo.ship_date<=e_date)
                
            #add@2011-07-20
            if kw.get("deliveryStartDate", False) and kw.get("deliveryEndDate", False):
                b_date=date(*time.strptime(kw.get("deliveryStartDate", '2009-12-12'), '%Y-%m-%d')[:3])
                e_date=date(*time.strptime(kw.get("deliveryEndDate", '2009-12-12'), '%Y-%m-%d')[:3])
                conditions.append(DBAOrderInfo.delivery_date>=b_date)
                conditions.append(DBAOrderInfo.delivery_date<=e_date)
            elif kw.get("deliveryStartDate", False):
                b_date=date(*time.strptime(kw.get("deliveryStartDate", '2009-12-12'), '%Y-%m-%d')[:3])
                conditions.append(DBAOrderInfo.delivery_date>=b_date)
            elif kw.get("deliveryEndDate", False):
                e_date=date(*time.strptime(kw.get("deliveryEndDate", '2009-12-12'), '%Y-%m-%d')[:3])
                conditions.append(DBAOrderInfo.delivery_date<=e_date)
            ############
            
            if kw.get("item_code", False):
                conditions.append(DBAItem.__table__.c.item_code.op('ilike')("%%%s%%" %kw["item_code"]))

            if kw.get("category_id", False):
                conditions.append(DBAItem.category_id==kw["category_id"])

            if kw.get("customer_id", False):
                conditions.append(DBAOrderInfo.customer_id == kw["customer_id"])

            if len(conditions):
                if kw.get("item_code", False) or kw.get("category_id", False):
                    obj=DBSession.query(DBAOrderInfo).join(DBAOrderDetail, DBAItem)
                else:
                    obj=DBSession.query(DBAOrderInfo)

                for condition in conditions: obj=obj.filter(condition)

                if not in_group("Admin") and not in_group("DBA_AE") and not in_group("DBA_BUYER"):
                    obj=obj.filter(DBAOrderInfo.create_by_id==request.identity["user"].user_id)
                result=obj.filter(DBAOrderInfo.active==0) \
                            .order_by(desc(DBAOrderInfo.id)) \
                            .all()
            else:
                if not in_group("Admin") and not in_group("DBA_AE") and not in_group("DBA_BUYER"):
                    result=DBSession.query(DBAOrderInfo) \
                         .filter(DBAOrderInfo.create_by_id==request.identity["user"].user_id) \
                         .filter(DBAOrderInfo.active==0) \
                         .order_by(desc(DBAOrderInfo.id)) \
                         .all()
                else:
                    result=DBSession.query(DBAOrderInfo) \
                                      .filter(DBAOrderInfo.active==0) \
                                      .order_by(desc(DBAOrderInfo.id)) \
                                      .all()
                        
            return result
        except:
            traceback.print_exc()





    def _returnList(self, data):
        if not isinstance(data, list):
            return list((data,))
        return data


    def _emailOrderCompleted(self, po, send_to):
        send_from="r-track@r-pac.com"
        cc_to=config.get("dba_notify_email_cc", "").split(";")
        subject="r-track Online Ordering Confirmation for DBA items"
        text=["Dear Customers,", "\n",
              "Thanks for your orders. Your online ordering records with PO %s is valid in the system." % po,
              "We will send the PI to you between 26th and 27th. Please kindly sign it back upon receipt." , "\n",
              "You can revise the order quantity between 5th and 25th.", "\n",
              "Please do not reply this email.",
              ]
        sendEmail(send_from, send_to, subject, "\n".join(text), cc_to)

    def _emailUrgentRequest(self, po, user, ship_date, last_revised_day,
                            send_to=None):
        if send_to is None:
            send_to=config.get("dba_urgent_request_email", "").split(";")
        send_from="r-track@r-pac.com"
        cc_to=config.get("dba_urgent_request_email_cc", "").split(";")
        subject="Urgent shipment request for DBA items"
        text=["\nPO/Order: %s" % po,  #reflect actual PO/order#
              "User/Vendor: %s" % user,  #reflect the actual system user
              "Requested shipdate: %s" % ship_date, #refer to system
              "Last revised day: %s" % last_revised_day, "\n", #refer to system
              "Please do not reply this email.",
              ]
        sendEmail(send_from, send_to, subject, "\n".join(text), cc_to)

    #===========================================================================
    # customer_item
    #===========================================================================
    @expose('tribal.templates.dba.customer_item')
    @paginate("result", items_per_page = 20)
    @tabFocus(tab_type = "master")
    def customer_item(self, **kw):
        if not kw:
            result=[]
        else:
            obj = DBSession.query(DBACustomer)
            if kw.get("name", False):
                obj = obj.filter(DBACustomer.__table__.c.name.op("ilike")("%%%s%%"%kw["name"]))
            if kw.get("code", False):
                obj = obj.filter(DBACustomer.__table__.c.code.op("ilike")("%%%s%%"%kw["code"]))
                 
            result = obj.order_by(DBACustomer.name).all()

        return {
                "searchWidget" : DBACustomerSearchFormInstance,
                "result" : result,
                "values" : kw
                }

    @expose()
    def customer_item_enable(self, **kw):
        if kw.get('selected_ids', ''):
            for i in kw.get('selected_ids', '').split(','):
                obj = getOr404(DBACustomer, i, "/dba/customer_item")
                obj.lastModifyBy = request.identity["user"]
                obj.lastModifyTime = dt.now()
                obj.active = 0
        flash("Enable the master successfully!")
        redirect("/dba/customer_item")

    @expose()
    def customer_item_disable(self, **kw):
        if kw.get('selected_ids', ''):
            for i in kw.get('selected_ids', '').split(','):
                obj = getOr404(DBACustomer, i, "/dba/customer_item")
                obj.lastModifyBy = request.identity["user"]
                obj.lastModifyTime = dt.now()
                obj.active = 1
        flash("Disable the master successfully!")
        redirect("/dba/customer_item")


    @expose("tribal.templates.dba.customer_item_manage")
    @tabFocus(tab_type="master")
    def customer_item_manage(self, **kw):
        u=getOr404(DBACustomer, kw["id"])
        included = u.items
        excluded = DBSession.query(DBAItem).filter(~DBAItem.customers.any(DBACustomer.id==u.id)).order_by(DBAItem.item_code)
        return {
                "customer" : u,
                "included" : included,
                "excluded" : excluded
                }

    @expose()
    def save_customer_item(self, **kw):
        u=getOr404(DBACustomer, kw["id"])

        if not kw["igs"] : u.items=[]
        else : u.items=DBSession.query(DBAItem).filter(DBAItem.id.in_(kw["igs"].split("|"))).all()
        flash("Save the update successfully!")
        redirect("/dba/customer_item")

    #===========================================================================
    # add by cl
    #===========================================================================
    @expose("tribal.templates.dba.report")
    @tabFocus(tab_type = "report")
    def report(self, **kw):
        return {"widget":report_form}

    @expose()
    def export(self, **kw):
        try:
            current=dt.now()
            dateStr=current.strftime("%Y%m%d")
            fileDir=os.path.join(config.get("download_dir"), "DBA", dateStr)
            if not os.path.exists(fileDir): os.makedirs(fileDir)
            templatePath = os.path.join(config.get("template_dir"),"DBA_TEMPLATE.xls")
            tempFileName=os.path.join(fileDir, "%s_%s_%d.xls"%(request.identity["user"].user_name,
                                                               current.strftime("%Y%m%d%H%M%S"), random.randint(0, 1000)))
            realFileName=os.path.join(fileDir, "%s_%s.xls"%(request.identity["user"].user_name, current.strftime("%Y%m%d%H%M%S")))
            shutil.copy(templatePath, tempFileName)
            dba_xls = DBAExcel(templatePath = tempFileName, destinationPath = realFileName)
            data = []
            itemInfo = [('Type', 'Item Code', 'Total Order Quantity')]
            if kw:
                kw.setdefault('category_id', returnCatId('DIM'))
                orders = self._query_result(kw)
            if orders:
                itemQty = {}
                itemType = {}
                for order in orders:
                    details = []                    
                    if order.details:
                        if kw.get("item_code", False):
                            details = DBSession.query(DBAOrderDetail).join(DBAItem).filter( \
                                    and_(DBAOrderDetail.header==order, DBAOrderDetail.active==0, \
                                    DBAItem.__table__.c.item_code.op('ilike')("%%%s%%" %kw["item_code"]))).all()
                        else:
                            details = [d for d in order.details if 0==d.active]
                    for d in details:
                        data.append((
                                    Date2Text(order.create_time, '%d-%b-%Y'),
                                    order.po,
                                    order.customer.name,
                                    order.bill_to,
                                    order.ship_to,
                                    d.item.type.name,
                                    d.item.item_code,
                                    d.commited_qty,
                                    d.forecast_qty or 0,
                                    Date2Text(order.ship_date, '%d-%b-%Y'),
                                    Date2Text(order.delivery_date, '%d-%b-%Y'),
                                    ''.join([log.remark for log in d.logs]),
                                    order.sob if order.sob else ''
                                    ))
                        if itemQty.has_key(d.item.item_code):
                            itemQty[d.item.item_code] += d.commited_qty
                        else:
                            itemQty[d.item.item_code] = d.commited_qty

                        if not itemType.has_key(d.item.item_code):
                            itemType[d.item.item_code] = d.item.type.name
                        
                if itemQty and itemType:
                    for k, v in itemQty.iteritems():
                        itemInfo.append((
                                         itemType.get(k, ''),
                                         k,
                                         v
                                        ))

            dba_xls.inputData(data=data, data2=itemInfo)
            dba_xls.outputData()
            try:
                os.remove(tempFileName)
            except:
                pass
            return serveFile(unicode(realFileName))

        except:
            traceback.print_exc()
            flash("Export Fail.")
            redirect("/dba/report")
            
