#coding=utf-8
import os
import logging
import random
import shutil
import transaction
from tribal.lib.base import BaseController
from repoze.what import authorize
from tg import request
from tg import expose
from tg import flash
from tg import redirect
from tg import config
from tg.decorators import paginate
from tribal.model import *
from tribal.util.common import *
from tribal.util.excel_helper import *
from tribal.widgets.cabelas import *
from sqlalchemy import asc, desc

__all__ = ['CabelasController']

log = logging.getLogger(__name__)

STATUS_LABEL_NEW = 1
STATUS_LABEL_FIRST_PROOF = 2
STATUS_LABEL_FINAL_PROOF = 3
STATUS_LABEL_RELEASED = 4

TYPE_VENDOR_SHIPTO = 1
TYPE_VENDOR_BILLTO = 2

class CabelasDevelopmentController(BaseController):

    allow_only = authorize.not_anonymous()

    @expose('tribal.templates.cabelas.development')
    @paginate("result", items_per_page = 20)
    @tabFocus(tab_type="main")
    def index(self, ** kw):
        return dict(developmentSearchForm=developmentSearchForm, kw=kw, result=CabelasLabel.find_by(order_func=desc(CabelasLabel.create_time), **kw))

    @expose('tribal.templates.cabelas.proof_new')
    @tabFocus(tab_type="main")
    def new(self, ** kw):
        return dict(vendors=CabelasVendor.all(), genders=CabelasGender.all(), box_sizes=CabelasBoxSize.all())

    @expose('tribal.templates.cabelas.proof_edit')
    @tabFocus(tab_type="main")
    def edit(self, ** kw):
        label = CabelasLabel.get(kw['id'])
        return dict(vendors=CabelasVendor.all(), genders=CabelasGender.all(), box_sizes=CabelasBoxSize.all(), 
                    label=label, label_logos=label.get_attachments('logo'), label_proofs=label.get_attachments('proof'))

    @expose()
    def save(self, ** kw):
        try:
            if kw.has_key('_create'):
                label = CabelasLabel.create(**kw)
                label.status = STATUS_LABEL_NEW
                flash("The package request created successful!")
            elif kw.has_key('id'):
                label = CabelasLabel.get(kw['id'])
                label.logo = '|'.join(kw['logo_id'] if type(kw['logo_id'])==list else [kw['logo_id']]) if kw.has_key('logo_id') else None
                label.proof = '|'.join(kw['proof_id'] if type(kw['proof_id'])==list else [kw['proof_id']]) if kw.has_key('proof_id') else None
                if kw.has_key('_approve_first'):
                    label.status = STATUS_LABEL_FIRST_PROOF
                elif kw.has_key('_approve_final'):
                    label.status = STATUS_LABEL_FINAL_PROOF
                elif kw.has_key('_release'):
                    label.status = STATUS_LABEL_RELEASED
                label.update(**kw)
                flash("The label design updated successful!")
        except Exception, e:
            log.exception(str(e))
            flash("Error occor on the server side!", 'warn')
            transaction.doom()
        finally:
            redirect('/cabelas/development')

    @expose('tribal.templates.cabelas.vendor_list')
    @tabFocus(tab_type="main")
    def list_vendor(self):
        return dict(result=CabelasVendor.all())

    @expose('tribal.templates.cabelas.vendor_new')
    @tabFocus(tab_type="main")
    def new_vendor(self):
        return {}

    @expose('tribal.templates.cabelas.vendor_edit')
    @tabFocus(tab_type="main")
    def edit_vendor(self, **kw):
        vendor = CabelasVendor.get(kw['id'])
        vendor_infos = vendor.vendor_infos
        shipto_infos, billto_infos = [],[]
        for i in vendor_infos:
            if i.type=='billto':
                billto_infos.append(i)
            elif i.type=='shipto':
                shipto_infos.append(i)
        return {'vendor': vendor, 'billto_infos': billto_infos, 'shipto_infos': shipto_infos}

    @expose('')
    def save_vendor(self, **kw):
        try:
            kw = extract_inline_list('vendor_obj','shipto_set','user_set','billto_set',** kw)
            if kw.has_key('_create'):
                vendor = CabelasVendor.create(**kw['vendor_obj'])
                DBSession.flush()
                for type in ['shipto', 'billto']:
                    type_set = '%s_set' % type
                    if kw.has_key(type_set):
                        for i in kw[type_set]:
                            vendor_info = CabelasVendorInfo.create(vendor_id=vendor.id, type=type, **i)
            else:
                vendor = CabelasVendor.get(kw['vendor_obj']['id'])
                vendor_info_map = {}
                for i in vendor.vendor_infos:
                    vendor_info_map.update({str(i.id):i})
                vendor.update(**kw['vendor_obj'])
                for type in ['shipto', 'billto']:
                    type_set = '%s_set' % type
                    if kw.has_key(type_set):
                        for i in kw[type_set]:
                            if i.has_key('id'):
                                vendor_info = CabelasVendorInfo.get(i['id'])
                                vendor_info.update(**i)
                                del vendor_info_map[str(vendor_info.id)]
                            else:
                                vendor_info = CabelasVendorInfo.create(vendor_id=vendor.id, type=type, **i)
                for k,v in vendor_info_map.iteritems():
                    v.disable()
            flash("The vendor saved successful!")
        except Exception, e:
            flash("Error occor on the server side!", 'warn')
            log.exception(str(e))
            transaction.doom()
        finally:
            redirect('/cabelas/development/list_vendor')


