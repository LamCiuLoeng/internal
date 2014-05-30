# -*- coding: utf-8 -*-
import simplejson as json
import traceback, random, shutil
import os
from datetime import datetime as dt, timedelta
from tg import request, redirect, flash, expose
from tg.decorators import paginate


from repoze.what import authorize
from repoze.what.predicates import has_permission
from sqlalchemy.sql import *


# project specific imports
from tribal.lib.base import BaseController
from tribal.model.prepress import *
from tribal.model import prepress as prepressDB
from tribal.util.common import *
from tribal.util.excel_helper import *
from tribal.widgets.prepress import *
from tribal.util.file_util import create_zip
from tribal.util.decorators import paginate_addition

from tribal.util.prepress_helper import getPSUserRegions, getPSUserTeams, \
    countTime


log = logging.getLogger( __name__ )



__all__ = ['PrepressController', ]


JOB_TYPE_MAPPING = {
                      'upload' : 'Upload',
                      'download' : 'Download',
                      'preflight' : 'Artwork Pre-Flight',
                      'adaption' : 'Artwork Adaption',
                      'design' : 'Artwork Design',
                      'artwork' : 'Artwork Checking',
                      'layout' : 'Full-set Layout',
                      'barcode' : 'Barcode',
                    }



class PrepressController( BaseController ):
    allow_only = authorize.not_anonymous()

    @expose( 'tribal.templates.prepress.index' )
    @paginate_addition( '/prepress/index' )
    @paginate( "result", items_per_page = 20 )
    @tabFocus( tab_type = "main" )
    def index( self, **kw ):
        ws = [PSMainForm.active == 0]
        if kw.get( "project_own", False ) : ws.append( PSMainForm.project_own_id == kw["project_own"] )

        if kw.get( "reference_code", False ) : ws.append( PSMainForm.__table__.c.reference_code.op( "ilike" )( "%%%s%%" % kw["reference_code"] ) )
        if kw.get( "contact_person", False ) : ws.append( PSMainForm.__table__.c.contact_person.op( "ilike" )( "%%%s%%" % kw["contact_person"] ) )
        if kw.get( "customer", False ) : ws.append( PSMainForm.customer_id == kw["customer"] )

        if kw.get( "item_category", False ) : ws.append( PSMainForm.item_category_id == kw["item_category"] )

        if kw.get( "project", False ) : ws.append( PSMainForm.__table__.c.project.op( "ilike" )( "%%%s%%" % kw["project"] ) )
        if kw.get( "create_by", False ) : ws.append( PSMainForm.create_by_id.in_( select( [User.user_id],
                                                                                   User.__table__.c.display_name.op( "ilike" )( "%%%s%%" % kw["create_by"] ) ) ) )
        if kw.get( "contact_team", False ) : ws.append( PSMainForm.team_id == kw["contact_team"] )
        if kw.get( "team", False ) :
            teams = DBSession.query( Team ).filter( Team.active == 0 ).filter( Team.id == kw["team"] ).first()
            ws.append( PSMainForm.rpt == teams.name )
        if kw.get( "project_owner", False ): ws.append( PSMainForm.__table__.c.project_owner.op( "ilike" )( "%%%s%%" % kw["project_owner"] ) )
        if kw.get( "item_description", False ) : ws.append( PSMainForm.__table__.c.item_description.op( "ilike" )( "%%%s%%" % kw["item_description"] ) )
        if kw.get( "system_no", False ) : ws.append( PSMainForm.__table__.c.system_no.op( "ilike" )( "%%%s%%" % kw["system_no"] ) )
        if kw.get( "item_code", False ) : ws.append( PSMainForm.__table__.c.item_code.op( "ilike" )( "%%%s%%" % kw["item_code"] ) )

        if kw.get( "create_time_from", False ) : ws.append( PSMainForm.create_time >= kw["create_time_from"] )
        if kw.get( "create_time_to", False ) : ws.append( PSMainForm.create_time <= kw["create_time_to"] )


        if kw.get( "status", False ) :
            ws.append( PSMainForm.status == int( kw["status"] ) )
        else:
            ws.append( PSMainForm.status > DRAFT )

        # for the sort function
        field = kw.get( "field", None ) or "update_time"
        direction = kw.get( "direction", None ) or "desc"

        if direction == 'desc':
            result = DBSession.query( PSMainForm ).filter( and_( *ws ) ).order_by( desc( getattr( PSMainForm, field ) ) ).all()
        else:
            result = DBSession.query( PSMainForm ).filter( and_( *ws ) ).order_by( getattr( PSMainForm, field ) ).all()
        return {"widget" : ps_search_form, "values" : kw, "result" : result}


    @expose( "tribal.templates.prepress.new_request" )
    @tabFocus( tab_type = "main" )
    def newRequest( self, **kw ):
        rpt = None
        teams = []
        regions = []
        request_team = None
        for g in request.identity["user"].groups:
            for profile in g.prepress_profiles:
                if profile.team :
                    rpt = profile.team
                    request_team = profile.team.id
                    if profile.team not in teams:teams.append( profile.team )
                if profile.region : regions.append( profile.region )


        return {
                "regions": regions, "regions_groups": Region.find_all(),
                "teams": teams, "teams_groups":Team.find_all(), "rpt": rpt, "request_team": request_team,
                "item_categries": PSItemCategory.find_all(), "token": createToken(), "isWorkTime" : isWorkTime(),
                }



    @expose( "tribal.templates.prepress.view_request" )
    @tabFocus( tab_type = "main" )
    def viewRequest( self, **kw ):
        try:
            h = getOr404( PSMainForm, kw["id"], "/prepress/index" )
            if h.status == DRAFT:
                raise Exception( "illegal operation: the main form can't viewed when status is draft" )
            childrenForms = []
            updatedChildrenForms = []
            canCancelForms = []

            for c in h.getChildrenForm():
                childrenForms.append( '%s-%s' % ( c.__class__.__name__, c.id ) )
                if c.status in [PS_NEW_REQUEST, ]:updatedChildrenForms.append( '%s-%s' % ( c.__class__.__name__, c.id ) )
                if c.status not in [PS_COMPLETED_REQUEST, PS_CANCELED_REQUEST, PS_DRAFT] : canCancelForms.append( '%s_%s' % ( c.__class__.__name__, c.id ) )
            rpt = None
            for g in h.create_by.groups:
                for profile in g.prepress_profiles:
                    if profile.team :
                        rpt = profile.team
            app_teams = DBSession.query( PSAppTeam ).filter( and_( PSAppTeam.active == 0 ) ).order_by( PSAppTeam.name ).all()

            return {"main": h,
                    "childrenForms": json.dumps( childrenForms ),
                    "rpt": rpt, "token": createToken(),
#                    "updatedChildrenForms" : json.dumps(h.new_or_update),
                    "updatedChildrenForms" : json.dumps( updatedChildrenForms ),
                    "canCancelForms" : "|".join( canCancelForms ),
                    "app_teams" : app_teams,
                    }
        except Exception, e:
            log.exception( str( e ) )
            flash( "Error occor on the server side!", 'warn' )
            redirect( "/prepress/index" )



    @expose( "tribal.templates.prepress.update_request" )
    @tabFocus( tab_type = "main" )
    def updateRequest( self, **kw ):
        try:
            h = getOr404( PSMainForm, kw["id"], "/prepress/index" )
            childrenForms = []
            for c in h.getChildrenForm():
                childrenForms.append( '%s-%s' % ( c.__class__.__name__, c.id ) )

            teams = []

            regions = []
            rpt = None
            for g in h.create_by.groups:
                for profile in g.prepress_profiles:
                    if profile.team :
                        teams.append( profile.team )
                        rpt = profile.team
                    if profile.region : regions.append( profile.region )
            return {"childrenForms": json.dumps( childrenForms ), "main": h, "rpt": rpt,
                    "regions": regions, "regions_groups": Region.find_all(),
                    "teams": teams, "teams_groups": Team.find_all(),
                    "item_categories": PSItemCategory.find_all(), "token": createToken(),
                    "is_draft": True if h.status == PS_DRAFT else False,
                    "isWorkTime" : isWorkTime(),
                    # "customers" : Customer.find_all(), "programs" : Program.find_all(), "users" : getAllSampleUsers(),
                    }
        except Exception, e:
            traceback.print_exc()
            log.exception( str( e ) )
            flash( "Error occor on the server side!", 'warn' )
            redirect( "/prepress/index" )



    @expose( 'tribal.templates.prepress.session_sub' )
    def getSubForm( self, **kw ):
        try:
            tab_id = kw["tab_id"]
            form_id = tab_id.split( '-' )[1]
            dbObject = getattr( prepressDB, form_id )
            widget = dbObject.getWidget()()
            prefix = "%s-" % form_id
            action = kw['action']
            regions = getPSUserRegions( request.identity["user"] )
            result = {"flag": 0, "js_url": widget.js_url, 'action': action, 'tab_id':tab_id, 'token': kw['token']}
            if kw.get( 'sub_id', None ):
                sub_id = kw['sub_id']
                cf = dbObject.get( sub_id )
                html = None
                if action == 'view':
                    jobdata = {}
                    for job in DBSession.query( PSJob ).filter( and_( PSJob.active == 0,
                                                                      PSJob.sub_form_type == form_id,
                                                                      PSJob.sub_form_id == sub_id ) ):
                        jobdata['%s_%s_%s' % ( job.sub_form_type, job.sub_form_id, job.job_type )] = job.status

                    html = widget( cf.populateAsDict( prefix ), formPrefix = prefix, isDisable = True,
                                   dbObject = cf, action = action, regions = regions, jobdata = jobdata )
                    result.update( {'cf': cf, "stocks": Stock.find_all()} )

                else:    # update or copy
                    html = widget( cf.populateAsDict( prefix ), formPrefix = prefix, dbObject = cf, action = action, regions = regions )
                result.update( {'sub_id': sub_id, 'main_id': cf.main_id, 'html': html} )
            else:
                result.update( {'html': widget( {}, formPrefix = prefix, dbObject = dbObject, action = action, regions = regions )} )
            return result
        except Exception, e:
            log.exception( str( e ) )
            return {"flag" : 1}


    @expose( 'json' )
    def saveMainForm( self, **kw ):
        try:
            DBSession.add( FormSerialize( **{'token': kw['token'], 'type': 'main', 'serialize': kw} ) )
            return {"flag":0}
        except Exception, e:
            log.exception( str( e ) )
            flash( "Error occur on the server side!", "warn" )
            return {"flag":1}


    @expose( '' )
    def saveSubForm( self, **kw ):
        try:
            uploadAttachments( kw )
            DBSession.add( FormSerialize( **{'token': kw['token'], 'type': 'sub', 'serialize': kw} ) )
        except Exception, e:
            log.exception( str( e ) )
            return 'error'

    @expose()
    def completeSubForm( self, **kw ):
        '''Complete or add_job_report action submits sub_form.'''
        try:
            uploadAttachments( kw )
            DBSession.add( FormSerialize( **{'token': kw['token'], 'type': 'sub', 'serialize': kw} ) )
            ( formType, id ) = kw['form_ids'].split( "_" )
            dbclz = self._getDBClzByID( formType )
            dbobj = DBSession.query( dbclz ).get( id )
            complete_attachment = dbobj.complete_attachment.split( '|' ) if dbobj.complete_attachment else []
            dbobj.complete_attachment = '|'.join( [str( id ) for id in kw.get( 'attachment_ids', [] ) + complete_attachment] )
            params = dict( 
                main_form_id = dbobj.main_id,
                sub_form_id = dbobj.id,
                sub_form_type = formType,
#                 time_spand = kw.get( "time_spand", None ),
                item = kw.get( "item", 0 ),
                remark = kw["remark"],
            )
            psjob = PSJob( **params )
            DBSession.add( psjob )
            if kw.get( "action" ) == 'C': self.ajaxMark( **kw )    # if action is complete, update sub form's status
        except Exception, e:
            log.exception( str( e ) )
            return 'error'
        else:
            redirect( "/prepress/getSubForm?tab_id=%s&action=view&token=%s&sub_id=%s" % ( kw['tab_id'], kw['token'], kw['sub_id'] ) )

    @expose()
    def saveFormSuccess( self, **kw ):

        def _after_save( main_obj ):
            h = main_obj
            # send email for new or update

            if main_obj.assign_users:
                ids = filter( bool, main_obj.assign_users.split( "|" ) )
                send_users = [u.email_address for u in DBSession.query( User ).filter( User.user_id.in_( ids ) ) if u.email_address]
            else:
                us = set()
                per = DBSession.query( Permission ).filter( Permission.permission_name == 'PREPRESS_ASSIGN' ).one()
                for g in per.groups:
                    for u in g.users:
                        if u.email_address : us.add( u.email_address )
                send_users = list( us )

            self._sendNotifyEmail( main_obj , send_users = send_users )

            # update the main form's percentage
            status_list = [c.status for c in main_obj.getChildrenForm()]
            completed_list = filter( lambda v: v == PS_COMPLETED_REQUEST, status_list )
            main_obj.percentage = float( len( completed_list ) ) / len( status_list )
            if len( completed_list ) != len( status_list ) and main_obj.status == PS_COMPLETED_REQUEST : main_obj.status = PS_UNDER_DEVELOPMENT
            elif len( completed_list ) == len( status_list ) and main_obj.status != PS_COMPLETED_REQUEST : main_obj.status = PS_COMPLETED_REQUEST

        def _before_update( main_obj ):
            # save the main obj and children history
            main_obj_copy = main_obj
            main_obj_copy.project_own = main_obj.project_own
            main_obj_copy.team = main_obj.team
            main_obj_copy.customer = main_obj.customer
            main_obj_copy.project = main_obj.project
            main_obj_copy.item_category = main_obj.item_category
            DBSession.add( PSFormVersion( **{'main_id': main_obj.id, 'version': "%s-RC%.2d" % ( main_obj.system_no, main_obj.revision ) if main_obj.revision else main_obj.system_no, 'serialize': {'main':main_obj_copy, 'subs': main_obj.getChildrenForm()}} ) )

        token = kw['token']
        is_draft = True if kw['is_draft'] == 'true' else False
        try:
            # forms = session['form'][token]
            forms = FormSerialize.find_by_token( kw['token'] )
            action = kw['action']
            main_obj = None
            old_sub_forms = {}

            childfroms_new_or_update = []    # mark which child form is new added or updated
            old_job_status = None

            for form in forms:
                if form.type == 'main':    # save the main form
                    main_kw = form.serialize
                    if action == 'new' or action == 'copy':
                        main_obj = PSMainForm.create( is_draft = is_draft, **main_kw )
                        DBSession.flush()
                    elif main_kw.get( 'id', None ):
                        main_obj = getOr404( PSMainForm, main_kw["id"], "/prepress/index" )
                        if not is_draft:
                            _before_update( main_obj )
                        old_sub_forms = main_obj.getChildrenDict()
                        log.debug( 'old_sub_forms initialize: %s' % old_sub_forms )
                        old_job_status = main_obj.status
                        main_obj.update( is_draft = is_draft, **main_kw )
                else:    # save the sub form
                    sub_kw = form.serialize
                    obj_id = sub_kw['tab_id'].split( '-' )[1]
                    main_id = main_obj.id
                    formPrefix = "%s-" % obj_id
                    dbclz = self._getDBClzByID( obj_id )
                    if not sub_kw.get( 'id', None ):    # when sub form is new
                        log.debug( 'create sub action %s: %s' % ( sub_kw['action'], obj_id ) )
                        obj = dbclz.saveNewWithDict( sub_kw, formPrefix )
                        obj.main_id = main_id
                        attachment_copy_ids = sub_kw.get( '%sattachment_copy' % formPrefix )
                        if action == 'copy' and attachment_copy_ids:
                            copy_attachments = [str( i ) for i in dbclz.copyAttachments( attachment_copy_ids )]
                            obj.attachment = '%s|%s' % ( obj.attachment, '|'.join( copy_attachments ) ) if obj.attachment else '|'.join( copy_attachments )
                        #=======================================================
                        # if the main form is assign before
                        #=======================================================
                        if main_obj is not None and main_obj.status != PS_NEW_REQUEST:    # the main form has been assigned bedore
                            obj.status = PS_ASSIGNED    # no need to assign again

                        DBSession.add( obj )
                        DBSession.flush()
                        childfroms_new_or_update.append( "%s-%s" % ( obj_id, obj.id ) )
                    else:    # when the sub form is update
                        sub_id = sub_kw['id']
                        log.debug( 'update sub action %s: %s id: %s' % ( sub_kw['action'], obj_id, sub_id ) )
                        del old_sub_forms[obj_id][sub_id]
                        sfForm = dbclz.get( sub_id )
                        old_object = sfForm.serialize()
                        attachment_update = sub_kw.get( '%sattachment_update' % formPrefix )
                        if isinstance( attachment_update, str ) or isinstance( attachment_update, unicode ):
                            attachment_update = [attachment_update]
                        sfForm.attachment = '|'.join( attachment_update ) if attachment_update else ''
                        sfForm.saveUpdateWithDict( sub_kw, prefix = "%s-" % dbclz.__name__ )
                        new_object = sfForm.serialize( False )
                        check_log = dbclz.compareObject( old_object, new_object )
                        log_str = []
                        for ( key, old_val, new_val ) in check_log['update']:
                            log_str.append( "Change [%s] from '%s' to '%s' " % ( key, old_val, new_val ) )
                        if log_str :    # if there is update
                            if old_job_status != PS_DRAFT:
                                DBSession.add( PSDevelopmentLog( system_no = str( sfForm.main ), main_form_id = sfForm.main_id, sub_form_id = sfForm.id, sub_form_type = dbclz.__name__, action_type = 'UPDATE', remark = " .\n".join( log_str ) ) )
                            sfForm.status = PS_NEW_REQUEST
                            sfForm.send_email = 0    # reset the send mail flag
                            childfroms_new_or_update.append( "%s-%s" % ( obj_id, sub_id ) )
                        else:
                            if not is_draft and old_job_status == PS_DRAFT:    # if the form is changed from draft to save, all the tabs should be views as 'new'!
                                childfroms_new_or_update.append( "%s-%s" % ( obj_id, sub_id ) )

            if action == 'update' and main_obj:
                log.debug( 'old_sub_forms will be inactive: %s' % old_sub_forms )
                for k, v in old_sub_forms.iteritems():
                    if v.keys():
                        for _k, _v in v.iteritems():
                            _v.active = 1
                log.debug( 'child form: %s' % main_obj.child_form )
            if not is_draft:
                main_obj.new_or_update = childfroms_new_or_update
                _after_save( main_obj )
            self._removeSession( token )
        except Exception, e:
            traceback.print_exc()
            log.exception( str( e ) )
            log.exception( 'Save job form success exception!!! %s' % kw )
            transaction.doom()
            flash( "Error occur on the server side!", "warn" )
            redirect( "/prepress/index" )
        else:
            if is_draft:
                flash( "Job draft has been successfully saved, Job No.: %s" % str( main_obj ) )
                redirect( "/prepress/index" )
            else:
                flash( "Job request has been successfully submitted, Job No.: %s" % str( main_obj ) )
                redirect( "/prepress/viewRequest?id=%s" % main_obj.id )


    @expose()
    def saveFormFail( self, **kw ):
        log.exception( 'Save job form failure!!! %s' % kw )
        flash( "Error occur on the server side!", "warn" )
        redirect( "/prepress/index" )




    #===========================================================================
    # ajax action for the job start ,pending ,complete ,restart, cancelled
    #===========================================================================
    @expose( "json" )
    @expose()
    def ajaxAction( self, **kw ):
        sf_id = kw.get( 'sf_id', None )
        sf_type = kw.get( 'sf_type', None )
        job_type = kw.get( 'job_type', None )
        action = kw.get( 'action', None )
        emailExtra = {}

        if not all( [sf_id, sf_type, job_type, action] ):
            traceback.print_exc()
            logError()
            return {"flag" : 1, "msg" : "No proper parameters provided!"}

        if sf_type not in ['PSSFUpload', 'PSSFBarcode'] : return {"flag" : 1, "msg" : "Parameters are not correct!"}
        if action not in ['START', 'COMPLETE', 'PENDING', 'RESTART', 'CANCEL' ] : return {"flag" : 1, "msg" : "No such action!"}


        job_type_mapping = {
                            'upload' : 'Upload', 'download' : 'Download', 'preflight' : 'Artwork Pre-Flight',
                            'adaption' : 'Artwork Adaption', 'design' : 'Artwork Design', 'artwork' : 'Artwork Checking',
                            'layout' : 'Full-set Layout', 'barcode' : 'Barcode',
                            }

        try:
            if sf_type == 'PSSFUpload': sfclz = PSSFUpload
            elif sf_type == 'PSSFBarcode' : sfclz = PSSFBarcode

            sfobj = DBSession.query( sfclz ).get( sf_id )
            current = Date2Text( dateTimeFormat = "%Y/%m/%d %H:%M", defaultNow = True )
            needEmail = False
            if action == 'START':
                isStart = DBSession.query( PSJob ).filter( and_( PSJob.active == 0,
                                                                 PSJob.main_form_id == sfobj.main_id ) ).count() < 1
                jobobj = PSJob( main_form_id = sfobj.main_id, sub_form_id = sfobj.id, sub_form_type = sf_type,
                               job_type = job_type, status = PS_JOB_NEW, time_list = current, )
                DBSession.add( jobobj )

                if isStart:
                    needEmail = True
                sfobj.status = PS_UNDER_DEVELOPMENT

            elif action == 'COMPLETE':
                jobobj = DBSession.query( PSJob ).filter( and_( PSJob.active == 0, PSJob.sub_form_type == sf_type,
                                                   PSJob.main_form_id == sfobj.main_id,
                                                   PSJob.sub_form_id == sfobj.id, PSJob.job_type == job_type ) ).one()

