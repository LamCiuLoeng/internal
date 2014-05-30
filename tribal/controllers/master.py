# -*- coding: utf-8 -*-
import os
from datetime import datetime

from tg import expose
from tg import flash
from tg import redirect, config
from tribal.controllers.basicMaster import *
from tribal.model import *
from tribal.util.common import *
from tribal.widgets.master import *
import transaction

__all__ = [
    "DBACustomerController",
    "DBAItemController",
    "DBACategoryController",
    "DBAItemTypeController",
    "BBYBrandController",
    "BBYPackagingFormatController",
    "BBYMaterialController",
    "BBYSpecController",
    "BBYClosureController",
    "BBYDisplayModeController",
    "BBYFailureReasonController",
    "BBYCourierController",
    "BBYMockupContentController",
    "BBYVendorController",
    "BBYTeammateController",
    "BBYSourceController",
    "BBYMaterialSpecController",
    "BBYAgentController",
    'SampleCustomerController',
    'SampleProgramController',
    'SampleProjectController',
    'SampleRegionController',
    'SampleStockController',
    'SampleTeamController',
    'SampleExtraInfoController',
    'SampleTypeMappingController',
    'SampleItemCategoryController',
    'PrepressItemCategoryController',
    ]


class DBACustomerController( BasicMasterController ):
    url = "dbacustomer"
    dbObj = DBACustomer
    template = "tribal.templates.master.index_dba_customer"
    searchWidget = DBACustomerSearchFormInstance
    updateWidget = DBACustomerUpdateFormInstance
    formFields = ["name", "code", "contact_person", "email_address", "bill_to", "ship_to"]

    @expose()
    def saveNew( self, ** kw ):
        params = {}
        for f in self.formFields:
            if f in kw: params[f] = kw[f]
        params = self.beforeSaveNew( kw, params )
        obj = self.dbObj( ** params )
        DBSession.add( obj )
        flash( "Save the new master successfully!" )
        redirect( "/%s/index" % self.url )



class DBAItemController( BasicMasterController ):
    url = "dbaitem"
    dbObj = DBAItem
    template = "tribal.templates.master.index_dba_item"
    searchWidget = DBAItemSearchFormInstance
    updateWidget = DBAItemUpdateFormInstance
    formFields = ["item_code", "category_id", "type_id", "image", "flatted_size"]
    search_config = {"item_code": ["item_code", str],
        "type_id": ["type_id", int],
        "category_id": ["category_id", int],
    }

    @expose( 'tribal.templates.master.dba_form_new' )
    @tabFocus( tab_type = "master" )
    def add( self, **kw ):
        dbaTypeOptons = [( "", "" )] + [( str( r.id ), r.name ) for r in DBSession.query( DBAItemType ).all()]
        return {
            "dbaTypeOptons": dbaTypeOptons,
            "saveURL": "/%s/saveNew" % self.url,
            "funcURL": self.url
        }

    @expose()
    def saveNew( self, ** kw ):
        item_code = kw.get( 'item_code', '' ).strip()
        item = DBAItem.get_by_code( item_code )
        if item:
            flash( "%s already in the system!" )
            redirect( "/%s/index?item_code=%s" % ( self.url, item_code ) )
        else:
            try:
                file_dir = os.path.join( config.get( 'public_dir' ), 'images/dba' )
                image = kw.get( 'image' )
                new_filename = '%s_%s' % ( item_code, datetime.now().strftime( "%Y%m%d%H%M%S" ) )
                save_file = os.path.join( file_dir, '%s%s' % ( new_filename, '.jpg' ) )
                with open( save_file, 'wb' ) as f:
                    f.write( image.file.read() )
                obj = self.dbObj()
                obj.item_code = item_code
                obj.category_id = kw.get( 'category_id' ).strip()
                obj.type_id = kw.get( 'type_id' ).strip()
                obj.flatted_size = kw.get( 'flatted_size' ).strip()
                obj.image = new_filename
                DBSession.add( obj )
            except:
                transaction.doom()
                flash( "The service is not avaiable now.", "warn" )
                redirect( "/%s/add" % self.url )
            else:
                flash( "Save the new DBA item successfully!" )
                redirect( "/%s/index?item_code=%s" % ( self.url, item_code ) )

    @expose( 'tribal.templates.master.dba_form_update' )
    @tabFocus( tab_type = "master" )
    def update( self, **kw ):
        obj = getOr404( self.dbObj, kw["id"], "/%s/index" % self.url )
        values = {}
        # for f in self.formFields : values[f]=getattr(obj, f)
        for f in self.formFields :
            v = getattr( obj, f )
            if isinstance( v, basestring ):values[f] = str( getattr( obj, f ) )
            else: values[f] = v
        return {
                "widget" : self.updateWidget,
                "values" : values,
                "saveURL" : "/%s/saveUpdate?id=%d" % ( self.url, obj.id ),
                "funcURL" :self.url
                }

    @expose()
    def saveUpdate( self, **kw ):
        # print kw
        obj = getOr404( self.dbObj, kw["id"], "/%s/index" % self.url )
        params = {"lastModifyBy": request.identity["user"], "lastModifyTime": dt.now()}
        for f in ["category_id", "type_id", "flatted_size"]:
            if f in kw:
                params[f] = kw[f] if kw[f] else None
        params = self.beforeSaveUpdate( kw, params )
        for k in params:
            setattr( obj, k, params[k] )
        image = kw.get( 'image', '' )
        if hasattr( image, 'file' ):
            # print image
            file_dir = os.path.join( config.get( 'public_dir' ), 'images/dba' )
            new_filename = '%s_%s' % ( obj.item_code, datetime.now().strftime( "%Y%m%d%H%M%S" ) )
            save_file = os.path.join( file_dir, '%s%s' % ( new_filename, '.jpg' ) )
            with open( save_file, 'wb' ) as f:
                f.write( image.file.read() )
            obj.image = new_filename
        flash( "Update %s successfully!" % obj.item_code )
        redirect( "/%s/index?item_code=%s" % ( self.url, obj.item_code ) )

    @expose()
    def inactivate( self, **kw ):
        if kw.get( 'selected_ids', '' ):
            for i in kw.get( 'selected_ids', '' ).split( ',' ):
                obj = getOr404( self.dbObj, i, "/%s/index" % self.url )
                obj.lastModifyBy = request.identity["user"]
                obj.lastModifyTime = dt.now()
                obj.customers = []
        flash( "Inactivate the item successfully!" )
        redirect( "/%s/index" % self.url )


