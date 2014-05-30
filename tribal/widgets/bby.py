# coding: utf-8

from tw.api import WidgetsList
from tribal.model import DBSession
from tribal.model.bby import *
from tribal.widgets.components import *

__all__ = ["search_form", "mockup_search_form", "casepack_search_form", "basic_form", "basic_info_widget", "report_form","mockup_report_form"]

def getOptions(obj, order_by_field = "name"):
    def fun():
        return [("", ""), ] + [(str(row.id), str(row)) for row in DBSession.query(obj).filter(obj.active == 0).order_by(getattr(obj, order_by_field)).all()]
    return fun


#===============================================================================
# update by CL.Lam on 2010-11-16
#===============================================================================

class SearchForm(RPACForm):
    fields = [
          RPACText("sku", label_text = "SKU#"),
          RPACSelect("brand_id", label_text = "Brand", options = getOptions(BBYBrand)),
          RPACCalendarPicker("issue_date_from", label_text = "Issue Date(from) "),
          RPACCalendarPicker("issue_date_to", label_text = "Issue Date(to)"),
          RPACSelect("vendor_id", label_text = "Vendor", options = getOptions(BBYVendor)),
          RPACSelect("packaging_format_id", label_text = "Packaging Format", options = getOptions(BBYPackagingFormat)),
          RPACSelect("pd_id", label_text = "PD", options = getOptions(BBYTeammate)),
          RPACSelect("ae_id", label_text = "AE", options = getOptions(BBYTeammate)),
          RPACCalendarPicker("pcr_date_from", label_text = "PCR Receive Date(from) "),
          RPACCalendarPicker("pcr_date_to", label_text = "PCR Receive Date(to) "),
          RPACText("pcr", label_text = "PCR#"),
          RPACSelect("status", label_text = "Status", options = [('', ''), ('NEW', 'New'), ('SUBMIT', 'Submit'), ('COMPLETED', 'Completed')]),
              ]

search_form = SearchForm()


class MockupSearchForm(RPACForm):
    fields = [
          RPACText("sku", label_text = "SKU#"),
          RPACSelect("brand_id", label_text = "Brand", options = getOptions(BBYBrand)),
          RPACCalendarPicker("issue_date_from", label_text = "Issue Date(from) "),
          RPACCalendarPicker("issue_date_to", label_text = "Issue Date(to)"),
          RPACSelect("vendor_id", label_text = "Vendor", options = getOptions(BBYVendor)),
          RPACSelect("packaging_format_id", label_text = "Packaging Format", options = getOptions(BBYPackagingFormat)),
          RPACSelect("pd_id", label_text = "PD", options = getOptions(BBYTeammate)),
          RPACSelect("ae_id", label_text = "AE", options = getOptions(BBYTeammate)),
          RPACSelect("status", label_text = "Status", options = [('', ''), ('NEW', 'New'), ('SENT', 'Sent'), ('CONFIRMED', 'Confirmed'), ('COMPLETED', 'Completed')]),
              ]

mockup_search_form = MockupSearchForm()


class CasepackSearchForm(RPACForm):
    fields = [
          RPACText("sku", label_text = "SKU#"),
          RPACSelect("brand_id", label_text = "Brand", options = getOptions(BBYBrand)),
          RPACCalendarPicker("issue_date_from", label_text = "Issue Date(from) "),
          RPACCalendarPicker("issue_date_to", label_text = "Issue Date(to)"),
          RPACSelect("vendor_id", label_text = "Vendor", options = getOptions(BBYVendor)),
          RPACSelect("packaging_format_id", label_text = "Packaging Format", options = getOptions(BBYPackagingFormat)),
          RPACSelect("pd_id", label_text = "PD", options = getOptions(BBYTeammate)),
          RPACSelect("ae_id", label_text = "AE", options = getOptions(BBYTeammate)),
          RPACSelect("status", label_text = "Status", options = [('', ''), ('NEW', 'New'), ('SENT', 'Sent'), ('COMPLETED', 'Completed')]),
              ]

casepack_search_form = CasepackSearchForm()


