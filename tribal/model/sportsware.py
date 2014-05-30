# coding: utf-8

from datetime import datetime as dt
from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, TypeDecorator, DateTime, Text, Float

from tribal.model import DeclarativeBase,metadata,DBSession
from tribal.model.auth import User

from tribal.util.common import *


__all__ = ["TRBHeaderPO", "TRBDetailPO", "TRBOrderFormHeader", "TRBOrderFormDetail",
           "TRBBillTo", "TRBShipTo"]


DB_DATETIME_FORMAT = ""
WEB_DATETIME_FORMAT = "%Y/%m/%d"

class RPACDateTime(TypeDecorator):
    impl = DateTime
    def process_bind_param(self, value, dialect):
        if not value : return None
        return dt.strptime(value,WEB_DATETIME_FORMAT)

class TRBBillTo(DeclarativeBase):
    __tablename__ = "trb_bill_to"

    id          = Column(Integer,primary_key=True)
    company     = Column("company",Unicode(100))
    address     = Column("address",Unicode(200))
    attn        = Column("attn",Unicode(20))
    tel         = Column("tel",Unicode(50))
    fax         = Column("fax",Unicode(50))
    email       = Column("email",Unicode(50))

    def __unicode__(self): return self.company

class TRBShipTo(DeclarativeBase):
    __tablename__ = "trb_ship_to"

    id          = Column(Integer,primary_key=True)
    company     = Column("company",Unicode(100))
    address     = Column("address",Unicode(200))
    attn        = Column("attn",Unicode(20))
    tel         = Column("tel",Unicode(50))
    fax         = Column("fax",Unicode(50))
    email       = Column("email",Unicode(50))

    def __unicode__(self): return self.company

class TRBHeaderPO(DeclarativeBase):
    __tablename__ = "trb_header_po"

    id = Column(Integer, primary_key = True)
    label = Column("label", Unicode(50))
    cutNo = Column("cut_no", Unicode(20))
    status = Column("status", Unicode(10))
    active = Column("active", Integer, default = 0)

    def __unicode__(self): return self.cutNo
    
   

class TRBDetailPO(DeclarativeBase):
    __tablename__ = "trb_detail_po"

    id = Column(Integer, primary_key = True)
    headerid = Column("header_id", Integer, ForeignKey("trb_header_po.id"))
    header = relation(TRBHeaderPO, backref = "details")
    barcode = Column("barcode", Unicode(25))
    style = Column("style", Unicode(20))
    size = Column("size", Integer)
    styleDesc = Column("style_desc", Unicode(50))
    cleDesc = Column("cle_desc", Unicode(50))
    sourcingZone = Column("sourcing_zone", Unicode(20))
    quantity = Column("quantity", Integer, default = 0)
    status = Column("status", Unicode(10))
    active = Column("active", Integer, default = 0)

    def __unicode__(self): return self.id

class TRBOrderFormHeader(DeclarativeBase):
    __tablename__ = "trb_order_form_header"

    id = Column(Integer, primary_key = True)
    headerId = Column("header_id", Integer, ForeignKey("trb_header_po.id"))
    header = relation(TRBHeaderPO, backref = "orders")
    orderDate = Column("order_date", DateTime, default = dt.now())
    customerPO = Column("cust_po", Unicode(50))
    tel = Column("tel",Unicode(30))
    requestShipDate = Column("request_ship_date",DateTime, default = dt.now())
    shipMethod = Column("ship_method",Unicode(20))
    billId = Column("bill_id", Integer, ForeignKey("trb_bill_to.id"))
    billTo = relation(TRBBillTo, backref = "billto")
    shipId = Column("ship_id", Integer, ForeignKey("trb_ship_to.id"))
    shipTo = relation(TRBShipTo, backref = "shipto")
    issuedById = Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy = relation(User, primaryjoin = issuedById == User.user_id)
    lastModifyById = Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy = relation(User, primaryjoin = lastModifyById == User.user_id)
    status = Column("status",Unicode(10))
    active = Column("active",Integer,default=0)

    def __unicode__(self): return self.id
  
    
    def total_qty(self):
        qty = 0
        for item in self.formDetails:
            qty += item.quantity
        
        return qty

    
    def populate(self, dateTimeFormat=None):

        return  [self.header.cutNo, Date2Text(self.orderDate, dateTimeFormat), null2blank(self.customerPO), null2blank(self.tel),
                 Date2Text(self.requestShipDate, dateTimeFormat), null2blank(self.shipMethod), null2blank(self.billTo.company), null2blank(self.billTo.address),
                 null2blank(self.billTo.attn), null2blank(self.billTo.tel), null2blank(self.billTo.fax), null2blank(self.billTo.email),
                 null2blank(self.shipTo.company), null2blank(self.shipTo.address), null2blank(self.shipTo.attn), null2blank(self.shipTo.tel),
                 null2blank(self.shipTo.fax), null2blank(self.shipTo.email),]

class TRBOrderFormDetail(DeclarativeBase):
    __tablename__ = "trb_order_form_detail"

    id = Column(Integer, primary_key = True)
    headerId = Column("header_id", Integer, ForeignKey("trb_order_form_header.id"))
    header = relation(TRBOrderFormHeader, backref = "formDetails")
    detailPOId = Column("detail_po_id", Integer, ForeignKey("trb_detail_po.id"))
    detailPO = relation(TRBDetailPO, backref = "detailPO")
    quantity = Column("quantity", Integer, default = 0)
    status = Column("status",Unicode(10))
    active = Column("active",Integer,default=0)

    def __unicode__(self): return self.id
    
   