#coding=utf-8
import logging, os, re
import simplejson as json
from datetime import datetime as dt
from tribal.lib.base import BaseController
from repoze.what import authorize
from repoze.what.predicates import not_anonymous, has_permission
from tg import request
from tg import expose
from tg import flash
from tg import redirect
from tg import config
from tg import require
from tg.decorators import paginate
from tribal.model import *
from tribal.util.common import *
from tribal.util.excel_helper import *
import transaction
import subprocess
from tribal.widgets.orchestra import *

log = logging.getLogger(__name__)

class OrchestraExcel(ExcelBasicGenerator):

    def inputData(self, params):
        excelSheet = self.workBook.Sheets(1)
        for i in ["sku", "age", 'specification', 'item_info1', "product_family", "origin", "compositions", "care_imgs", "cares"]:
            if params[i]:
                if i == 'care_imgs':
                    for index, j in enumerate(params[i]):
                        excelSheet.Shapes.AddPicture(os.path.join(config.here, 'tribal\\public', j[1:len(j)].replace('/', '\\')), 1, 1, 60+index*40, 380, 40, 40)
                else:
                    excelSheet.Range(i).Value = params[i]

def _redo_order(orders):
    
    def do(order):
        
        if not order.attachment:
            abs_path = os.path.join("orchestra", dt.now().strftime('%Y%m%d'))
            attachment_folder = os.path.join(config.download_dir, abs_path)
            if not os.path.exists(attachment_folder):
                os.makedirs(attachment_folder)
    
            attachments = []
            file_name = 'ORC_label-%s-%s' % ('_'.join(re.findall(r'\w+', order.customer_po)), dt.now().strftime('%H%M%S'))
    
            #generate pdf
            def gen_pdf():
                attachment_file = os.path.join(abs_path, '%s.pdf' % file_name)
                pdf_file = os.path.join(config.download_dir, attachment_file)
                phantomjs = os.path.join(config.public_dir, 'phantomjs', 'phantomjs.exe')
                rasterize = os.path.join(config.public_dir, 'phantomjs', 'rasterize.js')
                http_url = 'http://%s/orchestra/%s/show_layout?id=%s' % (request.headers.get('Host'), order.team, order.id)
                cmd = '%s %s %s %s' % (phantomjs, rasterize, http_url, pdf_file)
                sp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                while 1:
                    if sp.poll() is not None:
                        #print 'exec command completed.'
                        break
                    else:
                        line = sp.stdout.readline().strip() 
                attachments.append(attachment_file)
    
            #generate xls
            def gen_xls():
                attachment_file = os.path.join(abs_path, '%s.xls' % file_name)
                product_family_str = ''
                if order.product_family_langs:
                    for i in order.product_family_langs.split(','):
                        product_family_str += '%s\n' % getattr(order.product_family, i)
                composition_str = ''
                if order.fabrics:
                    for fabric_index, fabric in enumerate(order.fabrics):
                        if fabric:
                            composition_str += '%s / %s / %s / %s:\n' % (fabric.french, fabric.english, fabric.arabic, fabric.chinese)
                        for composition_index, composition in enumerate(order.compositions[fabric_index]):
                            composition_str += '%s %%\n' % (order.percents[fabric_index][composition_index])
                            composition_str += '%s/%s/%s/%s/%s/%s/%s/%s\n' % (composition.french, composition.english, composition.spanish, composition.portugese, composition.german, composition.chinese, composition.arabic, composition.russian)
                            #compositions = order.compositions(order.composition_ids.split('|')[index])
                care_imgs = [i.path for i in order.care_imgs] if order.care_imgs else []
                care_str = ''
                if order.care_ids:
                    for i in order.cares:
                        care_str += '%s\n%s\n%s\n%s\n%s\n%s\n%s\n%s\n\n' % (i.french, i.english, i.spanish, i.portugese, i.german, i.chinese, i.arabic, i.russian)
    
                age = ''
                if order.height:
                    age='年龄/身高%s' % order.height
                elif order.head_size:
                    age='年龄/头围%s' % order.head_size
                xls_params = dict(
                                  sku='款号:%s' % order.sku, age=age,
                                  specification='规格:%s' % order.specification if order.specification else '',
                                  product_family=product_family_str,
                                  item_info1='' if not order.item_info1 else '%s%s' % (order.item.info1, order.item_info1),
                                  origin='%s\n%s\n%s\n%s' % (order.origin.english, order.origin.spanish, order.origin.arabic, order.origin.chinese),
                                  ca_no='CA %s' % order.ca_no, compositions=composition_str, care_imgs=care_imgs, cares=care_str
                )
                xls_file = os.path.join(config.download_dir, attachment_file)
                xls_template = os.path.join(config.template_dir, "ORCHESTRA_TEMPLATE.xls")
                pe = OrchestraExcel(templatePath=xls_template, destinationPath=xls_file)
                pe.inputData(xls_params)
                pe.outputData()
                attachments.append(attachment_file)
    
            gen_pdf()
            gen_xls()
            order.add_attachments(attachments)

        if not order.send_mail:
            send_from = "r-pac-orchestra-order-system"
            send_to = request.identity["user"].email_address.split(";")
            cc_to = config.orchestra_email_cc.split(";") if config.has_key('orchestra_email_cc') else []
            cc_to.extend(order.create_by.email_address.split(";"))
            text = ["Thank you for your confirmation!",
                "You could view the order's detail information via the link below:",
                "%s/orchestra/%s/show_order?code=%s" % (config.website_url, order.team, rpacEncrypt(order.id)),
                "\n\n************************************************************************************",
                "This e-mail is sent by the r-pac Orchestra ordering system automatically.",
                "Please don't reply this e-mail directly!",
                "************************************************************************************"
                ]
            sendEmail(send_from, send_to, 'Orchestra Customer PO# %s' % order.customer_po, "\n".join(text), cc_to, order.get_attachments())
            order.send_mail = True
        return order

    if isinstance(orders, tuple) or isinstance(orders, list):
        attachments = []
        for order in orders:
            order.attachment = None
            do(order)
            attachments.extend(order.get_attachments())

        send_from = "r-pac-orchestra-order-system"
        send_to = request.identity["user"].email_address.split(";")
        cc_to = config.orchestra_email_cc.split(";") if config.has_key('orchestra_email_cc') else []
        cc_to.extend(order.create_by.email_address.split(";"))
        text = ["Thank you for your confirmation!",
            "\n\n************************************************************************************",
            "This e-mail is sent by the r-pac Orchestra ordering system automatically.",
            "Please don't reply this e-mail directly!",
            "************************************************************************************"
            ]
        sendEmail(send_from, send_to, 'Orchestra redo orders', "\n".join(text), cc_to, attachments)
    else:
        return do(orders)

