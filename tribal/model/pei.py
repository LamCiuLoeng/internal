# -*- coding: utf-8 -*-
from datetime import datetime as dt

from tg import request
from sqlalchemy import *
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.orm import mapper, relation
from sqlalchemy.orm import relation, backref
from sqlalchemy.schema import Table, Column
from sqlalchemy.sql.expression import desc
from sqlalchemy.types import Integer, Unicode

from tribal.model import DeclarativeBase, metadata, DBSession
from tribal.model.auth import *
from tribal.util.sql_helper import *

class PEIBillTo(DeclarativeBase):
    __tablename__ = "pei_bill_to"

    id = Column(Integer, primary_key = True)
    company = Column("company", Unicode(100))
    address = Column("address", Unicode(200))
    attn = Column("attn", Unicode(50))
    tel = Column("tel", Unicode(50))
    fax = Column("fax", Unicode(50))
    email = Column("email", Unicode(100))
    lastModifyTime = Column("last_modify_time", DateTime, default = dt.now())
    issuedById = Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy = relation(User, primaryjoin = issuedById == User.user_id)
    lastModifyById = Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy = relation(User, primaryjoin = lastModifyById == User.user_id)

    def __unicode__(self): return self.company

    @classmethod
    def all_billtos(cls): return DBSession.query(cls).order_by(cls.company).all()

    @classmethod
    def get(cls, ** args): return DBSession.query(cls).get(int(args.get('id', 0)))

class PEIShipTo(DeclarativeBase):
    __tablename__ = "pei_ship_to"

    id = Column(Integer, primary_key = True)
    company = Column("company", Unicode(100))
    address = Column("address", Unicode(200))
    attn = Column("attn", Unicode(50))
    tel = Column("tel", Unicode(50))
    fax = Column("fax", Unicode(50))
    email = Column("email", Unicode(100))
    lastModifyTime = Column("last_modify_time", DateTime, default = dt.now())
    issuedById = Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy = relation(User, primaryjoin = issuedById == User.user_id)
    lastModifyById = Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy = relation(User, primaryjoin = lastModifyById == User.user_id)

    def __unicode__(self): return self.company

    @classmethod
    def all_shiptos(cls): return DBSession.query(cls).order_by(cls.company).all()

    @classmethod
    def get(cls, ** args): return DBSession.query(cls).get(int(args.get('id', 0)))

class PEIBrand(DeclarativeBase):
    __tablename__ = 'pei_brand'

    id = Column(Integer, primary_key = True)
    name = Column(Unicode(50))
    lastModifyTime = Column("last_modify_time", DateTime, default = dt.now())
    issuedById = Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy = relation(User, primaryjoin = issuedById == User.user_id)
    lastModifyById = Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy = relation(User, primaryjoin = lastModifyById == User.user_id)

    def __unicode__(self): return self.name

class_attr = Table('pei_class_attr', metadata,
                   Column('class_id', Integer, ForeignKey('pei_item_class.id')),
                   Column('attr_id', Integer, ForeignKey('pei_item_class_attr.id')),
                   )

class PEIClassAttr(DeclarativeBase):
    __tablename__ = 'pei_item_class_attr'

    id = Column(Integer, primary_key = True)
    name = Column(Unicode(50))
    desc = Column(Unicode(200))
    lastModifyTime = Column("last_modify_time", DateTime, default = dt.now())
    issuedById = Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy = relation(User, primaryjoin = issuedById == User.user_id)
    lastModifyById = Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy = relation(User, primaryjoin = lastModifyById == User.user_id)

    def __unicode__(self): return self.name

class PEIItemClass(DeclarativeBase):
    __tablename__ = 'pei_item_class'

    id = Column(Integer, primary_key = True)
    name = Column(Unicode(50))
    desc = Column(Unicode(200))
    brand = relation(PEIBrand, backref = 'categories')
    brandId = Column('brand_id', Integer, ForeignKey('pei_brand.id'))
    attrs = relation(PEIClassAttr, secondary = class_attr, backref = 'attr_classes')
    lastModifyTime = Column("last_modify_time", DateTime, default = dt.now())
    issuedById = Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy = relation(User, primaryjoin = issuedById == User.user_id)
    lastModifyById = Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy = relation(User, primaryjoin = lastModifyById == User.user_id)

    def __unicode__(self): return self.name

    @classmethod
    def all_cls(cls): return DBSession.query(cls).order_by(cls.name).all()

    @classmethod
    def get(cls, ** args): return DBSession.query(cls).get(int(args.get('id', 0)))

