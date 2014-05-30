# -*- coding: utf-8 -*-

from tribal.model import *
from tribal.widgets.components import *

__all__ = [
#    "itemCodeSearchFormInstance", "itemCodeUpdateFormInstance",
#    "itemAttrSearchFormInstance", "itemAttrUpdateFormInstance",
#    "itemClassSearchFormInstance", "itemClassUpdateFormInstance",
#    "materialSearchFormInstance", "materialUpdateFormInstance",
#    "sizeSearchFormInstance", "sizeUpdateFormInstance",
#    "styleSearchFormInstance", "styleUpdateFormInstance",
#    "colorSearchFormInstance", "colorUpdateFormInstance",
#    "upcSearchFormInstance", "upcUpdateFormInstance",
    
    
    
    "DBACustomerSearchFormInstance", "DBACustomerUpdateFormInstance",
    "DBAItemSearchFormInstance", "DBAItemUpdateFormInstance",
    "DBACateogrySearchFormInstance", "DBACateogryUpdateFormInstance",
    "DBAItemTypeSearchFormInstance", "DBAItemTypeUpdateFormInstance",
    "BBYBrandSearchFormInstance", "BBYBrandUpdateFormInstance",
    "BBYVendorSearchFormInstance", "BBYVendorUpdateFormInstance",
    "BBYTeammateSearchFormInstance", "BBYTeammateUpdateFormInstance",
    "BBYSourceUpdateFormInstance", "BBYMaterialSpecSearchFormInstance",
    "BBYAgentUpdateFormInstance" ,
    "BBYContactSearchFormInstance" , "BBYContactUpdateFormInstance",
    "SampleCustomerSearchFormInstance", "SampleCustomerUpdateFormInstance",
    "SampleProjectSearchFormInstance", "SampleProjectUpdateFormInstance",
    "SampleRegionSearchFormInstance", "SampleRegionUpdateFormInstance",
    "SampleStockSearchFormInstance", "SampleStockUpdateFormInstance",
    "SampleTeamSearchFormInstance", "SampleTeamUpdateFormInstance",
    "SampleExtraInfoSearchFormInstance", "SampleExtraInfoUpdateFormInstance",
    "SampleTypeMappingSearchFormInstance", "SampleTypeMappingUpdateFormInstance",
    ]


getOptions = lambda obj,order_by="name" : lambda :[(str(o.id),str(o)) for o in DBSession.query(obj).filter(obj.active==0).order_by(getattr(obj, order_by))]


#===============================================================================
# widget for PEI project
#===============================================================================