class CabelasOrderingController(BaseController):
    
    allow_only = authorize.not_anonymous()
    
    @expose('tribal.templates.cabelas.order_index')
    @paginate('collections', items_per_page = 20)
    @tabFocus(tab_type="main")
    def index(self, ** kw):
        order = CabelsOrder.find_by(**kw)
        return dict(
                    kw = kw,
                    collections = order,
                    OrderingSearchForm=OrderingSearchForm
                    )

    @expose('tribal.templates.cabelas.order_view')
    @tabFocus(tab_type="main")
    def view(self, ** kw):
        order = DBSession.query(CabelsOrder).get(kw.get("id"))
        qty_dict = {}
        if order.qty:
            for i in order.qty.split(","):
                p = i.split(":")
                qty_dict.update({int(p[0]):p[1]})
        return dict(
                    kw = kw,
                    order = order,
                    qty_dict = qty_dict,
                    collections = order.lables(),
                    OrderingSearchForm=OrderingSearchForm
                    )


    @expose('tribal.templates.cabelas.order_new')
    @paginate('collections', items_per_page = 20)
    @tabFocus(tab_type="main")
    def new(self):
        labels = CabelasLabel.find_labels(request.identity["user"].user_id)
        return dict(collections = labels)
    
    @expose('tribal.templates.cabelas.order_ordering')
    @tabFocus(tab_type="main")
    def order(self, **kw):
        shipto, billto = None, None
        labels = CabelasLabel.find_labels_by_id(**kw)
        print "*"*30, request.identity["user"].user_id
        vendor = DBSession.query(CabelasVendor).filter(CabelasVendor.user_id == request.identity["user"].user_id).first()
        vendor_info = []
        print vendor
        if vendor:
            vendor_info = DBSession.query(CabelasVendorInfo).filter(CabelasVendorInfo.vendor_id == vendor.id).filter(CabelasVendorInfo.active == 0).all()
        for i in vendor_info:
            if i.type == "shipto":
                shipto = i.id
            elif i.type == "billto":
                billto = i.id
        return dict(
                    collections = labels,
                    vendor = vendor,
                    shipto = shipto,
                    billto = billto,
                    orderingConfirmForm = orderingConfirmForm
                    )
    
    @expose()
    def confirm(self, **kw):
        qty = {}
        try:
            if kw.get("submit") == "Submit":
                id = kw.get("id")
                name = kw.get("name")
                contact = kw.get("contact")
                vendor_id = kw.get("vendor_id")
                if not vendor_id:
                    raise
                if not isinstance(id, list):
                    id = [id]
                for i in id:
                    qty.update({i:kw.get("qty_%s" % i)})
                keys = {
                        "vendor_id":kw.get("vendor_id"),
                        "bill_to_id":kw.get("bill_to_id"),
                        "ship_to_id":kw.get("ship_to_id"),
                        'qty':",".join(["%s:%s" %(k,v ) for k,v in qty.iteritems()]),
                        'label':",".join(id),
                        'name':name,
                        'contact':contact,
                        'fax':kw.get("fax"),
                        'rcm_dcm':kw.get("rcm_dcm"),
                        'address':kw.get("address"),
                        'telephone':kw.get("telephone")
                        }
                order = CabelsOrder(** keys)
                DBSession.add(order)
                DBSession.flush()
            flash("successful!")
        except Exception, e:
            log.exception(str(e))
            flash("Error occor on the server side!", 'warn')
        finally:
            redirect('/cabelas/ordering')
            

class CabelasController(BaseController):
    
    allow_only = authorize.not_anonymous()

    development = CabelasDevelopmentController()
    ordering = CabelasOrderingController()

    @expose('tribal.templates.cabelas.index')
    @tabFocus(tab_type="main")
    def index(self):
        return dict()