item_attr = Table('pei_item_attr', metadata,
                  Column('item_id', Integer, ForeignKey('pei_item.id')),
                  Column('attr_id', Integer, ForeignKey('pei_attr.id')),
                  )

class PEIAttr(DeclarativeBase):
    __tablename__ = 'pei_attr'

    id = Column(Integer, primary_key = True)
    attrName = Column('attr_name', Unicode(50))
    attrDesc = Column('attr_desc', Unicode(500))
    lastModifyTime = Column("last_modify_time", DateTime, default = dt.now())
    issuedById = Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy = relation(User, primaryjoin = issuedById == User.user_id)
    lastModifyById = Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy = relation(User, primaryjoin = lastModifyById == User.user_id)

    def __unicode__(self): return self.attrName

    @classmethod
    def all_attrs(cls): return DBSession.query(cls).order_by(cls.attrName).all()

    @classmethod
    def get(cls, ** args): return DBSession.query(cls).get(int(args.get('id', 0)))

class PEIItem(DeclarativeBase):
    __tablename__ = 'pei_item'

    id = Column(Integer, primary_key = True)
    itemCode = Column('item_code', Unicode(50))
    itemDesc = Column('item_desc', Unicode(500))
    brand = relation(PEIBrand, backref = 'brand_items')
    brandId = Column('brand_id', Integer, ForeignKey('pei_brand.id'))
    itemClass = relation(PEIItemClass, backref = 'category_items')
    itemClassId = Column('category_id', Integer, ForeignKey('pei_item_class.id'))
    attrs = relation(PEIAttr, secondary = item_attr, backref = 'attr_items')
    lastModifyTime = Column("last_modify_time", DateTime, default = dt.now())
    issuedById = Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy = relation(User, primaryjoin = issuedById == User.user_id)
    lastModifyById = Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy = relation(User, primaryjoin = lastModifyById == User.user_id)

    def __unicode__(self): return self.itemCode

    @classmethod
    def all_items(cls): return DBSession.query(cls).order_by(cls.itemCode).all()

    @classmethod
    def get(cls, ** args):
        if args.get('id', 0):
            return DBSession.query(cls).get(int(args.get('id', 0)))
        elif args.get('itemCode', 0):
            return DBSession.query(cls).filter(cls.itemCode == args.get('itemCode', 0)).one()

class PEILanguage(DeclarativeBase):
    __tablename__ = 'pei_language'

    id = Column(Integer, primary_key = True)
    langName = Column('lang_name', Unicode(30))
    weight = Column(Integer)
    lastModifyTime = Column("last_modify_time", DateTime, default = dt.now())
    issuedById = Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy = relation(User, primaryjoin = issuedById == User.user_id)
    lastModifyById = Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy = relation(User, primaryjoin = lastModifyById == User.user_id)

    def __unicode__(self): return self.langName

class PEICategory(DeclarativeBase):
    """
    To differentiate the size, material and instruction,
    just use for same item in different language
    """
    __tablename__ = 'pei_category'

    id = Column(Integer, primary_key = True)
    name = Column(Unicode(10))
    lastModifyTime = Column("last_modify_time", DateTime, default = dt.now())
    issuedById = Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy = relation(User, primaryjoin = issuedById == User.user_id)
    lastModifyById = Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy = relation(User, primaryjoin = lastModifyById == User.user_id)

    def __unicode__(self): return self.name

