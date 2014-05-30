# -*- coding: utf-8 -*-
from datetime import datetime as dt

from tg import request
from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode

from tribal.model import DeclarativeBase, metadata, DBSession
from tribal.model.auth import *

__all__=["LemmiOrderHeader", "LemmiOrderDetail"]

def getUserID():
    user_id = 1
    try:
         user_id = request.identity["user"].user_id
    except:
        pass
    finally:
        return user_id

class SysMixin(object):
    create_time = Column(DateTime, default=dt.now)
    create_by_id = Column(Integer, default=getUserID)
    update_time = Column(DateTime, default=dt.now, onupdate=dt.now)
    update_by_id = Column(Integer, default=getUserID, onupdate=getUserID)
    active = Column(Integer, default = 0) # 0 is active ,1 is inactive

    @classmethod
    def get(cls, id):
        return DBSession.query(cls).get(int(id))

    @classmethod
    def find_all(cls):
        return DBSession.query(cls).all()

    @classmethod
    def find_by_ids(cls, ids):
        return DBSession.query(cls).filter(cls.id.in_([int(i) for i in ids.split(',')])).all()

    @property
    def create_by(self):
        return DBSession.query(User).filter(User.user_id==self.create_by_id).first()

    @property
    def update_by(self):
        return DBSession.query(User).filter(User.user_id==self.update_by_id).first()


class LemmiOrderHeader(DeclarativeBase, SysMixin):
    __tablename__='lemmi_order_header'

    id = Column(Integer, primary_key=True)
    # Application area
    type = Column('type', Unicode(100))
    versionId = Column('version_id', Unicode(30))
    sender = Column('sender', Unicode(100))
    receiver = Column('receiver', Unicode(100))
    created = Column('created', DateTime)
    # Application area =========================
    # Order Header
    orderNumber = Column('order_number', Unicode(100)) #
    dispatchDate = Column('dispatch_date', Date)
    releaseMethod = Column('release_method', Unicode(50))
    countryOfOrigin = Column('country_of_origin', Unicode(100))
    serviceLevel = Column('service_level', Unicode(50))
    vendorNumber = Column('vendor_number', Unicode(50))
    # DeliveryAddress 
    companyName = Column('company_name', Unicode(100))
    contactPerson = Column('contact_person', Unicode(100))
    street1 = Column('street1', Unicode(100))
    street2 = Column('street2', Unicode(100))
    street3 = Column('street3', Unicode(100))
    zip = Column('zip', Unicode(30))
    city = Column('city', Unicode(100))
    state = Column('state', Unicode(100))
    countryName = Column('country_name', Unicode(100))
    countryCode = Column('country_code', Unicode(50))
    phone = Column('phone', Unicode(50))
    fax = Column('fax', Unicode(50))
    email = Column('email', Unicode(100))
    # Order Header =====================================
    billTo = Column("bill_to", Unicode(300))
    status = Column('status', Integer, default=1) # 1, new ; 2,mutation(update); 3,detele; 4, released
    released = Column(DateTime)
    originalFilename = Column("original_filename", Unicode(100)) # original xml file name
    filename = Column("filename", Unicode(100)) # xml file name
    

    
class LemmiOrderDetail(DeclarativeBase, SysMixin):
    __tablename__='lemmi_order_detail'

    id = Column(Integer, primary_key=True)
    header_id = Column(Integer, ForeignKey('lemmi_order_header.id'))
    header = relation(LemmiOrderHeader,  backref=backref("details", order_by=id))
    # Order Line
    productId = Column('product_id', Unicode(100))
    type2 = Column('type2', Unicode(30)) # 1, new; 2, update; 3, delete
    customerOrderLineId = Column('customer_order_line_id', Unicode(100)) #
    quantity = Column('quantity', Integer)
    # Order Line ======================================================
    # Line Item
    quantity3 = Column('quantity3', Integer)
    # Variable data field
    itemNo = Column('item_no', Unicode(100))
    labelColor = Column('label_color', Unicode(50))
    textLine1 = Column('text_line1', Unicode(100))
    textLine2 = Column('text_line2', Unicode(100))
    textLine3 = Column('text_line3', Unicode(100))
    model = Column('model', Unicode(100))
    modelDescription = Column('model_description', Unicode(100))
    color = Column('color', Unicode(30))
    size = Column('size', Unicode(30))
    waistSize = Column('waist_size', Unicode(30))
    widthLength = Column('width_length', Unicode(80))
    age = Column('age', Unicode(50))
    sex = Column('sex', Unicode(30))
    season = Column('season', Unicode(30))
    currency = Column('currency', Unicode(20))
    retailPrice = Column('retail_price', Unicode(20))
    prodOrder = Column('prod_order', Unicode(30))
    gtin = Column('gtin', Unicode(30))
    # Line Item =======================================================
    filename = Column("filename", Unicode(100)) # xml file name












