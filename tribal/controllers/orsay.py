# -*- coding: utf-8 -*-
import traceback
import os
import subprocess

from datetime import datetime as dt
from orsayItem1 import OrsayItem1Controller
from orsayItem2 import OrsayItem2Controller
from orsayItem3 import OrsayItem3Controller
from repoze.what import authorize
from repoze.what.predicates import not_anonymous
from sqlalchemy.sql.expression import desc
from tg import request
from tg import expose
from tg import flash
from tg import override_template
from tg import redirect
from tg import require
from tg import config
from tg.decorators import paginate
from tribal.lib.base import BaseController
from tribal.model import *
from tribal.util.common import *
from tribal.util.master_helper import *
from tribal.widgets.orsay import *

class OrsayController(BaseController):
    #Uncomment this line if your controller requires an authenticated user

    item1 = OrsayItem1Controller()
    item2 = OrsayItem2Controller()
    item3 = OrsayItem3Controller()

    @expose('tribal.templates.orsay.index')
    @require(not_anonymous())
    @tabFocus(tab_type="main")
    def index(self):
        return dict(page='index')
    
    @expose('tribal.templates.orsay.invoice')
    def show_invoice(self, **kw):
        order = DBSession.query(OrsayOrder).get(int(kw['id']))
        invoice_no = 'SA%s-SZ' % dt.now().strftime('%Y%m%d')
        item_no = kw.get('item_no', '')
        return {'order':order, 'invoice_no':invoice_no, 'item_no':item_no}

    @expose('')
    def invoice(self, **kw):
        order = DBSession.query(OrsayOrder).get(int(kw['id']))
        item_no = kw.get('item_no', '')
        
        abs_path = os.path.join("orsay", dt.now().strftime('%Y%m%d'))
        attachment_file = os.path.join(abs_path, 'invoice_%s.pdf' % order.customer_po)
        pdf_file = os.path.join(config.download_dir, attachment_file)
        phantomjs = os.path.join(config.public_dir, 'phantomjs', 'phantomjs.exe')
        rasterize = os.path.join(config.public_dir, 'phantomjs', 'rasterize.js')
        http_url = 'http://%s/orsay/show_invoice?id=%s&item_no=%s' % (request.headers.get('Host'), order.id, item_no)
        cmd = '%s %s %s %s' % (phantomjs, rasterize, http_url, pdf_file)
        sp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while 1:
            if sp.poll() is not None:
                #print 'exec command completed.'
                break
            else:
                line = sp.stdout.readline().strip()
        return serveFile(pdf_file)

    @expose("json")
    @require(not_anonymous())
    def ajaxCustomerInfo(self, ** kw):
        try:
            result = getOrsayCustomerInfo(kw["cn"])
            return {"flag": 0, "data": result}
        except:
            traceback.print_exc()
            return {"flag": 1, "data": ""}

    @expose()
    @require(not_anonymous())
    @tabFocus(tab_type="main")
    def viewOrder(self, ** kw):
        (flag, id) = rpacDecrypt(kw.get("code", ""))
        if not flag:
            flash("Please don't access the resource illegally!")
            redirect("/orsay/index")
        return self.__viewOrder(method='viewOrder', id=id)

    @expose()
    @require(not_anonymous())
    @tabFocus(tab_type="main")
    def viewOrderByID(self, ** kw):
        return self.__viewOrder(method='viewOrderByID', ** kw)

    @expose()
    @require(not_anonymous())
    @tabFocus(tab_type="main")
    def editOrder(self, ** kw):
        return self.__viewOrder(True, method='editOrder', ** kw)

    @expose("tribal.templates.orsay.order_log")
    @require(not_anonymous())
    @paginate('result', items_per_page=30)
    @tabFocus(tab_type="main")
    def orderLog(self, ** kw):
        order_type = None
        if not kw.get("order_type", False):
            result = []
        else:
            (order_type, season) = kw["order_type"].split('_')
#            result = DBSession.query(OrsayOrder).filter(OrsayOrder.order_type == order_type).filter(OrsayOrder.season == season).filter(OrsayOrder.create_by == request.identity["user"]).order_by(desc(OrsayOrder.create_time)).all()
            result = DBSession.query(OrsayOrder).filter(OrsayOrder.order_type == order_type).filter(OrsayOrder.season == season).order_by(desc(OrsayOrder.create_time)).all()
        return {"result": result, "widget": orderSearchFormInstance, "values": kw, 'item_no': order_type[1:] if order_type else ''}

    @expose("tribal.templates.orsay.search")
    @require(not_anonymous())
    @paginate('result', items_per_page=30)
    @tabFocus(tab_type="view")
    def search(self, ** kw):
        if len(kw) > 0:
            keys = ['confirmedDateBegin', 'customer_po', 'order_type', 'confirmedDateEnd']
            result = DBSession.query(OrsayOrder)
            for key in keys:
                if len(kw[key]) > 0:
                    if key is 'confirmedDateBegin': result = result.filter(OrsayOrder.create_time >= dt.strptime(kw.get(key, '2009-12-1200:00:00') + "00:00:00", "%Y-%m-%d%H:%M:%S"))
                    elif key is 'confirmedDateEnd': result = result.filter(OrsayOrder.create_time <= dt.strptime(kw.get(key, '2009-12-1200:00:00') + "23:59:59", "%Y-%m-%d%H:%M:%S"))
                    else: result = result.filter(getattr(OrsayOrder, key).like('%' + kw[key] + '%'))
#            result = result.filter(OrsayOrder.create_by == request.identity["user"]).all()
            result = result.all()
        else:
            result = []
        return {"result": result, "widget": trakingForm, "values": kw}

    def __viewOrder(self, fromEdit=None, ** kw):
        order = getOr404(OrsayOrder, kw.get("id", None), redirect_url="/orsay/index")
        season = order.season
#        if order.create_by != request.identity["user"]:
#            flash("Permission denied to access this order!")
#            redirect("/orsay/index")

        try:
            if order.order_type == "C2":
                if fromEdit:
                    override_template(getattr(self, kw.get("method", None)), 'mako:tribal.templates.orsay.item2_form')
                    params = self.item2.getAddOrderDate(season)
                    params.update(action='edit')
                    return params
                else:
                    override_template(getattr(self, kw.get("method", None)), 'mako:tribal.templates.orsay.item2_view')
                    return self.item2.getViewOrderDate(order)
            elif order.order_type == "C1":
                if fromEdit:
                    override_template(getattr(self, kw.get("method", None)), 'mako:tribal.templates.orsay.item1_form')
                    params = self.item1.getAddOrderDate(season)
                    params.update(action='edit')
                    return params
                else:
                    override_template(getattr(self, kw.get("method", None)), 'mako:tribal.templates.orsay.item1_view')
                    return self.item1.getViewOrderDate(order)
            elif order.order_type == "C3":
                if fromEdit:
                    override_template(getattr(self, kw.get("method", None)), 'mako:tribal.templates.orsay.item3_form')
                    params = self.item3.getAddOrderDate(season)
                    params.update(action='edit')
                    return params
                else:
                    override_template(getattr(self, kw.get("method", None)), 'mako:tribal.templates.orsay.item3_view')
                    params = self.item3.getViewOrderDate(order)
                    params.update(self.item3.getAddOrderDate(season))
                    return params
            else:
                flash("No such order page!")
                redirect("/orsay/index")
        except:
            traceback.print_exc()
            flash("No detail info for this order.")
            redirect("/orsay/index")
