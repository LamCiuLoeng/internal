# coding: utf-8

from tw.api import WidgetsList
from tribal.model.sportsware import *
from tribal.widgets.components import *

__all__ = ["cut_no_form", "order_report","order_view_form","order_header_info"]

class CutNoForm(RPACForm):
    fields = [RPACText("cutNo", label_text = "Cut No"),]

cut_no_form = CutNoForm()



class OrderViewForm(RPACForm):
    fields = [RPACSearchText("cutNo", label_text = "Cut No"),
              RPACSearchText("customerPO", label_text = "Customer PO#"),
              RPACCalendarPicker("orderStartDate", label_text = "Order Date(from)"),
              RPACCalendarPicker("orderEndDate", label_text = "Order Date(to)")]

order_view_form = OrderViewForm()

class OrderHeaderDisplay(RPACDesplay):
    fields = [RPACText("cutNo", label_text = "Cut No"),
              RPACText("stock", label_text = "Stock#"),
              RPACText("sub", label_text = "JCP Sub#"),
              RPACText("lot", label_text = "JCP lot#"),
              RPACText("lotDescription", label_text = "Lot Description"),
              RPACText("line", label_text = "Line"),
              RPACText("fiberContent", label_text = "Fiber Content"),
              RPACText("washCode", label_text = "Wash Code"),
              RPACText("Cat", label_text = "Cat"),
              RPACText("poDate", label_text = "PO Date"),
              RPACText("importDate", label_text = "Import Date")]

order_header_info = OrderHeaderDisplay()


class OrderReportForm(RPACForm):
    fields = [RPACCalendarPicker("orderDate", label_text = "Order Date"),
              RPACText("customerPO", label_text = "Customer PO#"),
              RPACText("tel", label_text = "Tel"),
              RPACCalendarPicker("requestShipDate", label_text = "Request Ship Date"),
              RPACText("shipMethod", label_text = "Ship Method"),
              RPACText("billCompany", label_text = "Bill Company"),
              RPACText("billAddress", label_text = "Bill Address"),
              RPACText("billAttn", label_text = "Bill Attn"),
              RPACText("billTel", label_text = "Bill Tel"),
              RPACText("billFax", label_text = "Bill Fax"),
              RPACText("shipCompany", label_text = "Ship Company"),
              RPACText("shipAddress", label_text = "Ship Address"),
              RPACText("shipAttn", label_text = "Ship Attn"),
              RPACText("shipTel", label_text = "Ship Tel"),
              RPACText("shipFax", label_text = "Ship Fax"),]

order_report = OrderReportForm()