class DBACategoryController( BasicMasterController ):
    url = "dbacategory"
    dbObj = DBAItemCategory
    template = "tribal.templates.master.index_dba_category"
    searchWidget = DBACateogrySearchFormInstance
    updateWidget = DBACateogryUpdateFormInstance
    formFields = ["name"]


class DBAItemTypeController( BasicMasterController ):
    url = "dbaitemtype"
    dbObj = DBAItemType
    template = "tribal.templates.master.index_dba_itemtype"
    searchWidget = DBAItemTypeSearchFormInstance
    updateWidget = DBAItemTypeUpdateFormInstance
    formFields = ["name"]



#===============================================================================
# BBY Master
#===============================================================================
class BBYBrandController( BasicMasterController ):
    url = "bby_brand"
    dbObj = BBYBrand
    template = "tribal.templates.master.index_bby_brand"
    searchWidget = BBYBrandSearchFormInstance
    updateWidget = BBYBrandUpdateFormInstance
    formFields = ["name", "description"]

    def beforeSaveNew( self, kw, params ):
        del params["issuedBy"]
        del params["lastModifyBy"]
        del params["lastModifyTime"]
        return params

    def beforeSaveUpdate( self, kw, params ):
        del params["lastModifyBy"]
        del params["lastModifyTime"]
        return params


class BBYPackagingFormatController( BBYBrandController ):
    url = "bby_pf"
    dbObj = BBYPackagingFormat


class BBYMaterialController( BBYBrandController ):
    url = "bby_material"
    dbObj = BBYMaterial


class BBYSpecController( BBYBrandController ):
    url = "bby_spec"
    dbObj = BBYSpec


class BBYClosureController( BBYBrandController ):
    url = "bby_closure"
    dbObj = BBYClosure


class BBYDisplayModeController( BBYBrandController ):
    url = "bby_dm"
    dbObj = BBYDisplayMode


class BBYFailureReasonController( BBYBrandController ):
    url = "bby_fr"
    dbObj = BBYFailureReason


class BBYCourierController( BBYBrandController ):
    url = "bby_courier"
    dbObj = BBYCourier


class BBYMockupContentController( BBYBrandController ):
    url = "bby_mc"
    dbObj = BBYMockupContent

class BBYVendorController( BBYBrandController ):
    url = "bby_vendor"
    dbObj = BBYVendor
    template = "tribal.templates.master.index_bby_vendor"
    search_config = {"name": ["name", str],
        "ae_name": ["ae_name", str],
        "erp_code_ref": ["erp_code_ref", str],
        "program_involved": ["program_involved", str],
        }
    searchWidget = BBYVendorSearchFormInstance
    updateWidget = BBYVendorUpdateFormInstance
    formFields = ["name", "ae_name", "erp_code_ref", "full_name", "contact", "tel", "ext", "mobile", "email", "address", "program_involved"]


