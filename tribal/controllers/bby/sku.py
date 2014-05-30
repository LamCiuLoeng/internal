# -*- coding: utf-8 -*-
import traceback, transaction, os, itertools
from datetime import datetime as dt
import logging
# turbogears imports
from tg import expose, redirect, validate, flash, config, jsonify
from tg.decorators import paginate

from repoze.what import predicates, authorize
from repoze.what.predicates import not_anonymous, in_group, has_permission
from sqlalchemy.sql import *

# project specific imports
from tribal.lib.base import BaseController
from tribal.model import *
from tribal.util.common import *
from tribal.util.bby_helper import *
from tribal.widgets.bby import *


__all__ = ["BBYSKUController"]


log = logging.getLogger(__name__)

class BBYSKUController(BaseController):

    allow_only = authorize.not_anonymous()

    @expose('tribal.templates.bby.sku.index')
    @paginate("result", items_per_page = 20)
    @tabFocus(tab_type = "main")
    def index(self, **kw):
        if kw:
            conditions = [BBYJobHeader.active == 0]
            if kw.get("sku", False) : conditions.append(BBYJobHeader.__table__.c.sku.op('ilike')("%%%s%%" % kw["sku"]))
            if kw.get("upc_no", False) : conditions.append(BBYJobHeader.__table__.c.upc_no.op('ilike')("%%%s%%" % kw["upc_no"]))
            if kw.get("brand_id", False) : conditions.append(BBYJobHeader.brand_id == kw["brand_id"])
            if kw.get("vendor_id", False) : conditions.append(BBYJobHeader.vendor_id == kw["vendor_id"])
            if kw.get("packaging_format_id", False) : conditions.append(BBYJobHeader.packaging_format_id == kw["packaging_format_id"])
            if kw.get("pd_id", False) : conditions.append(BBYJobHeader.pd_id == kw["pd_id"])
            if kw.get("ae_id", False) : conditions.append(BBYJobHeader.ae_id == kw["ae_id"])
            if kw.get("issue_date_from", False) : conditions.append(BBYJobHeader.create_time > kw["issue_date_from"])
            if kw.get("issue_date_to", False) : conditions.append(BBYJobHeader.create_time < kw["issue_date_to"])

            if kw.get("status", False):
                if kw["status"] == 'NEW' : conditions.append(BBYJobHeader.status < MOCKUP_NEW)
                if kw["status"] == 'SUBMIT' : conditions.extend([MOCKUP_NEW <= BBYJobHeader.status, BBYJobHeader.status < COMPLETED])
                if kw["status"] == 'COMPLETED' : conditions.append(BBYJobHeader.status >= COMPLETED)


            if 'pcr' in kw or 'pcr_date_from' in kw or 'pcr_date_to' in kw:
                conditions.extend([
                                   BBYJobHeader.id == BBYPCR.header_id,
                                   BBYPCR.active == 0,
                                   ])
                
                if kw.get('pcr',None): conditions.append(BBYPCR.no.op('ilike')('%%%s%%' %kw['pcr']))
                if kw.get('pcr_date_from',None): conditions.append(BBYPCR.receive_date >= kw["pcr_date_from"])
                if kw.get('pcr_date_to',None):   conditions.append(BBYPCR.receive_date <= kw["pcr_date_to"])

            result = DBSession.query(BBYJobHeader).filter(and_(*conditions)).all()
        else:
            result = DBSession.query(BBYJobHeader).filter(BBYJobHeader.active == 0).all()
            
        return {"result":result, "values":kw, "widget" : search_form,"todolist" : self._toDoList()}


    @expose('tribal.templates.bby.sku.view')
    @tabFocus(tab_type = "main")
    def view(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/sku/index")
        images = []
        check = lambda n : os.path.splitext(n)[1].lower() in ['.jpg', '.png', '.gif']
        for row in h.sku_info:
            if not row.row_detail : continue
            for item in row.row_detail:
                images.extend([f['file_id'] for f in item['files'] if check(f["file_name"])])
        images = map(lambda a: DBSession.query(UploadObject).get(a), images)
        return {"obj" : h , "images" : images}


    @expose('tribal.templates.bby.sku.add')
    @tabFocus(tab_type = "main")
    def add(self, **kw):
        return {"widget" : basic_form , "action" : "/sku/save_new", "values" : {}}


    @expose('tribal.templates.bby.sku.update')
    @tabFocus(tab_type = "main")
    def update(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/sku/index")
        return {"obj": h}


    def _filterAndSorted(self, prefix, kw):
        return sorted(filter(lambda (k, v): k.startswith(prefix), kw.iteritems()), cmp = lambda x, y:cmp(x[0], y[0]))


    @expose()
    def save_new(self, **kw):
        try:
            params = {}
            for f in ["sku", "upc_no", "product_description", "brand_id", "received_date", "ioq", "aoq","agent_id", "vendor_id",
                      "vendor_address", "packaging_format_id", "pd_id", "ae_id", "closure_id", "display_mode_id",
                      "formed_size_l", "formed_size_w", "formed_size_h","bby_asia_contact_id","bby_us_contact_id"] :
                if kw.get(f, False) or None: params[f] = kw[f]

            h = BBYJobHeader(**params)
            DBSession.add(h)
            DBSession.flush()

            for (rn, rv) in self._filterAndSorted("row_name_", kw):
                if not rv : continue
                info = []
                id = rn[rn.rindex("_") + 1:]
                dates = self._filterAndSorted("row_date_%s" % id, kw)
                remarks = self._filterAndSorted("row_remark_%s" % id, kw)
                for (daten, datev), (remarkn, remarkv), info_id in zip(dates, remarks, itertools.count()):
                    if not datev : continue
                    tmp = {"date" : datev or None, "remark" : remarkv or None, "id" : info_id}
                    file_name = daten.replace("row_date", "row_file_name")
                    file_path = daten.replace("row_date", "row_file_path")
                    (flag, result) = sysUpload([kw.get(file_path, None)], [kw.get(file_name, None)], return_obj = True)
                    fs = filter(bool, result)
                    if fs :
                        tmp["files"] = [{"file_id":fs[0].id, "file_name":fs[0].file_name}]
                    else:
                        tmp["files"] = []

                    confirm = daten.replace("row_date", "row_confirm")
                    tmp["confirm"] = "Y" if kw.get(confirm, False) else None
                    info.append(tmp)

                record = BBYSKUInfo(header = h, row_name = rv, row_detail = info)
                DBSession.add(record)
            link = "/sku/view?id=%d" % h.id
            flash("Save the record successfully!")
            DBSession.add(BBYLog(job_id = h.id, action_type = "Create", remark = "New SKU"))
        except Exception, e:
            log.exception(str(e))
            transaction.doom()
            flash("Error when create the new record!")
            link = "index"
        redirect(link)

    @expose()
    def save_update(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/sku/index")

        def _mak(obj, attr, new_value):
            try:
                old_value = getattr(obj, attr)
                if  old_value != new_value :
                    attr_name = obj.__table__._columns.get(attr).info["field_name"]
                    return (attr_name, old_value, new_value)
                return None
            except Exception, e:
                log.exception(str(e))
                return None

        try:
            m = lambda n : kw.get(n, "") or None
            log = []

            for f in ["sku", "upc_no", "product_description", "brand_id", "received_date", "ioq", "aoq","agent_id", "vendor_id",
                      "vendor_address", "packaging_format_id", "pd_id", "ae_id", "closure_id", "display_mode_id",
                      "formed_size_l", "formed_size_w", "formed_size_h","bby_asia_contact_id","bby_us_contact_id"] :
                if f in kw :
                    setattr(h, f, m(f))

            def _split(l1, l2):
                new = [item for item in l2 if item not in l1]
                delete = [item for item in l1 if item not in l2]
                update = [item for item in l1 if item in l2]
                return (new, delete, update)

            old_row_ids = [str(r.id) for r in h.sku_info]
            new_row_ids = [name[name.rindex("_") + 1:] for name, value in self._filterAndSorted("row_name_", kw)]
            new_rows, delete_rows, update_rows = _split(old_row_ids, new_row_ids)

            #handle the delete
            for id in delete_rows:
                dbobj = DBSession.query(BBYSKUInfo).get(id)
                dbobj.active = 1
                log.append("Delete line '%s'." % dbobj.row_name)

            #handle the new
            for id in new_rows:
                if not kw["row_name_%s" % id] : continue
                row_name = kw["row_name_%s" % id]
                row_dates = self._filterAndSorted("row_date_%s" % id, kw)
                row_remarks = self._filterAndSorted("row_remark_%s" % id, kw)
                info = []
                for (dname, dvalue), (rname, rvalue), index in zip(row_dates, row_remarks, itertools.count()):
                    if not dvalue : continue
                    tmp = {"id":index, "date" : dvalue, "remark" : rvalue or None }

                    file_name = dname.replace("row_date", "row_file_name")
                    file_path = dname.replace("row_date", "row_file_path")
                    (flag, result) = sysUpload([kw.get(file_path, None)], [kw.get(file_name, None)], return_obj = True)
                    fs = filter(bool, result)
                    if fs :
                        tmp["files"] = [{"file_id":fs[0].id, "file_name":fs[0].file_name}]
                    else:
                        tmp["files"] = []

                    confirm = dname.replace("row_date", "row_confirm")
                    tmp["confirm"] = "Y" if kw.get(confirm, False) else None
                    info.append(tmp)
                DBSession.add(BBYSKUInfo(header = h, row_name = row_name, row_detail = info))
                log.append("Add line '%s'." % row_name)

            #handle update
            for id in update_rows:
                row = DBSession.query(BBYSKUInfo).get(id)
                row.row_name = kw["row_name_%s" % id]

                info = row.row_detail or []
                next_id = info[-1]['id'] + 1 if info else 0

                old_detail_ids = [str(detail["id"]) for detail in row.row_detail]
                new_detail_ids = [dname[dname.rindex("_") + 1:] for (dname, dvalue) in self._filterAndSorted("row_date_%s_" % id, kw)]

                new_details, delete_details, update_details = _split(old_detail_ids, new_detail_ids)

                #handle delete detail 
                info = filter(lambda item:str(item['id']) not in delete_details, info)
                #handle new detail

                for did in new_details:
                    if not kw["row_date_%s_%s" % (id, did)] : continue
                    tmp = {
                           "id" : next_id,
                           "date" : kw["row_date_%s_%s" % (id, did)],
                           "remark" : kw["row_remark_%s_%s" % (id, did)] or None
                           }

                    (flag, result) = sysUpload([kw["row_file_path_%s_%s" % (id, did)], ], [kw["row_file_name_%s_%s" % (id, did)], ], return_obj = True)
                    fs = filter(bool, result)
                    if fs :
                        tmp["files"] = [{"file_id":fs[0].id, "file_name":fs[0].file_name}]
                    else:
                        tmp["files"] = []
                    tmp["confirm"] = kw.get("row_confirm_%s_%s" % (id, did), None) or None
                    info.append(tmp)
                    next_id += 1



                #handle update detail
                for index, did in enumerate(update_details):
                    for obj in info:
                        if str(obj["id"]) == did:
                            item = obj
                            location = index
                            break
                    else:
                        continue

                    if not kw["row_date_%s_%s" % (id, did)] :
                        info.pop(location)                       
                        continue

                    item['date'] = kw["row_date_%s_%s" % (id, did)]
                    item['remark'] = kw["row_remark_%s_%s" % (id, did)] or None
                    item["confirm"] = kw.get("row_confirm_%s_%s" % (id, did), None) or None
                    (flag, result) = sysUpload([kw["row_file_path_%s_%s" % (id, did)], ], [kw["row_file_name_%s_%s" % (id, did)], ], return_obj = True)
                    fs = filter(bool, result)
                    if fs : item["files"].append({"file_id":fs[0].id, "file_name":fs[0].file_name})

                    info.pop(location)
                    info.insert(location, item)
                row.row_detail = None
                row.row_detail = info

            if log : DBSession.add(BBYLog(job_id = h.id, action_type = "UPDATE", remark = "[New SKU] " + " ".join(log)))
            flash("Update the record successfully!")
        except Exception, e:
            log.exception(str(e))
            transaction.doom()
            flash("Error when update the record!")
        redirect("/sku/view?id=%d" % h.id)

    @expose()
    def submit(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/sku/index")
        try:
            h.status = MOCKUP_NEW
            DBSession.add(BBYLog(job_id = h.id, action_type = "SUBMIT", remark = "[New SKU] %s submit the record." % request.identity["user"]))
            flash("Submit the record successfully!")
        except Exception, e:
            log.exception(str(e))
            transaction.doom()
            flash("Error when submit the record!")
        redirect("index")


    @expose()
    def action(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/sku/index")

        map = {
               'CANCEL' : (CANCEL, 'cancel'),
               'ON_HOLD' : (ON_HOLD, 'hold'),
               'ACTIVE' : (ACTIVE, 'active'),
               'UNLOCK' : (ACTIVE, 'unlock')
               }

        if kw.get("t", None) not in map:
            flash("No such action type for this record!")
            redirect("/sku/view?id=%s" % kw["id"])

        try:
            new_status, verb = map[kw['t']]
            h.control_flag = new_status
            DBSession.add(BBYLog(job_id = h.id, action_type = "SUBMIT", remark = "[New SKU] %s %s the record." % (request.identity["user"], verb)))
            flash("Update the record successfully!")
        except Exception, e:
            log.exception(str(e))
            transaction.doom()
            flash("Error when submit the record!")
        redirect("/sku/view?id=%s" % kw["id"])



    @expose('tribal.templates.bby.sku.history')
    @tabFocus(tab_type = "main")
    def history(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/sku/index")

        hs = DBSession.query(BBYLog).filter(BBYLog.active == 0).filter(BBYLog.job_id == h.id).order_by(desc(BBYLog.create_time)).all()
        return {"header" : h, "history" : hs}


    @expose()
    def download(self, **kw):
        try:
            obj = DBSession.query(UploadObject).get(kw["id"])
            return serveFile(os.path.join(config.download_dir, obj.file_path))
        except Exception, e:
            log.exception(str(e))
            flash("No such file!")
            redirect("/index")


    @expose("json")
    def ajaxDeleteFile(self, **kw):
        try:
            obj = DBSession.query(BBYSKUInfo).get(kw["row_id"])

            info = obj.row_detail
            for detail in info:
                if str(detail["id"]) == kw["detail_id"]:
                    for f in detail["files"]:
                        if str(f["file_id"]) == kw["file_id"]:
                            detail["files"].remove(f)
                            break
                    break
            obj.row_detail = info

            f = DBSession.query(UploadObject).get(kw["file_id"])
            content = "[New SKU] %s delete file [ID : %s ,File Name : %s,Upload By : %s ,Upload Time : %s]." % (request.identity["user"], kw["file_id"], f.file_name, f.upload_by, f.create_time)
            DBSession.add(BBYLog(job_id = obj.header_id, action_type = "UPDATE", remark = content))
            return {"result" : "0"}
        except Exception, e:
            log.exception(str(e))
            transaction.doom()
            return {"result" : "1"}
        
        
    def _toDoList(self,**kw):
        new_conditions = [BBYJobHeader.active == 0,BBYJobHeader.status < MOCKUP_NEW,BBYJobHeader.control_flag == 0]
        new_result = DBSession.query(BBYJobHeader).filter(and_(*new_conditions))
        new_result_count = new_result.count()
        
        onhold_conditions = [BBYJobHeader.active == 0,BBYJobHeader.control_flag == ON_HOLD]
        onhold_result = DBSession.query(BBYJobHeader).filter(and_(*onhold_conditions))
        onhold_result_count = onhold_result.count()
        
        cancel_conditions = [BBYJobHeader.active == 0,BBYJobHeader.control_flag == CANCEL]
        cancel_result = DBSession.query(BBYJobHeader).filter(and_(*cancel_conditions))
        cancel_result_count = cancel_result.count()
        
#        if kw.get("all",None):
#            new_result = new_result.all()
#            onhold_result = onhold_result.all()
#            cancel_result = cancel_result.all()
#        else:
#            qty = int(kw.get("qty",5))
#            new_result = new_result[:qty]
#            onhold_result = onhold_result[:qty]
#            cancel_result = cancel_result[:qty]
            
            
        new_result = new_result.all()
        onhold_result = onhold_result.all()
        cancel_result = cancel_result.all()    
            
            
        return {
                "new" : new_result,
                "new_count" : new_result_count,
                "cancel" : cancel_result,
                "cancel_count" : cancel_result_count,
                "onhold" : onhold_result,
                "onhold_count" : onhold_result_count,
                }
        
    @expose()   
    def copy(self,**kw):
        h = getOr404(BBYJobHeader, kw.get("id",None), "index", "The record doesn't exist!")
        fields = ["upc_no","product_description","brand_id","ioq","aoq","agent_id","vendor_id","packaging_format_id","pd_id",
                  "ae_id","closure_id","display_mode_id","formed_size_l","formed_size_w","formed_size_h"]
        params = {"status" : SKU_NEW,"sku" : "%s(copied)" %h.sku}
        for f in fields : params[f] = getattr(h, f)
        nh = BBYJobHeader(**params)
        DBSession.add(nh)
        DBSession.flush()
        
        #add the detail record
        for info in h.sku_info:
            tmp = BBYSKUInfo(header_id=nh.id,row_name=info.row_name,row_detail=info.row_detail)
            DBSession.add(tmp)
            
        DBSession.add(BBYLog(job_id = nh.id, action_type = "Copy", remark = "Copy new SKU form record[id : %s]." %h.id))
        flash("Copy the record successfully! Here are the new record's detail.")
        redirect("/sku/view?id=%d" %nh.id)
        
        
    @expose("json")
    def getVendorByAgent(self,**kw):
        agent_id = kw.get("agent_id",None)
        try:
            if not agent_id :
                vendors = DBSession.query(BBYVendor).filter(BBYVendor.active==0).order_by(BBYVendor.name).all()
            else:
                agent = DBSession.query(BBYAgent).get(agent_id)
                vendors = agent.vendors
            
            return {
                    "flag" : 0,
                    "vendors" : [(v.id,str(v)) for v in vendors],
                    }
        except Exception, e:
            log.exception(str(e))
            return {
                    "flag" : 1 ,
                    "vendors" : []
                    }
    
    @expose()
    def delete(self,**kw):
        h = getOr404(BBYJobHeader, kw["id"], "/sku/index")
        h.active = 1
        DBSession.add(BBYLog(job_id = h.id, action_type = "Delete", remark = "Delete record[id : %s]." %h.id))
        flash("Delete the record successfully!")
        return redirect("/sku/index")
    
    
    @expose('tribal.templates.bby.sku.pcr')
    @tabFocus(tab_type = "main")
    def pcr(self,**kw):
        h = getOr404(BBYJobHeader, kw.get("id",None), "index", "The record doesn't exist!")
        
        if kw.get('no',None):
            result = sysUpload(attachment_list=kw['file_info'],return_obj=True)
            for obj in result[1]:
                DBSession.add(BBYPCR(
                                     header_id = h.id,
                                     no = kw.get('no',None),
                                     file_name = obj.file_name,
                                     file_id = obj.id,
                                     receive_date = kw.get('receive_date',None)
                                         ))
            flash("Add the file successfully!")
        return {'obj' : h}
        
        
    @expose("json")
    def ajax_delete_pcr(self,**kw):
        if not kw.get('id',None):
            return {'result' : 1 , 'msg' : 'No ID supplied!'}
        
        try:
            obj = DBSession.query(BBYPCR).get(kw['id'])
            obj.active = 1
            DBSession.add(BBYLog(job_id = obj.header_id, action_type = "Delete", remark = "Delete PCR [NO:%s,FILE NAME:%s]" %(obj.no,obj.file_name)))
            return {'result' : 0 , 'msg' : 'Delete the record successfully!'}
        except:
            return {'result' : 1 , 'msg' : 'Server error occur!'}
        