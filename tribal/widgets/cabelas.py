# coding: utf-8

from tg import request
from tw.api import WidgetsList
from tribal.model import DBSession
from tribal.model.sportsware import *
from tribal.widgets.components import *
from tribal.model.cabelas import *

__all__ = ['developmentSearchForm', 'orderingConfirmForm', 'OrderingSearchForm']

def getOptions(obj, query_field="name", to = None, order_by_field="name", active=0):
    def fun():
        if active==None:
            data = DBSession.query(obj).order_by(getattr(obj, order_by_field))
        else:
            data = DBSession.query(obj).filter(obj.active == active).order_by(getattr(obj, order_by_field))
        if to:
            #data = data.filter(obj.type == to).filter(obj.vendor_id == request.identity["user"].user_id)
            data = data.filter(obj.type == to)
        return  [("", ""), ] + [(str(row.id), str(getattr(row, query_field))) for row in data.all()]
    return fun

class DevelopmentSearchForm(RPACNoForm):
    fields = [RPACText("product_desc", label_text = "Product Name"),
              RPACSelect('vendor_ids', label_text = 'Vendor', options = getOptions(CabelasVendor)),
              RPACSelect('box_size_id', label_text = 'Box Size', options = getOptions(CabelasBoxSize, active=None)),
              RPACSelect('gender_id', label_text = 'Gender', options = getOptions(CabelasGender, active=None)),
    ]

developmentSearchForm = DevelopmentSearchForm()

class OrderingSearchForm(RPACNoForm):
    fields = [
              RPACText("number", label_text = "No."),
              RPACText("product_desc", label_text = "Product Name"),
              RPACSelect("bill_to_id", label_text = "Bill To", options = getOptions(CabelasVendorInfo, query_field="address", to="billto", order_by_field="id")),
              RPACSelect("ship_to_id", label_text = "Ship To", options = getOptions(CabelasVendorInfo, query_field="address", to="shipto",  order_by_field="id")),
              RPACCalendarPicker("create_time_start", label_text = "Create Date(Start)"),
              RPACCalendarPicker("create_time_end", label_text = "Create Date(End)"),
    ]

class OrderingConfirmForm(RPACNoForm):
    fields = [
              RPACSelect("bill_to_id", label_text = "Bill To", options = getOptions(CabelasVendorInfo, query_field="address",to="billto", order_by_field="id")),
              RPACSelect("ship_to_id", label_text = "Ship To", options = getOptions(CabelasVendorInfo, query_field="address",to="shipto",  order_by_field="id")),
              RPACText("name", label_text = "Company"),
              RPACText("telephone", label_text = "Telephone"),
              RPACText("fax", label_text = "Fax"),
              RPACText("rcm_dcm", label_text = "RCM / DCM"),
              RPACText("contact", label_text = "Contact"),
              RPACTextarea("address", label_text = "Address"),
    ]
OrderingSearchForm = OrderingSearchForm()
orderingConfirmForm = OrderingConfirmForm()