class BBYTeammateController( BBYBrandController ):
    url = "bby_tm"
    dbObj = BBYTeammate
    search_config = {"name": ["name", str],
        "location": ["location", str],
        }
    searchWidget = BBYTeammateSearchFormInstance
    updateWidget = BBYTeammateUpdateFormInstance
    formFields = ["name", "location", "tel", "email", "address"]


class BBYSourceController( BBYBrandController ):
    url = "bby_source"
    dbObj = BBYSource
    search_config = {"name": ["name", str], }
    # searchWidget = BBYTeammateSearchFormInstance
    updateWidget = BBYSourceUpdateFormInstance
    formFields = ["name", "full_name", "contact", "tel", "mobile", "email", "address"]

    @expose( 'json' )
    def checkName( self, ** kw ):
        try:
            obj = DBSession.query( BBYSource ).filter_by( name = kw.get( 'name' ) ).one()
            message = "<p>The <a href='/bby_source/update?id=%s'>%s</a> had,Please click for modifly it</p>" % ( obj.id, obj.name )
        except:
            message = None
        return dict( Msg = message )

    @expose( 'tribal.templates.bby.source_add' )
    def add( self, ** kw ):
        return {
            "widget": self.updateWidget,
            "values": {},
            "saveURL": "/%s/saveNew" % self.url,
            "funcURL":self.url
            }

    @expose( 'json' )
    def ajaxDelete( self, ** kw ):
        try:
            objDetail = DBSession.query( BBYSourceDetail ).filter_by( id = int( kw.get( 'hid' ) ) ).one()
            DBSession.delete( objDetail )
            message = "successfully"
        except:
            message = "faild"
        return dict( Msg = message )

    @expose( 'tribal.templates.bby.source_add' )
    def update( self, ** kw ):
        obj = getOr404( self.dbObj, kw["id"], "/%s/index" % self.url )
        values = {}
        obj_detail = DBSession.query( BBYSourceDetail ).filter_by( header_id = kw["id"] ).all()
        self.formFields = ["name", "full_name"]
        for f in self.formFields:values[f] = str( getattr( obj, f ) )

        return {
            "widget": self.updateWidget,
            "values": values,
            "obj_detail": obj_detail,
            "saveURL": "/%s/saveUpdate?id=%d" % ( self.url, obj.id ),
            "funcURL": self.url
            }

    @expose( 'json' )
    def saveNew( self, ** kw ):
        print kw
        self.dbObj = BBYSource
        params = {"issuedBy":request.identity["user"], "lastModifyBy":request.identity["user"], "lastModifyTime":dt.now()}
        for f in self.formFields:
            if f in ["name", "full_name"]:
                if f in kw: params[f] = kw[f]
        params = self.beforeSaveNew( kw, params )
        obj = self.dbObj( ** params )
        DBSession.add( obj )

        for i in xrange( 0, int( kw['count'] ) + 1 ):
            args = {
                "header_id":obj,
                "header":obj,
                "contact":kw.get( 'contact%s' % i ),
                "tel":kw.get( 'tel%s' % i ),
                "mobile":kw.get( 'mobile%s' % i ),
                "email":kw.get( 'email%s' % i ),
                "address":kw.get( 'address%s' % i )
            }
            obj_detail = BBYSourceDetail( ** args )
            DBSession.add( obj_detail )
        # flash("Save the new master successfully!")
        # redirect("/%s/index" % self.url)
        message = "<p>Save the new master successfully!</p>"
        return dict( Msg = message )

    @expose( 'json' )
    def saveUpdate( self, ** kw ):
        obj = getOr404( self.dbObj, kw["id"], "/%s/index" % self.url )
        params = {"lastModifyBy":request.identity["user"], "lastModifyTime":dt.now()}
        for f in self.formFields:
            if f in kw: params[f] = kw[f] if kw[f] else None
        params = self.beforeSaveUpdate( kw, params )
        for k in params: setattr( obj, k, params[k] )
        # obj.set(**params)
        for i in xrange( 0, int( kw['count'] ) + 1 ):
            try:
                obj_detail = DBSession.query( BBYSourceDetail ).filter_by( id = kw.get( 'hid%s' % i ) ).first()
                obj_detail.contact = kw.get( 'contact%s' % i )
                obj_detail.tel = kw.get( 'tel%s' % i )
                obj_detail.mobile = kw.get( 'mobile%s' % i )
                obj_detail.email = kw.get( 'email%s' % i )
                obj_detail.address = kw.get( 'address%s' % i )
                DBSession.merge( obj_detail )
            except:
                args = {
                    "header_id":obj,
                    "header":obj,
                    "contact":kw.get( 'contact%s' % i ),
                    "tel":kw.get( 'tel%s' % i ),
                    "mobile":kw.get( 'mobile%s' % i ),
                    "email":kw.get( 'email%s' % i ),
                    "address":kw.get( 'address%s' % i )
                }
                obj_detail = BBYSourceDetail( ** args )
                DBSession.add( obj_detail )

        # flash("Update the master successfully!")
        # redirect("/%s/index" % self.url)
        message = "<p>Update the master successfully!</p>"
        return dict( Msg = message )