'''
#--------------------- for master item code
class ItemCodeSearchForm(RPACForm):
    brandOptions = DBSession.query(PEIBrand.id, PEIBrand.name).all()
    brandOptions.append(("", ""))
    brandOptions.reverse()

    itemClassOptions = DBSession.query(PEIItemClass.id, PEIItemClass.name).all()
    itemClassOptions.append(("", ""))
    itemClassOptions.reverse()

    fields = [RPACText("itemCode", label_text="Item Code Name"),
        RPACSelect("brandId", label_text="Brand", options=brandOptions),
        RPACSelect("itemClassId", label_text="Item Class", options=itemClassOptions),
        ]

itemCodeSearchFormInstance = ItemCodeSearchForm()

class ItemCodeUpdateForm(RPACForm):
    brandOptions = DBSession.query(PEIBrand.id, PEIBrand.name).all()
    brandOptions.append(("", ""))
    brandOptions.reverse()

    itemClassOptions = DBSession.query(PEIItemClass.id, PEIItemClass.name).all()
    itemClassOptions.append(("", ""))
    itemClassOptions.reverse()

    fields = [RPACText("itemCode", label_text="Item Code Name"),
        RPACTextarea("itemDesc", label_text="Description"),
        RPACSelect("brandId", label_text="Brand", options=brandOptions),
        RPACSelect("itemClassId", label_text="Item Class", options=itemClassOptions),
        ]

itemCodeUpdateFormInstance = ItemCodeUpdateForm()

#--------------------- for master item attr
class ItemAttrSearchForm(RPACForm):
    fields = [RPACText("attrName", label_text="Item Attribute Name")]

itemAttrSearchFormInstance = ItemAttrSearchForm()

class ItemAttrUpdateForm(RPACForm):
    fields = [RPACText("attrName", label_text="Item Attribute Name"),
        RPACTextarea("attrDesc", label_text="Description")]

itemAttrUpdateFormInstance = ItemAttrUpdateForm()

#--------------------- for master item class
class ItemClassSearchForm(RPACForm):
    brandOptions = DBSession.query(PEIBrand.id, PEIBrand.name).all()
    brandOptions.append(("", ""))
    brandOptions.reverse()

    fields = [RPACText("name", label_text="Form Category"),
        RPACText("desc", label_text="Form Description"),
        RPACSelect("brandId", label_text="Brand", options=brandOptions),
        ]
itemClassSearchFormInstance = ItemClassSearchForm()

class ItemClassUpdateForm(RPACForm):
    brandOptions = DBSession.query(PEIBrand.id, PEIBrand.name).all()
    brandOptions.append(("", ""))
    brandOptions.reverse()

    fields = [RPACText("name", label_text="Form Category"),
        RPACText("desc", label_text="Form Description"),
        RPACSelect("brandId", label_text="Brand", options=brandOptions),
        ]
itemClassUpdateFormInstance = ItemClassUpdateForm()



#--------------------- for master material
class MaterialSearchForm(RPACForm):
    langOptions = DBSession.query(PEILanguage.id, PEILanguage.langName).all()
    langOptions.insert(0, ("", ""))

    categoryOptions = DBSession.query(PEICategory.id, PEICategory.name).all()
    categoryOptions.insert(0, ("", ""))

    fields = [RPACText("content", label_text="Common Fabric Contents"),
        RPACSelect("langId", label_text="Language", options=langOptions),
        RPACSelect("categoryId", label_text="Category", options=categoryOptions),
        ]

materialSearchFormInstance = MaterialSearchForm()

class MaterialUpdateForm(RPACForm):
    langOptions = DBSession.query(PEILanguage.id, PEILanguage.langName).all()
    langOptions.insert(0, ("", ""))

    categoryOptions = DBSession.query(PEICategory.id, PEICategory.name).all()
    categoryOptions.insert(0, ("", ""))

    fields = [RPACText("content", label_text="Common Fabric Contents"),
        RPACSelect("langId", label_text="Language", options=langOptions),
        RPACSelect("categoryId", label_text="Category", options=categoryOptions),
        ]

materialUpdateFormInstance = MaterialUpdateForm()

#--------------------- for master size
class SizeSearchForm(RPACForm):
    langOptions = DBSession.query(PEILanguage.id, PEILanguage.langName).all()
    langOptions.insert(0, ("", ""))

    categoryOptions = DBSession.query(PEICategory.id, PEICategory.name).all()
    categoryOptions.insert(0, ("", ""))

    formOptions = DBSession.query(PEIItemClass.id, PEIItemClass.name).all()
    formOptions.insert(0, ("", ""))

    fields = [RPACText("content", label_text="Size"),
        RPACSelect("langId", label_text="Language", options=langOptions),
        RPACSelect("categoryId", label_text="Category", options=categoryOptions),
        RPACSelect("itemClassId", label_text="Order Form", options=formOptions),
        ]

sizeSearchFormInstance = SizeSearchForm()

class SizeUpdateForm(RPACForm):
    langOptions = DBSession.query(PEILanguage.id, PEILanguage.langName).all()
    langOptions.insert(0, ("", ""))

    categoryOptions = DBSession.query(PEICategory.id, PEICategory.name).all()
    categoryOptions.insert(0, ("", ""))

    formOptions = DBSession.query(PEIItemClass.id, PEIItemClass.name).all()
    formOptions.insert(0, ("", ""))

    fields = [RPACText("content", label_text="Size"),
        RPACSelect("langId", label_text="Language", options=langOptions),
        RPACSelect("categoryId", label_text="Category", options=categoryOptions),
        RPACSelect("itemClassId", label_text="Order Form", options=formOptions),
        ]

sizeUpdateFormInstance = SizeUpdateForm()

#--------------------- for master style
class StyleSearchForm(RPACForm):
    langOptions = DBSession.query(PEILanguage.id, PEILanguage.langName).all()
    langOptions.insert(0, ("", ""))

    categoryOptions = DBSession.query(PEICategory.id, PEICategory.name).all()
    categoryOptions.insert(0, ("", ""))

    fields = [RPACText("mainPart", label_text="Main Part"),
        RPACText("extraPart", label_text="Extra Part"),
        RPACSelect("langId", label_text="Language", options=langOptions),
        RPACSelect("categoryId", label_text="Category", options=categoryOptions),
        ]

styleSearchFormInstance = StyleSearchForm()

class StyleUpdateForm(RPACForm):
    langOptions = DBSession.query(PEILanguage.id, PEILanguage.langName).all()
    langOptions.insert(0, ("", ""))

    categoryOptions = DBSession.query(PEICategory.id, PEICategory.name).all()
    categoryOptions.insert(0, ("", ""))

    fields = [RPACText("mainPart", label_text="Main Part"),
        RPACText("extraPart", label_text="Extra Part"),
        RPACSelect("langId", label_text="Language", options=langOptions),
        RPACSelect("categoryId", label_text="Category", options=categoryOptions),
        ]

styleUpdateFormInstance = StyleUpdateForm()

#--------------------- for master color
class ColorSearchForm(RPACForm):
    langOptions = DBSession.query(PEILanguage.id, PEILanguage.langName).all()
    langOptions.insert(0, ("", ""))

    categoryOptions = DBSession.query(PEICategory.id, PEICategory.name).all()
    categoryOptions.insert(0, ("", ""))

    fields = [RPACText("name", label_text="Color Name"),
        RPACText("code", label_text="Color Code"),
        RPACSelect("langId", label_text="Language", options=langOptions),
        RPACSelect("categoryId", label_text="Category", options=categoryOptions),
        ]

colorSearchFormInstance = ColorSearchForm()

class ColorUpdateForm(RPACForm):
    langOptions = DBSession.query(PEILanguage.id, PEILanguage.langName).all()
    langOptions.insert(0, ("", ""))

    categoryOptions = DBSession.query(PEICategory.id, PEICategory.name).all()
    categoryOptions.insert(0, ("", ""))

    fields = [RPACText("name", label_text="Color Name"),
        RPACText("code", label_text="Color Code"),
        RPACSelect("langId", label_text="Language", options=langOptions),
        RPACSelect("categoryId", label_text="Category", options=categoryOptions),
        ]

colorUpdateFormInstance = ColorUpdateForm()

#--------------------- for master color
class UPCSearchForm(RPACForm):
    fields = [RPACText("name", label_text="UPC Name"),
        ]

upcSearchFormInstance = UPCSearchForm()

class UPCUpdateForm(RPACForm):
    fields = [RPACText("name", label_text="UPC Name"),
        ]

upcUpdateFormInstance = UPCUpdateForm()


'''

