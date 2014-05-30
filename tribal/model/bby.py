# -*- coding: utf-8 -*-
from datetime import datetime as dt

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.sql import *

from tribal.model import *
from tribal.model.sample import SysMixin
from tribal.model.sysutil import UploadObject
from tribal.util.sql_helper import MultiDateCol, JSONCol



#===============================================================================
# status const
#===============================================================================
SKU_NEW = 10
MOCKUP_NEW = 20
MOCKUP_SENT = 21
CASEPACK_NEW = 30
CASEPACK_SENT = 31
COMPLETED = 40
EOL = 50
INACTIVE = -1
ACTIVE = 0
CANCEL = -2
ON_HOLD = -3

#===============================================================================
# add the master table here
#===============================================================================
class BBYBrand(DeclarativeBase, SysMixin):
    __tablename__ = "bby_master_brand"

    id = Column(Integer, primary_key = True)
    name = Column(Unicode(100))
    description = Column(Unicode(1000))
    def __str__(self) : return self.name



class BBYPackagingFormat(DeclarativeBase, SysMixin):
    __tablename__ = "bby_master_packaging_format"

    id = Column(Integer, primary_key = True)
    name = Column(Unicode(100))
    description = Column(Unicode(1000))
    is_component = Column(Integer, default = 0) #0 means both format and component, 1 mean just format , 2 mean just component

    def __str__(self) : return self.name



class BBYVendor(DeclarativeBase, SysMixin):
    __tablename__ = "bby_master_vendor"

    id = Column(Integer, primary_key = True)
    name = Column(Unicode(100))
    ae_name = Column(Unicode(100))
    erp_code_ref = Column(Unicode(50))
    full_name = Column(Unicode(500))
    contact = Column(Unicode(100))
    tel = Column(Unicode(100))
    ext = Column(Unicode(20))
    mobile = Column(Unicode(50))
    email = Column(Unicode(100))
    address = Column(Unicode(1000))
    program_involved = Column(Unicode(500)) # Dynex|RocketFish|...

    def __str__(self) : return self.name


class BBYTeammate(DeclarativeBase, SysMixin):
    __tablename__ = "bby_master_teammate"

    id = Column(Integer, primary_key = True)
    name = Column(Unicode(100))
    location = Column(Unicode(100))
    tel = Column(Unicode(20))
    email = Column(Unicode(50))
    address = Column(Unicode(100))

    def __str__(self) : return self.name



class BBYMaterial(DeclarativeBase, SysMixin):
    __tablename__ = "bby_master_material"

    id = Column(Integer, primary_key = True)
#    component_id = Column(Integer, ForeignKey('bby_master_component.id'))
#    component = relation(BBYComponent, backref = "materials")
    name = Column(Unicode(100)) # CCNB | CCWB | C1S ...
    description = Column(Unicode(1000))

    def __str__(self) : return self.name


class BBYSpec(DeclarativeBase, SysMixin):
    __tablename__ = "bby_master_spec"

    id = Column(Integer, primary_key = True)
    name = Column(Unicode(100)) # S.F.Express | FedEx
    description = Column(Unicode(1000))

    def __str__(self) : return self.name


class BBYSource(DeclarativeBase, SysMixin):
    __tablename__ = "bby_master_source"

    id = Column(Integer, primary_key = True)
    name = Column(Unicode(100))
    full_name = Column(Unicode(500))

    def __str__(self) : return self.name

#kevin add
class BBYMaterialSpec(DeclarativeBase, SysMixin):
    __tablename__ = "bby_master_material_spec"
    id = Column(Integer, primary_key = True)
    name = Column(Unicode(100))
    head_id = Column(Integer, ForeignKey('bby_master_packaging_format.id'))
    material = Column(Unicode(100))
    spec = Column(Unicode(100))
    front_color = Column(Unicode(100))
    back_color = Column(Unicode(100))

