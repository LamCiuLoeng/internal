# -*- coding: utf-8 -*-
import traceback, logging, transaction

# turbogears imports
import types
import pylons
from tgext.ws import iconv
from tgext.ws import soap
from tgext.ws import xml_
from tgext.ws import json
from tg import config
from tg.controllers import TGController

from tribal.model import MglobalCustPo, DBSession,MglobalCustPoDetail
from tgext.ws.controllers import wsexpose, wsvalidate


__all__ = ['WSController']

log = logging.getLogger(__name__)

class WebServicesController(object):

    def _ws_gather_functions_and_types(self, prefix):
        funcs = dict()
        complex_types = set()

        for key in dir(self):
            if key.startswith("_") or key in ['mount_point', 'mount_steps']:
                continue
            item = getattr(self, key)
            if prefix:
                newname = prefix+key[0].upper()+key[1:]
            else:
                newname = key
            if hasattr(item, "_ws_gather_functions_and_types"):
                morefuncs, moretypes = \
                            item._ws_gather_functions_and_types(newname)
                funcs.update(morefuncs)
                complex_types.update(moretypes)
            elif isinstance(item, types.MethodType):
                deco = getattr(item, 'decoration', None)
                if hasattr(deco, "_ws_func_info"):
                    funcs[newname] = item
                    complex_types.update(deco._ws_func_info.complex_types)
        return funcs, complex_types
    
class WebServicesRoot(TGController, WebServicesController):

    def __init__(self, baseURL=None, tns=None, typenamespace=None):
        baseURL = baseURL or pylons.config.get('ws.baseURL', '')
        if not baseURL.endswith('/'):
            baseURL += '/'
        if not tns:
            tns = baseURL + "soap/"
        if not typenamespace:
            typenamespace = tns + "types"
        self._ws_baseURL = baseURL
        self._ws_parent = None
        self.soap = soap.SoapController(self, tns, typenamespace)
        self._ws_funcs, self._ws_complex_types = self._ws_gather_functions_and_types("")
        pylons.config['render_functions']['wsautoxml'] = xml_.render_autoxml
        pylons.config['render_functions']['wsautojson'] = json.render_autojson
    
        
class MSG(object):
    flag = int
    content = unicode

    def __init__(self,**kw):
        self.flag = kw.get("flag",0)
        self.content = kw.get("content",None)

class MglobalpackPODetail(object):

    item_no = unicode
    qty = int

    def __init__(self,**kw):
        self.item_no = kw.get("item_no",None)
        self.qty = kw.get('qty',0)

class MglobalpackPO(object):
    po_no = unicode
    cust_no = unicode
    detail = [MglobalpackPODetail]

    def __init__(self,**kw):
        self.po_no = kw.get("po_no",0)
        self.cust_no = kw.get("cust_no",None)
        self.detail = kw.get("detail",[])

class MglobalpackController(WebServicesController):

    @wsexpose(MSG)
    @wsvalidate([MglobalpackPO])
    def add(self, mgp_pos):
        if mgp_pos is None or len(mgp_pos) < 1:
            return MSG(flag=1,content = "The customer po param could not be blank.")

        try:
            for order_info in mgp_pos:
                if not order_info.po_no or not order_info.cust_no: continue
                if not MglobalCustPo.get_by_cust_po_no(order_info.po_no,order_info.cust_no):
                    header = MglobalCustPo(cust_po_no=order_info.po_no,cust_no=order_info.cust_no)
                    DBSession.add(header)
                    for d in order_info.detail:
                        DBSession.add(MglobalCustPoDetail(header = header, item_no = d.item_no, qty = d.qty))
            return MSG(flag=0,content="Adding the custoemr PO successfully!")
        except Exception, e:
            transaction.doom()
            log.exception(str(e))
            return MSG(flag=2,content="Error occur on the server side!")

class WSController(WebServicesRoot):

    def __init__(self):
        host = config.get("website_url")
        super(WSController, self).__init__('%s/ws/' %host,host,'%s/types/' %host)

    mg = MglobalpackController()

