# -*- coding: utf-8 -*-
import os
from datetime import datetime as dt
import logging, transaction

from tg import config

from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy import Table, ForeignKey, Column, or_, and_, desc
from sqlalchemy.types import Integer, Unicode, DateTime, Boolean, Text
from tribal.model import DeclarativeBase, metadata, DBSession
from tribal.model.auth import *
from tribal.model.sample import SysMixin

from tribal.util.oracle_helper import searchOracle
from tribal.util.date_util import over_days
from tribal.util.excel_helper import MglobalDailyExcel
from tribal.util.common import sendEmail

log = logging.getLogger(__name__)

def get_mglobal_upload_data():
    results = []
    _init_local_from_erp()
    _process_local_so()
    _proess_blank_awb()
    #prepare the upload data to MglobalPack for cron
    upload_list = MglobalErpDND.find_updated_dn()
    upload_map = {}
    for dnd in upload_list:
        so_hdr = dnd.local_so
        so_dtls = so_hdr.local_sods
        dn_client = dnd.local_client
        key = '%s-%s' % (so_hdr.cust_po_no, dn_client.client_id)
        upload_dn = upload_map.get(key, None)
        dnd_awb = dnd.get_awb()
        if dnd_awb:
            if not upload_dn:
                upload_dn = {'MGOrderNumber': so_hdr.cust_po_no, 'MGClientNumber': dn_client.client_id, 'OptionalNote': '', 'Items': {}}
                if so_hdr.has_done:
                    upload_dn.update({'MODE': 'C', 'InvoiceDate': dnd.dn_date.strftime('%Y-%m-%d %H:%M:%S'), 'InvoiceNumber': dnd.so_no, 
                            'TrackingNumber': dnd_awb[1], 
                            'TransportCompany': dnd_awb[0]})
                else:
                    upload_dn.update({'MODE': 'P'})
                upload_map[key] = upload_dn
            if not upload_dn['Items'].has_key(dnd.local_item.mg_item_code):
                upload_dn['Items'][dnd.local_item.mg_item_code] = {}
            if not upload_dn['Items'][dnd.local_item.mg_item_code].has_key(dnd.dn_no):
                upload_dn['Items'][dnd.local_item.mg_item_code][dnd.dn_no] = {
                    'ItemCode': dnd.local_item.mg_item_code, 
                    'PartialDeliveryDocument': dnd.dn_no, 
                    'PartialDeliveryDate': dnd.dn_date.strftime('%Y-%m-%d %H:%M:%S'), 
                    'InvoicedQty': dnd.dn_qty
                }
            else:
                item = upload_dn['Items'][dnd.local_item.mg_item_code][dnd.dn_no]
                item['InvoicedQty'] += dnd.dn_qty

    DBSession.add(MglobalSchedulerMg(**{'ci_date': dt.now(), 'qi_date': dt.now()}))
    for k, v in upload_map.iteritems():
        dn_items = []
        mg_cust_po = MglobalCustPo.get_by_cust_po_no(v['MGOrderNumber'], v['MGClientNumber'])
        if mg_cust_po:
            for i in mg_cust_po.detail:
                if v['Items'].has_key(i.item_no):
                    dn_items.extend(v['Items'][i.item_no].values())
        v['Items'] = dn_items
        results.append(v)
    transaction.commit()
    return results

def after_send_dn(flag, cust_po_no, client_id):
    if int(flag)==0:
        for dn in MglobalErpDND.find_updated_dn_by_po_and_client(cust_po_no, client_id):
            dn.has_update = False