class BBYSourceDetail(DeclarativeBase, SysMixin):
    __tablename__ = "bby_master_source_detail"

    id = Column(Integer, primary_key = True)
    header_id = Column(Integer, ForeignKey('bby_master_source.id'))
    header = relation(BBYSource, backref = backref("details", order_by = id), primaryjoin = "and_(BBYSource.id == BBYSourceDetail.header_id, BBYSourceDetail.active == 0)")
    contact = Column(Unicode(100))
    tel = Column(Unicode(20))
    mobile = Column(Unicode(20))
    email = Column(Unicode(100))
    address = Column(Unicode(1000))


class BBYClosure(DeclarativeBase, SysMixin):
    __tablename__ = "bby_master_closure"

    id = Column(Integer, primary_key = True)
    name = Column(Unicode(100))
    description = Column(Unicode(1000))
    def __str__(self) : return self.name


class BBYDisplayMode(DeclarativeBase, SysMixin):
    __tablename__ = "bby_master_display_mode"

    id = Column(Integer, primary_key = True)
    name = Column(Unicode(100))
    description = Column(Unicode(1000))
    def __str__(self) : return self.name



class BBYFailureReason(DeclarativeBase, SysMixin):
    __tablename__ = "bby_master_failure_reason"

    id = Column(Integer, primary_key = True)
    name = Column(Unicode(200))
    description = Column(Unicode(1000))
    def __str__(self) : return self.name


class BBYCourier(DeclarativeBase, SysMixin):
    __tablename__ = "bby_master_courier"

    id = Column(Integer, primary_key = True)
    name = Column(Unicode(200))
    description = Column(Unicode(1000))
    def __str__(self) : return self.name


class BBYMockupContent(DeclarativeBase, SysMixin):
    __tablename__ = "bby_master_mockup_content"

    id = Column(Integer, primary_key = True)
    name = Column(Unicode(200))
    value = Column(Integer)
    description = Column(Unicode(1000))
    def __str__(self) : return self.name


class BBYColor(DeclarativeBase, SysMixin):
    __tablename__ = "bby_master_color"

    id = Column(Integer, primary_key = True)
    name = Column(Unicode(200))
    description = Column(Unicode(1000))
    def __str__(self) : return self.name
    
    
agent_vendor_table=Table('bby_master_agent_vendor', metadata,
    Column('agent_id', Integer, ForeignKey('bby_master_agent.id',
        onupdate = "CASCADE", ondelete = "CASCADE"), primary_key = True),
    Column('vendor_id', Integer, ForeignKey('bby_master_vendor.id',
        onupdate = "CASCADE", ondelete = "CASCADE"), primary_key = True)
)



class BBYAgent(DeclarativeBase, SysMixin):
    __tablename__ = "bby_master_agent"

    id = Column(Integer, primary_key = True)
    name = Column(Unicode(200))
    description = Column(Unicode(1000))
    vendors =relation('BBYVendor', secondary = agent_vendor_table, backref = 'agents')
    
    def __str__(self) : return self.name

    @property
    def vendor_ids(self):
        return map(lambda o:str(o.id),self.vendors)
    
    
    
class BBYContact(DeclarativeBase, SysMixin):
    __tablename__ = "bby_master_contact"

    id = Column(Integer, primary_key = True)
    name = Column(Unicode(200))
    email = Column(Unicode(500))
    phone = Column(Unicode(50))
    
    def __str__(self) : return self.name
    
    


