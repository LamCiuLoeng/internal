# -*- coding: utf-8 -*-
from datetime import datetime as dt
import os
import random
import traceback

from repoze.what import authorize
from tg import config
from tg import expose
from tg import flash
from tg import redirect
from tg import request
from tg import session
from tribal.lib.base import BaseController
from tribal.model import *
from tribal.util import orsay_util
from tribal.util.common import *
from tribal.util.master_helper import *

class OrsayItem2Controller(BaseController):

    def getAddOrderDate(self, season):
        washing = {}
        for c in ["Washing", "Bleeding", "Various", "Ironing", "Accessories"]: washing[c] = getOrsayWashingList(c, season)
        return dict(customerList=getOrsayCustomerList(),
                    washing=washing,
                    token=orsay_util.create_token(),
                    action='add',
                    season=season)

    @expose('tribal.templates.orsay.item2_form')
    @tabFocus(tab_type="main")
    def index(self, **kw):
        if kw.get("season", None) not in ['s11', 's12']:
            flash("System error, please contact MIS Dept.!")
            redirect("/orsay/index")
        return self.getAddOrderDate(kw['season'])

    def getViewOrderDate(self, order):
        detail = DBSession.query(OrsayOrderDetail2).filter(OrsayOrderDetail2.head_id == order.id).one()
        return {"order": order, "detail": detail}

    @expose("json")
    def ajaxGetWashing(self, ** kw):
        try:
            w = DBSession.query(OrsayWashing).get(kw["id"])
            return {"flag":0, "img":imgURL % w.flag, "content":populateTranslation(w)}
        except:
            traceback.print_exc()
            return {"flag":1}

    @expose("json")
    def ajaxOrderInfo(self, ** kw):
        order = getOr404(OrsayOrder, kw.get("id", None), redirect_url="/orsay/index")
        return self.getViewOrderDate(order)

    @expose()
    def saveOrder(self, ** kw):
        if session.get("token", None) != kw.get("token", None):
            flash("Please don't submit the form repeatedly!")
            redirect("/orsay/index")
        else:
            if "token" in session: del session["token"]

        headerParamNames = ["company_code", "cust_name", "cust_code", "billto_address", "billto_contact_sales",
            "billto_tel_no", "shipto_address", "shipto_contact_person", "shipto_tel_no", "customer_po", "season"]
        emailSubject = " ".join([kw.get("customer_po", ""), dt.now().strftime("%d %b %Y")])

        try:
            headerParams = {
                "order_type": "C2",
                "qty": 0 if not kw.get("qty", False) else int(kw["qty"]),
                "email_subject": emailSubject,
                "create_by": request.identity["user"],
                }
            for pn in headerParamNames:
                if kw.get(pn, False): headerParams[pn] = kw[pn]

            header = OrsayOrder(** headerParams)
            if kw.get("action") == 'edit':
                header.id = kw.get('order_id')
                DBSession.merge(header)
                header = DBSession.query(OrsayOrder).get(header.id)
            else:
                DBSession.add(header)
            DBSession.flush()

            detailParams = {"head_id": header.id}
            for wi in ["washing", "bleeding", "various", "ironing", "accessories"]:
                if kw.get(wi, False): detailParams[wi] = DBSession.query(OrsayWashing).get(kw[wi])

            detail = OrsayOrderDetail2(** detailParams)
            if kw.get("action") == 'edit':
                detail.id = kw.get("detail_id")
                DBSession.merge(detail)
                detail = DBSession.query(OrsayOrderDetail2).get(detail.id)
            else:
                DBSession.add(detail)
            DBSession.flush()

            pdfFile = orsay_util.get_pdf_file(emailSubject)
            xlsFile = orsay_util.get_xls_file(emailSubject)
            template = 'ORSAY_ITEM2_TEMPLATE' if header.season=='s11' else 'ORSAY_ITEM5_TEMPLATE'
            orsay_util.gen_pdf(pdfFile, _get_pdf_params(detail), template)
            orsay_util.gen_xls(xlsFile, _get_xls_params(header, detail), template)
            orsay_util.send_mail(header, emailSubject, [pdfFile, xlsFile])
        except:
            traceback.print_exc()
            flash("Error on the server side,plase try it later!")
            raise redirect("/orsay/index")
        else:
            flash("Save the order successfully!")
            raise redirect("/orsay/index")

imgURL = config.website_url + "/images/care_label/%s"
imgPath = config.image_path + "/care_label/%s"

def _get_pdf_params(detail):
    return{
        "font_path": config.font_path,
        "washing_img": imgURL % detail.washing.flag,
        "washing": populateTranslation(detail.washing),
        "bleeding_img": imgURL % detail.bleeding.flag,
        "bleeding": populateTranslation(detail.bleeding),
        "various_img": imgURL % detail.various.flag,
        "various": populateTranslation(detail.various),
        "ironing_img": imgURL % detail.ironing.flag,
        "ironing": populateTranslation(detail.ironing),
        "accessories_img": imgURL % detail.accessories.flag,
        "accessories": populateTranslation(detail.accessories),
        }

def _get_xls_params(order, detail):
    return{
        "order_type": order.order_type,
        "washing": populateTranslation(detail.washing),
        "bleeding": populateTranslation(detail.bleeding),
        "various": populateTranslation(detail.various),
        "ironing": populateTranslation(detail.ironing),
        "accessories": populateTranslation(detail.accessories),
        "washing_img": imgPath % detail.washing.flag,
        "bleeding_img": imgPath % detail.bleeding.flag,
        "various_img": imgPath % detail.various.flag,
        "ironing_img": imgPath % detail.ironing.flag,
        "accessories_img": imgPath % detail.accessories.flag,
        }