def send_report_mail():

    def _gen_random_str(str_length, randomType=4):
        import random
        numberAlpha=[str(a) for a in range(10)]
        lowerAlpha=[chr(a) for a in range(ord("a"), ord("z")+1)]
        upperAlpha=[chr(a) for a in range(ord("A"), ord("Z")+1)]
        allAlpha=numberAlpha+lowerAlpha+upperAlpha
        randomRange = None
        if randomType==1:
            randomRange = numberAlpha
        elif randomType==2:
            randomRange = lowerAlpha
        elif randomType==3:
            randomRange = upperAlpha
        elif randomType==4:
            randomRange = allAlpha
        return ''.join(random.sample(randomRange, str_length))

    def _set_file_name():
        fileDir=os.path.join(config.download_dir, 'mglobal')
        if not os.path.exists(fileDir): os.makedirs(fileDir)
        return os.path.join(fileDir, "daily_report_%s.xls" % (dt.now().strftime("%Y%m%d%H%M%S")))

    def _gen_report(data):
        filename = _set_file_name()
        templatePath=os.path.join(os.path.abspath(os.path.curdir), "report_download/TEMPLATE/MGLOBAL_DAILY_REPORT_TEMPLATE.xls")
        pe = MglobalDailyExcel(templatePath=templatePath, destinationPath=filename)
        pe.inputData(data=data)
        pe.outputData()
        return filename

    def _send_email(_file):
        send_from = "r-pac-mglobal-report-system"
        send_to = config.mglobal_email.split(';')
        cc_to = config.mglobal_email_cc.split(";") if config.has_key('mglobal_email_cc') else []
        emailSubject = 'Mglobal Unconfirmed SO Daily Report'
        text = ["Attached Mglobal Unconfirmed SO Daily Report for your reference.",
            "This e-mail is sent by the r-pac Mglobal report system automatically.",
            "Please don't reply this e-mail directly!",
            "************************************************************************************"
            ]
        sendEmail(send_from, send_to, emailSubject, "\n".join(text), cc_to, [_file])

    dn_list = MglobalErpDND.find_blank_awb_dn()
    dn_map = {}
    for i in dn_list:
        if i.confirm_date and not dn_map.has_key(i.dn_no) and not i.awb_no and over_days(i.confirm_date)>1:
            dn_map[i.dn_no] = [
                i.so_no if i.so_no else '', 
                i.dr_no if i.dr_no else '', 
                i.dn_no if i.dn_no else '', 
                i.awb_no if i.awb_no else '', 
                i.confirm_date.strftime('%Y-%m-%d') if i.confirm_date else '', 
                over_days(i.confirm_date)
            ]
    filename = _gen_report(dn_map.values())
    print dn_map
    print filename
    _send_email(filename)
    print dn_map.values()

def _init_local_from_erp():
    #insert newset so dtl and hdr
    newest_date = MglobalSchedulerErp.get_last_date()
    qi_start_date = newest_date.qi_date.strftime('%Y-%m-%d 00:00:00') if newest_date else '2013-01-24 00:00:00'
    qi_end_date = dt.now().strftime('%Y-%m-%d 00:00:00')
    so_list = MglobalErpSO.find_from_erp_by_date(qi_start_date, qi_end_date)
    print 'add new so list size: %s' % len(so_list)
    for record in so_list:
        sod = MglobalErpSOD.merge(**{
                                'so_no':unicode(record[0]) if record[0] else None, 
                                'cust_po_no':unicode(record[1]) if record[1] else None, 
                                'customer_code':unicode(record[2]) if record[2] else None, 
                                'customer_name':unicode(record[3]) if record[3] else None, 
                                'line_no':unicode(record[4]) if record[4] else None, 
                                'item_code':unicode(record[5]) if record[5] else None, 
                                'order_qty':int(record[6]) if record[6] else None, 
                                'create_date':record[7]
                            })
    DBSession.add(MglobalSchedulerErp(**{'ci_date': dt.now(), 'qi_date': dt.now()}))
    client_id_list = MglobalMasterItem.find_client_id_list()
    mp_no_list = MglobalCustPo.find_cust_po_no(client_id_list)
    MglobalErpSO.update_in_mp_order(mp_no_list)

    #synchronize the uncomplete so hdr
    so_undone_list = MglobalErpSO.find_undone_mp_so()
    #so_undone_list = MglobalErpSO.find_undone_so()
    print 'undone so size: %s' % len(so_undone_list)
    so_undone_no_list = []
    so_undone_map = {}
    for i in so_undone_list:
        so_undone_no_list.append(i.so_no)
        so_undone_map[i.so_no] = i
    soh_so_list = MglobalErpSO.find_so_from_erp_by_so(so_undone_no_list)
    print 'search so size: %s' % len(soh_so_list)
    for i in soh_so_list:
        if so_undone_map[i[0]].so_qty != i[1]:
            soh = so_undone_map[i[0]]
            soh.has_update_so = True
            soh.so_qty = i[1]
    soh_si_list = MglobalErpSO.find_si_from_erp_by_so(so_undone_no_list)
    print 'search si size: %s' % len(soh_si_list)
    for i in soh_si_list:
        if so_undone_map[i[0]].so_invoice_qty != i[1]:
            soh = so_undone_map[i[0]]
            soh.has_update_si = True
            soh.so_invoice_qty = i[1]
            soh.cp_so_si = so_undone_map[i[0]].so_invoice_qty >= so_undone_map[i[0]].so_qty
    soh_dn_list = MglobalErpSO.find_dn_from_erp_by_so(so_undone_no_list)
    print 'search dn size: %s' % len(soh_dn_list)
    for i in soh_dn_list:
        if so_undone_map[i[0]].so_dn_qty != i[1]:
            soh = so_undone_map[i[0]]
            soh.has_update_dn = True
            soh.so_dn_qty = i[1]
            soh.cp_so_dn = so_undone_map[i[0]].so_dn_qty >= so_undone_map[i[0]].so_qty