#                 jobobj.time_spand = kw.get( 'job_time_spand', 0 )
                jobobj.item = kw.get( 'job_item', 0 )
                jobobj.remark = kw.get( 'job_remark', None )
                jobobj.status = PS_JOB_COMPLETE
                jobobj.time_list += '|' + current
                jobobj.time_count = countTime( jobobj.time_list )

                #===============================================================
                # check the sub form's status
                #===============================================================
                if sf_type == 'PSSFBarcode' : sfobj.status = PS_COMPLETED_REQUEST
                else:
                    completeJob = DBSession.query( PSJob ).filter( and_( PSJob.active == 0 , PSJob.sub_form_type == sf_type,
                                                       PSJob.main_form_id == sfobj.main_id,
                                                       PSJob.sub_form_id == sfobj.id, PSJob.status == PS_JOB_COMPLETE ) ).count()
                    if completeJob == len( sfobj.checking or [] ) :
                        sfobj.status = PS_COMPLETED_REQUEST
                        sfobj.complete_time = dt.now()
                        sfobj.complete_by_id = request.identity["user"].user_id
                #===============================================================
                # check the total main form's status is completed or no
                #===============================================================
                completedCount = DBSession.query( PSJob ).filter( and_( PSJob.active == 0, PSJob.main_form_id == sfobj.main_id,
                                                                        PSJob.status == PS_JOB_COMPLETE ) ).count()
                taskTotal = DBSession.query( PSSFBarcode ).filter( and_( PSSFBarcode.active == 0 ,
                                                                            PSSFBarcode.main_id == sfobj.main_id, ) ).count()
