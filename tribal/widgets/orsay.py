# coding: utf-8

from tw.api import WidgetsList
from tribal.model.sportsware import *
from tribal.widgets.components import *

__all__ = ['orderSearchFormInstance','trakingForm',]

class OrderSearchForm(RPACForm):
    fields = [RPACSelect("order_type", label_text = "Order Type",options=[("",""),("C1_s11","Item 1"),("C2_s11","Item 2"),("C3_s11","Item 3"),("C1_s12","Item 4"),("C2_s12","Item 5"),("C3_s12","Item 6")]),]
    
orderSearchFormInstance = OrderSearchForm()

class TrakingForm(RPACForm):
    fields = [RPACSelect("order_type", label_text = "Order Type",options=[("",""),("C1","Item 1"),("C2","Item 2"),("C3","Item 3")]),
        RPACText("customer_po", label_text = "Customer PO#"),
        RPACCalendarPicker("confirmedDateBegin", label_text = "Confirmed Date(from)"),
        RPACCalendarPicker("confirmedDateEnd", label_text = "Confirmed Date(to)"),
    ]

trakingForm = TrakingForm()