# -*- coding: utf-8 -*-
from datetime import datetime as dt

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode

from tribal.model import DeclarativeBase, metadata, DBSession
from tribal.model.auth import *

__all__ = ["TMWItem"]


class TMWItem(DeclarativeBase):
    __tablename__ = 'tmw_item'

    id = Column(Integer, primary_key=True)
    tag_format = Column('tag_format', Unicode(200))  # TAG.FORMAT
    qty = Column('qty', Unicode(200))  # QTY
    pofile_id = Column('pofile_id', Unicode(200))  # POFILE.ID catenated with LINE.CODE
    vendor_id = Column('vendor_id', Unicode(200))  # VENDOR.ID
    vendor_name = Column('vendor_name', Unicode(200))  # VENDOR.NAME
    ticket_name = Column('ticket_name', Unicode(200))  # TICKET.NAME
    szn_tag = Column('szn_tag', Unicode(200))  # SZN.TAG
    item_code = Column('item_code', Unicode(200))  # ITEMCODE
    english_size = Column('english_size', Unicode(200))  # ENGLISH.SIZE
    retail_price = Column('retail_price', Unicode(200))  # RETAIL.PRICE
    comp_price = Column('comp_price', Unicode(200))  # COMP.PRICE
    cdf_desc = Column('cdf_desc', Unicode(200))  # CDF.DESC
    lot = Column('lot', Unicode(200))  # LOT
    model = Column('model', Unicode(200))  # MODEL
    country_of_origin = Column('country_of_origin', Unicode(200))  # COUNTRY.OF.ORIGIN
    color_desc = Column('color_desc', Unicode(200))  # COLOR.DESC
    tag_vendor = Column('tag_vendor', Unicode(200))  # TAG.VENDOR
    inseam = Column('inseam', Unicode(200))  # INSEAM

    ###
    filename = Column('filename', Unicode(200))  # TMW002781.dat
    ##########
    create_time = Column(DateTime, default=dt.now)
    update_time = Column(DateTime, onupdate=dt.now)
    active = Column('active', Integer, default=0)  # 0 is active , 1 is inactive
