# -*- coding: utf-8 -*-
import os
import shutil
import traceback
import fnmatch
import time
import zipfile
import zlib
import random
from datetime import datetime as dt

from tg import config
from tgscheduler import start_scheduler
from tgscheduler.scheduler import add_interval_task

from tribal.model import *
from tribal.util.common import *
from tribal.util.excel_helper import ExcelBasicGenerator

from sqlalchemy.sql import *
import transaction

from pyquery import PyQuery as pq

__all__ = ["lemmiXMLNotify"]

def lemmiXMLNotify():
    if not _prepare():
        print "Can't prepare the config,nothing done."
        return 1
    start_scheduler()
    add_interval_task(action=_scan_lemmi, interval=60*60*3)

def _scan_lemmi():
    workFolder = config.get('lemmi_ftp')
    tempFolder = os.path.join(config.get('public_dir'), 'lemmi_xml', 'temp_folder')
    backupFolder = os.path.join(config.get('public_dir'), 'lemmi_xml', 'backup_folder')
    copyFolder = os.path.join(config.get('public_dir'), 'lemmi_xml', 'copy_folder')
    exist_folder = os.path.join(config.get('public_dir'), 'lemmi_xml', 'exist_folder')
    newBackupFolder = os.path.join(backupFolder, getNowStr())
    newCopyFolder = os.path.join(copyFolder, getNowStr())
    
    print "start"
    for fp in [fpath for fpath in os.listdir(workFolder) if fnmatch.fnmatch(fpath, '*.xml')]:
        workFile = os.path.join(workFolder, fp)
        print workFile
        # check file is complete?
        while(not checkFileComplete(workFile)):
            time.sleep(60*1) # one mins
        try:
            tempFile = os.path.join(tempFolder, fp)
            createIfNotExist(newCopyFolder)
            backupFile = os.path.join(newCopyFolder, fp)
            shutil.copy(workFile, backupFile)
            cut(workFile, tempFile)
            # check in db?
            exist_filename = DBSession.query(LemmiOrderHeader.filename) \
                        .filter(and_(LemmiOrderHeader.active==0, 
                                     LemmiOrderHeader.filename==fp)).first()
            if exist_filename:
                cut(tempFile, os.path.join(exist_folder, fp))
                continue
            # else
            data = _read_xml(tempFile, fp)
        except:
            # roolback
            transaction.doom()
            traceback.print_exc()
            try:
                cut(tempFile, workFile)
            except:
                traceback.print_exc()
        else:
            transaction.commit()
            createIfNotExist(newBackupFolder)
            dlzipFile = os.path.join(newBackupFolder, "lemmi-import_%s.zip" % (dt.now().strftime("%Y%m%d%H%M%S")))
            templatePath = os.path.join(config.get('template_dir'), "LEMMI_TEMPLATE.xls")
            copyTemplatePath = os.path.join(newBackupFolder, 
                                            "LEMMI_TEMPLATE_tmp_%s%d.xls" % (
                                             dt.now().strftime("%Y%m%d%H%M%S"), 
                                             random.randint(1, 1000)))
            shutil.copyfile(templatePath, copyTemplatePath)
            xls_file = _generate_excel(data, os.path.join(newBackupFolder, 
                                        '%s_%s.xls'%(fp, dt.now().strftime("%Y%m%d%H%M%S"))), 
                                       copyTemplatePath)
            dlzip = zipfile.ZipFile(dlzipFile, "w", zlib.DEFLATED)
            for fl in [tempFile, xls_file]:
                dlzip.write(os.path.abspath(str(fl)), os.path.basename(str(fl)))
            dlzip.close()
            try:
                os.remove(xls_file)
                os.remove(copyTemplatePath)
            except:
                pass
            cut(tempFile, os.path.join(newBackupFolder, fp))
            # send sucess mail
            _emailNotify(dlzipFile)
            print "send lemmi sucess mail"
        