#===============================================================================
# workflow's data header
#===============================================================================
class BBYJobHeader(DeclarativeBase, SysMixin):
    __tablename__ = 'bby_job_header'

    id = Column(Integer, primary_key = True)
    sku = Column(Unicode(100), info = {'field_name': "SKU#"})
    upc_no = Column(Unicode(100), info = {'field_name': "UPC#"})
    product_description = Column(Unicode(1000), info = {'field_name': "Product Descrption", 'auto_log' : True})
    brand_id = Column(Integer, ForeignKey('bby_master_brand.id'), info = {'field_name': "Brand"})
    brand = relation(BBYBrand)
    ioq = Column(Unicode(100), info = {'field_name': "IOQ"})
    aoq = Column(Unicode(100), info = {'field_name': "AOQ"})
    vendor_id = Column(Integer, ForeignKey('bby_master_vendor.id'), info = {'field_name': "Vendor"})
    vendor = relation(BBYVendor)
    packaging_format_id = Column(Integer, ForeignKey('bby_master_packaging_format.id'), info = {'field_name': "Package Format"})
    packaging_format = relation(BBYPackagingFormat)
    pd_id = Column(Integer, ForeignKey('bby_master_teammate.id'), info = {'field_name': "PD"})
    pd = relation(BBYTeammate, primaryjoin = pd_id == BBYTeammate.id, lazy = False)
    ae_id = Column(Integer, ForeignKey('bby_master_teammate.id'), info = {'field_name': "AE"})
    ae = relation(BBYTeammate, primaryjoin = ae_id == BBYTeammate.id, lazy = False)
    closure = relation(BBYClosure)
    closure_id = Column(Integer, ForeignKey('bby_master_closure.id'), info = {'field_name': "Closure"})
    display_mode = relation(BBYDisplayMode)
    display_mode_id = Column(Integer, ForeignKey('bby_master_display_mode.id'), info = {'field_name': "Display Mode"})
    formed_size_l = Column(Unicode(10))
    formed_size_w = Column(Unicode(10))
    formed_size_h = Column(Unicode(10))

    attachment = Column(Unicode(100), default = None)
    status = Column(Integer, default = 10)
    control_flag = Column(Integer, default = 0) #it's used to keep the status when it's on hold 
    
    agent_id = Column(Integer, ForeignKey('bby_master_agent.id'), info = {'field_name': "Agent"})
    agent = relation(BBYAgent, primaryjoin = agent_id == BBYAgent.id, lazy = False)

    bby_asia_contact_id = Column(Integer, ForeignKey('bby_master_contact.id'))
    bby_asia_contact = relation(BBYContact,primaryjoin = bby_asia_contact_id == BBYContact.id, lazy = False)
    bby_us_contact_id = Column(Integer, ForeignKey('bby_master_contact.id'))
    bby_us_contact = relation(BBYContact,primaryjoin = bby_us_contact_id == BBYContact.id, lazy = False)

    @property
    def history(self):
        return DBSession.query(BBYLog).filter(BBYLog.job_id == self.id).order_by(BBYLog.create_time)

    def basic_info_populate(self, strFormater = lambda v1 : v1 or "",
                 intFormater = lambda v2 : str(v2 or ""),
                 floatFormater = lambda v3 : str(v3 or ""),
                 dateFormater = lambda v4 : v4.strftime("%Y-%m-%d") if v4 else "",
                 relationFormater = lambda v5 : str(v5 or "")):

        strFields = ["sku", "upc_no", "product_description", "ioq", "aoq", ]
        intFields = ["id", "brand_id", "vendor_id", "packaging_format_id", "pd_id", "ae_id",
                     "closure_id", "display_mode_id", "create_by_id", "update_by_id","agent_id" ]
#        floatFields=["", "", "", "", "", "", "", "", "", "", "", "", "", "", ]
        dateFields = ["create_time", "update_time"]
        relationFields = ["brand", "vendor", "packaging_format", "pd", "ae", "create_by", 
                          "update_by", "closure", "display_mode","agent","bby_asia_contact","bby_us_contact"]
        vs = {
              "eol" : self.is_eol(),
              "completed" : self.is_complete(), 
              "cancel" : self.is_cancel(), 
              "on_hold" : self.is_on_hold(), 
              "formed_size" : self.formed_size
              }
        for f1 in strFields : vs[f1] = strFormater(getattr(self, f1))
        for f2 in intFields : vs[f2] = intFormater(getattr(self, f2))
#        for f3 in floatFields : vs[f3]=floatFormater(getattr(self, f3))
        for f4 in dateFields : vs[f4] = dateFormater(getattr(self, f4))
        for f5 in relationFields : vs[f5] = relationFormater(getattr(self, f5))
        return vs

    def is_eol(self):
        return self.status == EOL
        
    def is_complete(self):
        return self.status == COMPLETED

    def is_cancel(self):
        return self.control_flag == CANCEL

    def is_on_hold(self):
        return self.control_flag == ON_HOLD

    def is_editable(self):
        return self.status != COMPLETED and self.control_flag != CANCEL

    @property
    def formed_size(self):
        try:
            return " x ".join(filter(bool, [self.formed_size_l, self.formed_size_w, self.formed_size_h]))
        except:
            return ""
        
    def __str__(self): return self.sku
    def __repr__(self): return self.sku

