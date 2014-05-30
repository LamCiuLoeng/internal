# -*- coding: utf-8 -*-
from datetime import datetime as dt

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode

from tribal.model import DeclarativeBase, metadata, DBSession
from tribal.model.auth import *
from tribal.model.sample import SysMixin

__all__=["TAGItem", "TAGHistory"]


class TAGItem(DeclarativeBase):
    __tablename__='tag_item'

    id = Column(Integer, primary_key=True)
    legacyNum = Column('legacy_num', Unicode(30))
    tagNo  = Column('tag_no', Unicode(30))
    tagName = Column('tag_name', Unicode(100))
    poNo = Column('po_no', Unicode(30), nullable=False)
    poUnits = Column('po_units', Integer)
    upc = Column('upc', Unicode(30))
    style = Column('style', Unicode(30))
    color = Column('color', Unicode(30))
    prepack = Column('prepack', Unicode(30))
    label = Column('label', Unicode(30))
    styleDesc = Column('style_desc', Unicode(200))
    colorDesc = Column('color_desc', Unicode(100))
    sizeDesc = Column('size_desc', Unicode(100))
    season = Column('season', Unicode(30))
    merchGroupF = Column('merch_group_f', Unicode(200))
    msrp = Column('msrp', Unicode(20))
    retailPrice = Column('retail_price', Unicode(20))
    attachmentSet = Column('attachment_set', Unicode(200))
    brand = Column('brand', Unicode(100))
    
    ## removed@2011-06-03 #####################
    department = Column('department', Unicode(100))
    classNo = Column('class_no', Unicode(100))
    subClass = Column('sub_class', Unicode(100))
    itemNo = Column('item_no', Unicode(100))
    ##############

    ## new@2011-06-03 #####################
    custSKU = Column('cust_sku', Unicode(200))
    classCat = Column('class_cat', Unicode(200))
    subClassSubCat = Column('subclass_subcat', Unicode(200))
    dept = Column('dept', Unicode(200))
    custSeason = Column('cust_season', Unicode(200))
    pantone = Column('pantone', Unicode(200))
    outletPrice = Column('outlet_price', Unicode(200))
    sizeRangeDesc = Column('size_range_desc', Unicode(200))
    # not used
    merchStyle = Column('merch_style', Unicode(200)) 
    ########################################

    qty = Column('qty', Integer, default=0)
    importDate = Column('import_date', DateTime, default=dt.now)
    ediDate = Column('edi_date', DateTime)
    ediFile = Column('edi_file', Unicode(100))
    #user input
    soNo = Column('so_no', Unicode(100))
    soRemark = Column('so_remark', Unicode(300))
    soDate = Column('so_date', DateTime)
    ##########
    create_time=Column(DateTime, default = dt.now)
    update_time=Column(DateTime, onupdate = dt.now)
    active = Column('active', Integer, default=0) # 0 is active ,1 is inactive
    
    # added@2011-10-17
    latest  = Column("latest", Integer, default=0) # 0 is latest, 1 is old.


class TAGHistory(DeclarativeBase):

    __tablename__ = "tag_history"

    id             =  Column(Integer,autoincrement=True,primary_key=True)
    itemId       =  Column("item_id",Integer, ForeignKey('tag_item.id'))
    item   =  relation(TAGItem, backref="histories")
    actionTime     =  Column("action_time",DateTime, default=dt.now())
    actionUserId   =  Column("action_user",Integer, ForeignKey('tg_user.user_id'))
    actionUser     =  relation(User, primaryjoin = actionUserId == User.user_id)
    actionKind     =  Column("action_Kind",Unicode(100))
    actionContent  =  Column("action_Content",Unicode(3000))


