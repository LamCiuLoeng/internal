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
from tribal.model.sysutil import *
from tg import request

__all__ = ['OrchestraItem', 'OrchestraCustomer', 'OrchestraFabric', 'OrchestraComposition', 'OrchestraCare', 'OrchestraCareImg', 'OrchestraProductFamily', 'OrchestraOrigin', 'OrchestraOrder']

class OrchestraItem(DeclarativeBase, StaticTable):
    __tablename__ = 'orchestra_item'

    name = Column(Unicode(50))
    info1 =  Column(Unicode(50))
    team = Column(Unicode(20))

class OrchestraCustomer(DeclarativeBase, StaticTable):
    __tablename__ = 'orchestra_customer'

    name = Column(Unicode(200))
    contact = Column(Unicode(200))
    email = Column(Unicode(200))
    team = Column(Unicode(20))

class OrchestraFabric(DeclarativeBase, StaticTable):
    __tablename__ = 'orchestra_fabric'

    #the order is french english spanish portugese german chinese arabic russian
    french = Column(Unicode(50))
    english = Column(Unicode(50))
    spanish = Column(Unicode(50))
    portugese = Column(Unicode(50))
    german = Column(Unicode(50))
    chinese = Column(Unicode(50))
    arabic = Column(Unicode(50))
    russian = Column(Unicode(50))
    team = Column(Unicode(20))

class OrchestraComposition(DeclarativeBase, StaticTable):
    __tablename__ = 'orchestra_composition'

    #the order is french english spanish portugese german chinese arabic russian
    french = Column(Unicode(50))
    english = Column(Unicode(50))
    spanish = Column(Unicode(50))
    portugese = Column(Unicode(50))
    german = Column(Unicode(50))
    chinese = Column(Unicode(50))
    arabic = Column(Unicode(50))
    russian = Column(Unicode(50))
    team = Column(Unicode(20))

class OrchestraCare(DeclarativeBase, StaticTable):
    __tablename__ = 'orchestra_care'

    #the order is french english spanish portugese german chinese arabic russian
    french = Column(Unicode(200))
    english = Column(Unicode(200))
    spanish = Column(Unicode(200))
    portugese = Column(Unicode(200))
    german = Column(Unicode(200))
    chinese = Column(Unicode(200))
    arabic = Column(Unicode(200))
    russian = Column(Unicode(200))
    team = Column(Unicode(20))

class OrchestraCareImg(DeclarativeBase, StaticTable):
    __tablename__ = 'orchestra_care_img'
    
    name = Column(Unicode(200))
    path = Column(Unicode(200))
    type = Column(Unicode(50))
    rank = Column(Integer())
    team = Column(Unicode(20))

class OrchestraProductFamily(DeclarativeBase, StaticTable):
    __tablename__ = 'orchestra_product_family'

    french = Column(Unicode(50))
    english = Column(Unicode(50))
    arabic = Column(Unicode(50))
    type = Column(Unicode(50))
    code = Column(Unicode(50))
    team = Column(Unicode(20))

class OrchestraOrigin(DeclarativeBase, StaticTable):
    __tablename__ = 'orchestra_origin'

    #not show the french， the order is english spanish arabic
    name = Column(Unicode(50))
    french = Column(Unicode(50))
    english = Column(Unicode(50))
    spanish = Column(Unicode(50))
    arabic = Column(Unicode(50))
    chinese = Column(Unicode(50))
    rank = Column(Integer())
    team = Column(Unicode(20))

class OrchestraOrder(DeclarativeBase, DynamicTable):
    __tablename__ = 'orchestra_order'

    billto_customer_id = Column(Integer, ForeignKey('orchestra_customer.id'))
    billto_customer = relation(OrchestraCustomer, primaryjoin=billto_customer_id == OrchestraCustomer.id)
    billto_name = Column(Unicode(100))
    billto_address = Column(Unicode(600))
    billto_contact = Column(Unicode(100))
    billto_telephone = Column(Unicode(100))
    billto_email = Column(Unicode(100))

    shipto_customer_id = Column(Integer, ForeignKey('orchestra_customer.id'))
    shipto_customer = relation(OrchestraCustomer, primaryjoin=shipto_customer_id == OrchestraCustomer.id)
    shipto_name = Column(Unicode(100))
    shipto_address = Column(Unicode(800))
    shipto_contact = Column(Unicode(100))
    shipto_telephone = Column(Unicode(100))
    shipto_email = Column(Unicode(100))

    customer_po = Column(Unicode(100))
    order_type = Column(Unicode(10))
    email_subject = Column(Unicode(1000))
    comment = Column(Unicode(2000))
    attachment = Column(Unicode(100))
    send_mail = Column(Boolean(), default=False)
    team = Column(Unicode(20))

    item_id = Column(Integer, ForeignKey('orchestra_item.id'))
    item = relation(OrchestraItem)
    item_info1 = Column(Unicode(50))

    qty = Column(Integer, default=0)
    sku = Column(Unicode(20))
    height = Column(Unicode(50))
    head_size = Column(Unicode(50))
    specification = Column(Unicode(50))

    product_family_langs = Column(Unicode(200))
    product_family_id = Column(Integer, ForeignKey('orchestra_product_family.id'))
    product_family = relation(OrchestraProductFamily)
    product_family_txt = Column(Unicode(500))

    origin_id = Column(Integer, ForeignKey('orchestra_origin.id'))
    origin = relation(OrchestraOrigin)
    origin_txt = Column(Unicode(500))

    ca_no = Column(Unicode(20))

    fabric_ids = Column(Unicode(200))
    fabric_txt = Column(Unicode(500))
    composition_percents = Column(Unicode(200))
    composition_ids = Column(Unicode(200))
    composition_txt = Column(Unicode(500))
    care_img_ids = Column(Unicode(200))
    care_ids = Column(Unicode(200))
    care_txt = Column(Unicode(1000))

    @property
    def fabrics(self):
        return OrchestraFabric.find_by_ids(self.fabric_ids)

    @property
    def compositions(self):
        return [OrchestraComposition.find_by_ids(i) for i in self.composition_ids.split('|')]
    
    @property
    def percents(self):
        return [i.split(',') for i in self.composition_percents.split('|')]
    
    @property
    def cares(self):
        return OrchestraCare.find_by_ids(self.care_ids)

    @property
    def care_imgs(self):
        return OrchestraCareImg.find_by_ids(self.care_img_ids, order_func='rank asc')