class PEISize(DeclarativeBase):
    __tablename__ = 'pei_size'

    id = Column(Integer, primary_key = True)
    lang = relation(PEILanguage, backref = 'size_lang')
    langId = Column('lang_id', Integer, ForeignKey('pei_language.id'))
    category = relation(PEICategory, backref = 'size_cat')
    categoryId = Column('cat_id', Integer, ForeignKey('pei_category.id'))
    itemClass = relation(PEIItemClass, backref = "item_size")
    itemClassId = Column('item_class_id', Integer, ForeignKey('pei_item_class.id'))
    content = Column(Unicode(10))
    lastModifyTime = Column("last_modify_time", DateTime, default = dt.now())
    issuedById = Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy = relation(User, primaryjoin = issuedById == User.user_id)
    lastModifyById = Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy = relation(User, primaryjoin = lastModifyById == User.user_id)

    def __unicode__(self): return self.content

    @classmethod
    def all_sizes(cls, ** args):
        if 'itemClass' not in args.keys():
            return DBSession.query(cls) \
                    .filter(cls.langId == args.get('lang', 0)) \
                    .filter(cls.itemClassId == None).order_by(cls.id).all()
        else:
            return DBSession.query(cls) \
                    .filter(cls.langId == args.get('lang', 0)) \
                    .filter(cls.itemClassId == args.get('itemClass', '')).order_by(cls.id).all()

    @classmethod
    def get(cls, ** args): return DBSession.query(cls).get(int(args.get('id', 0)))

class PEIStyle(DeclarativeBase):
    __tablename__ = 'pei_style'

    id = Column(Integer, primary_key = True)
    lang = relation(PEILanguage, backref = 'style_lang')
    langId = Column('lang_id', Integer, ForeignKey('pei_language.id'))
    category = relation(PEICategory, backref = 'style_cat')
    categoryId = Column('cat_id', Integer, ForeignKey('pei_category.id'))
#    itemClass=relation(PEIItemClass, backref="item_style")
#    itemClassId=Column('item_class_id', Integer, ForeignKey('pei_item_class.id'))
    mainPart = Column('main_part', Unicode(100))
    extraPart = Column('extra_part', Unicode(100))
    lastModifyTime = Column("last_modify_time", DateTime, default = dt.now())
    issuedById = Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy = relation(User, primaryjoin = issuedById == User.user_id)
    lastModifyById = Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy = relation(User, primaryjoin = lastModifyById == User.user_id)

    def __unicode__(self): return self.content

    @classmethod
    def all_styles(cls, ** args):
        return DBSession.query(cls).filter(cls.langId == args.get('lang', 0)).order_by(cls.id).all()

    @classmethod
    def get(cls, ** args): return DBSession.query(cls).get(int(args.get('id', 0)))

class PEIColor(DeclarativeBase):
    __tablename__ = 'pei_color'

    id = Column(Integer, primary_key = True)
    lang = relation(PEILanguage, backref = 'color_lang')
    langId = Column('lang_id', Integer, ForeignKey('pei_language.id'))
    category = relation(PEICategory, backref = 'color_cat')
    categoryId = Column('cat_id', Integer, ForeignKey('pei_category.id'))
    name = Column(Unicode(100))
    code = Column(Unicode(100))
    lastModifyTime = Column("last_modify_time", DateTime, default = dt.now())
    issuedById = Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy = relation(User, primaryjoin = issuedById == User.user_id)
    lastModifyById = Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy = relation(User, primaryjoin = lastModifyById == User.user_id)

    def __unicode__(self): return self.content

    @classmethod
    def all_colors(cls, ** args):
        return DBSession.query(cls).filter(cls.langId == args.get('lang', 0)).order_by(cls.id).all()

    @classmethod
    def get(cls, ** args): return DBSession.query(cls).get(int(args.get('id', 0)))

class PEIUPC(DeclarativeBase):
    __tablename__ = 'pei_upc'

    id = Column(Integer, primary_key = True)
    name = Column(Unicode(100))
    lastModifyTime = Column("last_modify_time", DateTime, default = dt.now())
    issuedById = Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy = relation(User, primaryjoin = issuedById == User.user_id)
    lastModifyById = Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy = relation(User, primaryjoin = lastModifyById == User.user_id)

    def __unicode__(self): return self.content

    @classmethod
    def all_upcs(cls):
        return DBSession.query(cls).order_by(cls.id).all()

    @classmethod
    def get(cls, ** args): return DBSession.query(cls).get(int(args.get('id', 0)))

class PEIMaterial(DeclarativeBase):
    __tablename__ = 'pei_material'

    id = Column(Integer, primary_key = True)
    lang = relation(PEILanguage, backref = 'material_lang')
    langId = Column('lang_id', Integer, ForeignKey('pei_language.id'))
    category = relation(PEICategory, backref = 'mat_cat')
    categoryId = Column('cat_id', Integer, ForeignKey('pei_category.id'))
    content = Column(Unicode(50))
    lastModifyTime = Column("last_modify_time", DateTime, default = dt.now())
    issuedById = Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy = relation(User, primaryjoin = issuedById == User.user_id)
    lastModifyById = Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy = relation(User, primaryjoin = lastModifyById == User.user_id)

    def __unicode__(self): return self.content

