# -*- coding: utf-8 -*-
import os, re
from datetime import datetime as dt

from tg import request, config
from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, synonym, backref
from sqlalchemy.types import Integer, Unicode

from tribal.model import DeclarativeBase, metadata, DBSession
from tribal.model.auth import *
from tribal.util.file_util import *


__all__ =['getUserID','extract_inline_list',"History", "UploadObject", 'StaticTable', 'DynamicTable']

def extract_inline_list(*keys, ** kw):
    ignore_keys = []
    item_dict = {}
    item_set_dict = {}
    for k, v in kw.iteritems():
        for prefix in keys:
            if k.startswith('%s-' % prefix):
                ignore_keys.append(k)
                if not (k.find('__') >= 0 or k.find('FORMS') >= 0):
                    ks = k.split('-')
                    if len(ks) == 2:
                        name = ks[1]
                        if not item_dict.has_key(prefix):
                            item_dict[prefix] = {}
                        item_dict[prefix][name] = v
                    elif len(ks) == 3:
                        index = ks[1]
                        name = ks[2]
                        if not item_set_dict.has_key(prefix):
                            item_set_dict[prefix] = {}
                        if not item_set_dict[prefix].has_key(index):
                            item_set_dict[prefix][index] = {}
                        item_set_dict[prefix][index][name] = v
    for i in ignore_keys:
        del kw[i]
    for k, v in item_dict.iteritems():
        kw[k] = v
    for k, v in item_set_dict.iteritems():
        kw[k] = []
        for i in list(set(map(int, v.keys()))):
            kw[k].append(v[str(i)])
    return kw

def getUserID():
    return request.identity["user"].user_id

class History(DeclarativeBase):
    __tablename__ = 'sysutil_history'
    
    id = Column(Integer, primary_key=True)
    action_user_id =  Column(Integer, ForeignKey('tg_user.user_id'))
    action_user = relation(User)
    action_type = Column(Unicode(20))
    action_content = Column(Unicode(1000))
    create_time = Column(DateTime, default=dt.now)

class UploadObject(DeclarativeBase):
    __tablename__ = 'sysutil_upload'
    
    id = Column(Integer, primary_key=True)
    file_name = Column(Unicode(255))
    _file_path = Column("file_path", Unicode(1000), nullable=False)
    upload_by_id = Column(Integer, default=getUserID)
    create_time = Column(DateTime, default=dt.now)
    
    @property
    def upload_by(self):
        return DBSession.query(User).get(self.upload_by_id)

    @classmethod
    def find_by_ids(cls, ids):
        return DBSession.query(cls).filter(cls.id.in_(ids)).all()

    def _get_file_path(self):
        return os.path.join(config.get("download_dir"),self._file_path)
    
    def _set_file_path(self,value):
        self._file_path = value
    
    file_path = synonym('_file_path', descriptor=property(_get_file_path,_set_file_path))

class StaticTable():
    id = Column(Integer, primary_key=True)

    @classmethod
    def get(cls, id):
        return DBSession.query(cls).get(id)

    @classmethod
    def all(cls, order_func='id asc'):
        return DBSession.query(cls).order_by(order_func).all()

    @classmethod
    def find_by(cls, all=True, order_func='id asc', **kw):
        keytypeMap = {}
        for i in cls.__table__.columns:
            keytypeMap.update({i.key: type(i.type)})
        qyModel = DBSession.query(cls)
        for k,v in kw.iteritems():
            if k in keytypeMap.keys():
                    if keytypeMap[k] == Integer:
                        if v:
                            qyModel = qyModel.filter(getattr(cls, k)==int(v))
                    else:
                        qyModel = qyModel.filter(getattr(cls, k).ilike('%%%s%%' % v))
        qyModel = qyModel.order_by(order_func)
        return qyModel.all() if all else qyModel

    @classmethod
    def get_by(cls, **kw):
        return cls.find_by(all=False, **kw).first()

    @classmethod
    def find_by_ids(cls, ids, separator=',', order_func='id asc'):
        if type(ids) == str or type(ids) == unicode:
            results = []
            id_list = filter(lambda x: x, ids.split(separator))
            result_dict = {}
            for result in DBSession.query(cls).filter(cls.id.in_(id_list)).order_by(order_func).all():
                result_dict[result.id] = result
            for id in ids.split(separator):
                results.append(result_dict[int(id)] if id else None)
            return results
        elif type(ids) == list or type(ids) == tuple:
            return DBSession.query(cls).filter(cls.id.in_(ids)).order_by(order_func).all()

