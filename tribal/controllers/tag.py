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
from tribal.util.format47 import color_french, dept_french, attach_set_french

from tribal.widgets import *
from tribal.widgets.tag import *
import transaction


class TAGController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    allow_only = authorize.not_anonymous()

    @expose('tribal.templates.tag.index')
    @paginate('collections', items_per_page = 50)
    @tabFocus(tab_type = "main")
    def index(self, **kw):
        try:
            search_form = tag_search_form
            if kw:
                q = self._query_result(kw)
                if (not q) or q.count() < 1:
                    result = []
                else:
                    result = q.all()
                return dict(collections = result, values = kw, search_form = search_form)
            else:
                return dict(collections = [], values = {}, search_form = search_form)
        except:
            flash("There service is not avaiable now,please try it later.", status = "warn")
            traceback.print_exc()


    @expose('tribal.templates.tag.historyitems')
    @paginate('collections', items_per_page = 50)
    @tabFocus(tab_type = "view")
    def historyitems(self, **kw):
        """for tag old items"""
        try:
            search_form = tag_search_form
            if kw:
                q = self._query_result(kw)
                if (not q) or q.count() < 1:
                    result = []
                else:
                    result = q.all()
                return dict(collections = result, values = kw, search_form = search_form)
            else:
                return dict(collections = [], values = {}, search_form = search_form)
        except:
            flash("There service is not avaiable now,please try it later.", status = "warn")
            traceback.print_exc()


    @expose('json')
    def saveSO(self, **kw):
        #DBSession.begin(subtransactions = True)
        try:
            _config = {"so":"soNo",
                       "soRemark":"soRemark", }
            for k, v in kw.items():
                key = k.split("_")[0]
                ids = k.split("_")[1:]
                rs = DBSession.query(TAGItem).filter(TAGItem.id.in_([int(id) for id in ids if id])).all()
                if rs:
                    for r in rs:
                        oldValue = getattr(r, _config[key])
                        setattr(r, _config[key], str(v.strip()))
                        r.soDate = dt.now()
                        his = TAGHistory(item = r)
                        actionType = "modify" if oldValue else "Add"
                        his.actionKind = actionType
                        his.actionContent = "Change <%s> from [%s] to [%s]." % (key, oldValue, str(v.strip()))
                        his.actionUser = request.identity["user"]
                        DBSession.add(his)
                        DBSession.flush()
            return {"flag":"OK"}
        except:
            #DBSession.rollback()
            transaction.doom()
            traceback.print_exc()
            return {"flag":"error"}

    @expose()
    def export(self, **kw):
        try:
            fileDir = os.path.join(config.get("download_dir"), "TAG", dt.now().strftime("%Y%m%d"))
            if not os.path.exists(fileDir):
                os.makedirs(fileDir)
            dlzipFile = os.path.join(fileDir, "export_%s%d.zip" % (dt.now().strftime("%Y%m%d%H%M%S"), random.randint(1, 1000)))
            #xls_format = ['Flapdoodles_905', 'Flapdoodles_925', 'Flapdoodles_940', 'Flapdoodles', 'LittleMe']
            xls_format = kw.get("xls_format", 'LittleMe')
            templatePath = os.path.join(config.get('template_dir'), "TAG_%s_TEMPLATE.xls" % xls_format)
            copyTemplatePath = os.path.join(fileDir, "TAG_TEMPLATE_tmp_%s%d.xls" % (dt.now().strftime("%Y%m%d%H%M%S"), random.randint(1, 1000)))
            shutil.copyfile(templatePath, copyTemplatePath)
            fileList = []
            sid = kw.get("item_ids", '')
            id_list = [id for id in sid.split("_") if id]
            rs = DBSession.query(TAGItem).filter(TAGItem.id.in_(id_list)) \
                        .order_by(cast(TAGItem.poNo, Integer), TAGItem.id).all()
            dictData = defaultdict(list)
            if rs:
                for item in rs:

#                    #skip item when upc is null
#                    if not item.upc:
#                        item.active = 1
#                        continue
#
                    if xls_format == 'Flapdoodles_905': # used
                        appendData = [
                                   item.poNo, '905', item.upc, item.colorDesc, item.sizeDesc,
                                   item.brand, item.retailPrice, item.attachmentSet,
                                   '-'.join([i for i in [item.style, item.color, item.prepack, item.label] if i]),
                                   # new added
                                   item.styleDesc or '',
                                   item.tagNo or '',
                                   item.custSKU or '', item.classCat or '', item.subClassSubCat or '', item.dept or '',
                                   item.custSeason or '', item.pantone or '', item.outletPrice or '', item.sizeRangeDesc or '',
                                   ###
                                   item.qty or 0, item.poUnits or 0,
                                   ]
                    elif xls_format == 'Flapdoodles_925':
                        appendData = [
                                   item.poNo, '925', item.upc, item.colorDesc, item.sizeDesc,
                                   item.msrp, item.brand, item.attachmentSet,
                                   '-'.join([i for i in [item.style, item.color, item.prepack, item.label] if i]),
                                   # new added
                                   item.styleDesc or '',
                                   item.tagNo or '',
                                   item.custSKU or '', item.classCat or '', item.subClassSubCat or '', item.dept or '',
                                   item.custSeason or '', item.pantone or '', item.outletPrice or '', item.sizeRangeDesc or '',
                                   ###
                                   item.qty or 0, item.poUnits or 0,
                                   ]
                    elif xls_format == 'Flapdoodles_940': # used
                        appendData = [
                                   item.poNo, '940', item.upc, item.colorDesc, item.sizeDesc,
                                   item.merchGroupF, item.msrp, item.color, item.brand,
                                   #added by CL on 2011-03-22 PM ad Eva require
                                   item.attachmentSet or '',
                                   '-'.join([i for i in [item.style, item.color, item.prepack, item.label] if i]),
                                   # new added
                                   item.styleDesc or '',
                                   item.tagNo or '',
                                   item.custSKU or '', item.classCat or '', item.subClassSubCat or '', item.dept or '',
                                   item.custSeason or '', item.pantone or '', item.outletPrice or '', item.sizeRangeDesc or '',
                                   ###
                                   item.qty or 0, item.poUnits or 0,
                                   ]
                    elif xls_format == 'Flapdoodles': # used
                        appendData = [
                                   item.itemNo, item.poNo, item.upc,
                                   #'-'.join([i for i in [str(item.style), str(item.prepack  or '')] if i]),
                                   '-'.join([i for i in [item.style, item.color, item.prepack, item.label] if i]),
                                   item.colorDesc, item.sizeDesc, item.merchGroupF, item.msrp, item.color,
                                   item.attachmentSet, item.brand,
                                   # new added
                                   item.styleDesc or '',
                                   item.tagNo or '',
                                   item.custSKU or '', item.classCat or '', item.subClassSubCat or '', item.dept or '',
                                   item.custSeason or '', item.pantone or '', item.outletPrice or '', item.sizeRangeDesc or '',
                                   ###
                                   item.qty or 0, item.poUnits or 0,
                                   ]
                    elif xls_format == 'Guess':  # for Guess, add@20111222
                        attachmentSet, attachmentSetFrench = attach_set_french(item.attachmentSet)
                        appendData = [
                                   self._return_upper(item.poNo), self._return_upper(item.style), self._return_upper(item.styleDesc),
                                   self._return_upper(item.colorDesc),
                                   self._return_upper(color_french(item.colorDesc)),  # (French)
                                   self._return_upper(item.sizeDesc), item.upc, self._return_upper(item.sizeRangeDesc or ''),
                                   self._return_upper(dept_french(item.sizeRangeDesc)),  # (French)
                                   self._return_upper(item.merchGroupF),
                                   # '',
                                   item.msrp or '', item.outletPrice or '',
                                   self._return_upper(attachmentSet),
                                   self._return_upper(attachmentSetFrench),  # (French)
                                   self._return_upper('-'.join([i for i in [item.style, item.color, item.prepack, item.label] if i])),
                                   self._return_upper(item.style), item.qty or 0, item.poUnits or 0,
                                   ]
                    elif xls_format == 'KENSIEGIRL':  # for KENSIE GIRL, add@20121129
                        attachmentSet, attachmentSetFrench = attach_set_french(item.attachmentSet)
                        appendData = [
                                   self._return_upper(item.poNo), self._return_upper(item.style), self._return_upper(item.colorDesc),
                                   self._return_upper(color_french(item.colorDesc)),  # (French)
                                   self._return_upper(item.sizeDesc), item.upc, self._return_upper(item.sizeRangeDesc or ''),
                                   self._return_upper(dept_french(item.sizeRangeDesc)),  # (French)
                                   self._return_upper(item.merchGroupF), item.msrp or '', item.outletPrice or '',
                                   self._return_upper(attachmentSet),
                                   self._return_upper(attachmentSetFrench),  # (French)
                                   self._return_upper('-'.join([i for i in [item.style, item.color, item.prepack, item.label] if i])),
                                   self._return_upper(item.style), item.qty or 0, item.poUnits or 0,
                                   ]
                    else:
                        _brand = str(item.brand).upper() if item.brand else ''
                        _style = (item.style or '') if _brand == 'Splendid'.upper() or 'Ella'.upper() in _brand else '-'.join([i for i in [item.style, item.color, item.prepack, item.label] if i])

                        appendData = [
                                   item.itemNo, item.poNo, item.upc,
                                   #'-'.join([i for i in [str(item.style), str(item.prepack  or '')] if i]),
                                   # '-'.join([i for i in [item.style, item.color, item.prepack, item.label] if i]),
                                   _style,
                                   item.colorDesc, item.sizeDesc, item.merchGroupF, item.msrp, item.color,
                                   item.attachmentSet, item.brand,
                                   # new added
                                   item.styleDesc or '',
                                   item.tagNo or '',
                                   item.custSKU or '', item.classCat or '', item.subClassSubCat or '', item.dept or '',
                                   item.custSeason or '', item.pantone or '', item.outletPrice or '', item.sizeRangeDesc or '',
                                   ###
                                   item.qty or 0, item.poUnits or 0,
                                   ]
                    tmp_so = item.soNo.strip() if item.soNo else ''
                    dictData[tmp_so].append(appendData)
                    del tmp_so
                for key, value in dictData.items():
                    fileList.append(self._generateExcel('', value, key,
                                                        copyTemplatePath, fileDir))

                dlzip = zipfile.ZipFile(dlzipFile, "w", zlib.DEFLATED)
                for fl in fileList:
                    dlzip.write(os.path.abspath(str(fl)), os.path.basename(str(fl)))
                dlzip.close()
                try:
                    for fl in fileList:
                        os.remove(fl)
                    os.remove(copyTemplatePath)
                except:
                    pass
                return serveFile(unicode(dlzipFile))
        except:
            traceback.print_exc()

    def _generateExcel(self, sheetName, data, so, copyTemplatePath, fileDir):
        filename = os.path.join(fileDir, "%s_%s.xls" % (so, dt.now().strftime("%Y%m%d%H%M%S")))

        tag = TAGExcel(templatePath = copyTemplatePath, destinationPath = filename)
        try:
            tag.inputData(sheetName = sheetName, data = data, so = so)
            tag.outputData()
            return filename
        except:
            traceback.print_exc()
            if tag:
                tag.clearData()
            redirect("/tag/index")

    @expose()
    def getAjaxField(self, **kw):
        try:
            fieldName = kw.get("fieldName", '')
            latest = int(kw.get("latest", 0))
            result = []
            if fieldName == 'poNo':
                rs = DBSession.query(TAGItem).filter(and_(TAGItem.active==0, TAGItem.latest==latest, TAGItem.__table__.c.po_no.op('ilike')("%%%s%%" % str(kw["q"]).strip()))).all()
                result = list(set([v.poNo for v in rs ]))
            elif fieldName == 'brand':
                rs = DBSession.query(TAGItem).filter(and_(TAGItem.active==0, TAGItem.latest==latest, TAGItem.__table__.c.brand.op('ilike')("%%%s%%" % str(kw["q"]).strip()))).all()
                result = list(set([v.brand for v in rs ]))
            elif fieldName == 'style':
                rs = DBSession.query(TAGItem).filter(and_(TAGItem.active==0, TAGItem.latest==latest, TAGItem.__table__.c.style.op('ilike')("%%%s%%" % str(kw["q"]).strip()))).all()
                result = list(set([v.style for v in rs ]))
            elif fieldName == 'soNo':
                rs = DBSession.query(TAGItem).filter(and_(TAGItem.active==0, TAGItem.latest==latest, TAGItem.__table__.c.so_no.op('ilike')("%%%s%%" % str(kw["q"]).strip()))).all()
                result = list(set([v.soNo for v in rs ]))
            elif fieldName == 'tagNo':
                rs = DBSession.query(TAGItem).filter(and_(TAGItem.active==0, TAGItem.latest==latest, TAGItem.__table__.c.tag_no.op('ilike')("%%%s%%" % str(kw["q"]).strip()))).all()
                result = list(set([v.tagNo for v in rs ]))
            data = "\n".join(["%s|%s" % (row, row)  for row in result])
            return data
        except:
            traceback.print_exc()

    def _query_result(self, kw):
        try:
            conditions = []
            latest = int(kw.get("latest", 0))
            if kw.get("poNo", False):
                poNo = kw["poNo"].strip()
                if ',' in poNo and '-' in poNo:
                    poNo_list = [str(p.strip()) for p in poNo.split(',') if str(p)]
                    tmp_list = []
                    for index, po in enumerate(poNo_list):
                        if '-' in po:
                            tmp_list += [str(i) for i in range(int(po.split('-')[0].strip()), int(po.split('-')[1].strip()) + 1)]
                            del poNo_list[index]

                    conditions.append(TAGItem.poNo.in_(poNo_list + tmp_list))
                elif ',' in poNo:
                    conditions.append(TAGItem.poNo.in_([str(p.strip()) for p in poNo.split(',') if str(p)]))
                elif '-' in poNo:
                    conditions.append(TAGItem.poNo.in_([str(i) for i in range(int(poNo.split('-')[0].strip()), int(poNo.split('-')[1].strip()) + 1)]))
                else:
                    conditions.append(TAGItem.__table__.c.po_no.op('ilike')("%%%s%%" % kw["poNo"].strip()))