class PEIInstruction(DeclarativeBase):
    __tablename__ = 'pei_instruction'

    id = Column(Integer, primary_key = True)
    lang = relation(PEILanguage, backref = 'instruction')
    langId = Column('lang_id', Integer, ForeignKey('pei_language.id'))
    category = relation(PEICategory, backref = 'instr_cat')
    categoryId = Column('cat_id', Integer, ForeignKey('pei_category.id'))
    content = Column(Unicode(200))
    lastModifyTime = Column("last_modify_time", DateTime, default = dt.now())
    issuedById = Column("issued_by_id", Integer, ForeignKey('tg_user.user_id'))
    issuedBy = relation(User, primaryjoin = issuedById == User.user_id)
    lastModifyById = Column("last_modify_by_id", Integer, ForeignKey('tg_user.user_id'))
    lastModifyBy = relation(User, primaryjoin = lastModifyById == User.user_id)

    def __unicode__(self): return self.content

class PEIPOHeader(DeclarativeBase):
    __tablename__ = 'pei_po_hdr'

    id = Column(Integer, primary_key = True)
    billToId = Column('bill_to_id', Integer, ForeignKey('pei_bill_to.id'))
    billTo = relation(PEIBillTo, backref = 'billHeaders')
    shipToId = Column('ship_to_id', Integer, ForeignKey('pei_ship_to.id'))
    shipTo = relation(PEIShipTo, backref = 'shipHeaders')
    orderedBy = Column('ordered_by', Unicode(50))
    orderedTel = Column('ordered_tel', Unicode(50))
    shipDate = Column('ship_date', DateTime, default = dt.now())
    shipVia = Column('ship_via', Unicode(500))
    buyerPO = Column('buyer_po', Unicode(50))
    vendorPO = Column('vendor_po', Unicode(50))
    dropShip = Column(Boolean)

    @property
    def totalQty(self):
        qty = 0
        for item in self.details:
            if item.quantity: qty += item.quantity

        return qty

class PEIPODetail(DeclarativeBase):
    __tablename__ = 'pei_po_dtl'

    id = Column(Integer, primary_key = True)
    header = relation(PEIPOHeader, backref = 'details')
    headerId = Column('header_id', Integer, ForeignKey('pei_po_hdr.id'))
    item = relation(PEIItem, backref = 'order')
    itemId = Column('item_id', Integer, ForeignKey('pei_item.id'))
    itemDesc = Column('item_desc', Unicode(100))
    price = Column(Float(precision = 2, scale = 6))
    quantity = Column(Integer)

    @classmethod
    def get(cls, ** args):
        if args.get('id', 0):
            return DBSession.query(cls).get(int(args.get('id', 0)))
        elif args.get('header', 0) and args.get('item', 0):
            return DBSession.query(cls).filter(cls.header == args.get('header', 0)) \
                            .filter(cls.item == args.get('item', 0)).one()

class PEIItemDetail(DeclarativeBase):
    __tablename__ = 'pei_item_dtl'

    id = Column(Integer, primary_key = True)
    poDetail = relation(PEIPODetail, backref = 'po_items')
    poDetailId = Column('po_detail_id', Integer, ForeignKey('pei_po_dtl.id'))
    attr = relation(PEIAttr, backref = 'attribute')
    attrId = Column('attr_id', Integer, ForeignKey('pei_attr.id'))
    attrContent = Column('attr_content', Unicode(50))
    extraContent = Column('extra_content', Unicode(50))
    itemGroup = Column('item_group', Integer)

class PEIItemExtraDetail(DeclarativeBase):
    __tablename__ = 'pei_item_extra_dtl'

    id = Column(Integer, primary_key = True)
    itemDetail = relation(PEIItemDetail, backref = 'itemDetails')
    itemDetailId = Column('item_detail_id', Integer, ForeignKey('pei_item_dtl.id'))
    attrContent = Column('attr_content', Unicode(50))
    extraContent = Column('extra_content', Unicode(50))
    itemGroup = Column('item_group', Integer)