def _emailNotify(file):
    send_from = "LEMMI_XML_Robot"
    send_to = ['Jonna.Weiner@r-pac.com', 'raquel.polanco@r-pac.com.sv']
#    send_to = config.get('response_send_to').split(';') #test
    #cc_to = ['Ray.Zhang@r-pac.com.cn','CZ.Chen@r-pac.com.cn','CL.Lam@r-pac.com.cn']
    cc_to = ['CZ.Chen@r-pac.com.cn'] #test
#    cc_to = config.get('response_cc_to', '').split(';') if config.get('response_cc_to', '') else []
    subject = "LEMMI_XML_Import_OK"
    text = ["FYI", "\n",
          "***Please don't reply this E-mail directly.***",
          ]
    files = [file]
    sendEmail(send_from, send_to, subject, "\n".join(text), cc_to, files)

   
def _read_xml(file, filename):
    doc = pq(filename=file)
    aa = doc('ApplicationArea')
    type = aa('Type').text()
    versionId = aa('VersionId').text()
    sender = aa('Sender').text()
    receiver = aa('Receiver').text()
    created = dt.strptime(aa('Created').text(), '%Y-%m-%dT%H:%M:%S') \
                                        if aa('Created').text() else '' 
    del aa
    data = []
    num = 0
    total_orders = 0
    for order in doc('Order'):
        total_orders += 1
        o = pq(order)
        orderNumber = o('OrderNumber').text()
        dispatchDate =  dt.strptime(o('DispatchDate').text(), '%Y-%m-%d') \
                                         if o('DispatchDate').text() else ''
        releaseMethod = o('ReleaseMethod').text()
        countryOfOrigin = o('CountryOfOrigin').text()
        serviceLevel = o('ServiceLevel').text()
        vendorNumber = o('VendorNumber').text()
        # DeliveryAddress
        da = o('DeliveryAddress')
        companyName = da('CompanyName').text()
        contactPerson = da('ContactPerson').text()
        street1 = da('Street1').text()
        street2 = da('Street2').text()
        street3 = da('Street3').text()
        zip = da('Zip').text()
        city = da('City').text()
        state = da('State').text()
        countryCode = da('CountryCode').text()
        countryName = da('CountryName').text()
        phone = da('Phone').text()
        fax = da('Fax').text()
        email = da('Email').text()
        # db ======================================
        header_fields = ['type', 'versionId', 'sender', 'receiver', 'created', 
                         'orderNumber', 'dispatchDate', 'releaseMethod', 
                         'countryOfOrigin', 'serviceLevel', 'vendorNumber', 
                         'companyName', 'contactPerson', 'street1', 'street2', 
                         'street3', 'zip', 'city', 'state', 'countryCode', 
                         'countryName', 'phone', 'fax', 'email']
        header = LemmiOrderHeader()
        header.originalFilename = filename
        header.filename = filename
        for hf in header_fields:
            setattr(header, hf, locals().get(hf, '')) 

        # OrderLine    
        for orderLine in o('OrderLine'):
            ol = pq(orderLine)
            productId = ol('ProductId').text()
            type2 = ol('Type').text() # 1, new; 2, update; 3, delete
            customerOrderLineId = ol('CustomerOrderLineId').text()
            quantity = ol('Quantity').eq(0).text()
            # db ========================================
            detail = LemmiOrderDetail(header=header)
            detail.productId = productId
            detail.type2 = type2
            detail.customerOrderLineId = customerOrderLineId
            detail.quantity = int(quantity.strip())
            # LineItem
            for lineItem in ol('LineItem'):
                li = pq(lineItem)
                quantity3 = li('Quantity').text()
                # db ================================
                detail.quantity3 = int(quantity3.strip())
                tmp = [type, versionId, sender, receiver, created, orderNumber,
                       dispatchDate, releaseMethod, countryOfOrigin, 
                       serviceLevel, vendorNumber, companyName, contactPerson,
                       street1, street2, street3, zip, city, state, 
                       countryCode, countryName, phone, fax, email, productId,
                       type2, customerOrderLineId, quantity, quantity3]
                field_names = ['ItemNo', 'LabelColor', 'TextLine1', 'TextLine2', 
                          'TextLine3', 'Model', 'ModelDescription', 'Color', 
                          'Size', 'WaistSize', 'WidthLength', 'Age', 'Sex', 
                          'Season', 'Currency', 'RetailPrice', 'ProdOrder', 
                          'GTIN']
                fields = pq(li('Field'))
                for fname in field_names:
                    f = fields('[name="%s"]'%fname)
                    if f:
                        # db ---------------------------------
                        if fname == 'GTIN':
                            detail.gtin = f.attr['value']
                        else:
                            setattr(detail, 
                                    ''.join([fname[0].lower(), fname[1:]]), 
                                    f.attr['value'])
                        # db =================================
                        if fname == 'TextLine1' or fname == 'Age':
                            v = f.attr['value']
                            if v:
                                v = v.split(' ')
                                tmp.append(v[0])
                                tmp.append(v[1])
                            else:
                                tmp.append('')
                                tmp.append('')
                        elif fname == 'TextLine3':
                            tmp.append(f.attr['value'].replace('/', ' '))
                        elif fname == 'GTIN':
                            v = f.attr['value']
                            if v:
                                tmp.append(v[:12])
                                tmp.append(v[-1])
                            else:
                                tmp.append('')
                                tmp.append('')
                        else:
                            tmp.append(f.attr['value'])
                    else:
                         tmp.append('')                    
                data.append(tmp)
                DBSession.add(detail)
                DBSession.flush()
                num += 1
