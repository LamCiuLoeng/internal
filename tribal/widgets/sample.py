# coding: utf-8

from tw.api import WidgetsList
from tw.forms.fields import Form
from tribal.widgets.components import *
from tribal.model import *
from tribal.model.sample import *

#__all__=["search_form", "report_form", "SFSamplingWidget", "SFPrintoutWidget", "SF3DImageWidget"]


def getOptions(dbobj, orderField, user=None):
    def returnFun():
        rs=DBSession.query(dbobj).order_by(getattr(dbobj, orderField))
        if not user:
            rs = rs.filter(dbobj.active==0)
            return [("", "")]+[(str(r.id), str(r)) for r in rs]
        else:return [("", "")]+[(str(r.group_id), str(r)) for r in rs]
    return returnFun


class SearchForm(RPACForm):
    fields=[
              RPACSelect("project_own", label_text = "Region", options = getOptions(Region, "name")),
#              RPACSelect("customer", label_text = "Vendor/Customer", options = getOptions(Customer, "name")),
              RPACHidden('customer'),
              RPACAjaxText("customer_name", label_text = "Vendor/Customer"),
              RPACAjaxText("project_owner", label_text = "Project Owner"),
#              RPACSelect("program", label_text = "Program", options = getOptions(Program, "name")),
              RPACHidden('program'),
              RPACAjaxText("program_name", label_text = "Corporate Customer"),
              RPACSelect("contact_team", label_text = "Division Team", options = getOptions(Team, "name")),
              RPACSelect("project", label_text = "Brand", options = [("", ""), ]),
              RPACAjaxText("contact_person", label_text = "Contact Person"),
              
              RPACSelect("item_category", label_text = "Item Category", options = getOptions(ItemCategory, "name")),
              
              RPACText("item_description", label_text = "Item Description"),
              RPACSelect("team", label_text = "Request Person's Team", options = getOptions(Team, "name")),
              RPACText("item_code", label_text = "Item Code"),
              RPACAjaxText("create_by", label_text = "Request Person"),
              RPACCalendarPicker("create_time_from", label_text = "Request Date(from)"),
              RPACText("system_no", label_text = "Job Number"),
              RPACCalendarPicker("create_time_to", label_text = "Request Date(to)"),
              RPACText("reference_code", label_text = "Reference Code"),
              RPACSelect("status", label_text = "Status", options = [("", ""), (str(NEW_REQUEST), "New"),(str(UNDER_DEVELOPMENT), "Under Development"), (str(COMPLETED_REQUEST), "Complete"), (str(CANCELED_REQUEST), "Cancelled"), (str(DRAFT), "Draft")]),
              
              HiddenField("field"),
              HiddenField("direction"),
              ]

search_form=SearchForm()


class ReportForm(RPACForm):
    fields=[
#              RPACSelect("project_own", label_text="Region", options=getOptions(Region, "name")),
#              RPACSelect("customer", label_text="Vendor/Customer Name", options=getOptions(Customer, "name")),
#              RPACSelect("program", label_text="Program", options=getOptions(Program, "name")),
#              RPACSelect("team", label_text="Team", options=getOptions(Team, "name")),
#              RPACSelect("project", label_text="Project", options=[("", ""), ]),
#              RPACText("item_code", label_text="Item Code"),
              RPACCalendarPicker("create_time_from", label_text = "Request Date(from)"),
              RPACCalendarPicker("create_time_to", label_text = "Request Date(to)"),
              RPACSelect("report_type", label_text = "Report Tpe", options = [("weekly", "Weekly"), ("summary", "Summary")]),
              ]


report_form=ReportForm()

##################################################################
#
#  abstract widget for the sample development sub form
#
##################################################################

class AbstractWidget(Form):
    template="tribal.templates.sample.sub_form_master"

    def __init__(self, id = None, parent = None, children = [], **kw):
        super(Form, self).__init__(id, parent, children, **kw)