#===============================================================================
# widget for DBA project
#===============================================================================


class DBACustomerSearchForm(RPACForm):
    fields = [RPACText("name", label_text="Customer Name"),
        RPACText("code", label_text="Customer Code"),
        ]

DBACustomerSearchFormInstance = DBACustomerSearchForm()


class DBACustomerUpdateForm(RPACForm):
    fields = [
        RPACText("name", label_text="Customer Name"),
        RPACText("code", label_text="Customer Code"),
        RPACText("contact_person", label_text="Contact Person"),
        RPACText("email_address", label_text="E-mail Address"),
        RPACTextarea("bill_to", label_text="Bill To"),
        RPACTextarea("ship_to", label_text="Ship To"),
        ]

DBACustomerUpdateFormInstance = DBACustomerUpdateForm()




dbaCategoryOptions = lambda: [("", "")] + [(r.id, str(r.name)) for r in DBSession.query(DBAItemCategory).all()]
dbaTypeOptons = lambda: [("", "")] + [(r.id, str(r.name)) for r in DBSession.query(DBAItemType).all()]

class DBAItemSearchForm(RPACForm):
    fields = [RPACText("item_code", label_text="Item Code"),
        RPACSelect("category_id", label_text="Category", options=dbaCategoryOptions),
        RPACSelect("type_id", label_text="Type", options=dbaTypeOptons),
    ]

DBAItemSearchFormInstance = DBAItemSearchForm()


class DBAItemUpdateForm(RPACNoForm):

    fields = [RPACText("item_code", label_text="Item Code", attrs={'disabled': 'disabled'}),
        RPACSelect("category_id", label_text="Category", options=dbaCategoryOptions, css_class='width-250 required'),
        RPACSelect("type_id", label_text="Type", options=dbaTypeOptons, css_class='width-250 required'),
        RPACText("flatted_size", label_text="Flatted Size", css_class='width-250 required'),
        # RPACText("image", label_text="Image"),
    ]

