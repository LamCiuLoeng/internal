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
from tribal.widgets.tmw import *
# import transaction


class TMWController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    allow_only = authorize.not_anonymous()

    @expose('tribal.templates.tmw.index')
    @paginate('collections', items_per_page=80)
    @tabFocus(tab_type="main")
    def index(self, **kw):
        try:
            search_form = tmw_search_form
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
            fileDir = os.path.join(config.get("download_dir"), "TMW", dt.now().strftime("%Y%m%d"))
            if not os.path.exists(fileDir):
                os.makedirs(fileDir)
            dlzipFile = os.path.join(fileDir, "export_%s%d.zip" % (dt.now().strftime("%Y%m%d%H%M%S"), random.randint(1, 1000)))
            #xls_format = ['Flapdoodles_905', 'Flapdoodles_925', 'Flapdoodles_940', 'Flapdoodles', 'LittleMe']
            templatePath = os.path.join(config.get('template_dir'), "TMW_TEMPLATE.xls")
            copyTemplatePath = os.path.join(fileDir, "TMW_TEMPLATE_tmp_%s%d.xls" % (dt.now().strftime("%Y%m%d%H%M%S"), random.randint(1, 1000)))
            shutil.copyfile(templatePath, copyTemplatePath)
            rs = self._query_result(kw)
            data = []
            if rs:
                for item in rs:
                    appendData = []
                    appendData.append(item.filename)
                    for field in TMWItem.__table__.columns.keys()[1:-4]:
                        appendData.append(getattr(item, field, '') or '')
                    data.append(appendData)

                xls_file = self._generateExcel(data, copyTemplatePath, fileDir)
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

    def _generateExcel(self, data, copyTemplatePath, fileDir):
        filename = os.path.join(fileDir, "TMW-dat_%s.xls" % (dt.now().strftime("%Y%m%d%H%M%S")))

        tmw = TMWExcel(templatePath=copyTemplatePath, destinationPath=filename)
        try:
            tmw.inputData(data=data)
            tmw.outputData()
            return filename
        except:
            traceback.print_exc()
            if tmw:
                tmw.clearData()
            redirect("/tag/index")

    @expose()
    def getAjaxField(self, **kw):
        try:
            result = []
            fieldName = kw.get("fieldName", '')
            if fieldName == 'item_code':
                result = DBSession.query(distinct(TMWItem.item_code)).filter(and_(TMWItem.active == 0,
                  TMWItem.__table__.c.item_code.op('ilike')("%%%s%%" % str(kw["q"]).strip()))).all()
            elif fieldName == 'pofile_id':
                result = DBSession.query(distinct(TMWItem.pofile_id)).filter(and_(TMWItem.active == 0,
                  TMWItem.__table__.c.pofile_id.op('ilike')("%%%s%%" % str(kw["q"]).strip()))).all()
            elif fieldName == 'filename':
                result = DBSession.query(distinct(TMWItem.filename)).filter(and_(TMWItem.active == 0,
                  TMWItem.__table__.c.filename.op('ilike')("%%%s%%" % str(kw["q"]).strip()))).all()
            data = "\n".join(["%s|%s" % (row[0], row[0])  for row in result])
            return data
        except:
            traceback.print_exc()

    def _query_result(self, kw):
        try:
            conditions = []

            if kw.get("item_code", False):
                conditions.append(TMWItem.__table__.c.item_code.op('ilike')("%%%s%%" % kw["item_code"].strip()))

            if kw.get("pofile_id", False):
                conditions.append(TMWItem.__table__.c.pofile_id.op('ilike')("%%%s%%" % kw["pofile_id"].strip()))

            if kw.get("filename", False):
                conditions.append(TMWItem.__table__.c.filename.op('ilike')("%%%s%%" % kw["filename"].strip()))

            if kw.get('item_ids', False):
                conditions.append(TMWItem.id.in_([id for id in kw['item_ids'].split('|') if id]))

            obj = DBSession.query(TMWItem).filter(TMWItem.active == 0)
            if len(conditions):
                for value in conditions:
                    obj = obj.filter(value)
            return obj.order_by(desc(TMWItem.id))
        except:
            traceback.print_exc()

    def _returnList(self, data):
        if not isinstance(data, list):
            return list((data,))
        return data

    def _return_upper(self, s):
        if s:
            return s.upper()
        else:
            return s
