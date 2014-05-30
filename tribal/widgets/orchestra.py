# coding: utf-8

from tw.api import WidgetsList
from tribal.model.sportsware import *
from tribal.widgets.components import *

__all__ = ['orchestraSearchForm']

class OrchestraSearchForm(RPACNoForm):
    fields = [RPACText("customer_po", label_text = "Customer PO#")]

orchestraSearchForm = OrchestraSearchForm()
