# -*- coding: utf-8 -*-

import traceback, transaction, os
from datetime import datetime as dt
import logging

# turbogears imports
from tg import expose, redirect, validate, flash, config,request
from tg.decorators import paginate

from repoze.what import predicates, authorize
from repoze.what.predicates import not_anonymous, in_group, has_permission
from sqlalchemy.sql import *

# project specific imports
from tribal.lib.base import BaseController
from tribal.model import *
from tribal.model.bby import *
from tribal.util.common import *
from tribal.util.bby_helper import *
from tribal.widgets.bby import *


log = logging.getLogger(__name__)

class BBYCasepackController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    allow_only = authorize.not_anonymous()

    @expose('tribal.templates.bby.casepack.index')
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
                if kw["status"] == 'NEW' : conditions.extend([BBYJobHeader.status == CASEPACK_NEW])
                elif kw["status"] == 'SENT' : conditions.append(BBYJobHeader.status == CASEPACK_SENT)
                elif kw["status"] == 'COMPLETED' : conditions.append(BBYJobHeader.status >= COMPLETED)
            else:
                conditions.append(BBYJobHeader.status >= CASEPACK_NEW)

            result = DBSession.query(BBYJobHeader).filter(and_(*conditions)).all()
        else:
            result = DBSession.query(BBYJobHeader).filter(BBYJobHeader.active == 0).filter(BBYJobHeader.status >= CASEPACK_NEW).all()
        return {"result":result, "values":kw, "widget" : casepack_search_form,"todolist" : self._toDoList()}


    @expose('tribal.templates.bby.casepack.view')
    @tabFocus(tab_type = "main")
    def view(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/bbycasepack/index")
        option = self._get_final_option(h)
        if not option :
            flash("No final option for this SKU, please update the mockup info!")
            redirect("index")

        return {"header" : h ,
                "widget" : basic_info_widget,
                "values" : h.basic_info_populate(),
                "option" : option,
                }

    @expose('tribal.templates.bby.casepack.update')
    @tabFocus(tab_type = "main")
    def update(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/bbycasepack/index")
        options = [o for o in h.options if o.final]
        if not options :
            flash("No final option for this SKU, please update the mockup info!")
            redirect("index")

        return {"header" : h ,
                "widget" : basic_info_widget,
                "values" : h.basic_info_populate(),
                "option" : options[0],
                }


    def _filterAndSorted(self, prefix, kw):
        return sorted([(kk, vv or None) for (kk, vv) in filter(lambda (k, v): k.startswith(prefix), kw.iteritems())], cmp = lambda x, y:cmp(x[0], y[0]))


    def _get_final_option(self, header):
        try:
            return [o for o in header.options if o.final][0]
        except:
            return None

    def _split(self, l1, l2):
        new = [item for item in l2 if item not in l1]
        delete = [item for item in l1 if item not in l2]
        update = [item for item in l1 if item in l2]
        return (new, delete, update)

    @expose()
    def save_update(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/bbycasepack/index")

        option = self._get_final_option(h)
        if not option :
            flash("No final option for this SKU, please update the mockup info!")
            redirect("index")

        try:
            log = []
            _f = lambda n : kw.get(n, None) or None
            for component in option.components:
                component.factory_id = _f("factory_id_%d" % component.id)

                old_ids = [str(cp.id) for cp in component.casepack_details]
                new_ids = [k[k.rindex("_") + 1:] for (k, v) in self._filterAndSorted("qty_%d_" % component.id, kw)]
                new_ids, delete_ids, update_ids = self._split(old_ids, new_ids)

                #handle delete 
                for id in delete_ids :
                    dbobj = DBSession.query(BBYCasepackDetail).get(id)
                    dbobj.active = 1
                    log.append("Delete detail whose 'Required Ready Date' is '%s'." % Date2Text(dbobj.required_date))

                #handle new
                for id in new_ids:
                    qty = _f("qty_%d_%s" % (component.id, id))
                    required_date = _f("required_date_%d_%s" % (component.id, id))
                    ship_to_id = _f("ship_to_id_%d_%s" % (component.id, id))
                    attention = _f("attention_%d_%s" % (component.id, id))
                    remark = _f("remark_%d_%s" % (component.id, id))

                    if not any([qty, required_date, ship_to_id, attention, remark]) : continue

                    DBSession.add(BBYCasepackDetail(
                                      component = component,
                                      qty = qty,
                                      required_date = required_date,
                                      ship_to_id = ship_to_id,
                                      attention = attention,
                                      remark = remark,
                                      ))
                    log.append("Add new detail whose 'Required Ready Date' is '%s'." % required_date)

                #handle update
                for id in update_ids:
                    d = DBSession.query(BBYCasepackDetail).get(id)
                    d.qty = _f("qty_%d_%s" % (component.id, id))
                    d.required_date = _f("required_date_%d_%s" % (component.id, id))
                    d.ship_to_id = _f("ship_to_id_%d_%s" % (component.id, id))
                    d.attention = _f("attention_%d_%s" % (component.id, id))
                    d.remark = _f("remark_%d_%s" % (component.id, id))

            if log : DBSession.add(BBYLog(job_id = h.id, action_type = "UPDATE", remark = "[Casepack] " + " ".join(log)))
            flash("Save the update successfully!")
        except Exception, e:
            log.exception(str(e))
            transaction.doom()
            flash("The service is not avaiable now,please try it laster!")
        redirect("/bbycasepack/view?id=%d" % h.id)


    @expose()
    def download(self, **kw):
        try:
            obj = DBSession.query(UploadObject).get(kw["id"])
            return serveFile(os.path.join(config.download_dir, obj.file_path), obj.file_name)
        except Exception, e:
            log.exception(str(e))
            flash("No such file!")
            redirect("/bbycasepack/index")

    @expose("json")
    def ajaxDeleteFile(self, **kw):
        try:
            if kw.get("type", None) == "cpr":
                obj = DBSession.query(BBYCasepackResult).get(kw["id"])
                job_id = obj.header_id
            else : raise "No such Type"

            fs = obj.attachment.split("|")
            fs.remove(kw.get("fid"))
            if fs:
                obj.attachment = "|".join(fs)
            else:
                obj.attachment = None

            f = DBSession.query(UploadObject).get(kw["fid"])
            content = "[Casepack] %s delete file [ID : %s ,File Name : %s,Upload By : %s ,Upload Time : %s]." % (request.identity["user"], kw["fid"], f.file_name, f.upload_by, f.create_time)
            DBSession.add(BBYLog(job_id = job_id, action_type = "UPDATE", remark = content))
            return {"result" : "0"}
        except Exception, e:
            log.exception(str(e))
            transaction.doom()
            return {"result" : "1"}


    @expose()
    def complete(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/bbycasepack/index")
        try:
            h.status = COMPLETED
            DBSession.add(BBYLog(job_id = h.id, action_type = "SUBMIT", remark = "[Casepack] %s mark the record as completed." % request.identity["user"]))
            flash("Submit the record successfully!")
        except Exception, e:
            log.exception(str(e))
            transaction.doom()
            flash("Error when submit the record!")
        redirect("index")


    @expose('tribal.templates.bby.casepack.history')
    @tabFocus(tab_type = "main")
    def history(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/bbycasepack/index")

        hs = DBSession.query(BBYLog).filter(BBYLog.active == 0).filter(BBYLog.job_id == h.id).order_by(desc(BBYLog.create_time)).all()
        return {"header" : h, "history" : hs}


    @expose('tribal.templates.bby.casepack.email')
    @tabFocus(tab_type = "main")
    def email(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/bbycasepack/index")
        option = self._get_final_option(h)
        if not option :
            flash("No final option for this SKU, please update the mockup info!")
            redirect("index")

        component_casepack = [(c, c.casepack_details[-1]) for c in option.components if c.casepack_details]
        factory_info = {}
        for c, d in component_casepack:
            if c.factory_id:
                info = {"factory" : c.factory.name}
                if d.ship_to_id :
                    info["address"] = d.ship_to.address
                    info["phone"] = " ".join(filter(bool, [d.ship_to.tel, d.ship_to.ext, d.ship_to.mobile]))
                else:
                    info["address"] = ""
                    info["phone"] = ""
                factory_info[c.factory_id] = info

        seqs = {}
        for r in h.to_factory_records :
            if r.round not in seqs :
                seqs[r.round] = {"cids" : [str(r.component_id)], "last_date" : r.create_time}
            else:
                seqs[r.round]["cids"].append(str(r.component_id))
                seqs[r.round]["last_date"] = r.create_time

        attachments = []
        for rows in h.sku_info:
            for d in rows.row_detail:
                if d["confirm"] : attachments.extend(d["files"])

        cc_list = ["wings.tung@r-pac.com", "sam.cheng@r-pac.com", "phoebe.yip@r-pac.com", "norton.li@r-pac.com", "maya.xu@r-pac.com.cn"]
        if h.pd_id : cc_list.append(h.pd.email)
        if h.ae_id : cc_list.append(h.ae.email)

        return {
                "header" : h,
                "widget" : basic_info_widget,
                "values" : h.basic_info_populate(),
                "component_casepack" : component_casepack,
                "seqs" : seqs,
                "attachments" : attachments,
                "cc_list" : cc_list,
                "factory_info" : factory_info,
                }

    @expose()
    def email_save(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/bbycasepack/index")

        try:
            component_ids = kw.get("component_ids", []) or []
            if type(component_ids) != list : component_ids = [component_ids]
            
            print "_" * 20
            print component_ids
            print "*" * 20

            if kw.get("seq", None) != "NEW" :
                seq = kw["seq"]
            else:
                seq = (BBYCasepackToFactory.get_last_seq(h.id) or 0) + 1

            offices = kw.get("rpac_office", [])
            if type(offices) != list : offices = [offices, ]
            
            print "_" * 20
            print offices
            print "*" * 20

            component_info = {}
            records = []
            check_factory = check_vendor = None

            for id in component_ids:
                c = DBSession.query(BBYComponent).get(id)
                d = c.casepack_details[-1]

                if not check_factory : check_factory = c.factory
                elif check_factory.id != c.factory.id: raise makeException("Not the same factory, can't send out e-mail!")

                if not check_vendor : check_vendor = d.ship_to_id
                elif check_vendor != d.ship_to_id : raise makeException("Not the same shipto address, can't send out e-mail!")

                if c.id not in component_info : component_info[c.id] = (c, d)
                
                
            print "_" * 20
            print component_info
            print "*" * 20
            
            records = []
            email_session = []
            for office in offices:
                email_session.extend([
                                      "<div>"
                                      "<table cellspacing='0' cellpadding='3' border='1'>"
                                      "<tr><td width='150'>Address</td><td><b>%s</b></td></tr>" % kw.get("ship_to_address_%s" % office, ""),
                                      "<tr><td>Attention</td><td><b>%s</b></td></tr>" % kw.get("ship_to_att_%s" % office, ""),
                                      "<tr><td>Phone#</td><td><b>%s</b></td></tr>" % kw.get("ship_to_phone_%s" % office, ""),

                                      ])

                for k in component_info:
                    c, d = component_info[k]
                    params = {
                          "header_id" : h.id,
                          "round" : seq,
                          "component" : c.format,
                          "factory_id" : c.factory_id,
                          "required_date" : d.required_date,
                          "qty" : kw.get("qty_%s_%s" % (office, c.id), 0),
                          "ship_to" : str(d.ship_to) if office == 'vendor' else office,
                          "ship_to_address" : kw.get("ship_to_address_%s" % office, None),
                          "ship_to_att" : kw.get("ship_to_att_%s" % office, None),
                          "ship_to_phone" : kw.get("ship_to_phone_%s" % office, None),
                          }
                    records.append(BBYCasepackToFactory(**params))
                    email_session.append("<tr><td>Qty (%s)</td><td><b>%s</b></td></tr>" % (str(c), kw.get("qty_%s_%s" % (office, c.id), "")))

                email_session.extend([
                                      "</table>",
                                      "<p>Please advise courier name and AWB# once sent.<br />",
                                      "If you have any difficulty or concern, please advise ASAP.<br />",
                                      "Please see attached to the approved dieline and your quotation for further details.</p>",
                                      "<hr/>",
                                      "</div>"
                                      ])


            email_content = [
                            '<p>Dear <b>%s</b> Team:</p>' % check_factory,
                            '<p>The <b>%s</b> of <b>%s</b> is approved, please help to prepare case pack sample with correct LOGO TEMPLATE.</p>' % (",".join(map(lambda r:str(r.component), records)), h.sku),
                            '<table cellspacing="0" cellpadding="3" border="1">',
                                '<thead>',
                                    '<tr><th>Components</th><th>Material Name</th><th>Spec</th><th>Front Color</th><th>Back Color</th><th>Finished Size</th><th>Closure</th>',
                                    '<th>Display Mode</th><th>Required Ready Date</th></tr>',
                                '</thead>',
                            ]

            for key in component_info:
                cd = component_info[key]
                t = map(lambda v : str(v or "&nbsp;"), [cd[0].format, cd[0].material, cd[0].coating, cd[0].front_color, cd[0].back_color,
                    cd[0].finished_size, cd[0].closure, cd[0].display_mode, Date2Text(cd[1].required_date)])
                email_content.append("<tr>" + "".join(map(lambda c : "<td>%s</td>" % c, t)) + "</tr>")

            email_content.extend(["</table>", "<br />"])
            email_content.extend(email_session)
            email_content.extend([
                                "<p>It's sent by <b>%s.</b></p>" % request.identity["user"],
                                '\n\n',
                                '<p>************************************************************************************<br />',
                                'This e-mail is sent by the r-pac r-track system automatically.<br />',
                                "Please don't reply this e-mail directly!<br />",
                                "************************************************************************************</p>"
                                  ])


            #new update end
            attachments = kw.get("attachment", []) or []
            if type(attachments) != list : attachments = [attachments]

            email_params = {
                            "send_to" : kw.get("send_to", None),
                            "cc_to" : kw.get("cc_to", None),
                            "attachment" : "|".join(attachments),
                            "content" : "".join(email_content),
                            }

            email_obj = BBYCasepackEmail(**email_params)
            DBSession.add(email_obj)
            for r in records : r.email = email_obj
            DBSession.add_all(records)
            #===================================================================
            # send email
            #===================================================================
            def _getFile(id):
                obj = DBSession.query(UploadObject).get(id)

                class _info(object):
                    def __init__(self, file_name, file_path):
                        self.file_name = file_name
                        self.file_path = file_path
                return _info(obj.file_name, os.path.join(config.download_dir, obj.file_path))

            if config.debug :
                send_from = "r-tracktest@r-pac.com"
                subject = "[TESTING] Case Pack Sample Request for %s" % h.sku
            else:
                send_from = "r-track@r-pac.com"
                subject = "Case Pack Sample Request for %s" % h.sku

            send_to = kw.get("send_to", "").split(";")
#            send_to = ["cl.lam@r-pac.com.cn"]
            html = "".join(email_content)
            cc_to = kw.get("cc_to", "").split(";")
#            cc_to = []
            files = map(lambda i:_getFile(i), attachments)
            DBSession.flush()
        except Exception, e:
            log.exception(str(e))
            if hasattr(e, "is_customize") : flash(str(e))
            else:flash("Error occur when sending out the e-mail!")
            transaction.doom()
        else:
            try:
                advancedSendMail(send_from, send_to, subject, "", html, cc_to, files)
            except Exception, e:
                log.exception(str(e))
                flash("Error occur when sending out the e-mail!")
            else:
                flash("Send out the e-mail successfully!")

        redirect("/bbycasepack/factory?id=%d" % h.id)



    @expose('tribal.templates.bby.casepack.factory')
    @tabFocus(tab_type = "main")
    def factory(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/bbycasepack/index")

        rs = DBSession.query(BBYCasepackToFactory).filter(and_(BBYCasepackToFactory.active == 0,
                        BBYCasepackToFactory.header_id == h.id)).order_by(BBYCasepackToFactory.round, BBYCasepackToFactory.component_id)
        gs = OrderedDict()
        for r in rs:
            if r.round not in gs:
                gs[r.round] = OrderedDict()
                gs[r.round][r.component_id] = {"component" : r.component, "data" : [r, ]}
            else:
                if r.component_id not in gs[r.round]:
                    gs[r.round][r.component_id] = {"component" : r.component, "data" : [r, ]}
                else:
                    gs[r.round][r.component_id]["data"].append(r)

        return {"header" : h,
                "widget" : basic_info_widget,
                "values" : h.basic_info_populate(),
                "result" : gs,
                }

    @expose('tribal.templates.bby.casepack.factory_update')
    @tabFocus(tab_type = "main")
    def factory_update(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/bbycasepack/index")

        rs = DBSession.query(BBYCasepackToFactory).filter(and_(BBYCasepackToFactory.active == 0,
                        BBYCasepackToFactory.header_id == h.id)).order_by(BBYCasepackToFactory.round, BBYCasepackToFactory.component_id)
        gs = OrderedDict()
        for r in rs:
            if r.round not in gs:
                gs[r.round] = OrderedDict()
                gs[r.round][r.component_id] = {"component" : r.component, "data" : [r, ]}
            else:
                if r.component_id not in gs[r.round]:
                    gs[r.round][r.component_id] = {"component" : r.component, "data" : [r, ]}
                else:
                    gs[r.round][r.component_id]["data"].append(r)

        return {"header" : h,
                "widget" : basic_info_widget,
                "values" : h.basic_info_populate(),
                "result" : gs,
                }

#    def _split(self, l1, l2):
#        new = [item for item in l2 if item not in l1]
#        delete = [item for item in l1 if item not in l2]
#        update = [item for item in l1 if item in l2]
#        return (new, delete, update)


    @expose()
    def factory_save(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/bbycasepack/index")
        _f = lambda n : kw.get(n, None) or None
        try:
            fields = ["send_date", "courier_id", "awb", "received_date", "remark", "cancel", "approve", ]
            for r in h.to_factory_records:
                for f in fields:
                    setattr(r, f, _f("%s_%d" % (f, r.id)))
            flash("Update the record successfully!")
        except Exception, e:
            log.exception(str(e))
            transaction.doom()
            flash("The service is not avaiable now,please try it laster!")
        redirect("/bbycasepack/factory?id=%d" % h.id)



    @expose('tribal.templates.bby.casepack.customer')
    @tabFocus(tab_type = "main")
    def customer(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/bbycasepack/index")

        return {"header" : h,
                "widget" : basic_info_widget,
                "values" : h.basic_info_populate(),
                }

    @expose('tribal.templates.bby.casepack.customer_update')
    @tabFocus(tab_type = "main")
    def customer_update(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/bbycasepack/index")
        
        #get hte max rev day from the factory
        last_rev_day = DBSession.query(func.max(BBYCasepackToFactory.received_date))\
                           .filter(and_(BBYCasepackToFactory.active == 0, \
                                        BBYCasepackToFactory.header_id == h.id)).scalar() or None
        return {"header" : h,
                "widget" : basic_info_widget,
                "values" : h.basic_info_populate(),
                "last_rev_day" :last_rev_day,
                }


    @expose()
    def customer_save(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/bbycasepack/index")
        try:
            log = []
            old_ids = [str(r.id) for r in h.results]
            new_ids = [rname[rname.rindex("_") + 1:] for rname, rval in self._filterAndSorted("received_date_", kw)]

            new_ids, delete_ids, update_ids = self._split(old_ids, new_ids)

            #handle delete 
            for id in delete_ids :
                dbobj = DBSession.query(BBYCasepackResult).get(id)
                dbobj.active = 1
                log.append("Delete line from 'Customer' tab whose 'Received Date' is '%s'." % Date2Text(dbobj.received_date))

            _f = lambda n : kw.get(n, None) or None

            #handle new
            for id in new_ids:
                received_date = _f("received_date_%s" % id)
                send_out_date = _f("send_out_date_%s" % id)
#                source_id = _f("source_id_%s" % id)
                customer_received_date = _f('customer_received_date_%s' %id)
                test_by = _f("test_by_%s" % id)
                qty = _f("qty_%s" % id)
                result = _f("result_%s" % id)
                reported_date = _f("reported_date_%s" % id)
                reason_id = _f("reason_id_%s" % id)
                remark = _f("remark_%s" % id)

                if not any([received_date, send_out_date, customer_received_date, test_by, qty, result, reported_date, reason_id, remark]) : continue

                file_names = self._filterAndSorted("attachment_name_%s_" % id, kw)
                file_paths = self._filterAndSorted("attachment_path_%s_" % id, kw)
                (flag, fobjs) = sysUpload([kw.get(fpname) for fpname, fpvalue in file_paths], [fnvalue for fnname, fnvalue in file_names], return_obj = True)
 
                if any(fobjs):
                    attachment = "|".join(map(lambda r:str(r.id), filter(bool, fobjs)))
                else: attachment = None


                DBSession.add(BBYCasepackResult(header = h, received_date = received_date, send_out_date = send_out_date, customer_received_date = customer_received_date, test_by = test_by,
                                  qty = qty, result = result, reported_date = reported_date, reason_id = reason_id, attachment = attachment, remark = remark))

                log.append("Add new line into 'Customer' tab whose 'Received Date' is '%s'." % received_date)


            #handle update
            for id in update_ids:
                tmp = DBSession.query(BBYCasepackResult).get(id)
                tmp.received_date = _f("received_date_%s" % id)
                tmp.send_out_date = _f("send_out_date_%s" % id)
                tmp.customer_received_date = _f("customer_received_date_%s" % id)
#                tmp.source_id = _f("source_id_%s" % id)
                tmp.test_by = _f("test_by_%s" % id)
                tmp.qty = _f("qty_%s" % id)
                tmp.result = _f("result_%s" % id)
                tmp.reported_date = _f("reported_date_%s" % id)
                tmp.reason_id = _f("reason_id_%s" % id)
                tmp.remark = _f("remark_%s" % id)

                file_names = self._filterAndSorted("attachment_name_%s_" % id, kw)
                file_paths = self._filterAndSorted("attachment_path_%s_" % id, kw)
                (flag, fobjs) = sysUpload([kw.get(fpname) for fpname, fpvalue in file_paths], [fnvalue for fnname, fnvalue in file_names], return_obj = True)
                if any(fobjs):
                    attachment = "|".join(map(lambda r:str(r.id), filter(bool, fobjs)))
                else: attachment = None

                if tmp.attachment and attachment:
                    tmp.attachment += "|" + attachment
                elif attachment:
                    tmp.attachment = attachment
            if log : DBSession.add(BBYLog(job_id = h.id, action_type = "UPDATE", remark = "[Casepack] " + " ".join(log)))
            flash("Update the record successfully!")
        except Exception, e:
            log.exception(str(e))
            transaction.doom()
            flash("The service is not avaiable now,please try it laster!")
        redirect("/bbycasepack/customer?id=%d" % h.id)
        
        
    def _toDoList(self,**kw):
        new_conditions = [BBYJobHeader.active == 0,BBYJobHeader.control_flag == 0,BBYJobHeader.status == CASEPACK_NEW]
        new_result = DBSession.query(BBYJobHeader).filter(and_(*new_conditions))
        new_result_count = new_result.count()
        
        send_conditions = [BBYJobHeader.active == 0,BBYJobHeader.control_flag == 0,BBYJobHeader.status == CASEPACK_SENT]
        send_result = DBSession.query(BBYJobHeader).filter(and_(*send_conditions))
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


    @expose()
    def eol(self, **kw):
        h = getOr404(BBYJobHeader, kw["id"], "/bbycasepack/index")
        try:
            h.status = EOL
            DBSession.add(BBYLog(job_id = h.id, action_type = "SUBMIT", remark = "[Casepack] %s mark the record as EOL." % request.identity["user"]))
            flash("Submit the record successfully!")
        except Exception, e:
            log.exception(str(e))
            transaction.doom()
            flash("Error when submit the record!")
        redirect("index")