def _process_local_so():
    #synchronize the updated dn dtl and so dtl
    so_updated_list = MglobalErpSO.find_updated_so()
    print 'updated so size: %s' % len(so_updated_list)
    total_updated_dn = 0
    total_updated_so = 0
    total_has_done = 0
    for i in so_updated_list:

        if i.has_update_so:
            #all_item_mapped_flag = True
            sod_list = MglobalErpSOD.find_from_erp_by_so([i.so_no])
            for record in sod_list:
                sod = MglobalErpSOD.merge(**{'local_so_id':i.id,
                                        'so_no':unicode(record[0]) if record[0] else None, 
                                        'cust_po_no':unicode(record[1]) if record[1] else None, 
                                        'customer_code':unicode(record[2]) if record[2] else None, 
                                        'customer_name':unicode(record[3]) if record[3] else None, 
                                        'line_no':unicode(str(record[4])) if record[4] else None, 
                                        'item_code':unicode(record[5]) if record[5] else None, 
                                        'order_qty':int(record[6]) if record[6] else None, 
                                        'create_date':record[7]
                                    })
                #if all_item_mapped_flag and not sod.local_item_id:
                    #all_item_mapped_flag = False
            i.has_update_so = False
            #i.all_item_mapped = all_item_mapped_flag
            total_updated_so+=1

        #if i.all_item_mapped and i.has_update_dn:
        if i.has_update_dn:
            dn_list = MglobalErpDND.find_from_erp_by_so([i.so_no])
            for index, record in enumerate(dn_list):
                dn = MglobalErpDND.merge(**{
                                        'so_no':unicode(record[0]) if record[0] else None, 
                                        'dn_no':unicode(record[1]) if record[1] else None, 
                                        'country':unicode(record[2]) if record[2] else None,
                                        'dr_no':unicode(record[3]) if record[3] else None,
                                        'dn_line_no':unicode(record[4]) if record[4] else None, 
                                        'so_line_no':unicode(record[5]) if record[5] else None, 
                                        'item_code':unicode(record[6]) if record[6] else None, 
                                        'dn_qty':int(record[7]) if record[7] else None,
                                        'dn_date':record[8], 
                                        'confirm_date':record[9], 
                                        'awb_attach':unicode(record[10]) if record[10] else None, 
                                    })
            i.has_update_dn = False

        #if i.cp_so_si and i.cp_so_dn:
        if i.cp_so_dn:
            i.has_done = True
            total_has_done+=1
    print 'processed total updated dn: %s; total updated so: %s; total done: %s' % (total_updated_dn, total_updated_so, total_has_done)

def _proess_blank_awb():
    dn_no_list = [dnd.dn_no for dnd in MglobalErpDND.find_blank_awb_dn()]
    dn_awb_list = MglobalErpDND.find_awb_from_erp_by_dn(dn_no_list)
    for i in dn_awb_list:
        MglobalErpDND.update_blank_awb_dn(i[0], i[3])

class MglobalMasterTransCompany(DeclarativeBase, SysMixin):
    __tablename__ = 'mglobal_master_trans_company'

    id = Column(Integer, primary_key=True)
    code = Column(Unicode(100))
    name = Column(Unicode(100))
    name_cn = Column(Unicode(100))

class MglobalMasterClient(DeclarativeBase, SysMixin):
    __tablename__ = 'mglobal_master_client'

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer)
    client_name = Column(Unicode(100))
    erp_program = Column(Unicode(100))
    erp_brand = Column(Unicode(100))

    @classmethod
    def get_client(cls, program, brand):
        return DBSession.query(cls).filter(and_(cls.erp_program==program, cls.erp_brand==brand)).first()

class MglobalMasterItem(DeclarativeBase, SysMixin):
    __tablename__ = 'mglobal_master_item'

    id = Column(Integer, primary_key=True)
    erp_program = Column(Unicode(100))
    erp_brand = Column(Unicode(100))
    erp_item_code = Column(Unicode(100))
    mg_item_code = Column(Unicode(100))
    local_client_id = Column(Integer, ForeignKey('mglobal_master_client.id'))
    local_client_client_id = Column(Integer)
    local_client = relation(MglobalMasterClient, primaryjoin=local_client_id == MglobalMasterClient.id)

    @classmethod
    def init_master_data(cls):
        for i in DBSession.query(cls).filter(cls.local_client_id==None).all():
            sql = "SELECT DISTINCT tih.ITEM_CODE,tih.PROGRAM,tih.BRAND FROM t_item_hdr tih WHERE tih.ITEM_CODE='%s' and tih.COMPANY_CODE IN ('RPACEU','RPACPACKEU')" % i.erp_item_code
            records = searchOracle(sql, {})
            if records:
                record = records[0]
                if not i.erp_program or not i.erp_brand:
                    i.erp_program = record[1]
                    i.erp_brand = record[2]
                local_client = MglobalMasterClient.get_client(record[1], record[2])
                if local_client:
                    i.local_client_id = local_client.id
                    
    @classmethod
    def find_client_id_list(cls):
        return [unicode(i[0]) for i in DBSession.query(cls.local_client_client_id).distinct().all()]

    @classmethod
    def get_by_erp_code(cls, erp_code):
        try:
            return DBSession.query(cls).filter(and_(cls.erp_item_code == erp_code, cls.active == 0)).first()
        except Exception, e:
            return None