class BBYMaterialSpecController( BBYBrandController ):
    url = "bby_material_spec"
    dbObj = BBYMaterialSpec
    search_config = {"name": ["name", str]}
    searchWidget = BBYMaterialSpecSearchFormInstance
    updateWidget = BBYTeammateUpdateFormInstance
    formFields = ["name", "material", "spec", "front_color", "back_color"]

    @expose()
    def delete( self, ** kw ):
        obj = getOr404( self.dbObj, kw["id"], "/%s/index" % self.url )
        obj.lastModifyBy = request.identity["user"]
        obj.lastModifyTime = dt.now()
        obj.active = 1
        flash( "Delete the master successfully!" )
        redirect( "/%s/index" % self.url )

    @expose( 'tribal.templates.bby.materialspec.update' )
    def update( self, ** kw ):
        self.dbObj = BBYMaterialSpec
        obj = getOr404( self.dbObj, kw["id"], "/%s/index" % self.url )
        values = {}
        obj_detail = DBSession.query( self.dbObj ).filter_by( id = int( kw["id"] ) ).one()
        nameOptions = DBSession.query( BBYPackagingFormat ).all()
        materialOptions = DBSession.query( BBYMaterial ).all()
        specOptions = DBSession.query( BBYSpec ).all()
        colorOptions = DBSession.query( BBYColor ).all()

        return {
            "widget": self.updateWidget,
            "values": values,
            "obj_detail": obj_detail,
            "saveURL": "/%s/saveUpdate?id=%d" % ( self.url, obj.id ),
            "deleteURL": "/%s/delete?id=%d" % ( self.url, obj.id ),
            "funcURL": self.url,
            "nameOptions":nameOptions,
            "materialOptions":materialOptions,
            "specOptions":specOptions,
            "colorOptions":colorOptions
            }


    @expose( 'tribal.templates.bby.materialspec.add' )
    @tabFocus( tab_type = "master" )
    def add( self, ** kw ):
        nameOptions = DBSession.query( BBYPackagingFormat ).all()
        materialOptions = DBSession.query( BBYMaterial ).all()
        specOptions = DBSession.query( BBYSpec ).all()
        colorOptions = DBSession.query( BBYColor ).all()
        return {

            "values": {},
            "saveURL": "/%s/saveNew" % self.url,
            "funcURL":self.url,
            "nameOptions":nameOptions,
            "materialOptions":materialOptions,
            "specOptions":specOptions,
            "colorOptions":colorOptions
            }

    @expose( 'json' )
    def saveNew( self, ** kw ):
        self.url = "bby_material_spec"
        self.dbObj = BBYMaterialSpec
        objDetail = DBSession.query( BBYPackagingFormat ).filter_by( id = int( kw.get( 'head_id' ) ) ).one()
        params = {
            "name":objDetail.name,
            }
        for i in kw:
            if i == 'head_id':params[i] = int( kw[i] )
            else:
                params[i] = kw[i]

        obj = self.dbObj( ** params )
        DBSession.add( obj )


        return dict( Msg = "Save the new master successfully!" )

    @expose( 'json' )
    def checkName( self, ** kw ):
        try:
            dbObj = DBSession.query( BBYMaterialSpec ).filter( BBYMaterialSpec.head_id == int( kw.get( 'head_id' ) ) ).filter( BBYMaterialSpec.active == 0 ).one()
            msg = "The name(<a href='/bby_material_spec/update?id=%s'>%s</a>) had,You can modifly it!" % ( dbObj.id, dbObj.name )
        except:
            msg = None
        return dict( Msg = msg )