DBAItemUpdateFormInstance = DBAItemUpdateForm()


class DBACateogrySearchForm(RPACForm):
    fields = [RPACText("name", label_text="Name"),]

DBACateogrySearchFormInstance = DBACateogrySearchForm()


class DBACateogryUpdateForm(RPACForm):

    fields = [RPACText("name", label_text="Name"),]

DBACateogryUpdateFormInstance = DBACateogryUpdateForm()


class DBAItemTypeSearchForm(RPACForm):
    fields = [RPACText("name", label_text="Name"),]

DBAItemTypeSearchFormInstance = DBAItemTypeSearchForm()


class DBAItemTypeUpdateForm(RPACForm):

    fields = [RPACText("name", label_text="Name"),]

DBAItemTypeUpdateFormInstance = DBAItemTypeUpdateForm()



#===============================================================================
# for bby project
#===============================================================================
class BBYBrandSearchForm(RPACForm):
    fields = [RPACText("name", label_text="Name"),]

BBYBrandSearchFormInstance = BBYBrandSearchForm()

class BBYBrandUpdateForm(RPACForm):
    fields = [RPACText("name", label_text="Name"),
        RPACTextarea("description", label_text="Description")]

BBYBrandUpdateFormInstance = BBYBrandUpdateForm()



class BBYVendorSearchForm(RPACForm):
    fields = [RPACText("name", label_text="Name"),
        RPACText("ae_name", label_text="AE Name"),
        RPACText("erp_code_ref", label_text="ERP Code Ref"),
        RPACText("program_involved", label_text="Program Involved"),
            ]

BBYVendorSearchFormInstance = BBYVendorSearchForm()

class BBYVendorUpdateForm(RPACForm):
    fields = [RPACText("name", label_text="Name"),
        RPACText("ae_name", label_text="AE Name"),
        RPACText("erp_code_ref", label_text="ERP Code Ref"),
        RPACText("full_name", label_text="Full Name"),
        RPACText("contact", label_text="MP/AE Contact"),
        RPACText("tel", label_text="Tel"),
        RPACText("ext", label_text="Ext"),
        RPACText("mobile", label_text="Mobile"),
        RPACText("email", label_text="E-mail"),
        RPACTextarea("address", label_text="Address"),
        RPACText("program_involved", label_text="Program Involved"),
        ]

BBYVendorUpdateFormInstance = BBYVendorUpdateForm()


class BBYTeammateSearchForm(RPACForm):
    fields = [RPACText("name", label_text="Name"),
        RPACText("location", label_text="Location"),
            ]

BBYTeammateSearchFormInstance = BBYTeammateSearchForm()

class BBYTeammateUpdateForm(RPACForm):
    fields = [RPACText("name", label_text="Name"),
        RPACText("location", label_text="Location"),
        RPACText("tel", label_text="Tel"),
        RPACText("email", label_text="E-mail"),
        RPACTextarea("address", label_text="Address"),
        ]

BBYTeammateUpdateFormInstance = BBYTeammateUpdateForm()


class BBYSourceUpdateForm(RPACForm):
    fields = [RPACText("name", label_text="Name"),
        RPACText("full_name", label_text="Full Name"),
        RPACText("contact", label_text="Contact"),
        RPACText("tel", label_text="Tel"),
        RPACText("mobile", label_text="Mobile"),
        RPACText("email", label_text="E-mail"),
        RPACTextarea("address", label_text="Address"),
        ]

BBYSourceUpdateFormInstance = BBYSourceUpdateForm()

class BBYMaterialSpecSearchForm(RPACForm):
    fields = [RPACText("name", label_text="Name"),
        ]
BBYMaterialSpecSearchFormInstance = BBYMaterialSpecSearchForm()



class BBYAgentUpdateForm(RPACForm):
    fields = [RPACText("name", label_text="Agent Name"),
              RPACMultipleSelect("vendor_ids",label_text="Vendors",options=getOptions(BBYVendor)),
              RPACTextarea("description", label_text="Address"),
        ]

BBYAgentUpdateFormInstance = BBYAgentUpdateForm()



class BBYContactSearchForm(RPACForm):
    fields = [RPACText("name", label_text="Name"),
              RPACText("email", label_text="E-mail"),
              RPACText("phone", label_text="Phone"),
            ]

BBYContactSearchFormInstance = BBYContactSearchForm()