class OrchestraCommonController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()

    def index(self):
        return {}

    def order(self):
        customers = OrchestraCustomer.all(order_func='name')
        customers_json = {}
        for i in customers:
            customers_json[i.id] = dict(name=i.name, contact=i.contact, email=i.email)
        return dict(customers=customers,
                    customers_json=json.dumps(customers_json),
                    fabrics=OrchestraFabric.all(order_func='english'),
                    cares=OrchestraCare.all(order_func='english'),
                    compositions=OrchestraComposition.all(order_func='english'),
                    product_familys=OrchestraProductFamily.all(order_func='type desc, english'),
                    origins=OrchestraOrigin.all(order_func='rank, english'),
                    care_imgs=OrchestraCareImg.all(),
                    items=OrchestraItem.all())

    def edit_order(self, **kw):
        order = OrchestraOrder.get(kw['id'])
        customers = OrchestraCustomer.all(order_func='name')
        customers_json = {}
        for i in customers:
            customers_json[i.id] = dict(name=i.name, contact=i.contact, email=i.email)
        return dict(order=order,
                    customers=customers,
                    customers_json=json.dumps(customers_json),
                    fabrics=OrchestraFabric.all(order_func='english'),
                    cares=OrchestraCare.all(order_func='english'),
                    compositions=OrchestraComposition.all(order_func='english'),
                    product_familys=OrchestraProductFamily.all(order_func='type desc, english'),
                    origins=OrchestraOrigin.all(order_func='rank, english'),
                    care_imgs=OrchestraCareImg.all(),
                    items=OrchestraItem.all())

    def list_order(self, **kw):
        return dict(orders=OrchestraOrder.find_by(order_func='create_time', **kw), widget=orchestraSearchForm)

    def show_layout(self, **kw):
        return {'order':OrchestraOrder.get(kw['id'])}

    def show_order(self, **kw):
        try:
            id = None
            if kw.has_key('code'):
                (flag, id) = rpacDecrypt(kw.get("code", ""))
                if not flag:
                    flash("Please don't access the resource illegally!", 'warn')
                    redirect("/orchestra/%s" % kw['team'])
            else:
                id = kw['id']
            order = OrchestraOrder.get(id)
            order = _redo_order(order)
            return {'order': order}
        except Exception, e:
            log.exception(str(e))
            flash("Error occor on the server side!", 'warn')
            redirect('/orchestra/%s' % kw['team'])

    def delete_order(self, **kw):
        order = OrchestraOrder.get(kw['id'])
        if order.team == kw['team']:
            order.active = 1
        redirect('/orchestra/%s/list_order' % kw['team'])

    def download(self, **kw):
        order = OrchestraOrder.get(kw['id'])
        order = _redo_order(order)
        return serveFile(order.download_attachment()) 

    def downloads(self, **kw):
        if kw.has_key('cb_ids'):
            return serveFile(OrchestraOrder.download_attachments(kw['cb_ids']))
        redirect('/orchestra/%s/list_order' % kw['team'])

    def redo_order(self, **kw):
        if kw.has_key('cb_ids'):
            _redo_order(OrchestraOrder.find_by_ids(kw['cb_ids']))
            flash("Redo orders success, please check your e-mail!")
        redirect('/orchestra/%s/list_order' % kw['team'])

    def save_order(self, **kw):
        try:
            kw = extract_inline_list('fabric_set',** kw)
            if kw.has_key('fabric_set'):
                for i in kw['fabric_set']:
                    for k,v in i.iteritems():
                        if type(v)==list or type(v)==tuple:
                            v = ','.join(map(str, v))
                        if not kw.has_key(k):
                            kw[k] = v
                        elif k=='fabric_ids':
                            kw[k] = '%s,%s' % (kw[k], v)
                        else:
                            kw[k] = '%s|%s' % (kw[k], v)
                del kw['fabric_set']
            else:
                kw['fabric_ids'] = None
                kw['composition_percents'] = None
                kw['composition_ids'] = None
            if kw.get('id', None):
                order = OrchestraOrder.get(kw['id'])
                order.update(**kw)
                flash("Order update success!")
            else:
                if kw.has_key('id'): del kw['id']
                order = OrchestraOrder.create(**kw)
                flash("Order create success!")
            order.attachment = None
            DBSession.flush()
        except Exception, e:
            log.exception(str(e))
            transaction.doom()
            flash("Error occor on the server side!", 'warn')
            redirect('/orchestra/%s/index' % kw['team'])
        finally:
            redirect('/orchestra/%s/show_order?id=%s' % (order.team, order.id))