##################################################################
#
#    detail define for every form
#
##################################################################

#for Program -> Target
class SFTargetWidget(AbstractWidget):
    js_url="/js/custom/sample/SFTargetWidget.js"
    label="Target"
    sub_template="session_target.mak"


#for Program -> Avon
class SFAvonWidget(AbstractWidget):
    js_url="/js/custom/sample/SFAvonWidget.js"
    label="Avon"
    sub_template="session_avon.mak"


#for Program -> Besy Buy
class SFBestBuyWidget(AbstractWidget):
    js_url="/js/custom/sample/SFBestBuyWidget.js"
    label="Best Buy"
    sub_template="session_bestbuy.mak"



#for Structure -> box
class SFBoxWidget(AbstractWidget):
    js_url="/js/custom/sample/SFBoxWidget.js"
    label="Boxes Design"
    sub_template="session_box.mak"


#for Structure -> Tray
class SFTrayWidget(AbstractWidget):
    js_url="/js/custom/sample/SFTrayWidget.js"
    label="Tray Design"
    sub_template="session_tray.mak"



#for Structure -> Floor
class SFFloorWidget(AbstractWidget):
    js_url="/js/custom/sample/SFFloorWidget.js"
    label="Floor/Pallet Display/Sidekick"
    sub_template="session_floor.mak"



#for Structure -> General
class SFGeneralWidget(AbstractWidget):
    js_url="/js/custom/sample/SFGeneralWidget.js"
    label="General packaging design"
    sub_template="session_general.mak"



#for Artwork -> Label
class SFLabelWidget(AbstractWidget):
    js_url="/js/custom/sample/SFLabelWidget.js"
    label="Barcode Label"
    sub_template="session_label.mak"


#for Artwork -> Artwork
class SFArtworkWidget(AbstractWidget):
    js_url="/js/custom/sample/SFArtworkWidget.js"
    label="Artwork"
    sub_template="session_artwork.mak"



#for Output -> Printout
class SFPrintoutWidget(AbstractWidget):
    js_url="/js/custom/sample/SFPrintoutWidget.js"
    label="Printout"
    sub_template="session_printout.mak"


#for Output -> Sampling
class SFSamplingWidget(AbstractWidget):
    js_url="/js/custom/sample/SFSamplingWidget.js"
    label="Sampling"
    sub_template="session_sampling.mak"


#for Output -> 3D imges
class SF3DImageWidget(AbstractWidget):
    js_url="/js/custom/sample/SF3DImageWidget.js"
    label="3D Images"
    sub_template="session_3dimage.mak"



#for Output -> Assembly Sheet
class SFAssemblyWidget(AbstractWidget):
    js_url="/js/custom/sample/SFAssemblyWidget.js"
    label="Assembly Sheet"
    sub_template="session_assembly.mak"


#for Output -> drop test Sheet
class SFDropWidget(AbstractWidget):
    js_url="/js/custom/sample/SFDropWidget.js"
    label="Drop Test"
    sub_template="session_drop.mak"



#for Output -> Upload / Download / File Checking Sheet
class SFUploadWidget(AbstractWidget):
    js_url="/js/custom/sample/SFUploadWidget.js"
    label="Upload/Download/File Checking"
    sub_template="session_upload.mak"




#for Output -> Container Loading Sheet
class SFContainerWidget(AbstractWidget):
    js_url="/js/custom/sample/SFContainerWidget.js"
    label="Container Loading"
    sub_template="session_container.mak"


#for Output -> File Convert Sheet
class SFFileConvertWidget(AbstractWidget):
    js_url="/js/custom/sample/SFFileConvertWidget.js"
    label="File Convert"
    sub_template="session_fileconvert.mak"
    
    
#for Output -> Photo Shot
class SFPhotoWidget(AbstractWidget):
    js_url="/js/custom/sample/SFPhotoWidget.js"
    label="Photo Shot"
    sub_template="session_photo.mak"