#                 uploadTotal = 0
                for sf in DBSession.query( PSSFUpload ).filter( and_( PSSFUpload.active == 0 ,
                                                                      PSSFUpload.main_id == sfobj.main_id ) ):
                    taskTotal += len( sf.checking or [] )

                allComplete = completedCount == taskTotal
                #===============================================================
                # update the main job's percentage
                #===============================================================
                sfobj.main.percentage = float( completedCount ) / taskTotal if taskTotal else 0

                if allComplete:
                    needEmail = True
                    flag = "%s-%s" % ( sf_type, sfobj.id )
                    if  flag in sfobj.main.new_or_update : sfobj.main.new_or_update = sfobj.main.new_or_update.remove( flag )

                #===============================================================
                # handle the attachment
                #===============================================================
                flag, fids = sysUpload( attachment_list = [v for k, v in kw.iteritems() if k.startswith( "jobfile" )] )
                fids = filter( bool, fids )
                if fids :
                    if sfobj.complete_attachment :
                        sfobj.complete_attachment = '%s|%s' % ( sfobj.complete_attachment, '|'.join( map( unicode, fids ) ) )
                    else :
                        sfobj.complete_attachment = '|'.join( map( unicode, fids ) )

            elif action == 'PENDING':
                for j in DBSession.query( PSJob ).filter( and_( PSJob.active == 0, PSJob.sub_form_id == sfobj.id, PSJob.sub_form_type == sf_type,
                                                                PSJob.status == PS_JOB_NEW, ) ):
                    j.status = PS_JOB_PENDING
                    j.time_list += '|' + current

                sfobj.status = PS_PENDING
                needEmail = True
                emailExtra['reason'] = kw.get( 'reason', None )

            elif action == 'RESTART':
                for j in DBSession.query( PSJob ).filter( and_( PSJob.active == 0, PSJob.sub_form_id == sfobj.id, PSJob.sub_form_type == sf_type,
                                                                PSJob.status == PS_JOB_PENDING, ) ):
                    j.status = PS_JOB_NEW
                    j.time_list += '|' + current
                sfobj.status = PS_UNDER_DEVELOPMENT

            DBSession.add( PSDevelopmentLog( main_form_id = sfobj.main_id, system_no = str( sfobj.main ), sub_form_id = sfobj.id, sub_form_type = sf_type,
                                       action_type = "PROCESS", remark = '%s "%s".' % ( action, job_type_mapping.get( job_type, '' ) ) ) )

