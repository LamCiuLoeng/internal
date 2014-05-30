# -*- coding: utf-8 -*-
import random
from datetime import datetime as dt

from sqlalchemy import *
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import backref
from sqlalchemy.orm import mapper
from sqlalchemy.orm import relation
from sqlalchemy.orm import relationship
from sqlalchemy.types import Float
from sqlalchemy.types import Integer
from sqlalchemy.types import Unicode
from tribal.model import DBSession
from tribal.model import DeclarativeBase
from tribal.model import metadata
from tribal.model.auth import *
from tribal.model.sysutil import *
from tg import request
from tribal.util.common import sysUpload

__all__ = ['CabelasBoxSize', 'CabelasGender', 'CabelasVendor', 'CabelasVendorInfo', 'CabelasLabel', 'CabelsOrder', 'CabelsBillTo', 'CabelsShipTo']

class CabelasBoxSize(DeclarativeBase, StaticTable):
    __tablename__ = 'cabelas_box_size'

    name = Column(Unicode(20))

class CabelasGender(DeclarativeBase, StaticTable):
    __tablename__ = 'cabelas_gender'

    name = Column(Unicode(20))

class CabelasVendor(DeclarativeBase, DynamicTable):
    __tablename__ = 'cabelas_vendor'

    name = Column(Unicode(50))
    user_id = Column(Integer, ForeignKey('tg_user.user_id'))
    user = relation(User, primaryjoin=user_id == User.user_id)

class CabelasVendorInfo(DeclarativeBase, DynamicTable):
    __tablename__ = 'cabelas_vendor_info'

    type = Column(Unicode(50))
    vendor_id = Column(Integer, ForeignKey('cabelas_vendor.id'))
    vendor = relation(CabelasVendor, primaryjoin='and_(CabelasVendorInfo.vendor_id==CabelasVendor.id, CabelasVendorInfo.active==0)', backref=backref("vendor_infos", order_by='CabelasVendorInfo.create_time'))
    contact = Column(Unicode(100))
    email = Column(Unicode(100))
    phone = Column(Unicode(100))
    fax = Column(Unicode(100))
    address = Column(Unicode(200))
    city = Column(Unicode(100))
    country = Column(Unicode(100))
    

'''
class CabelasVendorUser(DeclarativeBase):
    __tablename__ = 'cabelas_vendor_user'
    
    user_id = Column(Integer, ForeignKey('tg_user.user_id'), primary_key=True)
    vendor_id = Column(Integer, ForeignKey('cabelas_vendor.id'), primary_key=True)
'''

class CabelasLabel(DeclarativeBase, DynamicTable):
    __tablename__ = 'cabelas_label'

    dept = Column(Unicode(20))
    sub_dept = Column(Unicode(20))
    set_no = Column(Unicode(20))
    color = Column(Unicode(20))

    product_desc = Column(Unicode(50))
    bullet_info = Column(Unicode(500))
    box_size_id = Column(Integer, ForeignKey('cabelas_box_size.id'))
    box_size = relation(CabelasBoxSize, primaryjoin=box_size_id == CabelasBoxSize.id)
    gender_id = Column(Integer, ForeignKey('cabelas_gender.id'))
    gender = relation(CabelasGender, primaryjoin=gender_id == CabelasGender.id)

    vendor_ids = Column(Unicode(100))
    logo = Column(Unicode(100))
    status = Column(Integer())
    price = Column(Float())
    currency = Column(Unicode(10))

    proof = Column(Unicode(100))
    first_proof = Column(Unicode(100))
    final_proof = Column(Unicode(100))
    
    @property
    def display_status(self):
        if self.status == 1:
            return 'Package request'
        elif self.status == 2:
            return 'First proof'
        elif self.status == 3:
            return 'Final proof'
        elif self.status == 4:
            return 'Released to printer'
    
    @property
    def vendor(self):
        return CabelasVendor.get(self.vendor_ids)
    
    @property
    def logos(self):
        return self.get_attachments('logo')
    
    @property
    def proofs(self):
        return self.get_attachments('proof')

    @classmethod
    def find_labels(cls, user_id):
        return cls.find_by(status=4)