#===============================================================================
# save the workflow's related log
#===============================================================================
class BBYLog(DeclarativeBase, SysMixin):
    __tablename__ = 'bby_log'

    id = Column(Integer, primary_key = True)
    job_id = Column(Integer, ForeignKey('bby_job_header.id'))
    job = relation(BBYJobHeader)
    detail_id = Column(Integer)
    detail_type = Column(Unicode(100), info = {'label': "Detail Type" , "cltest" : "kkk"})
    action_type = Column(Unicode(100), nullable = False)
    remark = Column(Unicode(2000))

    @property
    def detail(self):
        try:
            return DBSession.query(globals()[self.detail_type]).get(self.detail_id)
        except:
            return None


#===============================================================================
# define the logic data structure as below:(Please start the class with 'BBY')
#===============================================================================

class BBYSKUInfo(DeclarativeBase, SysMixin):
    __tablename__ = 'bby_sku_info'

    id = Column(Integer, primary_key = True)
    header_id = Column(Integer, ForeignKey('bby_job_header.id'))
    header = relation(BBYJobHeader, backref = backref("sku_info", order_by = id), primaryjoin = "and_(BBYJobHeader.id == BBYSKUInfo.header_id, BBYSKUInfo.active == 0)")
    row_name = Column(Unicode(100), default = None)
    row_detail = Column(JSONCol(5000)) #example : [{"date": "2011-05-03", "files": [{"file_name": "index_04.jpg", "file_id": 342}], "remark": null, "id": 0, "confirm": "Y"}]
    


class BBYPCR(DeclarativeBase, SysMixin):
    __tablename__ = 'bby_pcr'

    id = Column(Integer, primary_key = True)
    header_id = Column(Integer, ForeignKey('bby_job_header.id'))
    header = relation(BBYJobHeader, backref = backref("pcr", order_by = 'BBYPCR.receive_date'), primaryjoin = "and_(BBYJobHeader.id == BBYPCR.header_id, BBYPCR.active == 0)")
    no = Column(Text,default=None)
    file_name = Column(Text,default=None)
    file_id = Column(Integer)
    receive_date = Column(Text,default=None)
    

#class BBYMockup(DeclarativeBase, SysMixin):
#    __tablename__ = 'bby_mockup'
#    __detail_title = 'Mock Up'
#
#    id = Column(Integer, primary_key = True)
#    header_id = Column(Integer, ForeignKey('bby_job_header.id'))
#    header = relation(BBYJobHeader, backref = backref("mockups", order_by = id))
#    package_id = Column(Integer, ForeignKey('bby_master_packaging_format.id'))
#    package = relation(BBYPackagingFormat)
#    sample_received_date = Column(DateTime)
#    courier_id = Column(Integer, ForeignKey('bby_master_courier.id'))
#    courier = relation(BBYCourier)
#    awb = Column(Unicode(20))
#    attachment = Column(Unicode(100), default = None)
#    status = Column(Unicode(50))
#
#    def getAttachments(self):
#        try:
#            return DBSession.query(UploadObject).filter(UploadObject.id.in_(self.attachment.split("|"))).order_by(UploadObject.create_time).all()
#        except:
#            return []



