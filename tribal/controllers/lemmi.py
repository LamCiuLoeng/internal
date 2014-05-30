# -*- coding: utf-8 -*-
import shutil, os, zipfile, traceback, random, zlib
from datetime import datetime as dt
from collections import defaultdict
import re

# turbogears imports
from tg import expose
from tg import redirect, validate, flash, config, request
from tg.decorators import *

# third party imports
#from pylons.i18n import ugettext as _
from repoze.what import predicates, authorize
from repoze.what.predicates import not_anonymous, in_group, has_permission

# project specific imports
from tribal.lib.base import BaseController
#from tribal.model import DBSession, metadata
from tribal.model import *
from sqlalchemy.sql import *

from tribal.util.common import *
from tribal.util.excel_helper import *

from tribal.widgets import *
from tribal.widgets.lemmi import *
import transaction


class LemmiController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    allow_only = authorize.not_anonymous()

    @expose('tribal.templates.lemmi.index')
    @paginate('collections', items_per_page = 50)
    @tabFocus(tab_type = "main")
    def index(self, **kw):
        try:
            search_form = lemmi_search_form
            if kw:
                q = self._query_result(kw)
                if (not q) or q.count() < 1:
                    result = []
                else:
                    result = q.all()
                return dict(collections=result, values=kw, search_form=search_form)
            else:
                return dict(collections=[], values={}, search_form=search_form)
        except:
            flash("There service is not avaiable now,please try it later.", status="warn")
            traceback.print_exc()
 
 
    @expose()
    def export(self, **kw):
        try:
            fileDir = os.path.join(config.get("download_dir"), "LEMMI", dt.now().strftime("%Y%m%d"))
            if not os.path.exists(fileDir):
                os.makedirs(fileDir)
            new_file = os.path.join(fileDir, '%s.xls'% dt.now().strftime("%Y%m%d%H%M%S"))
            dlzipFile = os.path.join(fileDir, "export_%s%d.zip" % (dt.now().strftime("%Y%m%d%H%M%S"), random.randint(1, 1000)))
            templatePath = os.path.join(config.get('template_dir'), "LEMMI_TEMPLATE.xls")
            copyTemplatePath = os.path.join(fileDir, "LEMMI_TEMPLATE_tmp_%s%d.xls" % (dt.now().strftime("%Y%m%d%H%M%S"), random.randint(1, 1000)))
            shutil.copyfile(templatePath, copyTemplatePath)
            sid = kw.get("item_ids", '')
            id_list = [id for id in sid.split("_") if id]
            rs = DBSession.query(LemmiOrderHeader).filter(LemmiOrderHeader.id.in_(id_list)) \
                        .order_by(LemmiOrderHeader.id).all()
            data = []
            if rs:
                for item in rs:
                    for d in item.details:
                        textLine1_1 = ''
                        textLine1_2 = ''
                        if d.textLine1:
                            textLine1 = d.textLine1.split(' ')
                            textLine1_1 = textLine1[0]
                            textLine1_2 = textLine1[1]
                        textLine3 = d.textLine3.replace('/', ' ') if d.textLine3 else ''
                        age_1 = ''
                        age_2 = ''
                        if d.age:
                            age = d.age.split(' ')
                            age_1 = age[0]
                            age_2 = age[1]
                        gtin_1 = ''
                        gtin_2 = ''
                        gtin = d.gtin
                        if gtin and len(d.gtin.strip())==13:
                            gtin_1 = gtin.strip()[:12]
                            gtin_2 = gtin.strip()[-1]
                        else:
                            gtin_1 = gtin or ''
                        appendData = [
                               item.type, item.versionId, item.sender, item.receiver,
                               item.created, item.orderNumber, item.dispatchDate,
                               item.releaseMethod, item.countryOfOrigin, item.serviceLevel,
                               item.vendorNumber, item.companyName, item.contactPerson,
                               item.street1, item.street2, item.street3, item.zip, 
                               item.city, item.state, item.countryCode, item.countryName,
                               item.phone, item.fax, item.email, d.productId, 
                               d.type2, d.customerOrderLineId, d.quantity,
                               d.quantity3, d.itemNo, d.labelColor, textLine1_1,
                               textLine1_2, d.textLine2, textLine3, d.model, d.modelDescription,
                               d.color, d.size, d.waistSize, d.widthLength, 
                               age_1, age_2, d.sex, d.season, d.currency,
                               d.retailPrice, d.prodOrder, gtin_1, gtin_2]
                        data.append(appendData)
                        
                xls_file = self._generateExcel(data, new_file, copyTemplatePath)
                dlzip = zipfile.ZipFile(dlzipFile, "w", zlib.DEFLATED)
                dlzip.write(os.path.abspath(str(xls_file)), os.path.basename(str(xls_file)))
                dlzip.close()
                try:
                    os.remove(xls_file)
                    os.remove(copyTemplatePath)
                except:
                    pass
                return serveFile(unicode(dlzipFile))
        except:
            traceback.print_exc()

    def _generateExcel(self, data, filename, copyTemplatePath):
        lemmi = LemmiOrderExcel(templatePath=copyTemplatePath, destinationPath=filename)
        try:
            lemmi.inputData(data=data)
            lemmi.outputData()
            return filename
        except:
            traceback.print_exc()
            if lemmi:
                lemmi.clearData()
            redirect("/lemmi/index")
    




    def _query_result(self, kw):
        try:
            conditions = []
            if kw.get("orderNumber", False):
                orderNumber = kw["orderNumber"].strip()
                if ',' in orderNumber and '-' in orderNumber:
                    orderNumber_list = [str(p.strip()) for p in orderNumber.split(',') if str(p)]
                    tmp_list = []
                    for index, num in enumerate(orderNumber_list):
                        if '-' in num:
                            tmp_list += [str(i) for i in range(int(num.split('-')[0].strip()), int(num.split('-')[1].strip()) + 1)]
                            del orderNumber_list[index]

                    conditions.append(LemmiOrderHeader.orderNumber.in_(orderNumber_list + tmp_list))
                elif ',' in orderNumber:
                    conditions.append(LemmiOrderHeader.orderNumber.in_([str(p.strip()) for p in orderNumber.split(',') if str(p)]))
                elif '-' in orderNumber:
                    conditions.append(LemmiOrderHeader.orderNumber.in_(
                                      [str(i) for i in range(
                                        int(orderNumber.split('-')[0].strip()),  
                                        int(orderNumber.split('-')[1].strip()) + 1)]))
                else:
                    conditions.append(LemmiOrderHeader.__table__.c.order_number.op('ilike')("%%%s%%" % kw["orderNumber"].strip()))

            
            if kw.get("vendorNumber", False):
                conditions.append(LemmiOrderHeader.__table__.c.vendor_number.op('ilike')("%%%s%%" % kw["vendorNumber"].strip()))
                
            if kw.get("customerOrderLineId", False):
                conditions.append(LemmiOrderDetail.__table__.c \
                                   .customer_order_line_id.op('ilike')("%%%s%%" \
                                    % kw["customerOrderLineId"].strip()))
            
            if kw.get("countryOfOrigin", False):
                conditions.append(LemmiOrderHeader.__table__.c.country_of_origin.op('ilike')("%%%s%%" % kw["countryOfOrigin"].strip()))
                
            if kw.get("createdDateStart", False) and kw.get("createdDateEnd", False):
                b_date = dt.strptime(kw.get("createdDateStart", '2009-12-1200:00:00')+"00:00:00", "%Y-%m-%d%H:%M:%S")
                e_date = dt.strptime(kw.get("createdDateEnd", '2009-12-1200:00:00')+"23:59:59", "%Y-%m-%d%H:%M:%S")
                conditions.append(LemmiOrderHeader.created>=b_date)
                conditions.append(LemmiOrderHeader.created<=e_date)
            elif kw.get("createdDateStart", False):
                b_date = dt.strptime(kw.get("createdDateStart", '2009-12-1200:00:00')+"00:00:00", "%Y-%m-%d%H:%M:%S")
                conditions.append(LemmiOrderHeader.created>=b_date)
            elif kw.get("createdDateEnd", False):
                e_date = dt.strptime(kw.get("createdDateEnd", '2009-12-1200:00:00')+"23:59:59", "%Y-%m-%d%H:%M:%S")
                conditions.append(LemmiOrderHeader.created<=e_date)


            obj = DBSession.query(LemmiOrderHeader).join(LemmiOrderDetail) \
                    .filter(and_(LemmiOrderHeader.active==0, LemmiOrderDetail.active==0))
            if len(conditions):
                for value in conditions:
                    obj = obj.filter(value)
            return obj.order_by(desc(LemmiOrderHeader.id))
        except:
            traceback.print_exc()




