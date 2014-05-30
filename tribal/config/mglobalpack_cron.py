# -*- coding: utf-8 -*-
import traceback
import logging
import json
import transaction
from datetime import datetime as dt,date
from tgscheduler import start_scheduler
from tgscheduler.scheduler import add_weekday_task, add_interval_task

from suds.client import Client
from tribal.model import DBSession
from tribal.model.mglobalpack import get_mglobal_upload_data, MglobalResult,\
    MglobalTotalResult, after_send_dn, send_report_mail

__all__ = ['sendInfo2mglobalpack',]


_datetime_format = '%Y-%m-%d %H:%M:%S'

#logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)
#logging.getLogger('suds.transport').setLevel(logging.DEBUG)
#logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
#logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)



def sendInfo2mglobalpack():
    start_scheduler()
    add_interval_task(action=_sendInfo, interval = 60*60*24, initialdelay=10)
    #add_weekday_task(action=_sendInfo, weekdays=range(1,8), timeonday=(23, 59))
    


#===============================================================================
# scan the ERP and get back the required  SO
# @return: a list of SO ,for example :
# [ [MGOrderNumber,InvoiceDate,InvoiceNumber,TrackingNumber,
#    TransportCompany,OptionalNote, [(ItemCode,InvoicedQty),...]],... ]
#===============================================================================
def _fetchDataFromERP():
    data = get_mglobal_upload_data()
    return data
    #for testing
    return [
            {
             "MGOrderNumber" : '101569',
             "MGClientNumber" : 1,
             "MODE" : "C",  # C or P
             "InvoiceDate" : dt.strptime('10/19/12','%m/%d/%y').date(),
             "InvoiceNumber" : 'SOB1208456-E',
             "TrackingNumber" : 'SF852904590864',
             "TransportCompany" : 'SF',
             "OptionalNote" : '',
             "Items" : [{"ItemCode" : '22', "InvoicedQty" : 6110,
                         "PartialDeliveryDocument" :'DND12006957-E', "PartialDeliveryDate" : dt.strptime('10/19/12','%m/%d/%y').date()},
                        ]
             },  
                          
            ]
            


#===============================================================================
# format the ERP data to be feed the mglobalpack system
#===============================================================================
def _format_data(data,client):
    orders = client.factory.create('SDT_RtracOrdersToFinalize')
    for d in data:
        tmp = {}
        for f in ['MGOrderNumber','MGClientNumber','MODE','InvoiceDate','InvoiceNumber',
                  'TrackingNumber','TransportCompany','OptionalNote']:  
            if f in d : tmp[f] = d[f]
            
        if d.has_key('InvoiceDate'):
            si_date = d['InvoiceDate']
            tmp['InvoiceDate'] = None
            if isinstance(si_date,basestring) and si_date:
                tmp['InvoiceDate'] = dt.strptime(si_date,_datetime_format)
            elif isinstance(si_date, (date,dt)):
                tmp['InvoiceDate'] = si_date

        items = []
        for i in d['Items']:
            item = {}
            item['ItemCode'] = i['ItemCode'] if not i['ItemCode'].startswith('0') else i['ItemCode'][1:]  
            item['InvoicedQty'] = i['InvoicedQty']
            item['PartialDeliveryDocument'] = i['PartialDeliveryDocument']
            
            item['PartialDeliveryDate'] = '' #to be update
            if isinstance(i['PartialDeliveryDate'],basestring) and i['PartialDeliveryDate']:
                item['PartialDeliveryDate'] = dt.strptime(i['PartialDeliveryDate'],_datetime_format)
            elif isinstance(i['PartialDeliveryDate'], (date,dt)): 
                item['PartialDeliveryDate'] = i['PartialDeliveryDate']
                 
            items.append(item)             
        tmp['Items'] = {'Item' : items}
        orders['SDT_RtracOrdersToFinalize.Order'].append(tmp)
    return orders



