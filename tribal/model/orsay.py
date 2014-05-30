# -*- coding: utf-8 -*-
from datetime import datetime as dt

from sqlalchemy import *
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import backref
from sqlalchemy.orm import mapper
from sqlalchemy.orm import relation
from sqlalchemy.types import Float
from sqlalchemy.types import Integer
from sqlalchemy.types import Unicode
from tribal.model import DBSession
from tribal.model import DeclarativeBase
from tribal.model import metadata
from tribal.model.auth import *

class CommonBasic():
    id = Column(Integer, primary_key=True)
    active = Column(Integer, default=0) # 0 is active ,1 is inactive

    @classmethod
    def get(cls, id):
        return DBSession.query(cls).get(id)

    @classmethod
    def all(cls):
        return DBSession.query(cls).all()

    @classmethod
    def find_by_season(cls, season):
        return DBSession.query(cls).filter(cls.season == season).all()

class CommonLang():
    deutsch = Column(Unicode(300))
    franzosisch = Column(Unicode(300))
    englisch = Column(Unicode(300))
    polnisch = Column(Unicode(300))
    ungarisch = Column(Unicode(300))
    tcheschisch = Column(Unicode(300))
    slowakisch = Column(Unicode(300))
    rumanisch = Column(Unicode(300))
    slowenisch = Column(Unicode(300))
    russisch = Column(Unicode(300))
    chinese = Column(Unicode(300))
    season = Column(Unicode(10))

class OrsayItem(DeclarativeBase, CommonBasic):
    __tablename__ = 'orsay_item'

    item_code = Column(Unicode(100), nullable=False)
    name = Column(Unicode(100), nullable=False)
    currency = Column(Unicode(10), nullable=True)
    price = Column(Float(precision=6), default=0.000000)

class OrsayPart(DeclarativeBase, CommonBasic, CommonLang):
    __tablename__ = 'orsay_part'

    @classmethod
    def findByIds(cls, ids):
        ids = ids.split(',')
        if len(ids) == 0:
            ids = [0]
        return [DBSession.query(cls).filter(cls.id == id).one() if id and int(id) > 0 else None for id in ids]

class OrsayMaterial(DeclarativeBase, CommonBasic, CommonLang):
    __tablename__ = 'orsay_material'
    
    kurzel = Column(Unicode(300))

    @classmethod
    def find_by_season(cls, season):
        list = DBSession.query(cls).filter(cls.season == season).order_by(asc(cls.kurzel), cls.id)
        tmpList1 = []
        preObj = null
        for i in list:
            i.begin = 0
            i.end = 0
            if preObj is null:
                i.begin = 1;
                preObj = i;
            if preObj.kurzel != i.kurzel:
                preObj.end = 1;
                i.begin = 1;
            tmpList1.append(i)
            preObj = i;
        return tmpList1

    @classmethod
    def findByIds(cls, ids):
        id_list = ids.split(',')
        results = []
        for id in id_list:
            results.append(DBSession.query(cls).get(id))
        return results

class OrsayWashing(DeclarativeBase, CommonBasic, CommonLang):
    __tablename__ = 'orsay_washing'
    
    type = Column(Unicode(20))
    flag = Column(Unicode(50)) 
    addition = Column(Unicode(100))

class OrsayAppendix(DeclarativeBase, CommonBasic, CommonLang):
    __tablename__ = 'orsay_appendix'

    sub_cat = Column(Unicode(20))

    @classmethod
    def find_by_season(cls, season):
        list = DBSession.query(cls).filter(cls.season == season).order_by(desc(cls.sub_cat), cls.id)
        tmpList1 = []
        tmpList2 = []
        preObj = null
        for i in list:
            i.begin = 0
            i.end = 0
            if i.sub_cat and len(i.sub_cat) > 0:
                if preObj is null:
                    i.begin = 1;
                    preObj = i;
                if preObj.sub_cat != i.sub_cat:
                    preObj.end = 1;
                    i.begin = 1;
                tmpList2.append(i)
                preObj = i;
            else:
                tmpList1.append(i)
        tmpList1.extend(tmpList2)
        return tmpList1

    @classmethod
    def findByIds(cls, ids):
        if ids == '':
            return []
        return DBSession.query(cls).filter('id in (%s)' % ids)

class OrsaySize(DeclarativeBase, CommonBasic):
    __tablename__ = "orsay_size"

    season = Column(Unicode(10))
    
    name = Column("name", Unicode(50))
    name_euro = Column("name_euro", Unicode(50))
    name_slo = Column("name_slo", Unicode(50))

class OrsayArticleDesc(DeclarativeBase, CommonBasic, CommonLang):
    __tablename__ = "orsay_article_desc"

class OrsayOrignCollection(DeclarativeBase, CommonBasic):
    __tablename__ = "orsay_orign_collection"

    name = Column("name", Unicode(50))