#             if isStatusChange:
            # do if the job's status change
            # check the job's status
            header = sfobj.main
            childrenStatus = []
            for c in header.getChildren():
                clildClz = self._getDBClzByID( c )
                for sf in DBSession.query( clildClz ).filter( and_( clildClz.active == 0, clildClz.main_id == header.id ) ) : childrenStatus.append( sf.status )

            new = childrenStatus.count( PS_NEW_REQUEST )
            completed = childrenStatus.count( PS_COMPLETED_REQUEST )
            pending = childrenStatus.count( PS_PENDING )
            develop = childrenStatus.count( PS_UNDER_DEVELOPMENT )
            cancel = childrenStatus.count( PS_CANCELED_REQUEST )

#             header.percentage = float( completed + cancel ) / len( childrenStatus )

            # update the job's status
            #===================================================================
            # S2 New
            # S3 Under Development
            # S4 Pending
            # S5 Complete
            # S7 Cancel
            #===================================================================

            def _markComplete():
                header.status = PS_COMPLETED_REQUEST
                header.complete_time = dt.now()
                header.complete_by_id = request.identity["user"].user_id

            if new == len( childrenStatus ) : header.status = PS_NEW_REQUEST    # ALL S2
            elif develop == len( childrenStatus ) : header.status = PS_UNDER_DEVELOPMENT    # ALL S3
            elif pending == len( childrenStatus ) : header.status = PS_UNDER_DEVELOPMENT    # ALL S4
            elif cancel == len( childrenStatus ) : header.status = PS_CANCELED_REQUEST    # ALL S7
            elif completed == len( childrenStatus ) : _markComplete()    # ALL S5
            elif new + cancel == len( childrenStatus ) : header.status = PS_NEW_REQUEST    # S2 + S7
            elif completed + cancel == len( childrenStatus ) : _markComplete()    # S5 + S7
            else: header.status = PS_UNDER_DEVELOPMENT

            if needEmail:  self._sendNotifyEmail( h = header, type = action, task_label = sfobj.getWidget().label, extra = emailExtra )
        except:
            traceback.print_exc()
            logError()
            return {"flag" : 1, "msg" : "Error occur on the server side ,please try again or contact the system admin."}
        else:
            if action == 'COMPLETE':
                url = request.headers.get( 'referer', '' ) or '/prepress/getSubForm?tab_id=tab-PSSFUpload&action=view&is_draft=false&sub_id=%s&token=' % sf_id
                return redirect( url )
            else:
                return {"flag" : 0}


    '''
    @expose( "json" )
    def ajaxMark( self, **kw ):
        statusType = {
                      "G" : ( PS_UNDER_DEVELOPMENT, "Restart" ),    # need to send email
                      "C" : ( PS_COMPLETED_REQUEST, "Complete" ) ,
                      "X" : ( PS_CANCELED_REQUEST, "Cancel" ),    # need to send email
                      "P" : ( PS_PENDING, "Pending" ),    # need to send email
                      "S" : ( PS_UNDER_DEVELOPMENT, "Start work" ) ,
                      }

        if kw["action"] not in statusType : return {"flag" : 2}

        try:
            task_labels = []
            for form_id in kw["form_ids"].split( "|" ):
                ( formType, id ) = form_id.split( "_" )
                dbclz = self._getDBClzByID( formType )
                task_labels.append( dbclz.getWidget().label )    # used to send email for cancel and pending
                dbobj = DBSession.query( dbclz ).get( id )

                if kw["action"] == "G" :    # restore the status
                    dbobj.status_back , dbobj.status = dbobj.status, dbobj.status_back
                else:
                    dbobj.status_back , dbobj.status = dbobj.status, statusType[kw["action"]][0]
                # Record time of start/pending/complete action for counting worktime
                if kw["action"] in ['S', 'P', 'C', 'G']:
                    worktime = dbobj.worktime.split( '|' ) if dbobj.worktime else []
                    dbobj.worktime = '|'.join( worktime + [dt.now().strftime( "%Y/%m/%d %H:%M" ), ] )
                else:
                    dbobj.worktime = None

                l = PSDevelopmentLog( main = dbobj.main, system_no = str( dbobj.main ), sub_form_id = dbobj.id, sub_form_type = dbclz.__name__,
                                   action_type = "PROCESS", remark = statusType[kw["action"]][1] )
                DBSession.add( l )
                if kw["action"] == "C":
                    dbobj.complete_time = dt.now()
                    dbobj.complete_by_id = request.identity["user"].user_id
                    dbobj.spendmins = countTime( dbobj.worktime )
                    flag = "%s-%s" % ( formType, id )
                    if  flag in dbobj.main.new_or_update : dbobj.main.new_or_update = dbobj.main.new_or_update.remove( flag )

            # check the whold request's status
            header = dbobj.main
            childrenStatus = []
            for c in header.getChildren():
                clildClz = self._getDBClzByID( c )
                for sf in DBSession.query( clildClz ).filter( and_( clildClz.active == 0, clildClz.main_id == header.id ) ) : childrenStatus.append( sf.status )


            new = childrenStatus.count( PS_NEW_REQUEST )
            completed = childrenStatus.count( PS_COMPLETED_REQUEST )
            pending = childrenStatus.count( PS_PENDING )
            develop = childrenStatus.count( PS_UNDER_DEVELOPMENT )
            cancel = childrenStatus.count( PS_CANCELED_REQUEST )
            header.percentage = float( completed + cancel ) / len( childrenStatus )

            # update the job's status
            #===================================================================
            # S2 New
            # S3 Under Development
            # S4 Pending
            # S5 Complete
            # S7 Cancel
            #===================================================================

            def _markComplete():
                header.status = PS_COMPLETED_REQUEST
                header.complete_time = dt.now()
                header.complete_by_id = request.identity["user"].user_id

            if new == len( childrenStatus ) : header.status = PS_NEW_REQUEST    # ALL S2
            elif develop == len( childrenStatus ) : header.status = PS_UNDER_DEVELOPMENT    # ALL S3
            elif pending == len( childrenStatus ) : header.status = PS_UNDER_DEVELOPMENT    # ALL S4
            elif cancel == len( childrenStatus ) : header.status = PS_CANCELED_REQUEST    # ALL S7
            elif completed == len( childrenStatus ) : _markComplete()    # ALL S5
            elif new + cancel == len( childrenStatus ) : header.status = PS_NEW_REQUEST    # S2 + S7
            elif completed + cancel == len( childrenStatus ) : _markComplete()    # S5 + S7
            else: header.status = PS_UNDER_DEVELOPMENT


            if kw["action"] in ['S', 'X', 'P', 'C', ]:    # send email
                action_type = {
                        'S' : 'STARTED',
                        'X' : 'CANCELLED',
                        'P' : 'PENDING',
                        'G' : 'RESTART',
                        'C' : 'COMPLETED',
                        }.get( kw['action'], '' )
                if action_type == 'PENDING':
                    header.reason = kw.get( 'pending_reason', '' )
                self._sendNotifyEmail( header, action_type, ",".join( task_labels ) )

            return {"flag" : 0, "percentage" : int( header.percentage * 100 ) , "whole_status" : header.status, "status" : dbobj.status}
        except:
            traceback.print_exc()
            logError()
            return {"flag" : 1}
    '''


    @expose( "json" )
    def ajaxTodoList( self, **kw ):
        try:
            base_condition = [PSMainForm.active == 0, ]
            if not has_permission( "PREPRESS_VIEW_ALL" ):    # AE team
                teams = map( lambda t:t.id, getPSUserTeams( request.identity["user"] ) )
                base_condition = [or_( PSMainForm.team_id.in_( teams ), PSMainForm.request_team_id.in_( teams ) )]
            else:    # prepress team
                if not has_permission( "PREPRESS_ASSIGN" ):    # not supervisor
                    teams = map( lambda t:t.id, getPSUserTeams( request.identity["user"], "appteam" ) )
                    base_condition = [PSMainForm.status >= PS_ASSIGNED, PSMainForm.app_team_id.in_( teams )]

            draft = DBSession.query( PSMainForm ).filter( and_( PSMainForm.active == 0, PSMainForm.status == PS_DRAFT, PSMainForm.create_by_id == request.identity['user'].user_id ) ).order_by( desc( PSMainForm.create_time ) )

            cs = DBSession.query( PSMainForm ).filter( and_( PSMainForm.status == PS_CANCELED_REQUEST, PSMainForm.update_time > ( dt.now() - timedelta( days = 90 ) ), *base_condition ) ).order_by( desc( PSMainForm.update_time ) )
            def _s( statusType ):
                union_clause = []
                for n in prepressDB.__all__:
                    if n.startswith( "PSSF" ):
                        dbclz = getattr( prepressDB, n )
                        union_clause.append( select( [dbclz.main_id], and_( dbclz.active == 0, dbclz.status == statusType ) ) )
                return DBSession.query( PSMainForm ).filter( and_( PSMainForm.status != DRAFT, PSMainForm.id.in_( union( *union_clause ) ), *base_condition ) ).order_by( desc( PSMainForm.update_time ) )

            ns = _s( PS_NEW_REQUEST )
            devs = _s( PS_UNDER_DEVELOPMENT )
            ps = _s( PS_PENDING )

            return {"flag" : 0,
                    'draft': [( d.id, str( d ) ) for d in draft[:5]],
                    'draft_count': draft.count(),
                    "new" : [( n.id, str( n ) ) for n in ns[:5]],
                    "new_count" : ns.count(),
                    "cancel" : [( c.id, str( c ) ) for c in cs[:5]],
                    "cancel_count" : cs.count(),
                    "pending" : [( p.id, str( p ) ) for p in ps[:5]],
                    "pending_count" : ps.count(),
                    "dev" : [( p.id, str( p ) ) for p in devs[:5]],
                    "dev_count" : devs.count(),
                    }
        except:
