# -*- coding: utf-8 -*-

import traceback

# turbogears imports
from tg import expose, redirect, validate, flash, request, response, override_template,config
from tg.decorators import paginate

# third party imports
from repoze.what import predicates,authorize
from repoze.what.predicates import not_anonymous,in_group,has_permission
# project specific imports
from tribal.lib.base import BaseController
from tribal.model import *
from tribal.util.common import *
from tribal.widgets.order import *

__all__ = ['OrderController']

class OrderController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    allow_only = authorize.not_anonymous()
    
    @expose('tribal.templates.order.index')
    @paginate('collections',items_per_page = 25)
    @tabFocus(tab_type="main")
    def index(self, **kw):
        if not kw: return dict(collections = [], values = {}) 
        cut_no = kw.get("cutNo")
            
        if not cut_no:
            flash("Please input Cut No","warn")
            redirect("/order/index")
            
        results = self._query_tribal({"CutNbr":cut_no})
            
        if len(results) == 0 :
            flash("No such PO")
            redirect("/order/index")
        elif len(results) > 1:
            flash("There are too many POs, please confirm")
            return dict(collections = results, values = kw)
            
        override_template(self.index, 'mako:tribal.templates.order.order_form_new')
        return self.placeOrder({'result': results, 'customerPO': kw.get("customerPO","")})
#        else:
#            flash("No such order type!")
#            redirect("/order/index")
       
    
    @expose("tribal.templates.order.order_form_edit")
    @tabFocus(tab_type="main")
    def placeOrder(self, kw):
        result = kw.get('result', '')
        header = result[0]
        
        billTos = DBSession.query(TRBBillTo).order_by(TRBBillTo.company).all()
        shiptos = DBSession.query(TRBShipTo).order_by(TRBShipTo.company).all()
        custom_po = kw.get('customerPO', '')
        
        return {"msgHeader": header,
                "msgDetail": header.details,
                "billTos": billTos,
                "shipTos": shiptos,
                'custom_po': custom_po
                }
    
    @expose()
    def saveOrder(self, **kw):
        ph = DBSession.query(TRBHeaderPO).get(int(kw["msgID"]))
        billTo = DBSession.query(TRBBillTo).get(int(kw['billCompany']))
        shipTo = DBSession.query(TRBShipTo).get(int(kw['shipCompany']))
        DBSession.begin(subtransactions=True)
        try:
            pd_list = []
            params = {"header" : ph,
                      "customerPO" : kw.get('customerPO', ''),
                      "billTo" : billTo,
                      "shipTo" : shipTo,
                      #"issuedBy" : request.identity["user"],
                      #"lastModifyBy" : request.identity["user"],
                      }
            
            order = TRBOrderFormHeader(**params)

            DBSession.add(order)
            
            order_details = []
            for i in range(len(ph.details)):
                if kw['quantity_%d' % ph.details[i].id] != "":
                    order_detail = TRBOrderFormDetail(header = order, detailPO = ph.details[i], quantity = int(kw['quantity_%d' % ph.details[i].id]))
                    order_details.append(order_detail)
            
            DBSession.add_all(order_details)
            DBSession.commit()

            sendFrom  = "r-pac-Tribal-ordering-system"
            sendTo = config.trb_email_cc.split(";")
            ccTo = config.trb_email_cc.split(";")
            subject = "Order[%s] has been confirmed successfully!" % order.customerPO
            text = ["Thank you for your confirmation!","You could view the order's detail information via the link below:",
                    "%s/order/viewOrder?id=%d" % (config.website_url,order.id),
                    "\n\n************************************************************************************",
                    "This e-mail is sent by the r-pac Tribal ordering system automatically.",
                    "Please don't reply this e-mail directly!",
                    "************************************************************************************"]
            sendEmail(sendFrom,sendTo,subject,"\n".join(text),ccTo)
        except:
            traceback.print_exc()
            DBSession.rollback()
            flash("The service is not avaiable now,please try it later or contact the system administator.","warn")
            raise
        else:
            flash("The order has been save successfully!")
        redirect("/order/index")
    
    @expose("tribal.templates.order.order_form_view")
    @tabFocus(tab_type="main")
    def viewOrder(self,**kw):
        ph = DBSession.query(TRBOrderFormHeader).get(int(kw["id"]))

        if len(ph.formDetails) < 1 :
            flash("There's no order related to this PO!","warn")
            redirect("/order/index")

        return {"poheader" : ph,
                "podetails" : ph.formDetails,
#                "image_url" : image_url,
                }
        
    def _query_tribal(self, kw):
        whereClassList = []
      
        if kw.get("CutNbr", False):
            whereClassList.append(TRBHeaderPO.cutNo == kw.get("CutNbr", ""))

        if len(whereClassList):
            obj = DBSession.query(TRBHeaderPO)
            
            for condition in whereClassList: obj = obj.filter(condition)
            
            result = obj.all()   
        else:
            result = DBSession.query(TRBHeaderPO).all()
        
        return result

    @expose('tribal.templates.order.search')
    @paginate('collections',items_per_page = 25)
    @tabFocus(tab_type="view")
    def search(self, **kw):
        try:
            search_form = order_view_form

            if kw:
                result = self._query_result(kw)

                return dict(search_form = search_form, collections = result, values = kw)
            else:
                return dict(search_form = search_form, collections = [], values = {})
        except:
            flash("The service is not avaiable now,please try it later.",status="warn")
            traceback.print_exc()
            redirect("/order/index")

    
    def _query_result(self, kw):
        try:
            conditions = []
