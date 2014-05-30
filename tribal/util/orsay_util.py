# -*- coding: utf-8 -*-
from datetime import datetime as dt
import os
import random
import traceback
import sha

from tg import config
from tg import request
from tg import session
from tribal.util.common import *
from tribal.util.excel_helper import *

def create_token():
    token = request.identity["user"].user_name + dt.now().strftime("%y%m%d%H%M%S") + str(random.randint(100, 999))
    token = sha.new(token).hexdigest()
    session['token'] = token
    session.save()
    return token

def get_download_path():
    current = dt.now()
    dateStr = current.today().strftime("%Y%m%d%H%M%S")
    fileDir = os.path.join(config.download_dir, "orsay_download", request.identity["user"].user_name, dateStr)
    if not os.path.exists(fileDir):
        os.makedirs(fileDir)
    return fileDir

def send_mail(header, emailSubject, files):
    #Send e-mail out
    send_from = "r-pac-orsay-order-system"
    send_to = request.identity["user"].email_address.split(";")
    cc_to = config.orsay_email_cc.split(";") if config.has_key('orsay_email_cc') else []
    cc_to.extend(header.create_by.email_address.split(";"))
    text = ["Thank you for your confirmation!",
        "You could view the order's detail information via the link below:",
        "%s/orsay/viewOrder?code=%s" % (config.website_url, rpacEncrypt(header.id)),
        "\n\n************************************************************************************",
        "This e-mail is sent by the r-pac Orsay ordering system automatically.",
        "Please don't reply this e-mail directly!",
        "************************************************************************************"
        ]
    sendEmail(send_from, send_to, emailSubject, "\n".join(text), cc_to, files)

def get_pdf_file(emailSubject):
    return '_'.join(os.path.join(get_download_path(), "%s.pdf" % emailSubject).split(' '))

def gen_pdf(pdfFile, pdfParam, pdfTemplate):
    pdfTemplate = os.path.join(config.template_dir, "%s.html" % pdfTemplate)
    f = open(pdfTemplate)
    htmlContent = "".join(f.readlines())
    htmlFile = pdfFile.replace('pdf', 'html')
    open(htmlFile, 'w').write(htmlContent % pdfParam)
    f.close()
    return HTML2PDF(htmlContent % pdfParam, pdfFile)

def gen_pdf1(pdfFile, pdfParam, pdfTemplate):
    pdfTemplate = os.path.join(config.template_dir, "%s.html" % pdfTemplate)
    f = open(pdfTemplate)
    htmlContent = "".join(f.readlines())
    htmlFile = pdfFile.replace('pdf', 'html')
    open(htmlFile, 'w').write(htmlContent % pdfParam)
    f.close()
    return os.popen('wkhtmltopdf %s %s' % (htmlFile, pdfFile))

def get_xls_file(emailSubject):
    return '_'.join(os.path.join(get_download_path(), "%s.xls" % emailSubject).split(' '))

def gen_xls(xlsFile, xlsParam, xlsTemplate):
    try:
        xlsTemplate = os.path.join(config.template_dir, "%s.xls" % xlsTemplate)
        pe = OrsayExcel(templatePath=xlsTemplate, destinationPath=xlsFile)
        pe.inputData(xlsParam)
        pe.outputData()
    except:
        traceback.print_exc()

class OrsayExcel(ExcelBasicGenerator):

    def inputData(self, params):
        excelSheet = self.workBook.Sheets(1)
        if params['order_type'] == 'C1':
            for i in ["size1", "size2", "size3", "article", "reference", "order", "collection", "location", "trademark", "materials", "appendixs"]:
                excelSheet.Range(i).Value = params[i]
        elif params['order_type'] == 'C2':
            for i in ["washing", "bleeding", "various", "ironing", "accessories"]:
                excelSheet.Range(i).Value = params[i]
            excelSheet.Shapes.AddPicture(params["washing_img"], 1, 1, 60, 80, 40, 40)
            excelSheet.Shapes.AddPicture(params["bleeding_img"], 1, 1, 60, 210, 40, 40)
            excelSheet.Shapes.AddPicture(params["various_img"], 1, 1, 60, 340, 40, 40)
            excelSheet.Shapes.AddPicture(params["ironing_img"], 1, 1, 60, 470, 40, 40)
            excelSheet.Shapes.AddPicture(params["accessories_img"], 1, 1, 60, 600, 40, 40)
        elif params['order_type'] == 'C3':
            for i in ["size1", "size2", "size3", "article", "reference", "order", "collection", "location", "trademark", "materials", "appendixs"]:
                excelSheet.Range(i).Value = params[i]