class DynamicTable(StaticTable):
    create_time = Column(DateTime, default=dt.now)
    create_by_id = Column(Integer, default=getUserID)
    update_time = Column(DateTime, default=dt.now, onupdate=dt.now)
    update_by_id = Column(Integer, default=getUserID, onupdate=getUserID)
    active = Column(Integer, default=0) # 0 is active ,1 is inactive
    
    @property
    def create_by(self):
        return DBSession.query(User).get(self.create_by_id)
    
    @property
    def update_by(self):
        return DBSession.query(User).get(self.update_by_id)

    @classmethod
    def find_by(cls, order_func='create_time desc', active=0, **kw):
        keytypeMap = {}
        for i in cls.__table__.columns:
            keytypeMap.update({i.key: type(i.type)})
        qyModel = DBSession.query(cls)
        for k,v in kw.iteritems():
            if k in keytypeMap.keys():
                    if keytypeMap[k] == Integer:
                        if v:
                            qyModel = qyModel.filter(getattr(cls, k)==int(v))
                    else:
                        qyModel = qyModel.filter(getattr(cls, k).ilike('%%%s%%' % v))
        qyModel = qyModel.filter(getattr(cls, 'active')==active)
        qyModel = qyModel.order_by(order_func)
        return qyModel.all() if all else qyModel

    @classmethod
    def all(cls, order_func='create_time desc', active=0):
        return DBSession.query(cls).order_by(order_func).filter(cls.active==active).all()

    def enable(self):
        self.active = 0
        
    def disable(self):
        self.active = 1

    @classmethod
    def create(cls, **kw):
        obj = cls(**cls._resetKw(**kw))
        DBSession.add(obj)
        return obj

    def update(self, **kw):
        new_params = self.__class__._resetKw(**kw)
        old_params = self.__dict__
        for k,v in new_params.iteritems():
            if not old_params.get(k, None) == v:
                setattr(self, k, v)

    def get_attachments(self, key='attachment', wrapper=True):
        try:
            if not wrapper: return [id for id in getattr(self, key).split("|") if id]
            m = lambda id: DBSession.query(UploadObject).get(id)
            return map(m, [id for id in getattr(self, key).split("|") if id])
        except:
            return []
        
    @classmethod
    def upload_attachments(cls, *keys, **kw):
        from tribal.util.common import sysUpload
        if not keys:
            keys = ('attachment')
        for key in keys:
            if kw.has_key(key):
                (flag, ids) = sysUpload(kw[key])
                print '#' * 40, 'upload file: flag: %s, ids: %s' % (flag, ids)
                if flag != 0: 
                    raise "Error when upload the file(s)"
                else:
                    kw[key] = ids
        return kw

    def add_attachments(self, attachments=[], key='attachment'):
        ids = []
        for att in attachments:
            upObj = UploadObject(**{'_file_path':att, 'file_name': att.split('\\')[-1].split('/')[-1]})
            DBSession.add(upObj)
            DBSession.flush()
            ids.append(upObj.id)
        setattr(self, key, '|'.join(map(str, ids)))

    def download_attachment(self, key='attachment', wrapper=True):
        attachments = []
        zname = None
        for i in self.get_attachments(key, wrapper):
            attachments.append([i.file_path, i.file_name])
            if not zname:
                zname = i.file_name.split('.')[0]
        zfolder = os.path.join(config.download_dir, 'temp')
        if not os.path.exists(zfolder):
            os.makedirs(zfolder)
        zfile = os.path.join(zfolder, '%s.zip' % zname)
        create_zip(zfile, attachments)
        return zfile

    @classmethod
    def download_attachments(cls, ids, key='attachment', wrapper=True):
        orders = cls.find_by_ids(ids)
        attachments = []
        for i in orders:
            for j in i.get_attachments(key, wrapper):
                attachments.append([j.file_path, j.file_name])
        zfolder = os.path.join(config.download_dir, 'temp')
        if not os.path.exists(zfolder):
            os.makedirs(zfolder)
        zfile = os.path.join(zfolder, 'ORC_labels-%s.zip' % dt.now().strftime("%Y%m%d%H%M%S"))
        create_zip(zfile, attachments)
        return zfile   

    @classmethod
    def _resetKw(cls, **kw):
        keytypeMap = {}
        for i in cls.__table__.columns:
            keytypeMap.update({i.key: type(i.type)})
        params = {}
        for k,v in kw.iteritems():
            if not k.startswith('_') and k in keytypeMap.keys():
                if type(v) == list or type(v) == tuple:
                    params[k] = ','.join(map(str, v))
                elif k.endswith('_id'):
                    params[k] = int(v) if v else None
                else:
                    params[k] = v
        return params