class OrchestraHKController(OrchestraCommonController):

    @expose('tribal.templates.orchestra.index')
    @require(has_permission('ORCHESTRA_HK'))
    @tabFocus(tab_type="main")
    def index(self):
        result = super(OrchestraHKController, self).index()
        result.update({'team':'HK'})
        return result

    @expose('tribal.templates.orchestra.order')
    @require(has_permission('ORCHESTRA_HK'))
    def order(self):
        result = super(OrchestraHKController, self).order()
        result.update({'team':'HK'})
        return result

    @expose('tribal.templates.orchestra.order_edit')
    @tabFocus(tab_type='main')
    def edit_order(self, **kw):
        kw.update({'team':'HK'})
        result = super(OrchestraHKController, self).edit_order(**kw)
        result.update({'team':'HK'})
        return result

    @expose('tribal.templates.orchestra.order_list')
    @require(has_permission('ORCHESTRA_HK'))
    @tabFocus(tab_type='main')
    def list_order(self, **kw):
        result = super(OrchestraHKController, self).list_order(**kw)
        result.update({'team':'HK'})
        return result

    @expose('tribal.templates.orchestra.layout')
    def show_layout(self, **kw):
        result = super(OrchestraHKController, self).show_layout(**kw)
        result.update({'team':'HK'})
        return result

    @expose('tribal.templates.orchestra.order_show')
    @require(has_permission('ORCHESTRA_HK'))
    @tabFocus(tab_type='main')
    def show_order(self, **kw):
        kw.update({'team':'HK'})
        result = super(OrchestraHKController, self).show_order(**kw)
        result.update({'team':'HK'})
        return result

    @expose('')
    @require(has_permission('ORCHESTRA_HK'))
    def delete_order(self, **kw):
        kw.update({'team':'HK'})
        super(OrchestraHKController, self).delete_order(**kw)

    @expose('')
    @require(has_permission('ORCHESTRA_HK'))
    def download(self, **kw):
        kw.update({'team':'HK'})
        return super(OrchestraHKController, self).download(**kw)

    @expose('')
    @require(has_permission('ORCHESTRA_HK'))
    def downloads(self, **kw):
        kw.update({'team':'HK'})
        super(OrchestraHKController, self).downloads(**kw)

    @expose('')
    @require(has_permission('ORCHESTRA_HK'))
    def redo_order(self, **kw):
        kw.update({'team':'HK'})
        super(OrchestraHKController, self).redo_order(**kw)

    @expose('')
    @require(has_permission('ORCHESTRA_HK'))
    def save_order(self, **kw):
        kw.update({'team':'HK'})
        super(OrchestraHKController, self).save_order(**kw)