#            status = kw.get("orderStatus", False)

            if kw.get("cutNo", False):
                conditions.append(TRBHeaderPO.cutNo.like("%%%s%%" % kw.get("cutNo", "")))
#            if kw.get("sub", False):
#                conditions.append(JCPHeaderPO.sub == kw.get("sub", ""))
#            if kw.get("lot", False):
#                conditions.append(JCPHeaderPO.lot == kw.get("lot", ""))
#            if kw.get("orderStatus", False):
#                if status == "1":
#                    conditions.append(not_(JCPHeaderPO.id.in_(DBSession.query(JCPOrderForm.headerId))))
#                elif status == "2":
#                    conditions.append(JCPHeaderPO.id == JCPOrderForm.headerId)
            if kw.get("customerPO", False):
                conditions.append(TRBHeaderPO.id == TRBOrderFormHeader.headerId)
                conditions.append(TRBOrderForm.customerPO.like("%%%s%%" % kw.get("customerPO", "")))
            if kw.get("orderStartDate",False) and kw.get("orderEndDate",False):
                b_date = dt.strptime(kw.get("orderStartDate",'2009-12-1200:00:00') + "00:00:00", "%Y-%m-%d%H:%M:%S")
                e_date = dt.strptime(kw.get("orderEndDate",'2009-12-1200:00:00') + "23:59:59", "%Y-%m-%d%H:%M:%S")

                conditions.append(TRBOrderFormHeader.orderDate >= b_date)
                conditions.append(TRBOrderFormHeader.orderDate <= e_date)
            elif kw.get("orderStartDate",False):
                b_date = dt.strptime(kw.get("orderStartDate",'2009-12-1200:00:00') + "00:00:00", "%Y-%m-%d%H:%M:%S")

                conditions.append(TRBOrderFormHeader.orderDate >=  b_date)
            elif kw.get("orderEndDate",False):
                e_date = dt.strptime(kw.get("orderEndDate",'2009-12-1200:00:00') + "23:59:59", "%Y-%m-%d%H:%M:%S")

                conditions.append(TRBOrderFormHeader.orderDate <= e_date)

            if len(conditions):
                obj = DBSession.query(TRBHeaderPO)

                for condition in conditions: obj = obj.filter(condition)

                result = obj.filter(TRBHeaderPO.id.in_(DBSession.query(TRBOrderFormHeader.headerId))) \
                         .filter(TRBHeaderPO.active == 0) \
                         .order_by(TRBHeaderPO.id) \
                         .all()
            else:
                result = DBSession.query(TRBHeaderPO) \
                         .filter(TRBHeaderPO.active == 0) \
                         .filter(TRBHeaderPO.id.in_(DBSession.query(TRBOrderFormHeader.headerId))) \
                         .order_by(TRBHeaderPO.id) \
                         .all()

            return result
        except:
            traceback.print_exc()

