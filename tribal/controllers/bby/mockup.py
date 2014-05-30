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
from sqlalchemy.orm.exc import *

# project specific imports
from tribal.lib.base import BaseController
from tribal.model import *
from tribal.model.bby import *
from tribal.util.common import *
from tribal.util.bby_helper import *
from tribal.util.http_util import get_post_response
from tribal.util.date_util import format_today
from tribal.util.excel_helper import *
from tribal.widgets.bby import *
from _abcoll import Set


log = logging.getLogger(__name__)

class BBYMockupController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    allow_only = authorize.not_anonymous()

    @expose('tribal.templates.bby.mockup.index')
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
                if kw["status"] == 'NEW' : conditions.extend([MOCKUP_NEW == BBYJobHeader.status])
                elif kw["status"] == 'SENT' : conditions.extend([BBYJobHeader.status == MOCKUP_SENT])
                elif kw["status"] == 'CONFIRMED' : conditions.extend([BBYJobHeader.status > MOCKUP_SENT])
                elif kw["status"] == 'COMPLETED' : conditions.append(BBYJobHeader.status >= COMPLETED)
            else:
                conditions.append(BBYJobHeader.status >= MOCKUP_NEW)

            result = DBSession.query(BBYJobHeader).filter(and_(*conditions)).all()
        else:
            result = DBSession.query(BBYJobHeader).filter(BBYJobHeader.active == 0).filter(BBYJobHeader.status >= MOCKUP_NEW).all()
        return {"result":result, "values":kw, "widget" : mockup_search_form,"todolist" : self._toDoList()}


    @expose('tribal.templates.bby.mockup.item_view')
    @tabFocus(tab_type = "main")
    def item_view(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/bbymockup/index")
        return {"header" : h , "widget" : basic_info_widget, "values" : h.basic_info_populate(), "options" : h.options}



    @expose('tribal.templates.bby.mockup.item_edit')
    @tabFocus(tab_type = "main")
    def item_edit(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/bbymockup/index")
        return {"header" : h , "widget" : basic_info_widget, "values" : h.basic_info_populate(), "options" : h.options}


    def _filterAndSorted(self, prefix, kw):
        return sorted([(kk, vv or None) for (kk, vv) in filter(lambda (k, v): k.startswith(prefix), kw.iteritems())], cmp = lambda x, y:cmp(x[0], y[0]))

    def _split(self, l1, l2):
            new = [item for item in l2 if item not in l1]
            delete = [item for item in l1 if item not in l2]
            update = [item for item in l1 if item in l2]
            return (new, delete, update)

    @expose()
    def save_item_edit(self, **kw):
        h = getOr404(BBYJobHeader, kw["header_id"], "/bbymockup/index")

        _f = lambda n : kw.get(n, None) or None
        log = []
        try:
            old_row_ids = [str(r.id) for r in h.options]
            new_row_ids = [name[name.rindex("_") + 1:] for name, value in self._filterAndSorted("o_name_", kw)]
            new_rows, delete_rows, update_rows = self._split(old_row_ids, new_row_ids)

            #handle the delete
            for id in delete_rows :
                dbobj = DBSession.query(BBYOption).get(id)
                dbobj.active = 1
                log.append("Delete option '%s'." % dbobj.name)

            #handle the new
            for id in new_rows:
                name = _f("o_name_%s" % id)
                if not name : continue
                option = BBYOption(header = h, name = name, final = _f("o_final_%s" % id))
                DBSession.add(option)

                components = self._filterAndSorted("c_format_id_%s_" % id, kw)
                materials = self._filterAndSorted("c_material_id_%s_" % id, kw)
                coatings = self._filterAndSorted("c_coating_id_%s_" % id, kw)
                fronts = self._filterAndSorted("c_front_color_id_%s_" % id, kw)
                backs = self._filterAndSorted("c_back_color_id_%s_" % id, kw)
                sizes_l = self._filterAndSorted("c_finished_size_l_%s_" % id, kw)
                sizes_w = self._filterAndSorted("c_finished_size_w_%s_" % id, kw)
                sizes_h = self._filterAndSorted("c_finished_size_h_%s_" % id, kw)
                closures = self._filterAndSorted("c_closure_id_%s_" % id, kw)
                modes = self._filterAndSorted("c_display_mode_id_%s_" % id, kw)
                remarks = self._filterAndSorted("c_remark_%s_" % id, kw)


                for (cname, cval), (mname, mval), (ccname, ccval), (fname, fval), (bname, bval), \
                    (slname, slval), (swname, swval), (shname, shval), (cccname, cccval), (mmname, mmval), (rname, rval) in \
                    zip(components, materials, coatings, fronts, backs, sizes_l, sizes_w, sizes_h, closures, modes, remarks):
    #                if not any([cval, mval, ccval, fval, bval, sval, cccval, mmval, rval]) : continue

                    print "_^" * 30
                    print cval
                    print "_*" * 30

                    if not cval : continue

                    component = BBYComponent(option = option, format_id = cval or None, material_id = mval or None, coating_id = ccval or None,
                                             front_color_id = fval or None, back_color_id = bval or None, finished_size_l = slval or None,
                                             finished_size_w = swval or None, finished_size_h = shval or None,
                                             closure_id = cccval or None, display_mode_id = mmval or None, remark = rval or None)
                    DBSession.add(component)
                log.append("Add option '%s'." % option.name)

            #handle update
            for id in update_rows:
                print "_^" * 30
                print "come into update"
                print "_*" * 30


                option = DBSession.query(BBYOption).get(id)
                option.name = kw["o_name_%s" % id].strip()
                option.final = kw.get("o_final_%s" % id, None) or None

                old_component_ids = [str(c.id) for c in option.components]
                new_components_ids = [cname[cname.rindex("_") + 1:] for cname, cval in self._filterAndSorted("c_format_id_%s_" % id, kw)]
                new_ids, delete_ids, update_ids = self._split(old_component_ids, new_components_ids)

                #handle the delete component
                for cid in delete_ids : DBSession.query(BBYComponent).get(cid).active = 1

                #handle the new component
                for cid in new_ids:
                    if not _f("c_material_id_%s_%s" % (id, cid)) : continue

                    DBSession.add(BBYComponent(option = option,
                                 format_id = _f("c_format_id_%s_%s" % (id, cid)),
                                 material_id = _f("c_material_id_%s_%s" % (id, cid)),
                                 coating_id = _f("c_coating_id_%s_%s" % (id, cid)),
                                 front_color_id = _f("c_front_color_id_%s_%s" % (id, cid)),
                                 back_color_id = _f("c_back_color_id_%s_%s" % (id, cid)),
                                 finished_size_l = _f("c_finished_size_l_%s_%s" % (id, cid)),
                                 finished_size_w = _f("c_finished_size_w_%s_%s" % (id, cid)),
                                 finished_size_h = _f("c_finished_size_h_%s_%s" % (id, cid)),
                                 closure_id = _f("c_closure_id_%s_%s" % (id, cid)),
                                 display_mode_id = _f("c_display_mode_id_%s_%s" % (id, cid)),
                                 remark = _f("c_remark_%s_%s" % (id, cid)),
                                 ))
                    print "_^" * 30
                    print "come into update's new"
                    print "_*" * 30

                #handle the update component
                for cid in update_ids:
                    component = DBSession.query(BBYComponent).get(cid)
                    component.format_id = _f("c_format_id_%s_%s" % (id, cid))
                    component.material_id = _f("c_material_id_%s_%s" % (id, cid))
                    component.coating_id = _f("c_coating_id_%s_%s" % (id, cid))
                    component.front_color_id = _f("c_front_color_id_%s_%s" % (id, cid))
                    component.back_color_id = _f("c_back_color_id_%s_%s" % (id, cid))
                    component.finished_size_l = _f("c_finished_size_l_%s_%s" % (id, cid))
                    component.finished_size_w = _f("c_finished_size_w_%s_%s" % (id, cid))
                    component.finished_size_h = _f("c_finished_size_h_%s_%s" % (id, cid))
                    component.closure_id = _f("c_closure_id_%s_%s" % (id, cid))
                    component.display_mode_id = _f("c_display_mode_id_%s_%s" % (id, cid))
                    component.remark = _f("c_remark_%s_%s" % (id, cid))
            if log : DBSession.add(BBYLog(job_id = h.id, action_type = "UPDATE", remark = "[Mockup] " + " ".join(log)))
            flash("Save successfully!")
        except Exception, e:
            log.exception(str(e))
            flash("The service is not avaiable now,please try it laster!")
            transaction.doom()
        redirect("/bbymockup/item_view?id=%d" % h.id)


    @expose('tribal.templates.bby.mockup.detail_view')
    @tabFocus(tab_type = "main")
    def detail_view(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/bbymockup/index")
        try:
            testing_data = {}
            testing_type = ["DROP","HANGING"]
            for option in h.options:
                testing_data[option.id] = {}
                for tt in testing_type:
                    tmp_result = OrderedDict()
                    for testing in option.getTesting(tt):
                        key = "%d_%d" %(testing.round,testing.line)
                        if key not in tmp_result:
                            tmp_result[key] = []
                        tmp_result[key].append(testing)
                    testing_data[option.id][tt] = tmp_result
            
            
            can_submit = any([o.final for o in h.options]) and h.ae
        except NoResultFound:
            can_submit = False
        except Exception, e:
            log.exception(str(e))
            flash("Error occur on the serve side!")
            redirect("/bbymockup/index")

        return {"header" : h ,
                "widget" : basic_info_widget,
                "values" : h.basic_info_populate(),
                "testing_data" : testing_data,
                "can_submit" : can_submit,
                }


    @expose()
    def save_detail_edit(self, **kw):
        o = getOr404(BBYOption, kw["option_id"], "/bbymockup/index")

        _farmatdate = lambda d : "" if not d else d.strftime('%Y-%m-%d')
        f = lambda val : val or None
        try:
            log = []

            def _up(ns, ps):
                (flag, ids) = sysUpload([kw.get(pn, None) for (pn, pv) in ps], [nv for (nn, nv) in ns])
                return map(str, filter(bool, ids))

            #=======================================================================
            #delete the not exist record:
            #=======================================================================
            for round in o.internal_fittings:
                if "internal_round_%d" % round.id not in kw:
                    round.active = 1

            for line in o.testings:
                if "send_date_%d" % line.id not in kw:
                    line.active = 1
                    log.append("Delete line whose 'Sent out Date' is '%s'." % _farmatdate(line.send_date))
            #===============================================================================
            # internal fitting update
            #==============================================================================       
            
            for n_round,v_round in self._filterAndSorted("internal_round_", kw):
                id = n_round[n_round.rindex("_") + 1:]
                fitting = DBSession.query(BBYInternalFitting).get(id)
                tmp_content = kw.get("internal_content_%s" % id, None) or None
                if tmp_content : tmp_content = "|".join(tmp_content)
                fitting.content = tmp_content
                
                for d in fitting.details:
                    if "internal_received_date_%d" %d.id not in kw:
                        d.active = 1
                    else:
                        d.received_date = f(kw.get("internal_received_date_%d" %d.id,None))
                        d.source_id = f(kw.get("internal_source_id_%d" %d.id,None))
                        d.test_by_id = f(kw.get("internal_test_by_id_%d" %d.id,None))
                        d.qty = f(kw.get("internal_qty_%d" %d.id,None))
                        d.result = f(kw.get("internal_result_%d" %d.id,None))
                        d.reported_date = f(kw.get("internal_reported_date_%d" %d.id,None))
                        d.reason_id = f(kw.get("internal_reason_id_%d" %d.id,None))
                        d.remark = f(kw.get("internal_remark_%d" %d.id,None))
                        
                        names = self._filterAndSorted("internal_attachment_name_%s_" % d.id, kw)
                        paths = self._filterAndSorted("internal_attachment_path_%s_" % d.id, kw)
                        ids = _up(names, paths)
                        if ids :
                            if d.attachment : d.attachment = "|".join([d.attachment] + ids)
                            else: d.attachment = "|".join(ids)
            
            #===================================================================
            # handle new fitting
            #===================================================================
            for n_inr,v_inr in self._filterAndSorted("internal_new_round_",kw):
                id = n_inr[n_inr.rindex("_") + 1:]
                tmp_content = kw.get("internal_new_content_%s" % id, None) or None
                if tmp_content : tmp_content = "|".join(tmp_content)
                fitting = BBYInternalFitting(option_id=o.id,round=v_inr,content=tmp_content)
                DBSession.add(fitting)
                
                new_component = self._filterAndSorted("internal_new_component_id_%s" %id, kw)
                new_receive = self._filterAndSorted("internal_new_received_date_%s" %id, kw)
                new_source = self._filterAndSorted("internal_new_source_id_%s" %id, kw)
                new_test_by = self._filterAndSorted("internal_new_test_by_id_%s" %id, kw)
                new_qty = self._filterAndSorted("internal_new_qty_%s"%id, kw)
                new_result = self._filterAndSorted("internal_new_result_%s" %id, kw)
                new_reported = self._filterAndSorted("internal_new_reported_date_%s" %id, kw)
                new_reason = self._filterAndSorted("internal_new_reason_id_%s" %id, kw)
                new_remark = self._filterAndSorted("internal_new_remark_%s" %id, kw)
                new_courier = self._filterAndSorted("internal_new_courier_id_%s" %id, kw)
                new_awb = self._filterAndSorted("internal_new_awb_%s" %id, kw)
                
                for (n_component,v_component), (n_receive, v_receive), (n_source, v_source), (n_test, v_test), (n_qty, v_qty), (n_result, v_result), \
                (n_reported, v_reported), (n_reason, v_reason), (n_remark, v_remark), (n_courier, v_courier), (n_awb, v_awb) in \
                zip(new_component,new_receive, new_source, new_test_by, new_qty, new_result, new_reported, new_reason, new_remark, new_courier, new_awb) :
                
                    tmp = BBYInternalFittingDetail(header=fitting,component_id=v_component, received_date = v_receive, source_id = v_source, test_by_id = v_test, qty = v_qty,
                                         result = v_result, reported_date = v_reported, reason_id = v_reason, remark = v_remark, courier_id = v_courier, awb = v_awb)

                    names = self._filterAndSorted("internal_new_attachment_name_%s_%s" % (id,v_component), kw)
                    paths = self._filterAndSorted("internal_new_attachment_path_%s_%s" % (id,v_component), kw)
                    ids = _up(names, paths)
                    if ids :  tmp.attachment = "|".join(ids)
                    DBSession.add(tmp)
  
            #=======================================================================
            # update testing
            #=======================================================================
            send_dates = self._filterAndSorted("send_date_", kw)
            source_ids = self._filterAndSorted("source_id", kw)
            test_by_ids = self._filterAndSorted("test_by_id_", kw)
            qtys = self._filterAndSorted("qty_", kw)
            results = self._filterAndSorted("result_", kw)
            reported_dates = self._filterAndSorted("reported_date_", kw)
            reason_ids = self._filterAndSorted("reason_id_", kw)
            remarks = self._filterAndSorted("remark_", kw)

            for (n_send, v_send), (n_source, v_source), (n_qty, v_qty), (n_result, v_result), (n_report, v_report), \
                (n_reason, v_reason), (n_remark, v_remark) in \
                zip(send_dates, source_ids, qtys, results, reported_dates, reason_ids, remarks) :
                id = n_send[n_send.rindex("_") + 1:]
                t = DBSession.query(BBYTesting).get(id)
                t.send_date = f(v_send)
                t.source_id = f(v_source)
                t.qty = f(v_qty)
                t.result = f(v_result)
                t.reported_date = f(v_report)
                t.reason_id = f(v_reason)
                t.remark = f(v_remark)
                t.test_by_id = kw.get("test_by_id_%s" % id, None) or None

                names = self._filterAndSorted("attachment_name_%s_" % id, kw)
                paths = self._filterAndSorted("attachment_path_%s_" % id, kw)
                ids = _up(names, paths)
                if ids :
                    if t.attachment : t.attachment = "|".join([t.attachment] + ids)
                    else: t.attachment = "|".join(ids)


            #=======================================================================
            # add new testing
            #=======================================================================
            test_round = self._filterAndSorted("new_test_round_",kw)
            test_line = self._filterAndSorted("new_test_line_",kw)
            test_component_id = self._filterAndSorted("new_test_component_id_", kw)
            test_type = self._filterAndSorted("new_test_type_", kw)
            send_dates = self._filterAndSorted("new_send_date_", kw)
            source_ids = self._filterAndSorted("new_source_id_", kw)
            test_by_ids = self._filterAndSorted("new_test_by_id_", kw)
            qtys = self._filterAndSorted("new_qty_", kw)
            results = self._filterAndSorted("new_result_", kw)
            reported_dates = self._filterAndSorted("new_reported_date_", kw)
            reason_ids = self._filterAndSorted("new_reason_id_", kw)
            remarks = self._filterAndSorted("new_remark_", kw)

            for (n_round,v_round),(n_line,v_line),(n_component,v_component),(n_type, v_type), \
                (n_send, v_send), (n_source, v_source), (n_qty, v_qty), (n_result, v_result), \
                (n_reported, v_reported), (n_reason, v_reason), (n_remark, v_remark),(n_test_by,v_test_by) in \
                zip(test_round,test_line,test_component_id,test_type, send_dates, source_ids, \
                    qtys, results, reported_dates, reason_ids, remarks,test_by_ids):

                t = BBYTesting(option = o,round=int(v_round),line=int(v_line),component_id=v_component, \
                               send_date = f(v_send), source_id = f(v_source), qty = f(v_qty),result = f(v_result),\
                               reported_date = f(v_reported), reason_id = f(v_reason), remark = f(v_remark), \
                               test_type = f(v_type),test_by_id=v_test_by)

                id = n_send[n_send.rindex("_") + 1:]
                names = self._filterAndSorted("new_attachment_name_%s_" % id, kw)
                paths = self._filterAndSorted("new_attachment_path_%s_" % id, kw)
                ids = _up(names, paths)
                if ids :  t.attachment = "|".join(ids)
                DBSession.add(t)
                log.append("Add new line whose 'Sent out Date' is '%s'." % v_send)

            if log : DBSession.add(BBYLog(job_id = o.header_id, action_type = "UPDATE", remark = "[Mockup] " + " ".join(log)))
            flash("Save the update successfully!")
        except Exception, e:
            log.exception(str(e))
            transaction.doom()
            flash("The service is not avaiable now,please try it laster!")
        redirect("/bbymockup/detail_view?id=%d" % o.header_id)


    @expose('tribal.templates.bby.mockup.history')
    @tabFocus(tab_type = "main")
    def history(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/sku/index")

        hs = DBSession.query(BBYLog).filter(BBYLog.active == 0).filter(BBYLog.job_id == h.id).order_by(desc(BBYLog.create_time)).all()
        return {"header" : h, "history" : hs}


    @expose()
    def submit(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/bbymockup/index")
        try:
            h.status = CASEPACK_NEW
            DBSession.add(BBYLog(job_id = h.id, action_type = "SUBMIT", remark = "[Mockup] %s confirm the record." % request.identity["user"]))
            flash("Submit the record successfully!")
        except Exception, e:
            log.exception(str(e))
            transaction.doom()
            flash("Error when submit the record!")
        redirect("/bbymockup/index")



    @expose()
    def download(self, **kw):
        try:
            obj = DBSession.query(UploadObject).get(kw["id"])
            return serveFile(os.path.join(config.download_dir, obj.file_path), obj.file_name)
        except Exception, e:
            log.exception(str(e))
            traceback.print_exc()
            flash("No such file!")
            redirect("/index")


    @expose("json")
    def ajaxDeleteFile(self, **kw):
        try:
            job_id = None
            if kw.get("type", False) == "O":
                obj = DBSession.query(BBYOption).get(kw["id"])
                job_id = obj.header_id
            elif kw.get("type", False) == "I":
                obj = DBSession.query(BBYInternalFittingDetail).get(kw["id"])
                job_id = obj.header.option.header_id
            elif kw.get("type", False) == "T":
                obj = DBSession.query(BBYTesting).get(kw["id"])
                job_id = obj.option.header_id
            elif kw.get("type", False) == "V":
                obj = DBSession.query(BBYVendorFitting).get(kw["id"])
                job_id = obj.option.header_id
            else : raise "No such Type"

            if kw.get('attachment_pdf'):
                fs = obj.attachment_pdf.split("|")
                fs.remove(kw.get("fid"))
                if fs:
                    obj.attachment_pdf = "|".join(fs)
                else:
                    obj.attachment_pdf = None
            else:
                fs = obj.attachment.split("|")
                fs.remove(kw.get("fid"))
                if fs:
                    obj.attachment = "|".join(fs)
                else:
                    obj.attachment = None

            f = DBSession.query(UploadObject).get(kw["fid"])
            content = "[Mockup] %s delete file [ID : %s ,File Name : %s,Upload By : %s ,Upload Time : %s]." % (request.identity["user"], kw["fid"], f.file_name, f.upload_by, f.create_time)
            DBSession.add(BBYLog(job_id = job_id, action_type = "UPDATE", remark = content))
            return {"result" : "0"}
        except Exception, e:
            log.exception(str(e))
            transaction.doom()
            return {"result" : "1"}

    @expose()
    def send(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/bbymockup/index")
        try:
            h.status = MOCKUP_SENT
            DBSession.add(BBYLog(job_id = h.id, action_type = "UPDATE", remark = "[Mockup] %s mark the record as sent." % request.identity["user"]))
            flash("The record send successfully!")
        except Exception, e:
            log.exception(str(e))
            transaction.doom()
            flash("Error when sending this record to next step.")
        return redirect("/bbymockup/index")



    @expose('tribal.templates.bby.mockup.vendor_view')
    @tabFocus(tab_type = "main")
    def vendor_fitting(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/bbymockup/index")
        try:
            result = {}
            default = {}
            for option in h.options:
                result[option.id] = OrderedDict()
                default[option.id] = {}
                verdor_fittings = DBSession.query(BBYVendorFitting).filter(BBYVendorFitting.active == 0)\
                    .filter(BBYVendorFitting.option_id == option.id).order_by(BBYVendorFitting.round, BBYVendorFitting.id)
                for fit in verdor_fittings:
                    if fit.round in result[option.id]:
                        if fit.component_id in  result[option.id][fit.round]["data"]:
                            result[option.id][fit.round]["data"][fit.component_id]["data"].append(fit)
                        else:
                            result[option.id][fit.round]["data"][fit.component_id] = {
                                                                              "component" : fit.component,
                                                                              "data" : [fit, ]
                                                                              }
                    else:
                        result[option.id][fit.round] = OrderedDict(data = OrderedDict(), row_count = 0)
                        result[option.id][fit.round]["data"][fit.component_id] = {
                                                                          "component" : fit.component,
                                                                          "data" : [fit, ],
                                                                          }
                    result[option.id][fit.round]["row_count"] += 1
                    

                if len(option.internal_fittings) > 0 :
                    for d in  option.internal_fittings[-1].details:
                        default[option.id][d.component_id] = d
                print "*-" * 10
                print default
                print "^-" * 10
            can_submit = any([o.final for o in h.options]) and h.ae
            
            
        except NoResultFound:
            can_submit = False
        except Exception, e:
            log.exception(str(e))
            flash("Error occur on the serve side!")
            redirect("/bbymockup/index")

        return {"header" : h ,
                "widget" : basic_info_widget,
                "values" : h.basic_info_populate(),
                "can_submit" : can_submit,
                "result" : result,
                "default" : default,
                }

    @expose()
    def vendor_fitting_save(self, **kw):
        o = getOr404(BBYOption, kw["option_id"], "/bbymockup/index")

        _farmatdate = lambda d : "" if not d else d.strftime('%Y-%m-%d')
#        f = lambda val : val or None
        _f = lambda name : kw.get(name, None) or None

        def _up(ns, ps):
                (flag, ids) = sysUpload([kw.get(pn, None) for (pn, pv) in ps], [nv for (nn, nv) in ns])
                return map(str, filter(bool, ids))

        o.sample_received_date = kw.get("sample_received_date", None) or None
        names = self._filterAndSorted("mock_attachment_name_", kw)
        paths = self._filterAndSorted("mock_attachment_path_", kw)
        ids = _up(names, paths)
        if ids :
            if o.attachment : o.attachment = "|".join([o.attachment] + ids)
            else: o.attachment = "|".join(ids)


        old_row_ids = [str(f.id) for f in o.vendor_fittings]
        new_ids = [rname[rname.rindex("_") + 1:] for rname, rvalue in self._filterAndSorted("round_", kw)]

        new_rows, delete_rows, update_rows = self._split(old_row_ids, new_ids)

        #handle delete
        for id in delete_rows:
            DBSession.query(BBYVendorFitting).get(id).active = 1

        #handle new
        fields = ["component_id", "round", "receive_date", "send_date", "source_id", "qty", "reported_date", "remark", "courier_id", "awb","confirm"]
        for id in new_rows:
            if not _f("source_id_%s" % id) or not _f("send_date_%s" % id) : continue
            params = {"option_id" : o.id}
            for f in fields:
                params[f] = _f("%s_%s" % (f, id))

            names = self._filterAndSorted("attachment_name_%s_" % id, kw)
            paths = self._filterAndSorted("attachment_path_%s_" % id, kw)
            ids = _up(names, paths)
            if ids : params["attachment"] = "|".join(ids)

            tmp = BBYVendorFitting(**params)
            DBSession.add(tmp)

        #handle update
        for id in update_rows:
            tmp = DBSession.query(BBYVendorFitting).get(id)
            for f in fields:
                setattr(tmp, f, _f("%s_%s" % (f, id)))
            names = self._filterAndSorted("attachment_name_%s_" % id, kw)
            paths = self._filterAndSorted("attachment_path_%s_" % id, kw)
            ids = _up(names, paths)
            if ids :
                if tmp.attachment : tmp.attachment = "|".join([tmp.attachment] + ids)
                else: tmp.attachment = "|".join(ids)
        flash("Save the update successfully!")
        redirect("/bbymockup/vendor_fitting?id=%d" % o.header_id)


    @expose("json")
    def ajaxMaterialSpec(self, **kw):
        try:
            is_post = None
            h = DBSession.query(BBYMaterialSpec).filter(BBYMaterialSpec.head_id == kw["component"]).filter(BBYMaterialSpec.active == 0).first()
            parname = kw.get('parname')
            if parname:
                parname = parname.split('_')
                if len(parname)>1:
                    option_id = parname[1]
                    component_id = parname[2]
                c = DBSession.query(BBYComponent).get(component_id)
                if c:
                    is_post = 1
                    return dict(component = h.head_id, 
                                material = h.material, 
                                spec = h.spec, 
                                front_color = h.front_color, 
                                back_color = h.back_color, 
                                
                                base_material = c.material_id, 
                                base_spec = c.coating_id, 
                                base_front_color = c.front_color_id, 
                                base_back_color = c.back_color_id, 
                                active = 0)
            if not is_post:
                return dict(component = h.head_id, 
                            material = h.material, 
                            spec = h.spec, 
                            front_color = h.front_color, 
                            back_color = h.back_color, 
                            active = 0)
        except Exception, e:
            log.exception(str(e))
            return dict(msg = "fail" , active = 1)

    @expose()
    def genVendorFittingPDF(self, **kw):
        option = DBSession.query(BBYOption).get(kw['option_id'])
        max_vendor_round = option.getMaxVendorFittingRound()
        max_internal_round = option.getMaxInternalFittingRound()
        header = option.header
        vendor = header.vendor
        asia_contact = header.bby_asia_contact
        us_contact = header.bby_us_contact

        internal_content = []
        for i in option.internal_fittings:
            if i.round == max_internal_round:
                internal_content = i.getContent()
        header = option.header
        file_path = get_post_response('http://localhost:19999/bby', dict(
                sku=header.sku if header.sku else '',
                product_description=header.product_description if header.product_description else '',
                brand=header.brand if header.brand else '',
                packaging_format=header.packaging_format if header.packaging_format else '',
                closure=header.closure if header.closure else '',
                display_mode=header.display_mode if header.display_mode else '',
                fitting_round=max_vendor_round if max_vendor_round else '',
                vendor_date=format_today(),
                packaging_description=kw['packaging_description'] if kw['packaging_description'] else '',
                packaging_comment=kw['packaging_comment'] if kw['packaging_comment'] else '',
                score = kw.get('score','') or '',
                internal_content='|'.join([str(i.value) for i in internal_content]),
                vendor_contact='%s - %s - %s - %s' % (vendor.name, vendor.contact, vendor.email, vendor.tel) if vendor else '',
                asia_contact='%s - %s - %s' % (asia_contact.name, asia_contact.email, asia_contact.phone) if asia_contact else '',
                us_contact='%s - %s - %s' % (us_contact.name, us_contact.email, us_contact.phone) if us_contact else '',
            )
        )
        file_name = 'Packging_Fit_Confirmation_Form_Round_%s.zip' % max_vendor_round
        option.save_pdf(file_name, file_path.strip())
        redirect("/bbymockup/vendor_fitting?id=%d" % header.id)

    @expose("tribal.templates.bby.mockup.report")
    @tabFocus(tab_type = "report")
    def report(self, **kw):
        return {"widget":mockup_report_form}

    @expose()
    def export(self, **kw):
        try:
            current = dt.now()
            dateStr = current.strftime("%Y%m%d")
            fileDir = os.path.join(config.get("download_dir"), "BBY", dateStr)
            if not os.path.exists(fileDir): os.makedirs(fileDir)
            templatePath = os.path.join(config.get("template_dir"), "BBYMOCKUP_REPORT_TEMPLATE.xls")
            tempFileName = os.path.join(fileDir, "bby_mockup_report_tmp_%s_%d.xls" % (current.strftime("%Y%m%d%H%M%S"), random.randint(0, 1000)))
            realFileName = os.path.join(fileDir, "bby_mockup_report_%s.xls" % (dt.now().strftime("%Y%m%d%H%M%S")))
            shutil.copy(templatePath, tempFileName)
            bby_report_xls = BBYMockupExcel(templatePath = tempFileName, destinationPath = realFileName)

            tmp_data = {}
            tmp_data['new'] = []
            tmp_data['post'] = []
            tmp_data['cancell'] = []
            if kw:
                jobs = self._query_result(kw)
                for job in jobs:
                    if job.status == 30 and (job.control_flag != -2 or job.control_flag != -3):
                        options = job.options
                        itemPost = {}
                        for option in options:
                            if option.final == 'YES':
                                for fit in DBSession.query(BBYVendorFitting).filter(BBYVendorFitting.option_id == option.id).filter(BBYVendorFitting.active == 0).order_by(BBYVendorFitting.round, BBYVendorFitting.id):
                                    itemPost['item'] = job.sku
                                    itemPost['round'] = fit.round
                                    if itemPost.has_key('sendDate') and itemPost['sendDate'] and fit.send_date:
                                        if itemPost['sendDate'] < fit.send_date:
                                            itemPost['sendDate'] = fit.send_date
                                    else:
                                        itemPost['sendDate'] = fit.send_date

                                    if fit.reported_date  and itemPost.has_key('confirmDate') and itemPost['confirmDate']:
                                        if itemPost['confirmDate'] < fit.reported_date:
                                            itemPost['confirmDate'] = fit.reported_date
                                    else:
                                        itemPost['confirmDate'] = fit.reported_date
                        #print itemPost
                        if len(itemPost) > 0:tmp_data['post'].append(itemPost)
                        del itemPost

                    if job.status == 20 or job.status == 21 and (job.control_flag != -2 or job.control_flag != -3):
                        itemNew = {}
                        itemNew['item'] = job.sku
                        tmp_data['new'].append(itemNew)
                        del itemNew

                    if job.control_flag == -2 or job.control_flag == -3:
                        itemCancell = {}
                        itemCancell['item'] = job.sku
                        tmp_data['cancell'].append(itemCancell)
                        del itemCancell


            bby_report_xls.inputData(data = tmp_data)
            bby_report_xls.outputData()
            try:
                os.remove(tempFileName)
            except:
                pass
            return serveFile(unicode(realFileName))

        except Exception, e:
            log.exception(str(e))
            flash("Export Fail.")
            redirect("/bbymockup/report")


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
            
            
            
    def _toDoList(self,**kw):
        new_conditions = [BBYJobHeader.active == 0,BBYJobHeader.control_flag == 0,BBYJobHeader.status == MOCKUP_NEW]
        new_result = DBSession.query(BBYJobHeader).filter(and_(*new_conditions))
        
        send_conditions = [BBYJobHeader.active == 0,BBYJobHeader.control_flag == 0,BBYJobHeader.status == MOCKUP_SENT]
        send_result = DBSession.query(BBYJobHeader).filter(and_(*send_conditions))
        
        new_result_count = new_result.count()
        send_result_count = send_result.count()
        
#        if kw.get("all",None):
#            new_result = new_result.all()
#            send_result = send_result.all()
#        else:
#            qty = int(kw.get("qty",5))
#            new_result = new_result[:qty]
#            send_result = send_result[:qty]
            
        new_result = new_result.all()
        send_result = send_result.all()
        return {
                "new" : new_result,
                "new_count" : new_result_count,
                "send" : send_result,
                "send_count" : send_result_count,
                }
    
