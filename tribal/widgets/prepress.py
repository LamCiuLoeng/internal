# coding: utf-8

from tw.api import WidgetsList
from tw.forms.fields import Form
from tribal.widgets.components import *
from tribal.model import *

from tribal.model.prepress import PS_COMPLETED_REQUEST, PS_CANCELED_REQUEST, \
    PS_NEW_REQUEST, PS_UNDER_DEVELOPMENT, PS_ASSIGNED

# __all__=["search_form", "report_form", "SFSamplingWidget", "SFPrintoutWidget", "SF3DImageWidget"]


def getOptions( dbobj, orderField, user = None ):
    def returnFun():
        rs = DBSession.query( dbobj ).order_by( getattr( dbobj, orderField ) )
        if not user:
            rs = rs.filter( dbobj.active == 0 )
            return [( "", "" )] + [( str( r.id ), str( r ) ) for r in rs]
        else:return [( "", "" )] + [( str( r.group_id ), str( r ) ) for r in rs]
    return returnFun


class PSSearchForm( RPACForm ):
    fields = [
              RPACSelect( "project_own", label_text = "Region", options = getOptions( Region, "name" ) ),
#              RPACSelect("customer", label_text = "Vendor/Customer", options = getOptions(Customer, "name")),
              RPACHidden( 'customer' ),
              RPACAjaxText( "customer_name", label_text = "Vendor/Customer" ),
              RPACAjaxText( "project_owner", label_text = "Project Owner" ),
#              RPACSelect("program", label_text = "Program", options = getOptions(Program, "name")),
              RPACSelect( "contact_team", label_text = "Division Team", options = getOptions( Team, "name" ) ),
              RPACText( "project", label_text = "Brand" ),
              RPACAjaxText( "contact_person", label_text = "Contact Person" ),

              RPACSelect( "item_category", label_text = "Item Category", options = getOptions( PSItemCategory, "name" ) ),

              RPACText( "item_description", label_text = "Item Description" ),
              RPACSelect( "team", label_text = "Request Person's Team", options = getOptions( Team, "name" ) ),
              RPACText( "item_code", label_text = "Item Code" ),
              RPACAjaxText( "create_by", label_text = "Request Person" ),
              RPACCalendarPicker( "create_time_from", label_text = "Request Date(from)" ),
              RPACText( "system_no", label_text = "Job Number" ),
              RPACCalendarPicker( "create_time_to", label_text = "Request Date(to)" ),
              RPACText( "reference_code", label_text = "Reference Code" ),
              RPACSelect( "status", label_text = "Status", options = [( "", "" ), ( str( PS_NEW_REQUEST ), "New" ),
                                                                     ( str( PS_ASSIGNED ), "Assigned" ), ( str( PS_UNDER_DEVELOPMENT ), "Under Development" ), ( str( PS_COMPLETED_REQUEST ), "Complete" ), ( str( PS_CANCELED_REQUEST ), "Cancelled" ), ] ),

              HiddenField( "field" ),
              HiddenField( "direction" ),
              ]

ps_search_form = PSSearchForm()


#===============================================================================
#
#===============================================================================

class PSAbstractWidget( Form ):
    template = "tribal.templates.prepress.sub_form_master"

    def __init__( self, id = None, parent = None, children = [], **kw ):
        super( Form, self ).__init__( id, parent, children, **kw )







class PSSFUploadWidget( PSAbstractWidget ):
    js_url = "/js/custom/prepress/PSSFUploadWidget.js"
    label = "Prepress"
    sub_template = "session_upload.mak"


class PSSFBarcodeWidget( PSAbstractWidget ):
    js_url = "/js/custom/prepress/PSSFBarcodeWidget.js"
    label = "Barcode"
    sub_template = "session_barcode.mak"