class BBYOption(DeclarativeBase, SysMixin):
    __tablename__ = 'bby_mockup_option'

    id = Column(Integer, primary_key = True)

    header_id = Column(Integer, ForeignKey('bby_job_header.id'))
    header = relation(BBYJobHeader, backref = backref("options", order_by = id), primaryjoin = "and_(BBYJobHeader.id == BBYOption.header_id, BBYOption.active == 0)")
    name = Column(Unicode(50))
    final = Column(Unicode(5))
    sample_received_date = Column(DateTime)
    attachment = Column(Unicode(100), default = None)
    attachment_pdf = Column(Unicode(1000))

    def getAttachments(self):
        try:
            return DBSession.query(UploadObject).filter(UploadObject.id.in_(self.attachment.split("|"))).order_by(UploadObject.create_time).all()
        except:
            return []

    def getTesting(self, test_type):
        return DBSession.query(BBYTesting).filter(BBYTesting.active == 0).filter(BBYTesting.option_id == self.id).filter(BBYTesting.test_type == test_type).order_by(BBYTesting.round,BBYTesting.id)

    def getMaxVendorFittingRound(self):
        max = DBSession.query(func.max(BBYVendorFitting.round)).filter(BBYVendorFitting.option_id==self.id).filter(BBYVendorFitting.active==0).one()
        return max[0] if max else None

    def getMaxInternalFittingRound(self):
        max = DBSession.query(func.max(BBYInternalFitting.round)).filter(BBYInternalFitting.option_id==self.id).filter(BBYInternalFitting.active==0).one()
        return max[0] if max else None

    def get_pdf_attachments(self):
        try:
            results = DBSession.query(UploadObject).filter(UploadObject.id.in_(self.attachment_pdf.split("|"))).order_by(UploadObject.create_time).all()
            return DBSession.query(UploadObject).filter(UploadObject.id.in_(self.attachment_pdf.split("|"))).order_by(UploadObject.create_time).all()
        except:
            return []

    def save_pdf(self, file_name, file_path):
        upload_object = UploadObject(_file_path=file_path, file_name=file_name)
        DBSession.add(upload_object)
        DBSession.flush()
        self.attachment_pdf = self.attachment_pdf+"|"+str(upload_object.id) if self.attachment_pdf else upload_object.id
        DBSession.merge(self)
        
        
    def get_max_internal_fitting_round(self):
        return DBSession.query(func.max(BBYInternalFitting.round)).filter(and_(BBYInternalFitting.active == 0, 
                            BBYInternalFitting.option_id == self.id)).scalar() or 0
    
    def get_max_testing_line(self,test_type,round):
        return DBSession.query(func.max(BBYTesting.round)).filter(and_(BBYTesting.active == 0, 
                            BBYTesting.option_id == self.id, BBYTesting.test_type == test_type,
                            BBYTesting.round == round)).scalar() or 0

    def __str__(self): return str(self.name)

    def __repr__(self): return str(self.name)



class BBYComponent(DeclarativeBase, SysMixin):
    __tablename__ = 'bby_mockup_component'

    id = Column(Integer, primary_key = True)

    option_id = Column(Integer, ForeignKey('bby_mockup_option.id'))
    option = relation(BBYOption, backref = backref("components", order_by = id), primaryjoin = "and_(BBYOption.id == BBYComponent.option_id, BBYComponent.active == 0)")

    format_id = Column(Integer, ForeignKey('bby_master_packaging_format.id'))
    format = relation(BBYPackagingFormat)

    material_id = Column(Integer, ForeignKey('bby_master_material.id'))
    material = relation(BBYMaterial, primaryjoin = material_id == BBYMaterial.id)

    coating_id = Column(Integer, ForeignKey('bby_master_spec.id'))
    coating = relation(BBYSpec, primaryjoin = coating_id == BBYSpec.id)

    front_color_id = Column(Integer, ForeignKey('bby_master_color.id'))
    front_color = relation(BBYColor, primaryjoin = front_color_id == BBYColor.id)

    back_color_id = Column(Integer, ForeignKey('bby_master_color.id'))
    back_color = relation(BBYColor, primaryjoin = back_color_id == BBYColor.id)

#    finished_size = Column(Unicode(100))

    finished_size_l = Column(Unicode(10))
    finished_size_w = Column(Unicode(10))
    finished_size_h = Column(Unicode(10))

    closure = relation(BBYClosure)
    closure_id = Column(Integer, ForeignKey('bby_master_closure.id'))

    display_mode = relation(BBYDisplayMode)
    display_mode_id = Column(Integer, ForeignKey('bby_master_display_mode.id'))

    remark = Column(Unicode(500))

    factory_id = Column(Integer, ForeignKey('bby_master_source.id'))
    factory = relation(BBYSource)

    def __str__(self): return str(self.format)

    def __repr__(self): return str(self.format)

    @property
    def finished_size(self):
        try:
            return " x ".join(filter(bool, [self.finished_size_l, self.finished_size_w, self.finished_size_h]))
        except:
            return ""


