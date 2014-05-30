# -*- coding: utf-8 -*-
from datetime import datetime as dt
import random, traceback, transaction
from tg import expose, flash, require, url, request, redirect
from repoze.what import predicates
from repoze.what.predicates import not_anonymous, in_group
import json



from tribal.lib.base import BaseController
from tribal.model import DBSession, metadata
from tribal import model
from tribal.util.common import *
from tribal.controllers import *

import logging
from tribal.controllers.master import BBYContactController
logger = logging.getLogger( __name__ )

__all__ = ['RootController']

import thread
myLock = thread.allocate_lock()

class RootController( BaseController ):

    order = OrderController()
#    report=ReportController()
    orsay = OrsayController()
    orchestra = OrchestraController()
#    cabelas = CabelasController()
    sample = SampleController()
    prepress = PrepressController()
#    pei = PEIController()
    access = AccessController()
#    itemcode = ItemCodeController()
#    itemattr = ItemAttrController()
#    itemclass = ItemClassController()
#    material = MaterialController()
#    size = SizeController()
#    style = StyleController()
#    color = ColorController()
#    upc = UPCController()
    dba = DBAController()
    dba2 = DBA2Controller()
    dbacustomer = DBACustomerController()
    dbaitem = DBAItemController()
    dbacategory = DBACategoryController()
    dbaitemtype = DBAItemTypeController()
    tag = TAGController()
    lemmi = LemmiController()
    tmw = TMWController()
    ws = WSController()    # mglobalpack webservice

    #===========================================================================
    # bby controllers
    #===========================================================================
    sku = BBYSKUController()
    bbycasepack = BBYCasepackController()
    bbymockup = BBYMockupController()
    bbyreport = BBYReportController()
    #===========================================================================
    # master tag
    #===========================================================================
    bby_brand = BBYBrandController()
    bby_pf = BBYPackagingFormatController()
    bby_material = BBYMaterialController()
    bby_spec = BBYSpecController()
    bby_closure = BBYClosureController()
    bby_dm = BBYDisplayModeController()
    bby_fr = BBYFailureReasonController()
    bby_courier = BBYCourierController()
    bby_mc = BBYMockupContentController()
    bby_vendor = BBYVendorController()
    bby_tm = BBYTeammateController()
    bby_source = BBYSourceController()
    bby_material_spec = BBYMaterialSpecController()
    bby_agent = BBYAgentController()
    bby_contact = BBYContactController()


    #===========================================================================
    # master sample
    #===========================================================================
    sample_customer = SampleCustomerController()
    sample_program = SampleProgramController()
    sample_project = SampleProjectController()
    sample_region = SampleRegionController()
    sample_stock = SampleStockController()
    sample_team = SampleTeamController()
    sample_extra_info = SampleExtraInfoController()
    sample_type_mapping = SampleTypeMappingController()
    sample_item_category = SampleItemCategoryController()


    #===========================================================================
    # master press system
    #===========================================================================
    prepress_item_category = PrepressItemCategoryController()


    @require( not_anonymous() )
    @expose( 'tribal.templates.index' )
    @tabFocus( tab_type = "main" )
    def index( self ):
        return dict( page = 'index' )


    @require( not_anonymous() )
    @expose( 'tribal.templates.tracking' )
    @tabFocus( tab_type = "view" )
    def tracking( self ):
        return {}

    @require( not_anonymous() )
    @expose( 'tribal.templates.report' )
    @tabFocus( tab_type = "report" )
    def report( self ):
        return {}

    @expose( 'tribal.templates.login' )
    def login( self, came_from = url( '/' ) ):
        """Start the user login."""
        if request.identity: redirect( came_from )

        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash( 'Wrong credentials', 'warning' )
        return dict( page = 'login', login_counter = str( login_counter ), came_from = came_from )

    @expose()
    def post_login( self, came_from = url( '/' ) ):
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
            redirect( url( '/login', came_from = came_from, __logins = login_counter ) )
        userid = request.identity['repoze.who.userid']
#        flash('Welcome back, %s!' % userid)
        redirect( came_from )

    @expose()
    def post_logout( self, came_from = url( '/' ) ):
#        flash('We hope to see you soon!')
        redirect( url( "/" ) )

    @require( not_anonymous() )
    @expose( 'tribal.templates.page_master' )
    @tabFocus( tab_type = "master" )
    def master( self ):
        """Handle the front-page."""
        return {}

    @expose()
    def download( self, **kw ):
        try:
            obj = DBSession.query( UploadObject ).get( kw["id"] )
            return serveFile( obj.file_path, obj.file_name )
        except:
            traceback.print_exc()
            flash( "No such file!" )
            redirect( "/index" )


    @expose()
    def upload( self, **kw ):
        try:
            print "*-" * 30
            print type( kw["attachment"] )
            print "*-" * 30

            file_path = kw["attachment"].filename
            ( pre, ext ) = os.path.splitext( file_path )

            path_prefix = os.path.join( config.download_dir, "sys" )
            if not os.path.exists( path_prefix ) : os.makedirs( path_prefix )

            file_name = "%s%.4d%s" % ( dt.now().strftime( "%Y%m%d%H%M%S" ), random.randint( 1, 1000 ), ext )

            print file_name
            print "*-" * 30

            full_path = os.path.join( path_prefix, file_name )

            f = open( full_path, "wb" )
            f.write( kw["attachment"].file.read() )
            f.close()

            db_file_name = kw.get( "attachment_name", None ) or file_name
            if db_file_name.find( "." ) < 0 : db_file_name = db_file_name + ext

            obj = UploadObject( file_name = db_file_name, file_path = os.path.join( "sys", file_name ) )
            DBSession.add( obj )
            DBSession.flush()
            return obj.id
        except:
            traceback.print_exc()
            return None

