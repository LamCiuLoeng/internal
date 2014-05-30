# coding: utf-8

from tw.api import WidgetsList

#from repoze.what.predicates import not_anonymous, in_group, has_permission

from tribal.model import *
from tribal.model.tag import *
from tribal.widgets.components import *


__all__ = ['lemmi_search_form']

class LemmiSearchForm(RPACNoForm):
    fields = [RPACText("orderNumber", label_text = "OrderNumber"),
              RPACText("vendorNumber",label_text = "VendorNumber"),
              RPACText("customerOrderLineId",label_text = "CustomerOrderLineId"),
              RPACText("countryOfOrigin",label_text = "CountryOfOrigin"),
              RPACCalendarPicker("createdDateStart", label_text="Created(from)"),
              RPACCalendarPicker("createdDateEnd", label_text="Created(to)"),
              #RPACText("itemNo",label_text = "Item No"),
              ]
lemmi_search_form = LemmiSearchForm()