class BBYInternalFitting(DeclarativeBase, SysMixin):
    __tablename__ = 'bby_internal_fitting'

    id = Column(Integer, primary_key = True)
    option_id = Column(Integer, ForeignKey('bby_mockup_option.id'))
    option = relation(BBYOption, backref = backref("internal_fittings", order_by = id), primaryjoin = "and_(BBYOption.id == BBYInternalFitting.option_id, BBYInternalFitting.active == 0)")

    round = Column(Integer)
    content = Column(Unicode(50))

#    component_id = Column(Integer, ForeignKey('bby_mockup_component.id'))
#    component = relation(BBYComponent)
#    received_date = Column(DateTime)
#    source_id = Column(Integer, ForeignKey('bby_master_source.id'))
#    source = relation(BBYSource)
#    test_by_id = Column(Integer, ForeignKey('bby_master_teammate.id'))
#    test_by = relation(BBYTeammate)
#    qty = Column(Integer)
#    result = Column(Unicode(5))
#    reported_date = Column(DateTime)
#    reason_id = Column(Integer, ForeignKey('bby_master_failure_reason.id'))
#    reason = relation(BBYFailureReason)
#    attachment = Column(Unicode(100), default = None)
#    remark = Column(Unicode(1000))
#    courier_id = Column(Integer, ForeignKey('bby_master_courier.id'))
#    courier = relation(BBYCourier)
#    awb = Column(Unicode(20))

    def getContent(self, justID = False):
        if justID:
            try:
                return self.content.split("|")
            except:
                return []
        else:
            try:
                return [DBSession.query(BBYMockupContent).get(c) for c in self.content.split("|")]
            except:
                return []

    


class BBYInternalFittingDetail(DeclarativeBase, SysMixin):
    __tablename__ = 'bby_internal_fitting_detail'
    
    id = Column(Integer, primary_key = True)
    header_id = Column(Integer, ForeignKey('bby_internal_fitting.id'))
    header = relation(BBYInternalFitting, backref = backref("details", order_by = id), primaryjoin = "and_(BBYInternalFitting.id == BBYInternalFittingDetail.header_id, BBYInternalFittingDetail.active == 0)")
    
    component_id = Column(Integer, ForeignKey('bby_mockup_component.id'))
    component = relation(BBYComponent)

#    content = Column(Unicode(50))
    received_date = Column(DateTime)
    source_id = Column(Integer, ForeignKey('bby_master_source.id'))
    source = relation(BBYSource)
    test_by_id = Column(Integer, ForeignKey('bby_master_teammate.id'))
    test_by = relation(BBYTeammate)
    qty = Column(Integer)
    result = Column(Unicode(5))
    reported_date = Column(DateTime)
    reason_id = Column(Integer, ForeignKey('bby_master_failure_reason.id'))
    reason = relation(BBYFailureReason)
    attachment = Column(Unicode(100), default = None)
    remark = Column(Unicode(1000))
    courier_id = Column(Integer, ForeignKey('bby_master_courier.id'))
    courier = relation(BBYCourier)
    awb = Column(Unicode(20))


    def getAttachments(self):
        try:
            return DBSession.query(UploadObject).filter(UploadObject.id.in_(self.attachment.split("|"))).order_by(UploadObject.create_time).all()
        except:
            return []