#            traceback.print_exc()
            logError()
            return {"flag" : 1}



    '''
    @expose( "json" )
    def ajaxAddJob( self, **kw ):
        try:
            clz = self._getDBClzByID( kw["form_clz"] )
            obj = DBSession.query( clz ).get( kw["form_id"] )
            params = dict( 
                      main_form_id = obj.main_id,
                      sub_form_id = obj.id,
                      sub_form_type = kw["form_clz"],
#                       time_spand = kw.get( "time_spand", None ),
                      item = kw.get( "item", 0 ),
                      remark = kw["remark"],
                      )

            h = PSJob( **params )
            DBSession.add( h )
            DBSession.flush()
            data = {
                    "id" : h.id,
#                     "time_spand" : kw["time_spand"],
                    "item" : kw["item"],
                    "create_by" : request.identity["user"].user_name,
                    "create_time" : dt.now().strftime( "%Y-%m-%d %H:%M" ),
                    "remark" : kw["remark"] or '',
                    }

            return {"flag" : 0, "data":data}
        except:
            logError()
            transaction.doom()
            return {"flag" : 1}
    '''


    '''
    @expose( "json" )
    def ajaxDeleteJob( self, **kw ):
        try:
            job = DBSession.query( PSJob ).get( kw.get( "id", None ) )
            l = PSDevelopmentLog( main = job.main, sub_form_id = job.sub_form_id, sub_form_type = job.sub_form_type, action_type = "Update",
                             remark = '%s delete the job[id=%s].' % ( request.identity["user"], job.id ) )
            DBSession.add( l )
            job.active = 1
            return {"flag" : 0}
        except:
            logError()
            return {"flag" : 1}
    '''


    def _sendNotifyEmail( self, h, type = 'NORMAL', task_label = None, send_users = [], extra = {} ):
        send_from = "r-track@r-pac.com.hk"
        if type == 'NORMAL':
            subject = "[PREPRESS]%s / %s / %s / %s" % ( h, h.reference_code, h.customer or '', h.item_code or '' )
            templatePath = os.path.join( config.get( "template_dir" ), "PREPRESS_NORMAL_EMAIL_TEMPLATE.html" )
        elif type in ['START', 'CANCEL', 'COMPLETE', 'PENDING']:
            subject = "[PREPRESS][%s] %s / %s / %s / %s" % ( type, h, h.reference_code, h.customer or '', h.item_code or '' )
            templatePath = os.path.join( config.get( "template_dir" ), "PREPRESS_CANCEL_PENDING_EMAIL_TEMPLATE.html" )
        elif type == 'ASSIGNED':
            subject = "[PREPRESS][%s] %s / %s / %s / %s" % ( type, h, h.reference_code, h.customer or '', h.item_code or '' )
            templatePath = os.path.join( config.get( "template_dir" ), "PREPRESS_ASSIGN_EMAIL_TEMPLATE.html" )

        subject = subject.replace( "\n", ' ' )
        send_to = []
        if request.identity["user"].email_address : send_to.append( request.identity["user"].email_address )
        if send_users: send_to.extend( send_users )

        cc_to = config.get( "prepress_email_cc", '' ).split( ";" )
        if h.cc_to :
            cc_to.extend( filter( lambda c : bool( c ), h.cc_to.split( ";" ) ) )