#            if kw.get("upc", False):
#                conditions.append(TAGItem.__table__.c.upc.op('ilike')("%%%s%%"%kw["upc"]))
#
#            if kw.get("importDateStart", False) and kw.get("importDateEnd", False):
#                b_date=dt.strptime(kw.get("importDateStart", '2009-12-1200:00:00')+"00:00:00", "%Y-%m-%d%H:%M:%S")
#                e_date=dt.strptime(kw.get("importDateEnd", '2009-12-1200:00:00')+"23:59:59", "%Y-%m-%d%H:%M:%S")
#                conditions.append(TAGItem.importDate>=b_date)
#                conditions.append(TAGItem.importDate<=e_date)
#            elif kw.get("importDateStart", False):
#                b_date=dt.strptime(kw.get("importDateStart", '2009-12-1200:00:00')+"00:00:00", "%Y-%m-%d%H:%M:%S")
#                conditions.append(TAGItem.importDate>=b_date)
#            elif kw.get("importDateEnd", False):
#                e_date=dt.strptime(kw.get("importDateEnd", '2009-12-1200:00:00')+"23:59:59", "%Y-%m-%d%H:%M:%S")
#                conditions.append(TAGItem.importDate<=e_date)
#
            if kw.get("style", False):
                conditions.append(TAGItem.__table__.c.style.op('ilike')("%%%s%%" % kw["style"].strip()))
