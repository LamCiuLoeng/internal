# coding: utf-8

# from tw.api import WidgetsList

# from repoze.what.predicates import not_anonymous, in_group, has_permission

from tribal.model import *
# from tribal.model.tmw import *
from tribal.widgets.components import *


__all__ = ['tmw_search_form']


class TMWSearchForm(RPACNoForm):
    fields = [RPACAjaxText("item_code", label_text="ITEMCODE"),
              RPACAjaxText("pofile_id", label_text="POFILE.ID"),
              RPACAjaxText("filename", label_text="Filename"),
              ]
tmw_search_form = TMWSearchForm()
