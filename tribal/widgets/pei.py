# coding: utf-8

from tw.api import WidgetsList
from tribal.model.sportsware import *
from tribal.widgets.components import *

__all__ = ["order_view_form",
           ]

class OrderViewForm(RPACForm):
    fields = [RPACSearchText("buyerPO", label_text = "Buyer PO#"),
              RPACSearchText("vendorPO", label_text = "Vendor PO#"),
              RPACCalendarPicker("orderStartDate", label_text = "Order Date(from)"),
              RPACCalendarPicker("orderEndDate", label_text = "Order Date(to)")
              ]

order_view_form = OrderViewForm()