class MglobalSchedulerErp(DeclarativeBase, SysMixin):
    __tablename__ = 'mglobal_scheduler_erp'

    id = Column(Integer, primary_key=True)
    qi_date = Column(DateTime)
    ci_date = Column(DateTime, default=dt.now())

    @classmethod
    def get_last_date(cls):
        try:
            return DBSession.query(cls).order_by('id desc').first()
        except Exception, e:
            log.exception(str(e))
            return None

class MglobalSchedulerMg(DeclarativeBase, SysMixin):
    __tablename__ = 'mglobal_scheduler_mg'
    
    id = Column(Integer, primary_key=True)
    qi_date = Column(DateTime)
    ci_date = Column(DateTime, default=dt.now())

    @classmethod
    def get_last_date(cls):
        try:
            return DBSession.query(cls).order_by('id desc').first()
        except Exception, e:
            log.exception(str(e))
            return None

class MglobalErpSO(DeclarativeBase, SysMixin):
    __tablename__ = "mglobal_erp_so"

    id = Column(Integer, primary_key=True)

    so_no = Column(Unicode(100))
    cust_po_no = Column(Unicode(100))
    customer_code = Column(Unicode(100))
    customer_name = Column(Unicode(1000))

    so_qty = Column(Integer)
    so_invoice_qty = Column(Integer)
    so_dn_qty = Column(Integer)

    cp_so_si = Column(Boolean)
    cp_so_dn = Column(Boolean)
    has_update_so = Column(Boolean)
    has_update_si = Column(Boolean)
    has_update_dn = Column(Boolean)
    has_done = Column(Boolean)
    #all_item_mapped = Column(Boolean)
    in_mp_order = Column(Boolean)

    @classmethod
    def get(cls, id):
        try:
            DBSession.query(cls).get(int(id))
        except Exception, e:
            log.exception(str(e))
            return None

    @classmethod
    def get_so(cls, so_no):
        try:
            return DBSession.query(cls).filter(cls.so_no == unicode(so_no)).first()
        except Exception, e:
            log.exception(str(e))
            return None

    @classmethod
    def find_from_erp_by_so(cls, so_list):
        sql = '''
            SELECT tsh.SALES_CONTRACT_NO,tsh.CUST_PO_NO,tsh.CUSTOMER_CODE,tsh.CUSTOMER_NAME,tsp.LINE_NO,tsp.ITEM_CODE,tsp.ORDER_QTY,tsh.CREATE_DATE
                FROM t_sales_contract_packset tsp, t_sales_contract_hdr tsh
                WHERE tsh.COMPANY_CODE IN ('RPACEU','RPACPACKEU') AND tsh.ORDER_DEPT='ADMIN'
                AND tsh.SALES_CONTRACT_NO=tsp.SALES_CONTRACT_NO
                AND (%s)
        ''' % 'tsh.SALES_CONTRACT_NO=\'%s\'' % ('\' or tsh.SALES_CONTRACT_NO=\''.join(so_list))
        return searchOracle(sql, {})

    @classmethod
    def find_from_erp_by_date(cls, qi_start_date, qi_end_date):
        sql = '''
            SELECT tsh.SALES_CONTRACT_NO,tsh.CUST_PO_NO,tsh.CUSTOMER_CODE,tsh.CUSTOMER_NAME,tsp.LINE_NO,tsp.ITEM_CODE,tsp.ORDER_QTY,tsh.CREATE_DATE
                FROM t_sales_contract_packset tsp, t_sales_contract_hdr tsh
                WHERE tsh.COMPANY_CODE IN ('RPACEU','RPACPACKEU') AND tsh.ORDER_DEPT='B'
                AND tsh.SALES_CONTRACT_NO=tsp.SALES_CONTRACT_NO
                AND tsh.CREATE_DATE >= TO_DATE('%s','YYYY-MM-DD HH24:MI:SS')
                AND tsh.CREATE_DATE <= TO_DATE('%s','YYYY-MM-DD HH24:MI:SS')
        ''' % (qi_start_date, qi_end_date)
        print sql
        return searchOracle(sql, {})

    @classmethod
    def find_undone_so(cls):
        return DBSession.query(cls).filter(or_(cls.has_done==None, cls.has_done!=True)).all()

    @classmethod
    def find_undone_mp_so(cls):
        return DBSession.query(cls).filter(or_(cls.has_done==None, cls.has_done!=True)).filter(cls.in_mp_order==True).all()

    @classmethod
    def find_updated_so(cls):
        return DBSession.query(cls).filter(or_(cls.has_update_dn == True)).all()

    @classmethod
    def find_so_from_erp_by_so(cls, so_list):
        if so_list:
            sql = '''
                SELECT tsp.SALES_CONTRACT_NO SO_NO, SUM(tsp.ORDER_QTY) SO_QTY FROM t_sales_contract_packset tsp
                    WHERE tsp.COMPANY_CODE IN ('RPACEU','RPACPACKEU') AND (%s)
                    GROUP BY tsp.SALES_CONTRACT_NO
            ''' % 'tsp.SALES_CONTRACT_NO=\'%s\'' % ('\' or tsp.SALES_CONTRACT_NO=\''.join(so_list))
            return searchOracle(sql, {})
        else:
            return []

    @classmethod
    def find_si_from_erp_by_so(cls, so_list):
        if so_list:
            sql = '''
                SELECT tid.SC_NO SO_NO, SUM(tid.QTY) SO_INVOICE_QTY FROM t_invoice_dtl tid
                    WHERE tid.COMPANY_CODE IN ('RPACEU','RPACPACKEU') AND (%s)
                    GROUP BY tid.SC_NO
            ''' % 'tid.SC_NO=\'%s\'' % ('\' or tid.SC_NO=\''.join(so_list))
            return searchOracle(sql, {})
        else:
            return []

    @classmethod
    def find_dn_from_erp_by_so(cls, so_list):
        if so_list:
            sql = '''
                SELECT tdp.SC_NO SO_NO, SUM(tdp.QTY) SO_DN_QTY FROM t_dn_product tdp
                    WHERE tdp.COMPANY_CODE IN ('RPACEU','RPACPACKEU') AND (%s)
                    GROUP BY tdp.SC_NO
            ''' % 'tdp.SC_NO=\'%s\'' % ('\' or tdp.SC_NO=\''.join(so_list))
            return searchOracle(sql, {})
        else:
            return []

    @classmethod
    def update_in_mp_order(cls, cust_po_no_list):
        if cust_po_no_list:
            sql = 'update mglobal_erp_so set in_mp_order=true where (%s) and (in_mp_order=false or in_mp_order is null)' % 'cust_po_no=\'%s\'' % '\' or cust_po_no=\''.join(cust_po_no_list)
            DBSession.execute(sql)

