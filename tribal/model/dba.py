# -*- coding: utf-8 -*-
from datetime import datetime as dt

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode

from tribal.model import DeclarativeBase, metadata, DBSession
from tribal.model.auth import *
from tribal.model.sample import SysMixin

from tribal.util.db_extend import *

__all__=["DBAItemCategory", "DBAItemType", "DBAItem", "DBACustomer", "DBAOrderInfo", "DBAOrderDetail", "DBALog", "DBAProfile"]

customer_item = Table('dba_customer_item', metadata,
                   Column('customer_id', Integer, ForeignKey('dba_customer.id')),
                   Column('item_id', Integer, ForeignKey('dba_item.id'))
                   )

class DBAItemCategory(DeclarativeBase, SysMixin):
    __tablename__="dba_item_category"
    id=Column(Integer, primary_key=True)
    name=Column(Unicode(100), nullable=False)

    def __str__(self):return self.name

    @classmethod
    def find_all(self):
        return DBSession.query(self).all()


class DBAItemType(DeclarativeBase, SysMixin):
    __tablename__="dba_item_type"
    id=Column(Integer, primary_key=True)
    name=Column(Unicode(100), nullable=False)

    def __str__(self):return self.name

    @classmethod
    def find_all(self):
        return DBSession.query(self).all()


class DBAItem(DeclarativeBase, SysMixin):
    __tablename__='dba_item'

    id=Column(Integer, primary_key=True)
    item_code=Column(Unicode(100), nullable=False)
    category_id=Column(Integer, ForeignKey('dba_item_category.id'))
    category=relation(DBAItemCategory, backref="items")
    type_id=Column(Integer, ForeignKey('dba_item_type.id'))
    type=relation(DBAItemType, backref="items")
    image=Column(Unicode(100))
    flatted_size = Column(Unicode(100))

    customers = relation('DBACustomer', secondary = customer_item, backref = 'items')

    def __str__(self):return self.item_code

    @classmethod
    def find_by(cls, ** args):
        eqList = [('category_id', 'category'), ('type_id', 'type')]
        likeList = ['item_code']
        notInList = [('id', 'ids')]
        inList = [('id', 'in_ids')]
        orderList = ['order_by']
        result = DBSession.query(cls)
        queryExtend = QueryExtend(cls, result, ** args)
        queryExtend.query(const.QUERY_TYPE_EQ, eqList)
        queryExtend.query(const.QUERY_TYPE_LIKE, likeList)
        queryExtend.query(const.QUERY_TYPE_NOT_IN, notInList)
        queryExtend.query(const.QUERY_TYPE_IN, inList)
        queryExtend.query(const.QUERY_TYPE_ORDER_BY, orderList)
        return queryExtend.result.all()

    @classmethod
    def get_by_code(cls, item_code):
        return DBSession.query(cls).filter(cls.item_code == item_code).first()



class DBACustomer(DeclarativeBase, SysMixin):
    __tablename__='dba_customer'

    id=Column(Integer, primary_key=True)
    name=Column(Unicode(1000), nullable=False)
    code=Column(Unicode(100))
    bill_to=Column(Unicode(1000))
    ship_to=Column(Unicode(1000))
    contact_person=Column(Unicode(1000))
    email_address=Column(Unicode(1000))

    def __str__(self):return self.name

    @classmethod
    def find_all(self):
        return DBSession.query(self).all()

class DBAOrderInfo(DeclarativeBase, SysMixin):
    __tablename__='dba_order_info'

    id = Column(Integer, primary_key=True)
    po = Column(Unicode(100))
    customer_id = Column(Integer, ForeignKey('dba_customer.id'))
    customer = relation(DBACustomer, backref="orders")
    bill_to = Column(Unicode(1000))
    ship_to = Column(Unicode(1000))
    ship_date = Column(Date)
    
    #add@2011-07-20
    delivery_date = Column(Date)

    # add@20130725
    sob = Column(Unicode(100))

    status = Column(Integer, default=0)

    def __str__(self):return self.po


class DBAOrderDetail(DeclarativeBase, SysMixin):
    __tablename__='dba_order_detail'

    id=Column(Integer, primary_key=True)
    header_id=Column(Integer, ForeignKey('dba_order_info.id'))
    header=relation(DBAOrderInfo, backref="details")
    item_id=Column(Integer, ForeignKey('dba_item.id'))
    item=relation(DBAItem)
    order_month=Column(DateTime, default=dt.now)
    commited_qty=Column(Integer)
    input_commited_qty = Column(Integer)
    forecast_qty=Column(Integer)
    input_forecast_qty=Column(Integer)



class DBALog(DeclarativeBase, SysMixin):
    __tablename__='dba_log'

    id=Column(Integer, primary_key=True)
    action_type=Column(Unicode(100))
    remark=Column(Unicode(2000))
    order_id = Column(Integer, ForeignKey('dba_order_info.id'))
    order = relation(DBAOrderInfo, backref="logs")
    order_detail_id = Column(Integer, ForeignKey('dba_order_detail.id'))
    order_detail = relation(DBAOrderDetail, backref="logs")


class DBAProfile(DeclarativeBase, SysMixin):
    __tablename__='dba_profile'

    id=Column(Integer, primary_key=True)
    name=Column(Unicode(50))
    description=Column(Unicode(1000))
    group_id=Column(Integer, ForeignKey('tg_group.group_id'))
    group=relation(Group, backref='dba_profiles')
    customer_id=Column(Integer, ForeignKey('dba_customer.id'))
    customer=relation(DBACustomer)


    def __str__(self):return self.name


