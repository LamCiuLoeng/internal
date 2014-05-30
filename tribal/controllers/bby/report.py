# -*- coding: utf-8 -*-
import traceback, transaction, os, itertools, random, shutil
from datetime import datetime as dt
import logging
# turbogears imports
from tg import expose, redirect, validate, flash, config
from tg.decorators import paginate

from repoze.what import predicates, authorize
from repoze.what.predicates import not_anonymous, in_group, has_permission
from sqlalchemy.sql import *

# project specific imports
from tribal.lib.base import BaseController
from tribal.model import *
from tribal.util.common import *
from tribal.util.excel_helper import *
from tribal.util.bby_helper import *
from tribal.widgets.bby import *

__all__ = ["BBYReportController"]


log = logging.getLogger(__name__)

class BBYReportController(BaseController):

    allow_only = authorize.not_anonymous()

    @expose('tribal.templates.bby.report')
    @tabFocus(tab_type = "report")
    def index(self, **kw):
        return {"widget":report_form}


    @expose()
    def save_customer_item(self, **kw):
        u = getOr404(DBACustomer, kw["id"])

        if not kw["igs"] : u.items = []
        else : u.items = DBSession.query(DBAItem).filter(DBAItem.id.in_(kw["igs"].split("|"))).all()
        flash("Save the update successfully!")
        redirect("/dba/customer_item")

    #===========================================================================
    # add by cl
    #===========================================================================
    @expose("tribal.templates.bby.report")
    @tabFocus(tab_type = "report")
    def report(self, **kw):
        return {"widget":report_form,
                "action" : "/bbyreport/export",
                "current_url" : "/bbyreport/report",
                "current_nav" : "BBY Report"}

    @expose()
    def export(self, **kw):
        try:
            current = dt.now()
            dateStr = current.strftime("%Y%m%d")
            fileDir = os.path.join(config.get("download_dir"), "BBY", dateStr)
            if not os.path.exists(fileDir): os.makedirs(fileDir)
            templatePath = os.path.join(config.get("template_dir"), "BBY_REPORT_TEMPLATE.xls")
            tempFileName = os.path.join(fileDir, "bby_report_tmp_%s_%d.xls" % (current.strftime("%Y%m%d%H%M%S"), random.randint(0, 1000)))
            realFileName = os.path.join(fileDir, "bby_report_%s.xls" % (dt.now().strftime("%Y%m%d%H%M%S")))
            shutil.copy(templatePath, tempFileName)
            bby_report_xls = BBYREPORTExcel(templatePath = tempFileName, destinationPath = realFileName)
            data = []
            max_testings_len = 0
            max_casepack_len = 0
            status_dict = {10:'SKU_NEW', 20:'MOCKUP_NEW', 21:'MOCKUP_SENT', 30:'CASEPACK_NEW', 31:'CASEPACK_SENT', 40:'COMPLETED'}
            if kw:
                jobs = self._query_result(kw)
                for job in jobs:
                    for option in job.options:
                        tmp_data = {}
                        tmp_data['sku'] = job.sku
                        tmp_data['vendor'] = job.vendor.name if job.vendor else ''
                        tmp_data['testings'] = []
                        tmp_data['casepacks'] = []
                        tmp_data['status'] = status_dict.get(job.status, '')
                        tmp_data['option'] = option.name
                                              
                        grouped_info = DBSession.query(func.max(BBYVendorFitting.send_date),func.max(BBYVendorFitting.reported_date))\
                            .filter(and_(BBYVendorFitting.option_id==option.id,BBYVendorFitting.active==0)).\
                            group_by(BBYVendorFitting.option_id,BBYVendorFitting.round).\
                            order_by(BBYVendorFitting.round).all()
                        
                        if len(grouped_info) > max_testings_len : max_testings_len = len(grouped_info)
                        for info in grouped_info:
                            t_tmp = {}
                            t_tmp['express_date'] = info[0] or ''
                            t_tmp['feedback_date'] = info[1] or ''
                            tmp_data['testings'].append(t_tmp)
                            del t_tmp
                           
                        if option.final:
                            casepacks = job.results
                            if casepacks:
                                if len(casepacks) > max_casepack_len: max_casepack_len = len(casepacks)
                                for c in casepacks:
                                    c_tmp = {}
                                    c_tmp['express_date'] = c.send_out_date if c.send_out_date else ''
                                    c_tmp['feedback_date'] = c.reported_date if c.reported_date else ''
                                    tmp_data['casepacks'].append(c_tmp)
                                    del c_tmp
                        data.append(tmp_data)
            bby_report_xls.inputData(max_testings_len = max_testings_len, max_casepack_len = max_casepack_len, data = data)
            bby_report_xls.outputData()
            try:
                os.remove(tempFileName)
            except:
                pass
            return serveFile(unicode(realFileName))

        except Exception, e:
            log.exception(str(e))
            flash("Export Fail.")
            redirect("/bbyreport/index")


    def _query_result(self, kw):
        try:
            conditions = []
            if kw.get("sku", False) : conditions.append(BBYJobHeader.__table__.c.sku.op('ilike')("%%%s%%" % kw["sku"]))
            if kw.get("brand_id", False) : conditions.append(BBYJobHeader.brand_id == kw["brand_id"])
            if kw.get("vendor_id", False) : conditions.append(BBYJobHeader.vendor_id == kw["vendor_id"])
            if kw.get("packaging_format_id", False) : conditions.append(BBYJobHeader.packaging_format_id == kw["packaging_format_id"])
            if kw.get("pd_id", False) : conditions.append(BBYJobHeader.pd_id == kw["pd_id"])
            if kw.get("ae_id", False) : conditions.append(BBYJobHeader.ae_id == kw["ae_id"])
            if kw.get("issue_date_from", False) : conditions.append(BBYJobHeader.create_time > kw["issue_date_from"])
            if kw.get("issue_date_to", False) : conditions.append(BBYJobHeader.create_time < kw["issue_date_to"])

            if kw.get("status", False):
                if kw["status"] == 'NEW' : conditions.append(BBYJobHeader.status < 20)
                if kw["status"] == 'SUBMIT' : conditions.extend([20 <= BBYJobHeader.status, BBYJobHeader.status < 40])
                if kw["status"] == 'COMPLETED' : conditions.append(BBYJobHeader.status >= 40)

            if kw.get("factory_id", False) : conditions.append(BBYComponent.factory_id == kw["factory_id"])
            if kw.get("material_id", False) : conditions.append(BBYComponent.material_id == kw["material_id"])

            if kw.get("factory_id", False) or kw.get("material_id", False):
                obj = DBSession.query(BBYJobHeader).join(BBYOption, BBYComponent).filter(BBYJobHeader.active == 0)
            else:
                obj = DBSession.query(BBYJobHeader).filter(BBYJobHeader.active == 0)
            if len(conditions):
                for condition in conditions: obj = obj.filter(condition)

            return obj.order_by(BBYJobHeader.id).all()
        except Exception, e:
            log.exception(str(e))
            
            
    @expose("tribal.templates.bby.report")
    @tabFocus(tab_type = "report")
    def raw_report(self, **kw):
        return {"widget":report_form,
                "action" : "/bbyreport/raw_report_export",
                "current_url" : "/bbyreport/raw_report",
                "current_nav" : "BBY Raw Report"
                }
        
    @expose()
    def raw_report_export(self,**kw):
        current = dt.now()
        dateStr = current.strftime("%Y%m%d")
        fileDir = os.path.join(config.get("download_dir"), "BBY", dateStr)
        if not os.path.exists(fileDir): os.makedirs(fileDir)
        templatePath = os.path.join(config.get("template_dir"), "BBY_RAW_REPORT_TEMPLATE.xls")
        tempFileName = os.path.join(fileDir, "bby_raw_report_tmp_%s_%d.xls" % (current.strftime("%Y%m%d%H%M%S"), random.randint(0, 1000)))
        realFileName = os.path.join(fileDir, "bby_raw_report_%s.xls" % (dt.now().strftime("%Y%m%d%H%M%S")))
        shutil.copy(templatePath, tempFileName)
        bby_report_xls = BBYRawReportExcel(templatePath = tempFileName, destinationPath = realFileName)

        data = []
        max_component_count = 0
        max_fitting_round = 0
        max_casepack_round = 0
        component_header = ["Material","Spec","Front Color","Back Color","Supplier"]
        fitting_header = ["Sent out Date","Feedback Date","P/F","Reasons for Failure"]
        casepack_header = ["Sent out Date","Feedback Date","P/F","Reasons for Failure"]
                
        for job in self._query_result(kw):
            pdo = {
                   "base_info" : map(lambda v : v or '',[job.sku,job.pd,job.ae,Date2Text(job.create_time),'',job.brand,job.vendor,job.packaging_format,job.ioq,job.aoq,job.product_description]),
                   "sku_info" : [],
                   "other_sku_info" : [],
                   "options" : [],
                   "option_index" : 4,
                   }
            
            sku_info = {}
            for d in DBSession.query(BBYSKUInfo).filter(and_(BBYSKUInfo.active==0,BBYSKUInfo.header_id==job.id)):
                sku_info[d.row_name] = d.row_detail
            
            for name in ["PIF","Product Sample Photo","3D Drawing","Die Line"]:
                if name not in sku_info or not sku_info[name]: 
                    pdo["sku_info"].extend(["",""])
                    continue
                
                b = sorted(sku_info[name],cmp=lambda v1,v2:cmp(v1["date"],v2["date"]))
                pdo["sku_info"].append(b[0]["date"])
                a = filter(lambda d : bool(d['confirm']),b)
                if a : pdo["sku_info"].append(a[0]["date"])
                else: pdo["sku_info"].append("")

            #to be complete
            for name in ["Fit Waiver","Test Waiver","LOI"]:
                if sku_info.get(name,None) : 
                    d = sorted(sku_info[name],key=lambda v:v['date'])[0]['date']
                    pdo["other_sku_info"].append(d)
                else:
                    pdo["other_sku_info"].append("")
            pdo["other_sku_info"].extend([job.formed_size_l,job.formed_size_w,job.formed_size_h])


            for option in job.options:
                option_pdo = {
                              "name" : option.name,
                              "components" : [],
                              "fittings" : [],
                              "casepack" : [],
                              }
                for c in option.components:
                    fs = DBSession.query(BBYVendorFitting).filter(and_(BBYVendorFitting.active==0,
                                                                  BBYVendorFitting.option_id==option.id,BBYVendorFitting.component_id==c.id)).order_by(desc(BBYVendorFitting.round))
                    
                    if fs.count() < 1 :
                        option_pdo['components'].append([c.material,c.coating,c.front_color,c.back_color,''])
                    else:
                        option_pdo['components'].append([c.material,c.coating,c.front_color,c.back_color,fs[0].source])
                    
                if max_component_count < len(option.components) : max_component_count = len(option.components)
        
                current_round = None
                tmp = []
                _t = lambda v : [Date2Text(v[0]),Date2Text(v[1]),'' if v[2]=='B' else v[2], v[3]]
                for fitting in DBSession.query(BBYVendorFitting).filter(and_(BBYVendorFitting.active==0,
                                                                             BBYVendorFitting.option_id==option.id)).order_by(BBYVendorFitting.round):
                    if current_round == fitting.round:
                        if fitting.send_date and (not tmp[0] or fitting.send_date) < tmp[0] : tmp[0] = fitting.send_date
                        if fitting.reported_date and (not tmp[1] or fitting.reported_date > tmp[1]) : tmp[1] = fitting.reported_date
                        if fitting.remark : tmp[3] = tmp[3] + "\n" + fitting.remark if tmp[3] else fitting.remark
                        if tmp[2]=='P' : tmp[2] = ['F','P'][fitting.confirm=='YES'] if fitting.reported_date else 'B'                    
                        continue
                    elif current_round is not None and current_round != fitting.round:
                        option_pdo['fittings'].append(_t(tmp))
                         
                    current_round = fitting.round
                    flag = ['F','P'][fitting.confirm=='YES'] if fitting.reported_date else 'B'
                    tmp = [fitting.send_date,fitting.reported_date,flag,fitting.remark]
                    
                if tmp : option_pdo['fittings'].append(_t(tmp))
                if max_fitting_round < len(option_pdo['fittings']) : max_fitting_round = len(option_pdo['fittings'])                
                if option.final == 'YES' :
                    for c in job.results:
                        option_pdo['casepack'].append([Date2Text(c.send_out_date),Date2Text(c.reported_date),['F','P'][c.result=='PASS'] if c.result else '',c.reason])
                    if max_casepack_round < len(job.results) : max_casepack_round = len(job.results)
            
                pdo['options'].append(option_pdo)
            data.append(pdo)
            
        #generate the excel
        excel_data = self._flatRows(data,len(component_header),max_component_count,
                                    len(fitting_header),max_fitting_round,len(casepack_header),max_casepack_round)
        bby_report_xls.inputData(excel_data,component_header,max_component_count,
                                 fitting_header,max_fitting_round,casepack_header,max_casepack_round)
        bby_report_xls.outputData()
        return serveFile(unicode(realFileName))
        
        
    def _flatRows(self,data,compoent_unit,max_component_count,fitting_unit,max_fitting_round,casepack_unit,max_casepack_round):
        _blank = lambda l : map(lambda v:v or '',l)
        rows = []
        for d in data:
            header=[]
            header.extend(d['base_info'])
            header.extend(d['sku_info'])
            header.extend(d['other_sku_info'])
            
            if not d['options']:
                rows.append(map(lambda s:unicode(s),_blank(header+['']*(compoent_unit*max_component_count+fitting_unit*max_fitting_round+casepack_unit*max_casepack_round))))
                continue
                
            for o in d['options']:
                tmp_header = header
                tmp_header[d['option_index']] = o['name']
                if max_component_count > 0 :
                    tmp_compoent = o['components']
                    tmp_compoent.extend(([ [''] * compoent_unit ] * max_component_count))
                    tmp_compoent = reduce(lambda x,y:x+y,tmp_compoent[:max_component_count])
                else: tmp_compoent = []
          
                if max_fitting_round > 0:
                    tmp_fitting = o['fittings']
                    tmp_fitting.extend(([[''] * fitting_unit] * max_fitting_round))
                    tmp_fitting = reduce(lambda x,y:x+y,tmp_fitting[:max_fitting_round])
                else: tmp_fitting = []
                
                if max_casepack_round > 0:
                    tmp_casepack = o['casepack']
                    tmp_casepack.extend(([['']*casepack_unit] * max_casepack_round))
                    tmp_casepack = reduce(lambda x,y:x+y,tmp_casepack[:max_casepack_round])
                else: tmp_casepack = []
                
                rows.append(map(lambda s:unicode(s),_blank((tmp_header + tmp_compoent + tmp_fitting + tmp_casepack))))
        return rows
                
