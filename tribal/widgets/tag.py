# coding: utf-8

from tw.api import WidgetsList

from repoze.what.predicates import not_anonymous, in_group, has_permission

from tribal.model import *
from tribal.model.tag import *
from tribal.widgets.components import *


__all__ = ['tag_search_form']

class TAGSearchForm(RPACNoForm):
    fields = [RPACAjaxText("poNo", label_text = "PO#"),
              #RPACAjaxText("upc", label_text="UPC"),
              #RPACText("color",label_text = "Color"),
              RPACAjaxText("brand",label_text = "Brand"),
              RPACAjaxText("style",label_text = "Style#"),
              RPACAjaxText("soNo",label_text = "SO NO"),
              RPACAjaxText("tagNo",label_text = "Tag NO"),
              #RPACText("prepack",label_text = "Prepack"),
              #RPACText("label",label_text = "Label"),
              #RPACCalendarPicker("importDateStart", label_text="Receive Date(from)"),
              #RPACCalendarPicker("importDateEnd", label_text="Receive Date(to)"),
              #RPACText("itemNo",label_text = "Item No"),
              ]
tag_search_form = TAGSearchForm()