#        templatePath = os.path.join(config.get("template_dir"),"SAMPLE_NORMAL_EMAIL_TEMPLATE.html")
        template = open( templatePath )
        html = "".join( template.readlines() )
        template.close()

        url = "%s/prepress/viewRequest?id=%d" % ( config.get( 'website_url', 'http://service.r-pac.com.hk' ), h.id )

        if type in ['NORMAL', 'ASSIGNED']:
            labels = [c.getWidget().label for c in h.getChildrenForm() if "%s-%s" % ( c.__class__.__name__, c.id ) in h.new_or_update]
            content = html % ( h, h.rpt, h.create_by, h.update_by, h.customer or '', h.project, h.item_code or '', h.item_description or '', "/".join( labels ), url, url )
        else:
            if type == 'PENDING':
                reason = '<p>The pending reason: <span class="red">%s</span></p>.' % extra.get( 'reason', '' )
            else:
                reason = ''
            content = html % ( task_label, type, reason, h, h.rpt, h.create_by, h.update_by, h.customer or '', h.project, h.item_code or '', h.item_description or '', url, url )

        # if config.get("is_test", None) != 'true':  # if it's test, don't send email out
        advancedSendMail( send_from, send_to, subject, None, content, cc_to )



    @expose( "tribal.templates.prepress.report" )
    @tabFocus( tab_type = "report" )
    def report( self, **kw ):
        teams = DBSession.query( Team ).filter( and_( Team.active == 0 ) ).order_by( Team.name )
        return {"teams" : teams}



    @expose()
    def export( self, **kw ):
        if kw.get( "report_type", None ) not in ["SUMMARY", "DESIGNER_STATISTICS" ]:
            flash( "No such report type!" )
            return redirect( "/prepress/report" )

        if kw["report_type"] == "SUMMARY":
            try:
                teamTotal = self._getTeamTotal( kw )
                taskTotal = self._getTaskTotal( kw )
                summary = self._getJobSummary( kw )
                jobsummary = self._getJobTypeSummary( kw )
            except Exception, e:
                traceback.print_exc()
                raise e
            return serveFile( self._genSummaryReport( teamTotal, taskTotal, summary, jobsummary ) )



    def _getTeamTotal( self, kw ):
        cfrom = kw.get( 'create_time_from', '' ) or ''
        cto = kw.get( 'create_time_to', '' ) or ''
        cds = [PSMainForm.active == 0, PSMainForm.status == PS_COMPLETED_REQUEST,
               PSJob.active == 0, PSJob.status == PS_JOB_COMPLETE,
               PSMainForm.id == PSJob.main_form_id,
               Team.active == 0,
               Team.id == PSMainForm.team_id,
               ]
        if cfrom :  cds.append( PSMainForm.complete_time > cfrom )
        if cto:     cds.append( PSMainForm.complete_time <= cto + " 23:59:59" )

        data = DBSession.query( Team.name, func.sum( PSJob.item ) ).filter( and_( *cds ) ).group_by( Team.name ).order_by( Team.name )
        result = [( teamname, unicode( qty ) ) for ( teamname, qty ) in data]
        return result



    def _getTaskTotal( self, kw ):
        cfrom = kw.get( 'create_time_from', '' ) or ''
        cto = kw.get( 'create_time_to', '' ) or ''
        cds = [PSMainForm.active == 0, PSJob.active == 0 ,
               PSMainForm.status == PS_COMPLETED_REQUEST,
               PSMainForm.id == PSJob.main_form_id, PSJob.status == PS_JOB_COMPLETE, ]
        if cfrom :  cds.append( PSMainForm.complete_time > cfrom )
        if cto:     cds.append( PSMainForm.complete_time < ( cto + " 23:59:59" ) )

        tb = {
              'upload' : {'label' : 'Upload', 'count' : 0, },
              'download' : {'label' : 'Download', 'count' : 0, },
              'preflight' : {'label' : 'Artwork Pre-Flight', 'count' : 0, },
              'adaption' : {'label' : 'Artwork Adaption', 'count' : 0, },
              'design' : {'label' : 'Artwork Design', 'count' : 0, },
              'artwork' : {'label' : 'Artwork Checking', 'count' : 0, },
              'layout' : {'label' : 'Full-set Layout', 'count' : 0, },
              'barcode' : {'label' : 'Barcode', 'count' : 0, },
              }

        for jobtype, sitem in DBSession.query( PSJob.job_type, func.sum( PSJob.item ) ).filter( and_( *cds ) ).group_by( PSJob.job_type ):
            if jobtype not in tb : continue
            tb[jobtype]['count'] += sitem

        return [( v['label'], v['count'] ) for v in tb.values()]



    def _getJobTypeSummary( self, kw ):
        cfrom = kw.get( 'create_time_from', '' ) or ''
        cto = kw.get( 'create_time_to', '' ) or ''
        cds = [PSMainForm.active == 0, PSJob.active == 0 ,
               PSMainForm.status == PS_COMPLETED_REQUEST,
               PSMainForm.id == PSJob.main_form_id, PSJob.status == PS_JOB_COMPLETE,
#                PSMainForm.team_id == Team.id
               ]

        if cfrom :  cds.append( PSMainForm.complete_time > cfrom )
        if cto:     cds.append( PSMainForm.complete_time < ( cto + " 23:59:59" ) )

        result = {}
        for t in DBSession.query( Team ).filter( and_( Team.active == 0 ) ):
            jobMp = {}
            for v in JOB_TYPE_MAPPING.values() : jobMp[v] = 0
            result[t.id] = {
                            'label' : unicode( t ),
                            'jobs' : jobMp
                            }

        for m, j in DBSession.query( PSMainForm, PSJob ).filter( and_( *cds ) ) :
            if m.team_id not in result : continue
            if j.job_type not in JOB_TYPE_MAPPING : continue
            k = JOB_TYPE_MAPPING[j.job_type]
            if k not in result[m.team_id]['jobs'] : continue
            result[m.team_id]['jobs'][k] += j.item

        for k, v in result.items():
            if not any( v['jobs'].values() ) : result.pop( k )
            else:
                for kk, vv in v['jobs'].items():
                    if not vv : v['jobs'].pop( kk )