#        vendor = CabelasVendor.get_by(user_id=user_id)
#        if vendor:
#            return cls.find_by(vendor_ids='%d' % vendor.id)
#            #return cls.find_by(vendors=',%d,' % vendor.id)
#        else:
#            return []

    @classmethod
    def find_labels_by_id(cls,**kw): 
        id = kw.get('id')
        if isinstance(kw.get('id'), unicode):
            id = [id]
        return DBSession.query(cls).filter(cls.id.in_(id)).all()
    
    @classmethod
    def find_labels_by_name(cls, name):
        return DBSession.query(distinct(cls.id)).filter(cls.product_desc.ilike('%%%s%%' % name)).all()
    
    @classmethod
    def create(cls, **kw):
        params = cls.upload_attachments('logo', 'proof', **kw)
        params = cls._resetKw(**params)
        if params.has_key('logo'):
            params['logo'] = '|'.join(map(str, params['logo'].split(',')))
        elif params.has_key('proof'):
            params['proof'] = '|'.join(map(str, params['proof'].split(',')))
        obj = cls(**params)
        DBSession.add(obj)
        return obj

    def update(self, **kw):
        params = cls.upload_attachments('logo', 'proof', **kw)
        params = CabelasLabel._resetKw(**params)
        for k,v in params.iteritems():
            if k=='logo':
                new_logos = params['logo'].split(',') if params['logo'] else []
                new_logos.extend(filter(lambda x: len(x)>0, self.logo.split('|') if self.logo else []))
                self.logo = '|'.join(map(str, new_logos))
            elif k=='proof':
                new_proofs = params['proof'].split(',') if params['proof'] else []
                new_proofs.extend(filter(lambda x: len(x)>0, self.proof.split('|') if self.proof else []))
                self.proof = '|'.join(map(str, new_proofs))
            else:
                if not getattr(self, k) == v:
                    setattr(self, k, v)

class CabelsBillTo(DeclarativeBase, DynamicTable):
    __tablename__ = 'cabelas_bill_to'
    
    name = Column(Unicode(50))
    address = Column(Unicode(200))
    contact = Column(Unicode(100))
    telephone = Column(Unicode(50))
    email     = Column(Unicode(50))

class CabelsShipTo(DeclarativeBase, DynamicTable):
    __tablename__ = 'cabelas_ship_to'
    
    name = Column(Unicode(50))
    address = Column(Unicode(200))
    contact = Column(Unicode(100))
    telephone = Column(Unicode(50))
    email     = Column(Unicode(50))

class CabelsOrder(DeclarativeBase, DynamicTable):
    __tablename__ = 'cabelas_order'

    vendor_id = Column(Integer, ForeignKey('cabelas_vendor.id'))
    vendor = relation(CabelasVendor, primaryjoin=vendor_id == CabelasVendor.id)
    bill_to_id = Column(Integer, ForeignKey('cabelas_vendor_info.id'))
    bill_to = relation(CabelasVendorInfo, primaryjoin=bill_to_id == CabelasVendorInfo.id)
    ship_to_id = Column(Integer, ForeignKey('cabelas_vendor_info.id'))
    ship_to = relation(CabelasVendorInfo, primaryjoin=ship_to_id == CabelasVendorInfo.id)

    number = Column(Unicode(100), default=dt.now().strftime("%Y%m%d%H%M%S")+str(random.randint(0, 10000)))
    qty    = Column(Unicode(200))
    label  = Column(Unicode(200))
    name = Column(Unicode(50))
    address = Column(Unicode(200))
    contact = Column(Unicode(100))
    telephone = Column(Unicode(50))
    email     = Column(Unicode(50))
    fax       = Column(Unicode(50))
    rcm_dcm   = Column(Unicode(200))
    
    def lables(self):
        if self.label:
            return DBSession.query(CabelasLabel).filter(CabelasLabel.id.in_([int(i) for i in self.label.split(',')])).all()
        else:
            return []

    @classmethod
    def find_by(cls, **kw):
        data = DBSession.query(cls).filter(cls.active == 0).order_by(desc(cls.create_time))
        number = kw.get("number")
        name = kw.get("product_desc")
        bill_to_id = kw.get("bill_to_id")
        ship_to_id = kw.get("ship_to_id")
        create_data_start = kw.get("create_time_start")
        create_time_end = kw.get("create_time_end")
        if number:
            data = data.filter(cls.number.ilike('%%%s%%' % number))
        if bill_to_id:
            data = data.filter(cls.bill_to_id == bill_to_id)
        if ship_to_id:
            data = data.filter(cls.ship_to_id == ship_to_id)
        if create_data_start:
            data = data.filter(cls.create_time >= dt.strptime(create_data_start + "00:00:00", "%Y-%m-%d%H:%M:%S"))
        if create_time_end:
            data = data.filter(cls.create_time <= dt.strptime(create_time_end + "00:00:00", "%Y-%m-%d%H:%M:%S"))
        if name:
            rs = []
            labels = CabelasLabel.find_labels_by_name(name)
            labels = [i[0] for i in labels]
            da = data.all()
            for a in da:
                label = a.label
                if label:
                    label_ids = label.split(",")
                    for b in label_ids:
                        if int(b) in labels:
                            rs.append(a)
        else:
            rs = data.all()
        return list(set(rs))
        
        
    @classmethod
    def qtys(cls):
        q = {}
        if cls.qty:
            qtys = cls.qty.split(",")
            for i in qtys:
                id = i.split(":")
                if(len(id) == 1):
                    q.update({int(id[0]):id[1]})
        return q
     