class BasicForm(RPACForm):
    fields = [
          RPACText("sku", label_text = "SKU#"),
          RPACSelect("brand_id", label_text = "Brand", options = getOptions(BBYBrand)),
          RPACSelect("vendor_id", label_text = "Vendor", options = getOptions(BBYVendor)),
          RPACSelect("packaging_format_id", label_text = "Packaging Format", options = getOptions(BBYPackagingFormat)),
          RPACText("upc_no", label_text = "UPC"),

          RPACSelect("closure_id", label_text = "Closure", options = getOptions(BBYClosure)),
          RPACSelect("display_mode_id", label_text = "Display Mode", options = getOptions(BBYDisplayMode)),

          RPACText("ioq", label_text = "IOQ"),
          RPACText("aoq", label_text = "AOQ"),
          RPACTextarea("product_description", label_text = "Production Description"),
          RPACSelect("pd_id", label_text = "PD", options = getOptions(BBYTeammate)),
          RPACSelect("ae_id", label_text = "AE", options = getOptions(BBYTeammate)),
              ]

basic_form = BasicForm()



class BasicInfo(Form):
    template = "tribal.templates.bby.basic_info_widget"

#    fields = [
#          RPACText("sku", label_text = "SKU#"),
#          RPACText("brand", label_text = "Brand"),
#          RPACText("vendor", label_text = "Vendor"),
#          RPACText("packaging_format", label_text = "Packaging Format"),
#          RPACText("upc_no", label_text = "UPC"),
#          RPACText("closure", label_text = "Closure"),
#          RPACText("display_mode", label_text = "Display Mode"),
#          RPACText("ioq", label_text = "IOQ"),
#          RPACText("aoq", label_text = "AOQ"),
#          RPACTextarea("product_description", label_text = "Production Description"),
#          RPACText("pd", label_text = "PD", options = []),
#          RPACText("ae", label_text = "AE", options = []),
#              ]

basic_info_widget = BasicInfo()


class ReportForm(RPACForm):
    fields=[
          RPACText("sku", label_text = "SKU#"),
          RPACSelect("brand_id", label_text = "Brand", options = getOptions(BBYBrand)),
          RPACCalendarPicker("issue_date_from", label_text = "Issue Date(from) "),
          RPACCalendarPicker("issue_date_to", label_text = "Issue Date(to)"),
          RPACSelect("vendor_id", label_text = "Vendor", options = getOptions(BBYVendor)),
          RPACSelect("packaging_format_id", label_text = "Packaging Format", options = getOptions(BBYPackagingFormat)),
          RPACSelect("pd_id", label_text = "PD", options = getOptions(BBYTeammate)),
          RPACSelect("ae_id", label_text = "AE", options = getOptions(BBYTeammate)),
          RPACSelect("status", label_text = "Status", options = [('', ''), ('NEW', 'New'), ('SUBMIT', 'Submit'), ('COMPLETED', 'Completed')]),
          RPACSelect("factory_id", label_text = "Factory", options = getOptions(BBYSource)),
          RPACSelect("material_id", label_text = "Material", options = getOptions(BBYMaterial)),
      ]


report_form=ReportForm()


class MockupReportForm(RPACForm):
    fields=[
          RPACText("sku", label_text = "SKU#"),
          RPACSelect("brand_id", label_text = "Brand", options = getOptions(BBYBrand)),
          RPACCalendarPicker("issue_date_from", label_text = "Issue Date(from) "),
          RPACCalendarPicker("issue_date_to", label_text = "Issue Date(to)"),
          RPACSelect("vendor_id", label_text = "Vendor", options = getOptions(BBYVendor)),
          RPACSelect("packaging_format_id", label_text = "Packaging Format", options = getOptions(BBYPackagingFormat)),
          RPACSelect("pd_id", label_text = "PD", options = getOptions(BBYTeammate)),
          RPACSelect("ae_id", label_text = "AE", options = getOptions(BBYTeammate)),
          RPACSelect("status", label_text = "Status", options = [('', ''), ('NEW', 'New'), ('SUBMIT', 'Submit'), ('COMPLETED', 'Completed')]),
          RPACSelect("factory_id", label_text = "Factory", options = getOptions(BBYSource)),
          RPACSelect("material_id", label_text = "Material", options = getOptions(BBYMaterial)),
      ]


mockup_report_form=MockupReportForm()