class MglobalErpSOD(DeclarativeBase, SysMixin):
    __tablename__ = "mglobal_erp_sod"

    id = Column(Integer, primary_key=True)
    local_so_id = Column(Integer, ForeignKey('mglobal_erp_so.id'))
    local_so = relation(MglobalErpSO, primaryjoin=local_so_id == MglobalErpSO.id, backref='local_sods')

    local_item_id = Column(Integer, ForeignKey('mglobal_master_item.id'))
    local_item = relation(MglobalMasterItem, primaryjoin=local_item_id == MglobalMasterItem.id)

    so_no = Column(Unicode(100))
    line_no = Column(Integer)
    item_code = Column(Unicode(100))
    order_qty = Column(Integer)
    create_date = Column(DateTime)

    has_update = Column(Boolean)

    @classmethod
    def merge(cls, **kw):
        try:
            sod = cls.get_sod(kw['so_no'], kw['line_no'])
            if not sod:
                soh = MglobalErpSO.get_so(kw['so_no']) if not kw.has_key('local_so_id') else MglobalErpSO.get(kw['local_so_id'])
                if not soh:
                    soh = MglobalErpSO(**{'so_no':kw['so_no'], 'cust_po_no':kw['cust_po_no'], 'customer_code':kw['customer_code'], 'customer_name':kw['customer_name']})
                    DBSession.add(soh)
                    DBSession.flush()
                sod = cls(**{'local_so_id':soh.id, 'so_no':kw['so_no'], 'line_no':kw['line_no'], 'item_code':kw['item_code'], 'order_qty':kw['order_qty'], 'create_date':kw['create_date']})
                item = MglobalMasterItem.get_by_erp_code(sod.item_code)
                if item:
                    sod.local_item_id = item.id
                DBSession.add(sod)
            else:
                sod.order_qty = kw['order_qty']
                item = MglobalMasterItem.get_by_erp_code(sod.item_code)
                if item:
                    sod.local_item_id = item.id
            return sod
        except Exception, e:
            log.exception(str(e))
            raise

    @classmethod
    def get_sod(cls, so_no, line_no):
        try:
            return DBSession.query(cls).filter(and_(cls.so_no == so_no, cls.line_no == line_no)).first()
        except Exception, e:
            log.exception(str(e))
            return None

    @classmethod
    def find_from_erp_by_so(cls, so_list):
        if so_list:
            sql = '''
                SELECT tsh.SALES_CONTRACT_NO,tsh.CUST_PO_NO,tsh.CUSTOMER_CODE,tsh.CUSTOMER_NAME,tsp.LINE_NO,tsp.ITEM_CODE,tsp.ORDER_QTY,tsh.CREATE_DATE
                    FROM t_sales_contract_packset tsp, t_sales_contract_hdr tsh
                    WHERE tsh.COMPANY_CODE IN ('RPACEU','RPACPACKEU') AND tsh.ORDER_DEPT='B'
                    AND tsh.SALES_CONTRACT_NO=tsp.SALES_CONTRACT_NO
                    AND tsh.CREATE_DATE <= TO_DATE('%s','YYYY-MM-DD HH24:MI:SS')
                    AND (%s)
            ''' % (dt.now().strftime('%Y-%m-%d 00:00:00'), 'tsh.SALES_CONTRACT_NO=\'%s\'' % ('\' or tsh.SALES_CONTRACT_NO=\''.join(so_list)))
            return searchOracle(sql, {})
        else:
            return []

