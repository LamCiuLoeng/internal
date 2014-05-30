# -*- coding: utf-8 -*-
import traceback

from pylons import cache
from tg import config
from tribal.model import *
from tribal.util.oracle_helper import *

__all__ = ['getOrsayCustomerList', 'getOrsayCustomerInfo', 'getOrsayWashingList', 'getOrsayWashingDetailInfo', 'populateTranslation', 'populateTranslation1']

def getOrsayCustomerList():
    def _getInfo():
        '''
        sql = [
            "select distinct(th.CUSTOMER_CODE),th.CUSTOMER_NAME from t_sales_contract_dtl td,t_sales_contract_hdr th ",
            "where td.program='ORSAY' and td.company_code='RPACEU' and brand like '%ORSAY%' and td.SALES_CONTRACT_NO=th.SALES_CONTRACT_NO",
            "and td.COMPANY_CODE=th.COMPANY_CODE",
            "order by th.CUSTOMER_NAME"
            ]
        '''
        sql = ["select distinct(th.CUST_CODE),th.CUST_NAME from t_cust_hdr th where th.company_code='RPACEU' and th.STATUS='1' order by th.CUST_NAME"]
        return searchOracle("\n".join(sql), {})
    return _getCacheOrSearch("orsay_customer_list", "all", _getInfo)

def getOrsayCustomerInfo(cn):
    
    def _getInfo():
        billto_sql = [
            "select tc.ADDRESS_1||tc.ADDRESS_2||tc.ADDRESS_3||tc.ADDRESS_4 BillTo,tc.CONTACT_SALES,tc.TEL_NO,",
            "tc.COMPANY_CODE,tc.CUST_NAME,tc.CUST_CODE,tc.LINE_NO,tc.STATUS,tc.CITY, tc.COUNTRY, tc.EXTENSION,tc.FAX_NO,tc.BASE_CCY,tc.PAY_TERM",
            "from t_cust_hdr tc",
            "where tc.CUST_CODE=:P_Customer",
            "and tc.COMPANY_CODE='RPACEU' and tc.STATUS=1  "
            ]
        
        shipto_sql = [
            "select tcd.ADDRESS_1||tcd.ADDRESS_2||tcd.ADDRESS_3||tcd.ADDRESS_4 ShipTo,tcd.CONTACT_PERSON,tcd.TEL_NO,",
            "tcd.CUST_CODE,tcd.COMPANY_CODE,tcd.CITY,tcd.COUNTRY,tcd.STATUS,tcd.FAX_NO",
            "from t_cust_hdr tc, t_cust_deliv_addr    tcd ",
            "where tc.CUST_CODE=:P_Customer",
            "and tc.LINE_NO=tcd.HDR_LINE_NO",
            "and tc.COMPANY_CODE='RPACEU'",
            ]
        return {
            "billto": searchOracle("\n".join(billto_sql), {"P_Customer":str(cn)}),
            "shipto": searchOracle("\n".join(shipto_sql), {"P_Customer":str(cn)}),
            }

    return _getCacheOrSearch("orsay_customer_head", cn, _getInfo)

def getOrsayWashingList(cat, season):  

    def _getInfo():
        return DBSession.query(OrsayWashing).filter(OrsayWashing.active == 0).filter(OrsayWashing.type == cat).filter(OrsayWashing.season == season).order_by(OrsayWashing.englisch).all()
    
    return _getCacheOrSearch("orsay_washing_instruction", '%s%s' % (cat, season), _getInfo)

def getOrsayWashingDetailInfo(id):
    
    def _getInfo():
        return DBSession.query(OrsayWashing).get(id)
    
    return _getCacheOrSearch("orsay_washing_instruction", "washing_%d" % id, _getInfo)

def _getCacheOrSearch(namepace, key, fun, expiretime=60 * 5):
    if config.get("use_cache", None) == "true":
        print "-------- cached ----------"
        c = cache.get_cache(namepace)
        return c.get_value(key=key, createfunc=fun, expiretime=expiretime)
    else:
        print "-------- no cache --------"
        return fun()

def populateTranslation(obj, style=' / ', default="", attrs=["deutsch", "franzosisch", "polnisch", "ungarisch", "tcheschisch", "englisch", "slowakisch", "rumanisch", "slowenisch"]):
    if not obj: 
        return default
    elif obj.season == 's12':
        attrs = ["englisch", "deutsch", "polnisch", "franzosisch", "ungarisch", "tcheschisch", "slowakisch", "rumanisch", "slowenisch", "russisch"]
    try:
        content = []
        for a in attrs: content.append(getattr(obj, a))
        return style.join(content)
    except:
        traceback.print_exc()
        return defalut

def populateTranslation1(obj, style=' / ', default=""):
    return populateTranslation(obj, style, default, ["deutsch", "franzosisch", "englisch", "polnisch", "ungarisch", "tcheschisch", "slowakisch", "rumanisch", "slowenisch"])