BBYContactUpdateFormInstance = BBYContactSearchForm()




#===============================================================================
# for sample project
#===============================================================================
class SampleCustomerSearchForm(RPACForm):
    fields = [RPACText("name", label_text="Name")]

SampleCustomerSearchFormInstance = SampleCustomerSearchForm()

class SampleCustomerUpdateForm(RPACForm):
    fields = [RPACText("name", label_text="Name")]

SampleCustomerUpdateFormInstance = SampleCustomerUpdateForm()

programOptions = lambda:[("", "")] + [(str(r.id), r.name) for r in DBSession.query(Program).order_by(Program.name).all()]

class SampleProjectSearchForm(RPACForm):
    fields = [RPACText("name", label_text="Name"), RPACSelect("program_id", label_text="Program Name", options=programOptions)]

SampleProjectSearchFormInstance = SampleProjectSearchForm()

class SampleProjectUpdateForm(RPACForm):
    fields = [RPACText("name", label_text="Name"), RPACSelect("program_id", label_text="Program Name", options=programOptions)]

SampleProjectUpdateFormInstance = SampleProjectUpdateForm()

class SampleRegionSearchForm(RPACForm):
    fields = [RPACText("name", label_text="Name"), RPACText("code", label_text="Code")]

SampleRegionSearchFormInstance = SampleRegionSearchForm()

class SampleRegionUpdateForm(RPACForm):
    fields = [RPACText("name", label_text="Name"), RPACText("code", label_text="Code")]

SampleRegionUpdateFormInstance = SampleRegionUpdateForm()

class SampleStockSearchForm(RPACForm):
    fields = [RPACText("name", label_text="Name"), RPACText("cost", label_text="Cost")]

SampleStockSearchFormInstance = SampleStockSearchForm()

class SampleStockUpdateForm(RPACForm):
    fields = [RPACText("name", label_text="Name"), RPACText("cost", label_text="Cost")]

SampleStockUpdateFormInstance = SampleStockUpdateForm()

class SampleTeamSearchForm(RPACForm):
    fields = [RPACText("name", label_text="Name"), RPACText("manager", label_text="manager"), RPACText("short_name", label_text="Short Name")]

SampleTeamSearchFormInstance = SampleTeamSearchForm()

class SampleTeamUpdateForm(RPACForm):
    fields = [RPACText("name", label_text="Name"), RPACText("manager", label_text="manager"), RPACText("short_name", label_text="Short Name")]

SampleTeamUpdateFormInstance = SampleTeamUpdateForm()

class SampleExtraInfoSearchForm(RPACForm):
    fields = [RPACText("name", label_text="Name"), RPACText("estimate_time", label_text="Estimate Time"), RPACText("job_config", label_text="Job Config"),
        RPACSelect("need_stock", label_text="Need Stock?", options=(("", ""), (0, "Yes"), (1, 'No'), ))]

SampleExtraInfoSearchFormInstance = SampleExtraInfoSearchForm()

class SampleExtraInfoUpdateForm(RPACForm):
    fields = [RPACText("name", label_text="Name"), RPACText("estimate_time", label_text="Estimate Time"), RPACText("job_config", label_text="Job Config"),
        RPACSelect("need_stock", label_text="Need Stock?", options=(("", ""), (0, "Yes"), (1, 'No'), ))]

SampleExtraInfoUpdateFormInstance = SampleExtraInfoUpdateForm()

class SampleTypeMappingSearchForm(RPACForm):
    fields = [RPACText("name", label_text="Name"), RPACText("label", label_text="Label"), RPACText("category", label_text="Category"), RPACText("report_header", label_text="Report Header"),
        RPACText("category2", label_text="Category 2"), RPACText("report_header2", label_text="Report Header 2"), RPACText("category2index", label_text="Category 2 Index")]

SampleTypeMappingSearchFormInstance = SampleTypeMappingSearchForm()

class SampleTypeMappingUpdateForm(RPACForm):
    fields = [RPACText("name", label_text="Name"), RPACText("label", label_text="Label"), RPACText("category", label_text="Category"), RPACText("report_header", label_text="Report Header"),
        RPACText("category2", label_text="Category 2"), RPACText("report_header2", label_text="Report Header 2"), RPACText("category2index", label_text="Category 2 Index")]

SampleTypeMappingUpdateFormInstance = SampleTypeMappingUpdateForm()