class MglobalErpDND(DeclarativeBase, SysMixin):
    __tablename__ = 'mglobal_erp_dnd'

    id = Column(Integer, primary_key=True)

    so_no = Column(Unicode(100))
    so_line_no = Column(Integer)
    dn_no = Column(Unicode(100))
    dn_line_no = Column(Integer)
    dn_qty = Column(Integer)
    dn_date = Column(DateTime)

    item_code = Column(Unicode(100))
    country = Column(Unicode(100))
    dr_no = Column(Unicode(100))

    confirm_date = Column(DateTime)
    awb_no = Column(Unicode(100))
    awb_corp = Column(Unicode(100))
    awb_attach = Column(Unicode(100))

    cust_po_no = Column(Unicode(100))
    local_so_id = Column(Integer, ForeignKey('mglobal_erp_so.id'))
    local_so = relation(MglobalErpSO, primaryjoin=local_so_id == MglobalErpSO.id)

    local_item_id = Column(Integer, ForeignKey('mglobal_master_item.id'))
    local_item = relation(MglobalMasterItem, primaryjoin=local_item_id == MglobalMasterItem.id)

    client_id = Column(Integer)
    local_client_id = Column(Integer, ForeignKey('mglobal_master_client.id'))
    local_client = relation(MglobalMasterClient, primaryjoin=local_client_id == MglobalMasterClient.id)

    has_update = Column(Boolean)

    def compare(self, *args, **kwargs):
        keys = args if args else kwargs.keys()
        for k,v in keys:
            if str(getAttr(self, k)) != str(kwargs[v]):
                return False
        return True

    @classmethod
    def merge(cls, **kw):

        def _update_awb(dnd):
            dnd_awb = dnd.get_awb()
            if dnd_awb:
                dnd.awb_corp, dnd.awb_no = dnd_awb
            return dnd

        dnd = cls.get_dnd(kw['dn_no'], kw['dn_line_no'])
        if not dnd:
            dnd = cls(**kw)
            local_so = MglobalErpSO.get_so(dnd.so_no)
            dnd.local_so_id = local_so.id
            dnd.cust_po_no = local_so.cust_po_no
            item = MglobalMasterItem.get_by_erp_code(dnd.item_code)
            if item:
                dnd.local_item_id = item.id
                dnd.local_client_id = item.local_client.id
                dnd.client_id = item.local_client.client_id
                dnd.has_update = True
            else:
                dnd.has_update = None
            _update_awb(dnd)
            DBSession.add(dnd)
        elif not dnd.awb_no:
            _update_awb(dnd)