class OrsayOrder(DeclarativeBase, CommonBasic):
    __tablename__ = 'orsay_order'

    season = Column(Unicode(10))
    status = Column(Unicode(20))
    #Will add the vendor detail info later
    company_code = Column(Unicode(30))
    cust_name = Column(Unicode(200))
    cust_code = Column(Unicode(30))
    #billto_company_name = Column(Unicode(200))
    billto_address = Column(Unicode(600))
    billto_contact_sales = Column(Unicode(100))
    billto_tel_no = Column(Unicode(200))
    #shipto_company_name = Column(Unicode(200))
    shipto_address = Column(Unicode(800))
    shipto_contact_person = Column(Unicode(200))
    shipto_tel_no = Column(Unicode(200))
    
    customer_po = Column(Unicode(100), nullable=False)
    order_type = Column(Unicode(10), nullable=False)
    item_id = Column(Integer, ForeignKey('orsay_item.id'))
    item = relation(OrsayItem)
    qty = Column(Integer, default=0)
    price = 0.2
    #amount = Column(Unicode(50))
    email_subject = Column(Unicode(1000), nullable=True)
    comment = Column(Unicode(2000), nullable=True)
    
    create_time = Column(DateTime, default=dt.now)
    create_by_id = Column(Integer, ForeignKey('tg_user.user_id'))
    create_by = relation(User, primaryjoin=create_by_id == User.user_id)

class OrsayOrderDetail1(DeclarativeBase):
    __tablename__ = 'orsay_order_detail_1'

    id = Column(Integer, primary_key=True)
    head_id = Column(Integer, ForeignKey('orsay_order.id'))
    head = relation(OrsayOrder, backref='item1_details')

    size_id = Column(Integer, ForeignKey("orsay_size.id"))
    size = relation(OrsaySize, backref='item1_size')
    article_desc_id = Column(Integer, ForeignKey("orsay_article_desc.id"))
    article_desc = relation(OrsayArticleDesc, backref='item1_article_desc')
    reference_no = Column(Unicode(20))
    reference_color_no = Column(Unicode(20))
    order_no = Column(Unicode(20))
    orign_collection_id = Column(Integer, ForeignKey("orsay_orign_collection.id"))
    orign_collection = relation(OrsayOrignCollection, backref='item1_orign_collection')
    orign_location = Column(Unicode(100))
    trademark = Column(Unicode(100))
    part_ids = Column(Unicode(1000))#use mark to split multiple parts
    material_ids = Column(Unicode(1000))#use mark to split multiple meterialId
    #use mark to split multiple percent, the result of add all percent is 100
    material_percents = Column(Unicode(1000))
    appendix_ids = Column(Unicode(1000))#use mark to split multiple particularIndication

class OrsayOrderDetail2(DeclarativeBase):
    __tablename__ = 'orsay_order_detail_2'

    id = Column(Integer, primary_key=True)
    head_id = Column(Integer, ForeignKey('orsay_order.id'))
    head = relation(OrsayOrder, backref='item2_details')
    
    washing_id = Column(Integer, ForeignKey('orsay_washing.id'))
    washing = relation(OrsayWashing, primaryjoin=washing_id == OrsayWashing.id, lazy=False)
    bleeding_id = Column(Integer, ForeignKey('orsay_washing.id'))
    bleeding = relation(OrsayWashing, primaryjoin=bleeding_id == OrsayWashing.id, lazy=False)
    various_id = Column(Integer, ForeignKey('orsay_washing.id'))
    various = relation(OrsayWashing, primaryjoin=various_id == OrsayWashing.id, lazy=False)
    ironing_id = Column(Integer, ForeignKey('orsay_washing.id'))
    ironing = relation(OrsayWashing, primaryjoin=ironing_id == OrsayWashing.id, lazy=False)
    accessories_id = Column(Integer, ForeignKey('orsay_washing.id'))
    accessories = relation(OrsayWashing, primaryjoin=accessories_id == OrsayWashing.id, lazy=False)

class OrsayOrderDetail3(DeclarativeBase):
    __tablename__ = 'orsay_order_detail_3'
    
    id = Column(Integer, primary_key=True)
    head_id = Column(Integer, ForeignKey('orsay_order.id'))
    head = relation(OrsayOrder, backref='item3_details')

    size_id = Column(Integer, ForeignKey("orsay_size.id"))
    size = relation(OrsaySize, backref='item3_size')
    article_desc_id = Column(Integer, ForeignKey("orsay_article_desc.id"))
    article_desc = relation(OrsayArticleDesc, backref='item3_article_desc')
    reference_no = Column(Unicode(20))
    reference_color_no = Column(Unicode(20))
    order_no = Column(Unicode(20))
    orign_collection_id = Column(Integer, ForeignKey("orsay_orign_collection.id"))
    orign_collection = relation(OrsayOrignCollection, backref='item3_orign_collection')
    orign_location = Column(Unicode(100))
    trademark = Column(Unicode(100))
    part_ids = Column(Unicode(1000))#use mark to split multiple parts
    material_ids = Column(Unicode(1000))#use mark to split multiple meterialId
    #use mark to split multiple percent, the result of add all percent is 100
    material_percents = Column(Unicode(1000))
    appendix_ids = Column(Unicode(1000))#use mark to split multiple particularIndication
