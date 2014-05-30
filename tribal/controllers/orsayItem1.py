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
from tribal.model.orsay import *
from tribal.util import orsay_util
from tribal.util.common import *
from tribal.util.master_helper import *

class OrsayItem1Controller(BaseController):

    def getAddOrderDate(self, season=None):
        return dict(customerList=getOrsayCustomerList(),
                    sizeList=OrsaySize.find_by_season(season),
                    articleList=OrsayArticleDesc.find_by_season(season),
                    collectionList=OrsayOrignCollection.all(),
                    partList=OrsayPart.find_by_season(season),
                    materialList=OrsayMaterial.find_by_season(season),
                    appendixList=OrsayAppendix.find_by_season(season),
                    token=orsay_util.create_token(),
                    action='add',
                    season=season)

    @expose('tribal.templates.orsay.item1_form')
    @tabFocus(tab_type="main")
    def index(self, **kw):
        if kw.get("season", None) not in ['s11', 's12']:
            flash("System error, please contact MIS Dept.!")
            redirect("/orsay/index")
        return self.getAddOrderDate(kw['season'])

    def getViewOrderDate(self, order, isJson=None):
        detail = DBSession.query(OrsayOrderDetail1).filter(OrsayOrderDetail1.head_id == order.id).one()
        _materials = OrsayMaterial.findByIds(detail.material_ids)
        if not isJson:
            detail.parts = OrsayPart.findByIds(detail.part_ids)
            detail.appendixs = OrsayAppendix.findByIds(detail.appendix_ids)
        (index2, index3, count, percents, materials) = (0, 0, 0, [], [])
        for i in detail.material_percents.split(','):
            count += float(i)
            index3 += 1
            if count == 100:
                count = 0
                percents.append(detail.material_percents.split(',')[index2:index3])
                materials.append(_materials[index2:index3])
                index2 = index3
        return {"order": order, "detail": detail, "percents":percents, "materials":materials}

    @expose("json")
    def ajaxOrderInfo(self, ** kw):
        order = getOr404(OrsayOrder, kw.get("id", None), redirect_url="/orsay/index")
        return self.getViewOrderDate(order, True)

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
                "order_type": "C1",
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
            for wi in ["size_id", "article_desc_id", "reference_no", "reference_color_no", "order_no", "orign_collection_id", "orign_location", "trademark", "part_ids", "material_ids", "material_percents", "appendix_ids"]:
                detailParams[wi] = kw.get(wi, False)

            detail = OrsayOrderDetail1(** detailParams)
            if kw.get("action") == 'edit':
                detail.id = kw.get("detail_id")
                DBSession.merge(detail)
                detail = DBSession.query(OrsayOrderDetail1).get(detail.id)
            else:
                DBSession.add(detail)
            DBSession.flush()
            pdfFile = orsay_util.get_pdf_file(emailSubject)
            xlsFile = orsay_util.get_xls_file(emailSubject)
            orsay_util.gen_pdf(pdfFile, _get_pdf_params(detail), 'ORSAY_ITEM1_TEMPLATE')
            orsay_util.gen_xls(xlsFile, _get_xls_params(header, detail), 'ORSAY_ITEM1_TEMPLATE')
            orsay_util.send_mail(header, emailSubject, [pdfFile, xlsFile])
        except:
            traceback.print_exc()
            flash("Error on the server side,plase try it later!")
            raise redirect("/orsay/index")
        else:
            flash("Save the order successfully!")
            raise redirect("/orsay/index")

def _get_materials(detail):
    parts = OrsayPart.findByIds(detail.part_ids)
    materials = OrsayMaterial.findByIds(detail.material_ids)
    material_percents = detail.material_percents
    (index2, index3, count, _percents, _materials) = (0, 0, 0, [], [])
    for i in material_percents.split(','):
        count += float(i)
        index3 += 1
        if count == 100:
            count = 0
            _percents.append(material_percents.split(',')[index2:index3])
            _materials.append(materials[index2:index3])
            index2 = index3
    return [parts, _materials, _percents]

def _get_appendixs(detail):
    return [populateTranslation(i) for i in OrsayAppendix.findByIds(detail.appendix_ids)]

def _get_pdf_params(detail):

    def get_materials():
        (parts, _materials, _percents) = _get_materials(detail)
        html = ''
        i = 0
        for a in parts:
            html += '<tr><td colspan="2" valign="top" class="part1">%s</td></tr>' % populateTranslation(a)
            k = 0
            for b in _materials[i]:
                html += '<tr><td valign="top" class="material1">%s %%</td><td class="material2">%s</td></tr>' % (_percents[i][k], populateTranslation(b))
                k += 1
            i += 1
        return html

    def get_appendixs():
        return ('<br/><br/>').join(_get_appendixs(detail))

    return {
        "font_path": config.font_path,
        "size1": detail.size.name,
        "size2": detail.size.name_euro,
        "size3": detail.size.name_slo,
        "article": populateTranslation(detail.article_desc),
        "number1": detail.reference_no,
        "number2": detail.reference_color_no,
        "number3": detail.order_no,
        "collection": detail.orign_collection.name,
        "location": detail.orign_location,
        "trademark": detail.trademark,
        "materials": get_materials(),
        "appendixs": get_appendixs()
    }


def _get_xls_params(order, detail):

    def get_materials():
        (parts, _materials, _percents) = _get_materials(detail)
        htmls = []
        i = 0
        for a in parts:
            html = "%s\n" % populateTranslation(a)
            k = 0
            for b in _materials[i]:
                html += '%s%% %s\n' % (_percents[i][k], populateTranslation(b))
                k += 1
            i += 1
            htmls.append(html)
        return ('\n').join(htmls)

    def get_appendixs():
        return ('\n\n').join(_get_appendixs(detail))

    return{
        "order_type": order.order_type,
        "size1": "SIZE %s" % detail.size.name,
        "size2": "EUR %s" % detail.size.name_euro,
        "size3": "SLO %s" % detail.size.name_slo,
        "article": populateTranslation(detail.article_desc),
        "reference": '%s / %s' % (detail.reference_no, detail.reference_color_no),
        "order": detail.order_no,
        "collection": detail.orign_collection.name,
        "location": "Made in %s" % detail.orign_location,
        "trademark": detail.trademark,
        "materials": get_materials(),
        "appendixs": get_appendixs()
        }