#        elif not self.compare(**kw):
#            dnd.dn_qty = kw['dn_qty']
#            dnd.dn_date = kw['dn_date']
#            dnd.awb_no = kw['awb_no']
#            dnd.item_code = kw['item_code']
#            item = MglobalMasterItem.get_by_erp_code(dnd.item_code)
#            if item:
#                dnd.local_item_id = item.id
#                dnd.has_update = True
#            else:
#                dnd.has_update = None
        return dnd

    def get_awb(self):
        companies = DBSession.query(MglobalMasterTransCompany).all()
        if self.country.upper() == '852HK' and self.dr_no:
            return [None, unicode(self.dr_no)]
        elif self.awb_no:
            corp_name = []
            awb_name = []
            for no in self.awb_no.split('/'):
                for corp in companies:
                    if no.upper().startswith(corp.code):
                        awb_no = no.split('_')[0]
                        corp_name.append(corp.code)
                        awb_name.append(awb_no)
            return [unicode('/'.join(list(set(corp_name)))), unicode('/'.join(awb_name))]
        return None

    @classmethod
    def get_dnd(cls, dn_no, dn_line_no):
        try:
            return DBSession.query(cls).filter(and_(cls.dn_no==dn_no, cls.dn_line_no==dn_line_no)).first()
        except Exception, e:
            return None

    @classmethod
    def update_blank_awb_dn(cls, dn_no, awb_no):
        if awb_no and dn_no:
            sql = '''
                update mglobal_erp_dnd set awb_no='%s' where dn_no='%s'
            ''' % (awb_no, dn_no)
            DBSession.execute(sql)

    @classmethod
    def find_blank_awb_dn(cls):
        return DBSession.query(cls).filter(or_(cls.awb_no==None, cls.awb_no==u'')).all()

    @classmethod
    def find_updated_dn(cls):
        return DBSession.query(cls).filter(cls.has_update==True).order_by(desc(cls.dn_date)).all()

    @classmethod
    def find_updated_dn_by_po_and_client(cls, cust_po_no, client_id):
        return DBSession.query(cls).filter(and_(cls.has_update==True, cls.client_id==client_id)).order_by(desc(cls.dn_date)).all()

    @classmethod
    def find_awb_from_erp_by_dn(cls, dn_list):
        dn_awb_sql = '''
            SELECT DISTINCT tdh.DN_NO, tdh.CREATE_DATE,tdh.CONFIRM_DATE, tda.NAME AWB_NO FROM t_dn_hdr tdh,t_dn_attach tda
                WHERE tdh.COMPANY_CODE IN ('RPACEU','RPACPACKEU') AND tdh.DN_NO = tda.DN_NO(+)
                AND tdh.DN_NO IN ('%s')
        ''' % '\',\''.join(dn_list)
        dn_awb_result = searchOracle(dn_awb_sql, {})
        dn_awb_map = {}
        for i in dn_awb_result:
            if dn_awb_map.has_key(i[0]):
                dn_awb_map[i[0]][3]+=('/'+i[3])
            else:
                dn_awb_map[i[0]]=list(i)
        return dn_awb_map.values()

    @classmethod
    def find_from_erp_by_so(cls, so_list):
        if so_list:
            dn_sql = ''' 
                SELECT tdp.SC_NO SO_NO,tdp.DN_NO,tdrh.COUNTRY,tdrh.DELIVERY_REQUEST_NO DR_NO,tdp.LINE_NO DN_Line_No,tdp.SC_LINE_NO SO_Line_No,tdp.ITEM_NO,tdp.QTY DN_QTY
                    FROM t_dn_product tdp,t_delivery_request_hdr tdrh
                    WHERE tdp.SC_NO in ('%s')
                    AND tdp.DELIVERY_REQ_NO=tdrh.DELIVERY_REQUEST_NO
            ''' % '\',\''.join(so_list)
            dn_result = searchOracle(dn_sql, {})
            dn_no_map = {}
            for i in dn_result:
                dn_item_list = dn_no_map.get(i[1], [])
                dn_item_list.append(list(i))
                dn_no_map[i[1]] = dn_item_list
            dn_no_list = dn_no_map.keys()

            for i in cls.find_awb_from_erp_by_dn(dn_no_list):
                dn_item_list = dn_no_map.get(i[0], [])
                for dn_item in dn_item_list:
                    dn_item.extend(i[1:4])
            result = []
            for i in dn_no_map.values():
                result.extend(i)
            return result
        else:
            return []

class MglobalTotalResult(DeclarativeBase, SysMixin):
    __tablename__ = "mglobal_total_result"

    id = Column(Integer, primary_key=True)
    flag = Column(Text)
    msg = Column(Text)

class MglobalResult(DeclarativeBase, SysMixin):
    __tablename__ = "mglobal_result"

    id = Column(Integer, primary_key=True)
    total_result_id = Column(Integer, ForeignKey('mglobal_total_result.id'))
    total_result = relation(MglobalTotalResult)
    mglobal_no = Column(Text)
    cust_no = Column(Text)
    si_no = Column(Text)
    flag = Column(Text)
    msg = Column(Text)
    content = Column(Text)

class MglobalCustPo(DeclarativeBase, SysMixin):
    __tablename__ = 'mglobal_cust_po'

    id = Column(Integer, primary_key=True)
    cust_po_no = Column(Unicode(100))
    cust_no = Column(Unicode(100))

    @classmethod
    def find_all_cust_po_no(cls):
        return [i.cust_po_no for i in DBSession.query(cls).all()]
        
    @classmethod
    def find_cust_po_no(cls, cust_no_list):
        return [i.cust_po_no for i in DBSession.query(cls).filter(cls.cust_no.in_(cust_no_list)).all()]

    @classmethod
    def get_by_cust_po_no(cls, po_no, cust_no):
        try:
            return DBSession.query(cls).filter(and_(cls.cust_po_no == po_no,cust_no==cust_no)).first()
        except Exception, e:
            log.exception(str(e))
            return None

#    @classmethod
#    def add(cls, mgp_pos):
#        for obj in mgp_pos:
#            if not obj.po_no or not obj.cust_no: continue
#            if not cls.get_by_cust_po_no(obj.po_no,obj.cust_no):
#                DBSession.add(cls(cust_po_no=obj.po_no,cust_no=obj.cust_no))