#===============================================================================
# parse the SOAP result in the format
# {
#    'GeneralResult': 2,
#    'OrderResult': [{'Result': 12, 'MGOrderNumber': 101109}], 
# }
#===============================================================================
def _parse_result(result):
    r = {
     'GeneralResult' : result.GeneralResult,
     }
    if getattr(result,'OrderLevelResults',None):
        OrderLevelResults = []
        for k in result.OrderLevelResults.OrderResult:
            OrderLevelResults.append({
                                      'MGOrderNumber' : k[0],
                                      'MGClientNumber' : k[1],
                                      'Result' : k[2] 
                                      })
        r['OrderResult'] =  OrderLevelResults
    else:
        r['OrderResult'] = []
    return r                         


#===============================================================================
# log the return result back to db ,for the check later
#===============================================================================
def _insert_result_db(result,data):
    total_msg_mapping = {
                        "1" : "No error, all the orders was processed successfully.",
                        "2" : "Some orders have a specific error.",
                        "3" : "Internal error, we can’t finalize your orders.",
                        "4" : "No orders to finalize.",
                         }
    
    level_msg_mapping = {
                    "0" : "Success",
                    "1" : "Finalized date is required",
                    "2" : "Invoice number is required",
                    "3" : "Invoice date must not be greater than two days from today.",
                    "4" : "Tracking number is required",
                    "5" : "Invoice date corresponds to a closed period.",
                    "10" : "Order is not at Received status.",
                    "11" : "Order is not a HK's order.",
                    "12" : "Order is not found",
                    "13" : "Internal error.",
                    "14" : "Order contains not matching items.",
                    "15" : "No items to finalize.",
                   }
    mapping = {}
    try:
        header = MglobalTotalResult(
                           flag = unicode(result['GeneralResult']),
                           msg = unicode(total_msg_mapping.get(unicode(result['GeneralResult']), '')),
                           )
        DBSession.add(header)
        for d in data :  
            mapping['%s-%s' % (d['MGOrderNumber'], d['MGClientNumber'])] = d
            if d.has_key('InvoceDate'):
                si_date = d['InvoiceDate'] 
                if si_date and isinstance(si_date, (date,dt)):
                    d['InvoiceDate'] = si_date.strftime(_datetime_format)
                else:
                    d['InvoiceDate'] = unicode(si_date)

            for item in d["Items"]:
                tmp_date = item['PartialDeliveryDate']
                if tmp_date and isinstance(tmp_date, (date,dt)):
                    item['PartialDeliveryDate'] = tmp_date.strftime(_datetime_format)
                else:
                    item['PartialDeliveryDate'] = unicode(tmp_date)
                    
                
        for line in result['OrderResult']:
            so_info = mapping.get('%s-%s' % (line['MGOrderNumber'], line['MGClientNumber']), '')   
            DBSession.add(MglobalResult(
                                        total_result = header,
                                        mglobal_no = unicode(line['MGOrderNumber']),
                                        si_no = unicode(so_info.get('InvoiceNumber', None)),
                                        flag = unicode(line['Result']),
                                        cust_no = unicode(line['MGClientNumber']),
                                        msg = unicode(level_msg_mapping.get(unicode(line['Result']),'')),
                                        content = json.dumps(so_info),
                                        ))
            after_send_dn(int(line['Result']), line['MGOrderNumber'], line['MGClientNumber'])
        transaction.commit()
    except:
        traceback.print_exc()
        transaction.doom()




#===============================================================================
# send one SO to mglobalpack and return back the WSDL result
# @return: 
#===============================================================================
def _sendInfo():
#    url = "http://zensistemas.dyndns.org/mglobalpack.NetEnvironment/aws_rtracorderstofinalize.aspx?wsdl"
    try:
        url = "http://www.mglobalpack.com/mglobalx/aws_rtracorderstofinalize.aspx?wsdl"
        print "------start input date to mglobalpack--------"
        data = _fetchDataFromERP()
        client = Client(url)
        param = _format_data(data, client)
        print param
        #result = client.service.Execute(param)
        #result = _parse_result(result)
        #_insert_result_db(result,data)
    except:
        traceback.print_exc()
    try:
        print "------start send daily report--------"
        send_report_mail()
    except:
        traceback.print_exc()
    print "------finish--------"
    

if __name__ == "__main__":
    _sendInfo()