#
#            if kw.get("color", False):
#                conditions.append(TAGItem.__table__.c.color.op('ilike')("%%%s%%"%kw["color"]))
#
#            if kw.get("prepack", False):
#                conditions.append(TAGItem.__table__.c.prepack.op('ilike')("%%%s%%"%kw["prepack"]))
#
#            if kw.get("label", False):
#                conditions.append(TAGItem.__table__.c.label.op('ilike')("%%%s%%"%kw["label"]))

            if kw.get("brand", False):
                conditions.append(TAGItem.__table__.c.brand.op('ilike')("%%%s%%" % kw["brand"].strip()))

            if kw.get("soNo", False):
                conditions.append(TAGItem.__table__.c.so_no.op('ilike')("%%%s%%" % kw["soNo"].strip()))

            if kw.get("tagNo", False):
                conditions.append(TAGItem.__table__.c.tag_no.op('ilike')("%%%s%%" % kw["tagNo"].strip()))

            obj = DBSession.query(TAGItem.poNo, TAGItem.style, TAGItem.soNo, TAGItem.soRemark, TAGItem.tagNo, \
                                            func.sum(TAGItem.__table__.c.po_units), TAGItem.brand, TAGItem.attachmentSet, TAGItem.ediFile) \
                                                .filter(and_(TAGItem.active==0, TAGItem.latest==latest))
            if len(conditions):
                for value in conditions:
                    obj = obj.filter(value)
            return obj.group_by(TAGItem.poNo, TAGItem.style, TAGItem.soNo, TAGItem.soRemark, TAGItem.tagNo, TAGItem.brand, TAGItem.attachmentSet, TAGItem.ediFile) \
                            .order_by(desc(cast(TAGItem.poNo, Integer)))
        except:
            traceback.print_exc()

    def _returnList(self, data):
        if not isinstance(data, list):
            return list((data,))
        return data

    def _return_upper(self, s):
        if s:
            if "Charcoal Grey H".upper() == s.upper():
                return "Charcoal Grey Heather".upper()
            else:
                return s.upper()
        else:
            return s