class MglobalCustPoDetail(DeclarativeBase, SysMixin):
    __tablename__ = 'mglobal_cust_po_detail'

    id = Column(Integer, primary_key=True)
    header_id = Column(Integer, ForeignKey('mglobal_cust_po.id'))
    header = relation(MglobalCustPo, backref="detail")

    item_no = Column(Text)
    qty = Column(Integer, default=0)

'''
SELECT b.SO_NO, b.DN_NO, a.CREATE_DATE DN_Date, DECODE(b.COUNTRY,'852HK',b.DR_NO,a.AWB_NO) AWB_NO, b.DN_Line_No, b.SO_Line_No, b.ITEM_NO, b.DN_QTY FROM
                    (SELECT DISTINCT tdh.DN_NO, tdh.CREATE_DATE, DECODE(SUBSTR(tda.NAME,1,3),'AWB',tda.NAME,NULL) AWB_NO FROM t_dn_hdr tdh,t_dn_attach tda,
                        (SELECT DISTINCT tdp.DN_NO FROM t_dn_product tdp WHERE (%s)) dn_tdp
                        WHERE tdh.COMPANY_CODE IN ('RPACEU','RPACPACKEU') AND tdh.DN_NO = tda.DN_NO(+) AND tdh.DN_NO=dn_tdp.DN_NO) a,
                    (SELECT tdp.SC_NO SO_NO,tdp.DN_NO,tdrh.COUNTRY,tdrh.DELIVERY_REQUEST_NO DR_NO,tdp.LINE_NO DN_Line_No,tdp.SC_LINE_NO SO_Line_No,tdp.ITEM_NO,tdp.QTY DN_QTY
                        FROM t_dn_product tdp,t_delivery_request_hdr tdrh
                        WHERE (%s)
                        AND tdp.DELIVERY_REQ_NO=tdrh.DELIVERY_REQUEST_NO) b
                WHERE a.DN_NO = b.DN_NO

SELECT b.SO_NO, b.DN_NO, a.CREATE_DATE DN_Date,b.CONFIRM_DATE, DECODE(b.COUNTRY,'852HK',b.DR_NO,a.AWB_NO) AWB_NO, b.DN_Line_No, b.SO_Line_No, b.ITEM_NO, b.DN_QTY FROM
        (SELECT DISTINCT tdh.DN_NO, tdh.CREATE_DATE,tdh.CONFIRM_DATE, DECODE(SUBSTR(tda.NAME,1,3),'AWB',tda.NAME,NULL) AWB_NO FROM t_dn_hdr tdh,t_dn_attach tda,
                   (SELECT DISTINCT tdp.DN_NO FROM t_dn_product tdp WHERE tdp.SC_NO IN ('SOB1202652-EPG' )) dn_tdp
                   WHERE tdh.COMPANY_CODE IN ('RPACEU','RPACPACKEU') AND tdh.DN_NO = tda.DN_NO(+) AND tdh.DN_NO=dn_tdp.DN_NO) a,
        (SELECT tdp.SC_NO SO_NO,tdp.DN_NO,tdrh.COUNTRY,tdrh.DELIVERY_REQUEST_NO DR_NO,tdp.LINE_NO DN_Line_No,tdp.SC_LINE_NO SO_Line_No,tdp.ITEM_NO,tdp.QTY DN_QTY,tdh.CONFIRM_DATE
                   FROM t_dn_product tdp,t_delivery_request_hdr tdrh,t_dn_hdr tdh
                   WHERE tdp.SC_NO IN ('SOB1202652-EPG') AND tdh.DN_NO=tdp.DN_NO
                   AND tdp.DELIVERY_REQ_NO=tdrh.DELIVERY_REQUEST_NO) b
WHERE a.DN_NO = b.DN_NO

SELECT tdp.SC_NO SO_NO,tdp.DN_NO,tdrh.COUNTRY,tdrh.DELIVERY_REQUEST_NO DR_NO,tdp.LINE_NO DN_Line_No,tdp.SC_LINE_NO SO_Line_No,tdp.ITEM_NO,tdp.QTY DN_QTY
                   FROM t_dn_product tdp,t_delivery_request_hdr tdrh
                   WHERE tdp.SC_NO IN ('SOB1202652-EPG')
                   AND tdp.DELIVERY_REQ_NO=tdrh.DELIVERY_REQUEST_NO

SELECT DISTINCT tdh.DN_NO, tdh.CREATE_DATE,tdh.CONFIRM_DATE, tda.NAME AWB_NO FROM t_dn_hdr tdh,t_dn_attach tda
                   WHERE tdh.COMPANY_CODE IN ('RPACEU','RPACPACKEU') AND tdh.DN_NO = tda.DN_NO(+)
                   AND tdh.DN_NO IN ('DND12003998-EPG','DND12003999-EPG')
'''