class BBYTesting(DeclarativeBase, SysMixin):
    __tablename__ = 'bby_testing'

    id = Column(Integer, primary_key = True)
    #the field below to identify the testing
    option_id = Column(Integer, ForeignKey('bby_mockup_option.id'))
    option = relation(BBYOption, backref = backref("testings", order_by = id), primaryjoin = "and_(BBYOption.id == BBYTesting.option_id, BBYTesting.active == 0)")
    round = Column(Integer)
    line = Column(Integer,default=0)
    component_id = Column(Integer, ForeignKey('bby_mockup_component.id'))
    component = relation(BBYComponent)
    test_type = Column(Unicode(10))

    send_date = Column(DateTime)
    source_id = Column(Integer, ForeignKey('bby_master_source.id'))
    source = relation(BBYSource)
    test_by_id = Column(Integer, ForeignKey('bby_master_teammate.id'))
    test_by = relation(BBYTeammate)
    qty = Column(Integer)
    result = Column(Unicode(5))
    reported_date = Column(DateTime)
    reason_id = Column(Integer, ForeignKey('bby_master_failure_reason.id'))
    reason = relation(BBYFailureReason)
    attachment = Column(Unicode(100), default = None)
    remark = Column(Unicode(1000))
#    courier_id = Column(Integer, ForeignKey('bby_master_courier.id'))
#    courier = relation(BBYCourier)
#    awb = Column(Unicode(20))

    def getAttachments(self):
        try:
            return DBSession.query(UploadObject).filter(UploadObject.id.in_(self.attachment.split("|"))).order_by(UploadObject.create_time).all()
        except:
            return []



class BBYVendorFitting(DeclarativeBase, SysMixin):
    __tablename__ = 'bby_vendor_fitting'

    id = Column(Integer, primary_key = True)
    option_id = Column(Integer, ForeignKey('bby_mockup_option.id'))
    option = relation(BBYOption, backref = backref("vendor_fittings", order_by = id), primaryjoin = "and_(BBYOption.id == BBYVendorFitting.option_id, BBYVendorFitting.active == 0)")
    component_id = Column(Integer, ForeignKey('bby_mockup_component.id'))
    component = relation(BBYComponent, backref = backref("vendor_fittings", order_by = id), primaryjoin = "and_(BBYComponent.id == BBYVendorFitting.component_id, BBYVendorFitting.active == 0)")
    round = Column(Integer)
    receive_date = Column(DateTime)

    send_date = Column(DateTime)
    source_id = Column(Integer, ForeignKey('bby_master_source.id'))
    source = relation(BBYSource)
    qty = Column(Integer)
    reported_date = Column(DateTime)
    attachment = Column(Unicode(100), default = None)
    remark = Column(Unicode(1000))
    courier_id = Column(Integer, ForeignKey('bby_master_courier.id'))
    courier = relation(BBYCourier)
    awb = Column(Unicode(20))
    confirm = Column(Unicode(5))

    def getAttachments(self):
        try:
            return DBSession.query(UploadObject).filter(UploadObject.id.in_(self.attachment.split("|"))).order_by(UploadObject.create_time).all()
        except:
            return []

class BBYCasepackDetail(DeclarativeBase, SysMixin):
    __tablename__ = 'bby_casepack_detail'

    id = Column(Integer, primary_key = True)

    component_id = Column(Integer, ForeignKey('bby_mockup_component.id'))
    component = relation(BBYComponent, backref = backref("casepack_details", order_by = id), primaryjoin = "and_(BBYComponent.id == BBYCasepackDetail.component_id, BBYCasepackDetail.active == 0)")
    qty = Column(Integer, default = None)
    required_date = Column(DateTime)
    ship_to_id = Column(Integer, ForeignKey('bby_master_vendor.id'))
    ship_to = relation(BBYVendor)
#    attention_id = Column(Integer, ForeignKey('bby_master_teammate.id'))
#    attention = relation(BBYTeammate)
    attention = Column(Unicode(100))
    remark = Column(Unicode(2000))



class BBYCasepackEmail(DeclarativeBase, SysMixin):
    __tablename__ = 'bby_casepack_email'

    id = Column(Integer, primary_key = True)

    send_to = Column(Unicode(500))
    cc_to = Column(Unicode(500))
    content = Column(Unicode(10000))
    attachment = Column(Unicode(100))