class BBYAgentController( BBYBrandController ):
    url = "bby_agent"
    dbObj = BBYAgent
    updateWidget = BBYAgentUpdateFormInstance
    formFields = ["name", "description", "vendor_ids"]

    def afterSaveNew( self, obj, kw ):
        ids = kw.get( "vendor_ids[]", [] )
        if type( ids ) != list : ids = [ids, ]
        obj.vendors = DBSession.query( BBYVendor ).filter( BBYVendor.id.in_( ids ) ).all()
        return obj

    def afterSaveUpdate( self, obj, kw ):
        ids = kw.get( "vendor_ids[]", [] )
        if type( ids ) != list : ids = [ids, ]
        obj.vendors = DBSession.query( BBYVendor ).filter( BBYVendor.id.in_( ids ) ).all()
        return obj




class BBYContactController( BBYBrandController ):
    url = "bby_contact"
    dbObj = BBYContact
    search_config = {"name": ["name", str], "email" : ["email", str] , "phone" : ["phone" , str] }
    searchWidget = BBYContactSearchFormInstance
    updateWidget = BBYContactUpdateFormInstance
    formFields = ["name", "email", "phone"]



#===============================================================================
# sample master
#===============================================================================

class SampleCustomerController( BasicMasterController ):
    url = "sample_customer"
    template = "tribal.templates.master.index_sample_customer"
    dbObj = Customer
    searchWidget = SampleCustomerSearchFormInstance
    updateWidget = SampleCustomerUpdateFormInstance
    formFields = ["name"]

    def beforeSaveNew( self, kw, params ):
        del params["issuedBy"]
        del params["lastModifyBy"]
        del params["lastModifyTime"]
        return params

    def beforeSaveUpdate( self, kw, params ):
        del params["lastModifyBy"]
        del params["lastModifyTime"]
        return params

class SampleProgramController( SampleCustomerController ):
    url = "sample_program"
    dbObj = Program

class SampleProjectController( SampleCustomerController ):
    url = "sample_project"
    template = "tribal.templates.master.index_sample_project"
    dbObj = Project
    searchWidget = SampleProjectSearchFormInstance
    search_config = {"name": ["name", str], "program_id": ["program_id", int]}
    updateWidget = SampleProjectUpdateFormInstance
    formFields = ["name", "program_id"]

class SampleRegionController( SampleCustomerController ):
    url = "sample_region"
    template = "tribal.templates.master.index_sample_region"
    dbObj = Region
    searchWidget = SampleRegionSearchFormInstance
    search_config = {"name": ["name", str], "code": ["code", int]}
    updateWidget = SampleRegionUpdateFormInstance
    formFields = ["name", "code"]

class SampleStockController( SampleCustomerController ):
    url = "sample_stock"
    template = "tribal.templates.master.index_sample_stock"
    dbObj = Stock
    searchWidget = SampleStockSearchFormInstance
    search_config = {"name": ["name", str], "cost": ["cost", float]}
    updateWidget = SampleStockUpdateFormInstance
    formFields = ["name", "cost"]

class SampleTeamController( SampleCustomerController ):
    url = "sample_team"
    template = "tribal.templates.master.index_sample_team"
    dbObj = Team
    searchWidget = SampleTeamSearchFormInstance
    search_config = {"name": ["name", str], "manager": ["cost", str], "short_name": ["short_name", str]}
    updateWidget = SampleTeamUpdateFormInstance
    formFields = ["name", "manager", "short_name"]

class SampleExtraInfoController( SampleCustomerController ):
    url = "sample_extra_info"
    template = "tribal.templates.master.index_sample_extra_info"
    dbObj = FormExtraInfo
    searchWidget = SampleExtraInfoSearchFormInstance
    search_config = {"name": ["name", str], "estimate_time": ["estimate_time", datetime], "job_config": ["job_config", str], "need_stock": ["need_stock", int]}
    updateWidget = SampleExtraInfoUpdateFormInstance
    formFields = ["name", "estimate_time", "job_config", 'need_stock']

class SampleTypeMappingController( SampleCustomerController ):
    url = "sample_type_mapping"
    template = "tribal.templates.master.index_sample_type_mapping"
    dbObj = FormTypeMapping
    searchWidget = SampleTypeMappingSearchFormInstance
    search_config = {"name": ["name", str], "label": ["label", str], "category": ["category", str], "report_header": ["report_header", str],
    "category2": ["category2", str], "report_header2": ["report_header2", str], "category2index": ["category2index", int], }
    updateWidget = SampleTypeMappingUpdateFormInstance
    formFields = ["name", "label", "category", 'report_header', 'category2', 'report_header2', 'category2index']


class SampleItemCategoryController( SampleCustomerController ):
    url = "sample_item_category"
    dbObj = ItemCategory




class PrepressItemCategoryController( SampleCustomerController ):
    url = "prepress_item_category"
    dbObj = PSItemCategory
