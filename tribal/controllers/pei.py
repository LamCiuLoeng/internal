# -*- coding: utf-8 -*-
import traceback

from datetime import datetime as dt

from repoze.what import authorize
from sqlalchemy import func
from sqlalchemy.sql.expression import desc
from tg import request
from tg import expose
from tg import flash
from tg import override_template
from tg import redirect
from tg.decorators import paginate

import simplejson as json

from tribal.lib.base import BaseController
from tribal.model import *
from tribal.util import const
from tribal.util.common import *
from tribal.util.const import *
from tribal.util.master_helper import *
from tribal.widgets.pei import *

class PEIController(BaseController):
    #Uncomment this line if your controller requires an authenticated user
    allow_only=authorize.not_anonymous()

    @expose('tribal.templates.pei.index')
    @tabFocus(tab_type="main")
    def index(self):
        order_forms=PEIItemClass.all_cls()

        return {'forms': order_forms}

    @expose('tribal.templates.pei.order')
    @tabFocus(tab_type="main")
    def order(self, **kw):
        try:
            form=PEIItemClass.get(id=kw.get('itemclass', ''))
            items=form.category_items
            billTos=PEIBillTo.all_billtos()
            shiptos=PEIShipTo.all_shiptos()

            return {'form': form,
                    'billTos': billTos,
                    'shipTos': shiptos,
                    'items': items,
                    }
        except:
            traceback.print_exc()
            flash("Error occured! please contact the administrator.")

    @expose('tribal.templates.pei.tf_woven_label')
    def ajax_tf_woven_label(self, **kw):
        item=PEIItem.get(id=kw.get('item', ''))
        sizes=PEISize.all_sizes(itemClass=kw.get('form', ''), lang=const.LANG_ENGLISH)

        return {'include_item': item,
                'sizes': sizes
                }

    @expose('tribal.templates.pei.ca_hangtag')
    def ajax_ca_hangtag(self, **kw):
        item=PEIItem.get(id=kw.get('item', ''))
        styles=PEIStyle.all_styles(lang=const.LANG_ENGLISH)
        colors=PEIColor.all_colors(lang=const.LANG_ENGLISH)
        upcs=PEIUPC.all_upcs()
        sizes=PEISize.all_sizes(lang=const.LANG_ENGLISH)

        return {'include_item': item,
                'styles': styles,
                'colors': colors,
                'upcs': upcs,
                'sizes': sizes
                }

    @expose('tribal.templates.pei.view_tf_woven_label')
    def ajax_view_tf_woven_label(self, **kw):
        header=getOr404(PEIPOHeader, int(kw.get('header', '')))
        item=PEIItem.get(id=kw.get('item', ''))
        poDetail=PEIPODetail.get(header=header, item=item)
        sizes={}
        itemDetails=poDetail.po_items
        detailRows=DBSession.query(func.max(PEIItemDetail.itemGroup)).filter(PEIItemDetail.id.in_([detail.id for detail in itemDetails])).one()[0]

        for detail in itemDetails:
            if detail.attr.attrName=='Size':
                size=PEISize.get(id=detail.attrContent)
                sizes[detail.itemGroup]=size.content

        return {'item': item,
                'itemDetails': itemDetails,
                'sizes': sizes,
                'rows': detailRows,
                }

    @expose('tribal.templates.pei.view_ca_hangtag')
    def ajax_view_ca_hangtag(self, **kw):
        header=getOr404(PEIPOHeader, int(kw.get('header', '')))
        item=PEIItem.get(id=kw.get('item', ''))
        poDetail=PEIPODetail.get(header=header, item=item)
        sizes={}
        styleMainPart={}
        styleExtraPart={}
        colorName={}
        colorCode={}
        upcs={}
        itemDetails=poDetail.po_items
        detailRows=DBSession.query(func.max(PEIItemDetail.itemGroup)).filter(PEIItemDetail.id.in_([detail.id for detail in itemDetails])).one()[0]

        for detail in itemDetails:
            if detail.attr.attrName=='Size':
                size=PEISize.get(id=detail.attrContent)
                sizes[detail.itemGroup]=size.content
            elif detail.attr.attrName=='Style':
                mainStyle=PEIStyle.get(id=detail.attrContent)
                extraStyle=PEIStyle.get(id=detail.extraContent)
                styleMainPart[detail.itemGroup]=mainStyle.mainPart
                styleExtraPart[detail.itemGroup]=extraStyle.extraPart
            elif detail.attr.attrName=='Color':
                nmColor=PEIColor.get(id=detail.attrContent)
                cdColor=PEIColor.get(id=detail.extraContent)
                colorName[detail.itemGroup]=nmColor.name
                colorCode[detail.itemGroup]=cdColor.code
            elif detail.attr.attrName=='UPC':
                upc=PEIUPC.get(id=detail.attrContent)
                upcs[detail.itemGroup]=upc.name

        return {'item': item,
                'itemDetails': itemDetails,
                'sizes': sizes,
                'mainStyles': styleMainPart,
                'extraStyles': styleExtraPart,
                'colorNames': colorName,
                'colorCodes': colorCode,
                'upcs': upcs,
                'rows': detailRows,
                }

    @expose()
    def saveOrder(self, **kw):
        DBSession.begin(subtransactions=True)
        try:
            def getDropShop(select): return bool(int(select))

            storeObjs=[]
            form=PEIItemClass.get(id=kw.get('order_form', ''))
            billId=kw.get('billCompany', '')
            shipId=kw.get('shipCompany', '')

            billShipParams={'issuedBy': request.identity["user"],
                              'lastModifyBy': request.identity["user"],
                              }

            if int(billId)!=0: billTo=PEIBillTo.get(id=billId)
            else:
                billShipParams['company']=kw['other_billto']
                billShipParams['address']=kw['billAddress']
                billShipParams['attn']=kw['billAttn']
                billShipParams['tel']=kw['billTel']
                billShipParams['fax']=kw['billFax']
                billTo=PEIBillTo(**billShipParams)
                storeObjs.append(billTo)

            if int(shipId)!=0: shipTo=PEIShipTo.get(id=shipId)
            else:
                billShipParams['company']=kw['other_shipto']
                billShipParams['address']=kw['shipAddress']
                billShipParams['attn']=kw['shipAttn']
                billShipParams['tel']=kw['shipTel']
                billShipParams['fax']=kw['shipFax']
                shipTo=PEIShipTo(**billShipParams)
                storeObjs.append(shipTo)

            headerFields=[("orderedBy", None),
                            ("orderedTel", None),
                            ("shipDate", None),
                            ("shipVia", None),
                            ("buyerPO", None),
                            ("vendorPO", None),
                            ("dropShip", getDropShop),
                            ]
            headerParams={"billTo" : billTo,
                            "shipTo" : shipTo,
                            }

            for f, fun in headerFields:
                if kw[f]: headerParams[f]=fun(kw[f]) if fun else kw[f]
            headerPO=PEIPOHeader(**headerParams)
            storeObjs.append(headerPO)

            details=[]
            itemDetails=[]
            itemDetailExtras=[]
            detailParams={}
            itemDtlExParams={}
            multiAttrs=[]
            extraAttrs=["Style", "Color"]
            attrContents=["mainPart", "name"]
            extraContents=["extraPart", "code"]

            for item in form.category_items:
                itemDetailParams={}
                priceKey="price_%d"%item.id
                quantityKey="quantity_%d"%item.id
                variableKey="variable_%d"%item.id

                if kw[quantityKey] and int(kw[quantityKey])>0 :
                    if priceKey in kw and kw[priceKey] : detailParams["price"]=kw[priceKey]
                    detailParams["quantity"]=int(kw[quantityKey])
                    detailParams["item"]=item
                    detailParams["header"]=headerPO
                    detail=PEIPODetail(**detailParams)
                    details.append(detail)

                    if variableKey in kw and kw[variableKey]:
                        variable_json=json.loads(kw.get(variableKey, '').replace("'", '"'))

                        for json_item in variable_json:
                            for attr in item.attrs:
                                itemDetailParams['poDetail']=detail
                                itemDetailParams['attr']=attr
                                itemDetail=PEIItemDetail(**itemDetailParams)

                                if attr.attrName in multiAttrs:
                                    detailExtra=json_item[attr.attrName]

                                    for key, val in detailExtra.iteritems():
                                        itemDtlExParams['itemDetail']=itemDetail
                                        itemDtlExParams['attrContent']=key
                                        itemDtlExParams['extraContent']=val
                                        itemDtlEx=PEIItemExtraDetail(**itemDtlExParams)
                                        itemDetailExtras.append(itemDtlEx)
                                elif attr.attrName in extraAttrs:
                                    detailAttr=json_item[attr.attrName]

                                    for key, val in detailAttr.iteritems():
                                        if key in attrContents:
                                            itemDetail.attrContent=val
                                        elif key in extraContents:
                                            itemDetail.extraContent=val

                                        itemDetail.itemGroup=int(json_item[GROUP_FLAG])
                                else:
                                    itemDetail.attrContent=json_item[attr.attrName]
                                    itemDetail.itemGroup=int(json_item[GROUP_FLAG])

                                itemDetails.append(itemDetail)

            storeObjs.extend(details)
            storeObjs.extend(itemDetails)
            storeObjs.extend(itemDetailExtras)
            DBSession.add_all(storeObjs)
            DBSession.commit()
        except:
            traceback.print_exc()
            DBSession.rollback()
            flash("The service is not avaiable now,please try it later or contact the system administator.", "warn")
            raise
        else:
            flash("The order has been confirmed successfully!")
        redirect("/pei/viewOrder?code=%s"%(rpacEncrypt(headerPO.id)))

    @expose('tribal.templates.pei.view_order')
    @tabFocus(tab_type="main")
    def viewOrder(self, **kw):
        (flag, id)=rpacDecrypt(kw.get("code", ""))

        if not flag:
            flash("Please don't access the resource illegally!")
            redirect("/pei/index")

        ph=getOr404(PEIPOHeader, id)

        #if ph.active == 1:
        #    flash("The order has been canceled!", "warn")
        #    redirect("/order/index")

        if len(ph.details)<1 :
            flash("There's no order related to this PO!", "warn")
            redirect("/pei/index")

        return {'billTo'  : ph.billTo,
                'shipTo'  : ph.shipTo,
                'header'  : ph,
                'details' : ph.details,
                }

    @expose("tribal.templates.pei.search")
    @paginate('result', items_per_page=30)
    @tabFocus(tab_type="view")
    def search(self, ** kw):
        if len(kw)>0:
            keys=["buyerPO",
                    "vendorPO",
                    "orderStartDate",
                    "orderEndDate",
                    ]
            result=DBSession.query(PEIPOHeader)

            for key in keys:
                if len(kw[key])>0:
                    if key is 'orderStartDate': result=result.filter(PEIPOHeader.shipDate>=dt.strptime(kw.get(key, '2009-12-1200:00:00')+"00:00:00", "%Y-%m-%d%H:%M:%S"))
                    elif key is 'orderEndDate': result=result.filter(PEIPOHeader.shipDate<=dt.strptime(kw.get(key, '2009-12-1200:00:00')+"23:59:59", "%Y-%m-%d%H:%M:%S"))
                    else:                       result=result.filter(getattr(PEIPOHeader, key).like('%'+kw[key]+'%'))
            result=result.order_by(desc(PEIPOHeader.id)).all()
        else:
            result=[]
        return {"result" : result,
                "widget" : order_view_form,
                "values" : kw
                }