class BBYCasepackToFactory(DeclarativeBase, SysMixin):
    __tablename__ = 'bby_casepack_factory_record'

    id = Column(Integer, primary_key = True)

    header_id = Column(Integer, ForeignKey('bby_job_header.id'))
    header = relation(BBYJobHeader, backref = backref("to_factory_records", order_by = id), primaryjoin = "and_(BBYJobHeader.id == BBYCasepackToFactory.header_id, BBYCasepackToFactory.active == 0)")

    round = Column(Integer)
    component_id = Column(Integer, ForeignKey('bby_master_packaging_format.id'))
    component = relation(BBYPackagingFormat)
    factory_id = Column(Integer, ForeignKey('bby_master_source.id'))
    factory = relation(BBYSource)
    required_date = Column(DateTime)
    qty = Column(Integer, default = None)
    email_id = Column(Integer, ForeignKey('bby_casepack_email.id'))
    email = relation(BBYCasepackEmail)

    #new add
#    ship_to_id = Column(Integer, ForeignKey('bby_master_vendor.id'))
#    ship_to = relation(BBYVendor)
    ship_to = Column(Unicode(100))
    ship_to_address = awb = Column(Unicode(1000))
    ship_to_att = Column(Unicode(100))
    ship_to_phone = Column(Unicode(50))
    send_date = Column(DateTime)
    courier_id = Column(Integer, ForeignKey('bby_master_courier.id'))
    courier = relation(BBYCourier)
    awb = Column(Unicode(100))
    received_date = Column(DateTime)
    remark = Column(Unicode(2000))
    cancel = Column(Unicode(10))
    approve = Column(Unicode(10))

    @classmethod
    def get_last_seq(clz, header_id):
        return DBSession.query(func.max(clz.round)).filter(and_(clz.active == 0, clz.header_id == header_id)).scalar()

#
#class BBYCasepackFromFactory(DeclarativeBase, SysMixin):
#    __tablename__ = 'bby_casepack_from_factory_record'
#
#    id = Column(Integer, primary_key = True)
#
#    header_id = Column(Integer, ForeignKey('bby_job_header.id'))
#    header = relation(BBYJobHeader, backref = backref("from_factory_records", order_by = id), primaryjoin = "and_(BBYJobHeader.id == BBYCasepackFromFactory.header_id, BBYCasepackFromFactory.active == 0)")
#
#    qty = Column(Integer, default = None)
#    ship_to_id = Column(Integer, ForeignKey('bby_master_vendor.id'))
#    ship_to = relation(BBYVendor)
#    send_date = Column(DateTime)
#    courier_id = Column(Integer, ForeignKey('bby_master_courier.id'))
#    courier = relation(BBYCourier)
#    awb = Column(Unicode(100))
#    received_date = Column(DateTime)
#    remark = Column(Unicode(2000))
#    cancel = Column(Unicode(10))
#    approve = Column(Unicode(10))



class BBYCasepackResult(DeclarativeBase, SysMixin):
    __tablename__ = 'bby_casepack_result'

    id = Column(Integer, primary_key = True)
    header_id = Column(Integer, ForeignKey('bby_job_header.id'))
    header = relation(BBYJobHeader, backref = backref("results", order_by = id), primaryjoin = "and_(BBYJobHeader.id == BBYCasepackResult.header_id, BBYCasepackResult.active == 0)")
    received_date = Column(DateTime)
    send_out_date = Column(DateTime)
#    source_id = Column(Integer, ForeignKey('bby_master_source.id'))
#    source = relation(BBYSource)
#    test_by_id = Column(Integer, ForeignKey('bby_master_teammate.id'))
#    test_by = relation(BBYTeammate)
    customer_received_date = Column(DateTime)
    test_by = Column(Unicode(100))
    qty = Column(Integer)
    result = Column(Unicode(5))
    reported_date = Column(DateTime)
    reason_id = Column(Integer, ForeignKey('bby_master_failure_reason.id'))
    reason = relation(BBYFailureReason)
    attachment = Column(Unicode(100), default = None)
    remark = Column(Unicode(1000))
    status = Column(Unicode(50))

    refer_to_id = Column(Integer)

#    @property
#    def refer_to(self):
#        try:
#            return DBSession.query(BBYCasepackFromFactory).get(self.refer_to_id)
#        except:
#            return None

    def getAttachments(self):
        try:
            return DBSession.query(UploadObject).filter(UploadObject.id.in_(self.attachment.split("|"))).order_by(UploadObject.create_time).all()
        except:
            return []