#
#    @property
#    def product_family(self):
#        return DBSession.query(OrchestraProductFamily).get(self.product_family_id)

class OrchestraOrderHeader(DeclarativeBase, DynamicTable):
    __tablename__ = 'orchestra_order_header'
    
    billto_customer_id = Column(Integer, ForeignKey('orchestra_customer.id'))
    billto_customer = relation(OrchestraCustomer, primaryjoin=billto_customer_id == OrchestraCustomer.id)
    billto_name = Column(Unicode(100))
    billto_address = Column(Unicode(600))
    billto_contact = Column(Unicode(100))
    billto_telephone = Column(Unicode(100))
    billto_email = Column(Unicode(100))

    shipto_customer_id = Column(Integer, ForeignKey('orchestra_customer.id'))
    shipto_customer = relation(OrchestraCustomer, primaryjoin=shipto_customer_id == OrchestraCustomer.id)
    shipto_name = Column(Unicode(100))
    shipto_address = Column(Unicode(800))
    shipto_contact = Column(Unicode(100))
    shipto_telephone = Column(Unicode(100))
    shipto_email = Column(Unicode(100))

    customer_po = Column(Unicode(100))
    order_type = Column(Unicode(10))
    email_subject = Column(Unicode(1000))
    comment = Column(Unicode(2000))
    attachment = Column(Unicode(100))

    send_mail = Column(Boolean(), default=False)
    team = Column(Unicode(20))

class OrchestraOrderDetail(DeclarativeBase, DynamicTable):
    __tablename__ = 'orchestra_order_detail'

    head_id = Column(Integer, ForeignKey('orchestra_order_header.id'))
    head = relation(OrchestraOrderHeader, backref='order_details')

    item_id = Column(Integer, ForeignKey('orchestra_item.id'))
    item = relation(OrchestraItem)
    item_info1 = Column(Unicode(50))

    qty = Column(Integer, default=0)
    sku = Column(Unicode(20))
    height = Column(Unicode(50))
    head_size = Column(Unicode(50))
    specification = Column(Unicode(50))

    product_family_langs = Column(Unicode(200))
    product_family_id = Column(Integer, ForeignKey('orchestra_product_family.id'))
    product_family = relation(OrchestraProductFamily)
    product_family_txt = Column(Unicode(500))

    origin_id = Column(Integer, ForeignKey('orchestra_origin.id'))
    origin = relation(OrchestraOrigin)
    origin_txt = Column(Unicode(500))

    ca_no = Column(Unicode(20))

    fabric_ids = Column(Unicode(200))
    fabric_txt = Column(Unicode(500))
    composition_percents = Column(Unicode(200))
    composition_ids = Column(Unicode(200))
    composition_txt = Column(Unicode(500))
    care_img_ids = Column(Unicode(200))
    care_ids = Column(Unicode(200))
    care_txt = Column(Unicode(1000))

    @property
    def fabrics(self):
        return OrchestraFabric.find_by_ids(self.fabric_ids)

    @property
    def compositions(self):
        return [OrchestraComposition.find_by_ids(i) for i in self.composition_ids.split('|')]

    @property
    def percents(self):
        return [i.split(',') for i in self.composition_percents.split('|')]
    
    @property
    def cares(self):
        return OrchestraCare.find_by_ids(self.care_ids)

    @property
    def care_imgs(self):
        return OrchestraCareImg.find_by_ids(self.care_img_ids, order_func='rank asc')

    @property
    def product_family(self):
        return DBSession.query(OrchestraProductFamily).get(self.product_family_id)