#         result = {}
#         for t, j in DBSession.query( PSMainForm, PSJob ).filter( and_( *cds ) ) :
#             tname = unicode( t )
#             if j.job_type not in result :
#                 result[j.job_type] = {
#                                        'label' : JOB_TYPE_MAPPING[j.job_type],
#                                        'data' : {tname : j.item}
#                                        }
#             else:
#                 if tname not in result[j.job_type]['data'] : result[j.job_type]['data'][tname] = j.item
#                 else: result[j.job_type]['data'][tname] += j.item
        return result




    def _getJobSummary( self, kw ):
        cfrom = kw.get( 'create_time_from', '' ) or ''
        cto = kw.get( 'create_time_to', '' ) or ''

        inputcds = [PSMainForm.active == 0, PSMainForm.status == PS_COMPLETED_REQUEST, ]
        if cfrom :  inputcds.append( PSMainForm.complete_time > cfrom )
        if cto:     inputcds.append( PSMainForm.complete_time < ( cto + " 23:59:59" ) )

        # grab the job detail first
        jobmapping = {}
        jobcds = [PSJob.active == 0, PSMainForm.id == PSJob.main_form_id,
                  PSJob.update_by_id == User.user_id, PSJob.status == PS_JOB_COMPLETE]
        jobcds.extend( inputcds )
        for job, user in DBSession.query( PSJob, User ).filter( and_( *jobcds ) ).order_by( PSJob.main_form_id, PSJob.id ):
            tmp = map( unicode, [JOB_TYPE_MAPPING.get( job.job_type, '' ), job.item, job.time_count, user] )

            if job.main_form_id not in jobmapping:
                jobmapping[job.main_form_id] = {'data' : [tmp, ] , 'total_item' : job.item, 'total_time' : job.time_count}
            else:
                jobmapping[job.main_form_id]['data'].append( tmp )
                jobmapping[job.main_form_id]['total_item'] += job.item
                jobmapping[job.main_form_id]['total_time'] += job.time_count

        datalen = map( lambda v : len( v['data'] ), jobmapping.values() )
        maxlen = max( datalen ) if datalen else 0

        maindata = [( 'Job Number', 'Team', 'AE', 'Program', 'Items', 'Date', 'Time(mins)' ), ]
        jobdata = [[['Type', 'Items', 'Time(mins)', 'Designer']] for i in range( maxlen )]

        DATE_FORMAT = "%Y-%m-%d"
        maincds = [
                   Team.id == PSMainForm.team_id, User.user_id == PSMainForm.create_by_id,
                   ]
        for main, user, team in DBSession.query( PSMainForm, User, Team ).filter( and_( *maincds ) ).order_by( PSMainForm.id ):
            total_item = total_time = 0
            if main.id not in jobmapping :
                for i in range( maxlen ) : jobdata[i].append( ['', '', '', ''] )
            else:
                tmp = ( jobmapping[main.id]['data'] + [['', '', '', ''] for i in range( maxlen )] )[:maxlen]
                for i in range( maxlen ) :
                    jobdata[i].append( tmp[i] )
                total_item, total_time = jobmapping[main.id]['total_item'], jobmapping[main.id]['total_time']

            maindata.append( map( unicode, [main.system_no, team.name, user.user_name, main.project,
                             total_item, main.create_time.strftime( DATE_FORMAT ), total_time] ) )

        return [maindata, ] + jobdata



    @expose( "json" )
    def ajaxDeleteAttachment( self, **kw ):
        try:
            clz = self._getDBClzByID( kw["form_id"] )
            obj = DBSession.query( clz ).get( kw["id"] )
            atts = obj.getAttachment()
            del atts[atts.index( kw["a_id"] )]
            obj.attachment = "|".join( atts )
            DBSession.add( PSDevelopmentLog( main_form_id = obj.main_id, sub_form_id = obj.id,
                                         sub_form_type = clz.__name__, action_type = 'UPDATE',
                                         remark = "user[%s] delete the attachment[id=%s]." % ( request.identity["user"], kw["a_id"] ) ) )
            DBSession.flush()
            return {"flag":0}
        except:
            logError()
            return {"flag":1}



    @expose()
    def downloadAllAttachment( self, **kw ):
        try:
            obj_id = kw['form_id']
            dbclz = self._getDBClzByID( obj_id )
            paths = []
            attach_type = kw.get( "attach_type", "attachment" )
            for i in dbclz.get( int( kw['sub_id'] ) ).getAttachment( wrapper = True, attach_type = attach_type ):
                paths.append( [i.file_path, i.file_name.encode( 'gbk' )] )
            zip_folder = os.path.join( config.download_dir, 'prepress' )
            if not os.path.exists( zip_folder ):
                os.makedirs( zip_folder )
            zip_path = os.path.join( zip_folder, '%s_%s.zip' % ( obj_id, dt.now().strftime( "%Y%m%d%H%M%S" ) ) ).replace( '\\', '/' )
            create_zip( zip_path, paths )
            return serveFile( zip_path )
        except:
            logError()
            flash( "Error occor on the server side!", 'warn' )
            redirect( "/prepress/index" )


    @expose( "json" )
    def checkDuplicate( self, **kw ):
        if not kw.get( "item_code", None ) : return {"flag" : 1}
        _query = DBSession.query( PSMainForm ).filter( and_( PSMainForm.active == 0, PSMainForm.item_code == kw["item_code"], PSMainForm.status != DRAFT ) )
        if kw.get( 'main_id', None ):
            _query = _query.filter( PSMainForm.id != int( kw['main_id'] ) )
        if _query.filter( PSMainForm.project == kw["project"] ).count() > 0:
            return {"flag": 1}
        else:
            return {"flag": 0}


    def _removeSession( self, token ):
        FormSerialize.delete_by_token( token )



    def _getDBClzByID( self, id ):
        try:
            return getattr( prepressDB, id )
        except:
            logError()
            return None




    @expose( "tribal.templates.prepress.view_development" )
    @tabFocus( tab_type = "main" )
    def viewDevelopmentLog( self, **kw ):
        h = getOr404( PSMainForm, kw["id"], "/prepress/index", "The record is not exist!" )
        field = kw.get( 'f', 'update_time' )
        direction = kw.get( 'd', 'desc' )
        try:
            query = DBSession.query( PSDevelopmentLog ).filter( and_( PSDevelopmentLog.active == 0,
                                                                  PSDevelopmentLog.main_form_id == kw["id"] ) )
            if direction == 'desc' :
                result = query.order_by( desc( getattr( PSDevelopmentLog, field ) ) )
            else:
                result = query.order_by( getattr( PSDevelopmentLog, field ) )
            return {"result" : result , "main" : h, "field" : field, "direction" : direction}
        except:
            logError()
            flash( "Error occur on the serve side!" )
            redirect( "/prepress/index" )



    @expose( "tribal.templates.prepress.copy_request" )
    @tabFocus( tab_type = "main" )
    def copyRequest( self, **kw ):
        try:
            h = getOr404( PSMainForm, kw["id"], "/prepress/index" )
            childrenForms = []

            for c in h.getChildrenForm():
                childrenForms.append( '%s-%s' % ( c.__class__.__name__, c.id ) )

            ms = DBSession.query( PSMainForm ).filter( and_( PSMainForm.active == 0, PSMainForm.revision == 0 ) ).order_by( PSMainForm.system_no ).all()
            rpt = None
            request_team = None
            teams = []
            regions = []
            for g in request.identity["user"].groups:
                for profile in g.prepress_profiles:
                    if profile.team :
                        rpt = profile.team
                        request_team = profile.team.id
                        if profile.team not in teams:teams.append( profile.team )
                    if profile.region : regions.append( profile.region )
            return {"childrenForms": json.dumps( childrenForms ), "rpt" : rpt, "request_team" : request_team, "main" : h,
                    "regions" : regions, "teams" : teams, "original_versions" : ms,
                    "customers" : Customer.find_all(), "programs" : Program.find_all(),
                    "projects" : Project.find_all(), "teams_groups":Team.find_all(), "regions_groups":Region.find_all(),
                    "item_categories" : PSItemCategory.find_all(),
#                    "users" : getAllSampleUsers(),
                    "token": createToken(),
                    "isWorkTime" : isWorkTime(),
                    }
        except Exception, e:
            log.exception( str( e ) )
            flash( "Error occor on the server side!", 'warn' )
            redirect( "/prepress/index" )


    @expose( 'json' )
    def ajaxAssign( self, **kw ):
        form_id = kw.get( 'form_id', None )
        assign_user_ids = kw.get( 'assign_user_ids', None )
        if not form_id or not assign_user_ids :
            return {
                    'code' : 1 ,
                    'msg'  : 'Not enough params provide!'
                    }
        try:
            obj = DBSession.query( PSMainForm ).get( form_id )
            assign_users = DBSession.query( User ).filter( User.user_id.in_( assign_user_ids.split( '|' ) ) ).all()
            assign_user_names = ','.join( [user.display_name for user in assign_users] )
            obj.status_back, obj.status = obj.status, PS_ASSIGNED
            obj.assign_users = assign_user_ids

            for c in obj.getChildrenForm() :
                if c.active == 0 : c.status = PS_ASSIGNED

            DBSession.add( PSDevelopmentLog( main = obj, system_no = str( obj ), sub_form_id = None, sub_form_type = None,
                                   action_type = "ASSIGN", remark = '%s assign the job to %s' % ( request.identity["user"].user_name, assign_user_names ) ) )
            # send a mail to these assigned users
            send_to = [user.email_address for user in assign_users]
            self._sendNotifyEmail( obj, type = 'ASSIGNED', send_users = send_to )

            return {'code': 0, 'msg': 'successfully!'}
        except Exception, e:
            log.exception( str( e ) )
            return {
                    'code' : 1,
                    'msg'  : 'Error occue on server !'
                    }




    @expose( "tribal.templates.prepress.view_todolist" )
    @paginate( "result", items_per_page = 20 )
    @tabFocus( tab_type = "main" )
    def viewToDoList( self, **kw ):
        try:
            statusType = int( kw["statusType"] )
            base_condition = [PSMainForm.active == 0, ]
            if not has_permission( "PREPRESS_VIEW_ALL" ):    # AE team
                teams = map( lambda t:t.id, getPSUserTeams( request.identity["user"] ) )
                base_condition = [or_( PSMainForm.team_id.in_( teams ), PSMainForm.request_team_id.in_( teams ) )]
            else:    # prepress team
                if not has_permission( "PREPRESS_ASSIGN" ):    # not supervisor
                    teams = map( lambda t:t.id, getPSUserTeams( request.identity["user"], "appteam" ) )
                    base_condition = [PSMainForm.status >= PS_ASSIGNED, PSMainForm.app_team_id.in_( teams )]

            def _s( statusType ):
                union_clause = []
                for n in prepressDB.__all__:
                    if n.startswith( "PSSF" ):
                        dbclz = getattr( prepressDB, n )
                        union_clause.append( select( [dbclz.main_id], and_( dbclz.active == 0, dbclz.status == statusType ) ) )
                return DBSession.query( PSMainForm ).filter( and_( PSMainForm.status != DRAFT, PSMainForm.id.in_( union( *union_clause ) ), *base_condition ) ).order_by( desc( PSMainForm.update_time ) ).all()

            if statusType == PS_DRAFT:
                result = DBSession.query( PSMainForm ).filter( and_( PSMainForm.active == 0, PSMainForm.status == PS_DRAFT, PSMainForm.create_by_id == request.identity['user'].user_id ) ).order_by( desc( PSMainForm.create_time ) ).all()
            elif statusType == PS_CANCELED_REQUEST:
                result = DBSession.query( PSMainForm ).filter( and_( PSMainForm.status == PS_CANCELED_REQUEST, PSMainForm.update_time > ( dt.now() - timedelta( days = 90 ) ), *base_condition ) ).order_by( desc( PSMainForm.update_time ) ).all()
            else:
                result = _s( statusType )
            return {"result" : result, "statusType" : statusType}
        except Exception, e:
            log.exception( str( e ) )
            flash( "Error occur on the server side!" )
            redirect( "/prepress/index" )


    def _getReportFilePath( self, templatePath ):
        current = dt.now()
        dateStr = current.strftime( "%Y%m%d" )
        fileDir = os.path.join( config.get( "download_dir" ), "prepress", dateStr )
        if not os.path.exists( fileDir ): os.makedirs( fileDir )
        tempFileName = os.path.join( fileDir, "%s_%s_%d.xls" % ( request.identity["user"].user_name,
                                                           current.strftime( "%Y%m%d%H%M%S" ), random.randint( 0, 1000 ) ) )
        realFileName = os.path.join( fileDir, "%s_%s.xls" % ( request.identity["user"].user_name, current.strftime( "%Y%m%d%H%M%S" ) ) )
        shutil.copy( templatePath, tempFileName )
        return tempFileName, realFileName


    def _genSummaryReport( self, teamTotal, taskTotal, summary, jobsummary ):
        templatePath = os.path.join( config.get( "template_dir" ), "PREPRESS_SUMMERY_TEMPLATE.xls" )
        tempFileName, realFileName = self._getReportFilePath( templatePath )
        try:
            sdexcel = PrepressSummary( templatePath = tempFileName, destinationPath = realFileName )
            sdexcel.inputData( teamTotal, taskTotal, summary, jobsummary )
            sdexcel.outputData()
            return realFileName
        except:
            traceback.print_exc()
            logError()
            if sdexcel:sdexcel.clearData()
            raise ReportGenerationException()


    @expose( 'tribal.templates.prepress.list_item_category' )
    def ajaxListItemCategory( self ):
        return {'data':DBSession.query( PSItemCategory ).filter( PSItemCategory.active == 0 ).order_by( PSItemCategory.name ).all()}



    @expose( 'json' )
    def ajaxAddItemCategory( self, ** kw ):
        try:
            if DBSession.query( PSItemCategory ).filter( PSItemCategory.name == kw.get( 'name' ) ).first():
                return {'flag': 2}
            it = PSItemCategory( name = kw.get( 'name' ) )
            DBSession.add( it )
            DBSession.flush()
            return {'flag':0, 'item_category':it, 'data':[[i.id, i.name] for i in DBSession.query( PSItemCategory ).filter( PSItemCategory.active == 0 ).order_by( PSItemCategory.name ).all()]}
        except:
#            traceback.print_exc()
            logError()
            return {"flag": 1}

    @expose( 'json' )
    def ajaxUpdateItemCategory( self, ** kw ):
        try:
            if DBSession.query( PSItemCategory ).filter( PSItemCategory.name == kw.get( 'name' ) ).first():
                return {'flag': 2}
            DBSession.merge( PSItemCategory( name = kw.get( 'name' ), id = kw.get( 'item_category_id' ) ) )
            DBSession.flush()
            return {'flag':0, 'data':[[i.id, i.name] for i in DBSession.query( PSItemCategory ).filter( PSItemCategory.active == 0 ).order_by( PSItemCategory.name ).all()]}
        except:
            traceback.print_exc()
            logError()
            return {"flag": 1}
