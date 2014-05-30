# coding: utf-8

from tw.api import WidgetsList

from repoze.what.predicates import not_anonymous, in_group, has_permission

from tribal.model import *
from tribal.model.dba import *
from tribal.widgets.components import *


__all__ = ['item_search_form', 'order_view_form', 'report_form']

def getOptions(dbobj,orderField='id'):
    def returnFun():
        return [("","")] + [(str(r.id),str(r.name)) for r in dbobj.find_all()]
    return returnFun

class ItemSearchForm(RPACNoForm):
    fields = [
        RPACHidden("ids"),
        RPACHidden("code"),
        RPACHidden("hidden_po"),
        RPACHidden("hidden_sob"),
        #RPACSelect("category", label_text="Category", options=getOptions(DBAItemCategory)),
        RPACSelect("type", label_text="Type", options=getOptions(DBAItemType)),
        RPACText("item_code", label_text="Item Code"),
    ]

item_search_form = ItemSearchForm()

class OrderViewForm(RPACForm):
    fields = [
              RPACCalendarPicker("orderStartDate", label_text = "Order Date(from)"),
              RPACCalendarPicker("orderEndDate", label_text = "Order Date(to)"),
              RPACCalendarPicker("shipStartDate", label_text = "Request Ship Date(from)"),
              RPACCalendarPicker("shipEndDate", label_text = "Request Ship Date(to)"),
              RPACCalendarPicker("deliveryStartDate", label_text = "Delivery Date(from)"),
              RPACCalendarPicker("deliveryEndDate", label_text = "Delivery Date(to)"),
              RPACSearchText("customerPO", label_text = "Customer PO#"),
              RPACSearchText("sob", label_text = "SOB#")]

order_view_form = OrderViewForm()

def getDBAOptions(dbobj):
    def returnFun():
#        if in_group("Admin") or in_group("DBA_AE"):
        if has_permission("DBA_VIEW_ALL_CUSTOMER"): #update by CL on 2011-06-28
            return [("","")] + [(str(r.id),str(r.name)) for r in dbobj.find_all()]
        else:
            if request.identity["user"].groups and request.identity["user"].groups[0].dba_profiles:
                customer=request.identity["user"].groups[0].dba_profiles[0].customer
                return [("",""), (str(customer.id), str(customer.name))]
            else:
                return [("","")]
    return returnFun

class ReportForm(RPACForm):
    fields=[
              RPACSelect("customer_id", label_text="Vendor/Customer Name", options=getDBAOptions(DBACustomer)),
              RPACText("item_code", label_text="Item Code"),
              RPACCalendarPicker("orderStartDate", label_text="Order Date(from)"),
              RPACCalendarPicker("orderEndDate", label_text="Order Date(to)"),
              RPACSearchText("customerPO", label_text = "Customer PO#")
              ]


report_form=ReportForm()