#                print num


#    print num
#    print total_orders
    return data
#################################################################
class LemmiExcel(ExcelBasicGenerator):
    def inputData(self, data=None):
        excelSheet = self.workBook.Sheets(1)
        if not data:
            data = [("",), ]
        col = len(data[0])
        startRow = 2
#        sheet.Range("A%d:%s%d" %(startRow, number2alphabet(col), 
#                                 startRow+row-1)).Value = data
        for d in data:
            excelSheet.Range("A%d:%s%d" % (startRow, number2alphabet(col), 
                                     startRow)).Value = [d] 
            startRow += 1 
        
def _generate_excel(data, filename, copyTemplatePath):
    lemmi = LemmiExcel(templatePath=copyTemplatePath, destinationPath=filename)
    try:
        lemmi.inputData(data=data)
        lemmi.outputData()
        return filename
    except:
        traceback.print_exc()
        if lemmi:
            lemmi.clearData()

#def is_old_order(orderNumber):
#    order = DBSession.query(LemmiOrderHeader) \
#                        .filter(and_(LemmiOrderHeader.active==0, 
#                                     LemmiOrderHeader.orderNumber==orderNumber, 
#                                LemmiOrderHeader.status<3)).first()


def _prepare():
    try:
        for fd in ["exist_folder", "temp_folder", "backup_folder", "copy_folder"]:
            createIfNotExist(os.path.join(config.get('public_dir'), 'lemmi_xml', fd))
        return True
    except:
        traceback.print_exc()
        return False
    
def getNowStr(format = "%Y%m%d%H%M%S"):
    return dt.now().strftime(format)

def createIfNotExist(folderPath):
    if not os.path.exists(folderPath): os.makedirs(folderPath)
    
def cut(f, t):
    os.rename(f, t)
    
def checkFileComplete(workFile):
#    fileSize = os.path.getsize(workFile)
#    time.sleep(10)
#    if fileSize==os.path.getsize(workFile):
#        return True
#    else:
#        return False
     try:
        file(workFile)
        return True
     except IOError as e:
        if 'Permission denied' in str(e):
            return False
        else:
            return True