class OrchestraSHController(OrchestraCommonController):
    
    @expose('tribal.templates.orchestra.index')
    @require(has_permission('ORCHESTRA_SH'))
    @tabFocus(tab_type="main")
    def index(self):
        result = super(OrchestraSHController, self).index()
        result.update({'team':'SH'})
        return result

    @expose('tribal.templates.orchestra.order')
    @require(has_permission('ORCHESTRA_SH'))
    def order(self):
        result = super(OrchestraSHController, self).order()
        result.update({'team':'SH'})
        return result

    @expose('tribal.templates.orchestra.order_edit')
    @require(has_permission('ORCHESTRA_SH'))
    @tabFocus(tab_type='main')
    def edit_order(self, **kw):
        kw.update({'team':'SH'})
        result = super(OrchestraSHController, self).edit_order(**kw)
        result.update({'team':'SH'})
        return result

    @expose('tribal.templates.orchestra.order_list')
    @require(has_permission('ORCHESTRA_SH'))
    @tabFocus(tab_type='main')
    def list_order(self, **kw):
        result = super(OrchestraSHController, self).list_order(**kw)
        result.update({'team':'SH'})
        return result

    @expose('tribal.templates.orchestra.layout')
    def show_layout(self, **kw):
        result = super(OrchestraSHController, self).show_layout(**kw)
        result.update({'team':'SH'})
        return result

    @expose('tribal.templates.orchestra.order_show')
    @require(has_permission('ORCHESTRA_SH'))
    @tabFocus(tab_type='main')
    def show_order(self, **kw):
        kw.update({'team':'SH'})
        result = super(OrchestraSHController, self).show_order(**kw)
        result.update({'team':'SH'})
        return result

    @expose('')
    @require(has_permission('ORCHESTRA_SH'))
    def delete_order(self, **kw):
        kw.update({'team':'SH'})
        super(OrchestraSHController, self).delete_order(**kw)

    @expose('')
    @require(has_permission('ORCHESTRA_SH'))
    def download(self, **kw):
        kw.update({'team':'SH'})
        return super(OrchestraSHController, self).download(**kw)

    @expose('')
    @require(has_permission('ORCHESTRA_SH'))
    def downloads(self, **kw):
        kw.update({'team':'SH'})
        super(OrchestraSHController, self).downloads(**kw)

    @expose('')
    @require(has_permission('ORCHESTRA_SH'))
    def redo_order(self, **kw):
        kw.update({'team':'SH'})
        super(OrchestraSHController, self).redo_order(**kw)

    @expose('')
    @require(has_permission('ORCHESTRA_SH'))
    def save_order(self, **kw):
        kw.update({'team':'SH'})
        super(OrchestraSHController, self).save_order(**kw)

class OrchestraController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    #allow_only = authorize.not_anonymous()

    HK = hk = OrchestraHKController()
    SH = sh = OrchestraSHController()
