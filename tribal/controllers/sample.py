# -*- coding: utf-8 -*-
import simplejson as json
import traceback, os, random, shutil, json, operator, zipfile, zlib
import subprocess
import logging

from functools import wraps
from urlparse import urlparse

from datetime import datetime as dt, timedelta
from tg import request, expose, redirect, validate, flash, expose, override_template, config, url, session
from tg.decorators import paginate
from tg import tmpl_context

from repoze.what import predicates, authorize
from repoze.what.predicates import not_anonymous, in_group, has_permission
from sqlalchemy.sql import *
import transaction

# project specific imports
from win32com.client import CDispatch
from tribal.lib.base import BaseController
from tribal.model import *
from tribal.model import sample as sampleDB
from tribal.model.sample import *

from tribal.util.common import *
from tribal.util.sample_helper import sample_dict, getManagerByTeam, getUserTeams, getAllSampleUsers, \
    getUserRegions
from tribal.util.excel_helper import *
from tribal.widgets.sample import *
from tribal.util.file_util import create_zip
from tribal.util.decorators import paginate_addition

log = logging.getLogger( __name__ )

_setattr_ = CDispatch.__setattr__


def wrap_text_setattr_( self, attr, value ):
    _setattr_( self, attr, value )
    if attr == 'Value':
        _setattr_( self, 'WrapText', True )


class SampleController( BaseController ):
    allow_only = authorize.not_anonymous()

    @expose( 'tribal.templates.sample.index' )
    @paginate_addition( '/sample/index' )
    @paginate( "result", items_per_page = 20 )
    @tabFocus( tab_type = "main" )
    def index( self, **kw ):
        if not kw:
            result = []
            project_list = []
        else:
            if in_group( 'Admin' ) :  # if it's admin, could see the deleted job
                ws = []
            else:
                ws = [MainForm.active == 0]

            if kw.get( "project_own", False ) : ws.append( MainForm.project_own_id == kw["project_own"] )

            if kw.get( "reference_code", False ) : ws.append( MainForm.__table__.c.reference_code.op( "ilike" )( "%%%s%%" % kw["reference_code"] ) )
            if kw.get( "contact_person", False ) : ws.append( MainForm.__table__.c.contact_person.op( "ilike" )( "%%%s%%" % kw["contact_person"] ) )
            if kw.get( "customer", False ) : ws.append( MainForm.customer_id == kw["customer"] )

            if kw.get( "program", False ) :
                ws.append( MainForm.program_id == kw["program"] )
                project_list = DBSession.query( Project ).filter( and_( Project.active == 0, Project.program_id == kw['program'] ) ).order_by( Project.name ).all()
            else:
                project_list = []

            if kw.get( "item_category", False ) : ws.append( MainForm.item_category_id == kw["item_category"] )


            if kw.get( "project", False ) : ws.append( MainForm.project_id == kw["project"] )
            if kw.get( "create_by", False ) : ws.append( MainForm.create_by_id.in_( select( [User.user_id],
                                                                                       User.__table__.c.display_name.op( "ilike" )( "%%%s%%" % kw["create_by"] ) ) ) )
            if kw.get( "contact_team", False ) : ws.append( MainForm.team_id == kw["contact_team"] )
            if kw.get( "team", False ) :
                teams = DBSession.query( Team ).filter( Team.active == 0 ).filter( Team.id == kw["team"] ).first()
                ws.append( MainForm.rpt == teams.name )
            if kw.get( "project_owner", False ): ws.append( MainForm.__table__.c.project_owner.op( "ilike" )( "%%%s%%" % kw["project_owner"] ) )
            if kw.get( "item_description", False ) : ws.append( MainForm.__table__.c.item_description.op( "ilike" )( "%%%s%%" % kw["item_description"] ) )
            if kw.get( "system_no", False ) : ws.append( MainForm.__table__.c.system_no.op( "ilike" )( "%%%s%%" % kw["system_no"] ) )
            if kw.get( "item_code", False ) : ws.append( MainForm.__table__.c.item_code.op( "ilike" )( "%%%s%%" % kw["item_code"] ) )

            if kw.get( "create_time_from", False ) : ws.append( MainForm.create_time >= kw["create_time_from"] )
            if kw.get( "create_time_to", False ) : ws.append( MainForm.create_time <= kw["create_time_to"] )
            if kw.get( "status", False ) :
                # updated by Wing.Kwok on 2014-04-17
                # if kw["status"] == str( UNDER_DEVELOPMENT ): ws.append( MainForm.status > COMPLETED_REQUEST )
                if kw["status"] == str( DRAFT ): ws.append( and_( MainForm.status == DRAFT, MainForm.create_by_id == request.identity['user'].user_id ) )
                else: ws.append( MainForm.status == int( kw["status"] ) )
            else:
                ws.append( MainForm.status > DRAFT )

            if not has_permission( "SAMPLE_VIEW_ALL" ):
                team_ids = map( lambda t : t.id, getUserTeams( request.identity["user"] ) )
                _orws = [MainForm.team_id.in_( team_ids ),
                         MainForm.request_team_id.in_( team_ids ),
                         MainForm.cowork_team_id.in_( team_ids )]
                ws.append( or_( *_orws ) )


            # for the sort function
            field = kw.get( "field", None ) or "update_time"
            direction = kw.get( "direction", None ) or "desc"

            if direction == 'desc':
                result = DBSession.query( MainForm ).filter( and_( *ws ) ).order_by( desc( getattr( MainForm, field ) ) ).all()
            else:
                result = DBSession.query( MainForm ).filter( and_( *ws ) ).order_by( getattr( MainForm, field ) ).all()


        return {"widget" : search_form, "values" : kw, "result" : result, "project_list" : project_list}


    @expose( "tribal.templates.sample.new_request" )
    @tabFocus( tab_type = "main" )
    def newRequest( self, **kw ):
        rpt = None
        teams = []
        regions = []
        request_team = None
        for g in request.identity["user"].groups:
            for profile in g.sample_profiles:
                if profile.team :
                    rpt = profile.team
                    request_team = profile.team.id
                    if profile.team not in teams:teams.append( profile.team )
                if profile.region : regions.append( profile.region )

        cowork_teams = DBSession.query( Team ).filter( Team.active == 0 ).order_by( Team.name )

        return {
                "regions": regions, "regions_groups": Region.find_all(),
                "teams": teams, "teams_groups":Team.find_all(), "rpt": rpt, "request_team": request_team,
                "item_categries": ItemCategory.find_all(), "token": createToken(), "isWorkTime" : isWorkTime(),
                "cowork_teams" : cowork_teams,
                # "customers" : Customer.find_all(), "programs" : Program.find_all(), "users" : getAllSampleUsers(),
                }

    def _getSubFormFlag( self, subForm ):
        return '%s-%s-%s' % ( subForm.__class__.__name__, subForm.id, subForm.group_no or 1 )

    @expose( "tribal.templates.sample.view_request" )
    @tabFocus( tab_type = "main" )
    def viewRequest( self, **kw ):
        try:
            h = getOr404( MainForm, kw["id"], "/sample/index" )
            if h.active != 0 and not in_group( 'Admin' ):
                flash( 'The job does not exist!' )
                redirect( "/sample/index" )

            if h.status == DRAFT:
                raise Exception( "illegal operation: the main form can't viewed when status is draft" )

            childrenForms = []
            updatedChildrenForms = []
            canCancelForms = []
            groupFormDict = {}
            for i in range( h.group_no or 1 ):
                groupFormDict[i + 1] = []
            for c in h.getChildrenForm():
                form_name = c.__class__.__name__
                group_no = c.group_no or 1
                groupFormDict[group_no].append( {'id': c.id,
                    'form_name': form_name,
                    'form_label': SFTabLabel[form_name],
                    'group_no': group_no} )
                childrenForms.append( self._getSubFormFlag( c ) )
                if c.status in [NEW_REQUEST, WAIT_FOR_APPROVAL]:updatedChildrenForms.append( self._getSubFormFlag( c ) )
                if c.status not in [COMPLETED_REQUEST, CANCELED_REQUEST, DRAFT] : canCancelForms.append( self._getSubFormFlag( c ) )
            rpt = None
            for g in h.create_by.groups:
                for profile in g.sample_profiles:
                    if profile.team :
                        rpt = profile.team

            return {
                    "main": h,
                    'groupFormDict': groupFormDict,
                    "childrenForms": json.dumps( childrenForms ),
                    "rpt": rpt, "token": createToken(),
#                    "updatedChildrenForms" : json.dumps( updatedChildrenForms ),
                    "updatedChildrenForms" : updatedChildrenForms,
                    "canCancelForms" : "|".join( canCancelForms ),
                    'selected': kw.get( 'selected', '' )}

        except Exception, e:
            log.exception( str( e ) )
            flash( "Error occor on the server side!", 'warn' )
            redirect( "/sample/index" )

    @expose( "tribal.templates.sample.update_request" )
    @tabFocus( tab_type = "main" )
    def updateRequest( self, **kw ):
        try:
            h = getOr404( MainForm, kw["id"], "/sample/index" )
            if h.active != 0 and not in_group( 'Admin' ):
                flash( 'The job does not exist!' )
                redirect( "/sample/index" )

            childrenForms = []
            groupFormDict = {}
            for i in range( h.group_no or 1 ):
                groupFormDict[i + 1] = []
            for c in h.getChildrenForm():
                form_name = c.__class__.__name__
                group_no = c.group_no or 1
                groupFormDict[group_no].append( {'id': c.id,
                    'form_name': form_name,
                    'form_label': SFTabLabel[form_name],
                    'group_no': group_no} )
                childrenForms.append( self._getSubFormFlag( c ) )

            teams = []
            regions = []
            rpt = None
            for g in h.create_by.groups:
                for profile in g.sample_profiles:
                    if profile.team :
                        teams.append( profile.team )
                        rpt = profile.team
                    if profile.region : regions.append( profile.region )

            return {"childrenForms": json.dumps( childrenForms ),
                    'groupFormDict': groupFormDict,
                    "main": h, "rpt": rpt,
                    "regions": regions, "regions_groups": Region.find_all(),
                    "teams": teams, "teams_groups": Team.find_all(),
                    "item_categories": ItemCategory.find_all(), "token": createToken(),
                    "projects" : Project.find_by_program( h.program_id ),
                    "is_draft": True if h.status == DRAFT else False,
                    "isWorkTime" : isWorkTime(),
                    # "customers" : Customer.find_all(), "programs" : Program.find_all(), "users" : getAllSampleUsers(),
                    }
        except Exception, e:
            log.exception( str( e ) )
            flash( "Error occor on the server side!", 'warn' )
            redirect( "/sample/index" )

    @expose( "tribal.templates.sample.copy_request" )
    @tabFocus( tab_type = "main" )
    def copyRequest( self, **kw ):
        try:
            h = getOr404( MainForm, kw["id"], "/sample/index" )
            childrenForms = []
            groupFormDict = {}
            for i in range( h.group_no or 1 ):
                groupFormDict[i + 1] = []
            for c in h.getChildrenForm():
                form_name = c.__class__.__name__
                group_no = c.group_no or 1
                groupFormDict[group_no].append( {'id': c.id,
                    'form_name': form_name,
                    'form_label': SFTabLabel[form_name],
                    'group_no': group_no} )
                childrenForms.append( self._getSubFormFlag( c ) )

            ms = DBSession.query( MainForm ).filter( and_( MainForm.active == 0, MainForm.revision == 0 ) ).order_by( MainForm.system_no ).all()
            rpt = None
            request_team = None
            teams = []
            regions = []
            for g in request.identity["user"].groups:
                for profile in g.sample_profiles:
                    if profile.team :
                        rpt = profile.team
                        request_team = profile.team.id
                        if profile.team not in teams:teams.append( profile.team )
                    if profile.region : regions.append( profile.region )

            return {"childrenForms": json.dumps( childrenForms ),
                    'groupFormDict': groupFormDict,
                    "rpt" : rpt, "request_team" : request_team, "main" : h,
                    "regions" : regions, "teams" : teams, "original_versions" : ms,
                    "customers" : Customer.find_all(), "programs" : Program.find_all(),
                    "projects" : Project.find_all(), "teams_groups":Team.find_all(), "regions_groups":Region.find_all(),
                    "item_categories" : ItemCategory.find_all(), "users" : getAllSampleUsers(),
                    "token": createToken(),
                    "isWorkTime" : isWorkTime(),
                    }

        except Exception, e:
            log.exception( str( e ) )
            flash( "Error occor on the server side!", 'warn' )
            redirect( "/sample/index" )


    @expose( 'tribal.templates.sample.session_sub' )
    def getSubForm( self, **kw ):
        try:
            tab_id = kw["tab_id"]
            form_id = tab_id.split( '-' )[1]
            dbObject = getattr( sampleDB, form_id )
            widget = dbObject.getWidget()()
            prefix = "%s-" % form_id
            action = kw['action']
            regions = getUserRegions( request.identity["user"] )
            result = {"flag": 0, "js_url": widget.js_url, 'action': action,
                'tab_id':tab_id, 'token': kw['token'], 'group_no': kw['group_no'], 'prefix': prefix}
            if kw.get( 'sub_id', None ):
                sub_id = kw['sub_id']
                cf = dbObject.get( sub_id )
                html = None
                if action == 'view':
                    html = widget( cf.populateAsDict( prefix ), formPrefix = prefix, isDisable = True, dbObject = cf, action = action, regions = regions )
                    result.update( {'cf': cf, "stocks": Stock.find_all()} )
                else:  # update or copy
                    if form_id in ['SFSampling', 'SFPrintout'] and kw.get( "is_draft", 'false' ) != 'true' and action != 'copy':  # the 'sample' and 'target' form could not be revised even it's update status
                        html = widget( cf.populateAsDict( prefix ), formPrefix = prefix, isDisable = True, dbObject = cf, action = action, regions = regions )
                    else:
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
    def saveFormSuccess( self, **kw ):

        def _after_save( main_obj ):
            # send email for new or update
            self._sendNotifyEmail( main_obj )

            # only the HK ,SZ team need to approve for the request
            if not main_obj.team.need_approval:
                for c in main_obj.getChildrenForm():
                    if c.status == WAIT_FOR_APPROVAL: c.status = NEW_REQUEST
            else:
                reasons_html = []
                html_template = '<tr><td style="width:300px">%s</td><td style="width:100px"><a href="%s" target="_blank">Approve</a></td><td style="width:100px"><a href="%s" target="_blank">NOT Approve</a></td></tr>'
                send_email_obj = []
                for c in main_obj.getChildrenForm():
                    if c.send_email != 0 : continue  # have send the email before
                    if c.status != WAIT_FOR_APPROVAL and not c.why_need_approve() : continue  # no need to approve and the revise don't change the status

                    if c.status != WAIT_FOR_APPROVAL and c.why_need_approve(): c.status = WAIT_FOR_APPROVAL  # if the revise has changed the status

                    yes_url = "%s/sample/actionFromEmail?type=%s&id=%s&result=Y" % ( config.get( "website_url" ), c.__class__.__name__, c.id, )
                    no_url = "%s/sample/actionFromEmail?type=%s&id=%s&result=N" % ( config.get( "website_url" ), c.__class__.__name__, c.id, )
                    reasons_html.append( html_template % ( c.why_need_approve(), yes_url, no_url ) )
                    send_email_obj.append( c )

                if reasons_html:
                    managers = getManagerByTeam( main_obj.team_id, False )
                    if managers:
                        if config.get( "is_test", False ):
                            send_from = "r-tracktest@r-pac.com.hk"
                            subject = "[TESTING]Need your approval on the job : %s" % str( main_obj )
                        else:
                            send_from = "r-track@r-pac.com.hk"
                            subject = "Need your approval on the job : %s" % str( main_obj )

                        #=======================================================
                        # required by Wing.Kwok on 2013.10.13 ,the approval email
                        # should send to the manager, don't filter out the current user
                        #=======================================================
#                         send_to = map( lambda m:m.email_address, filter( lambda n:n.user_id != request.identity["user"].user_id , managers ) )
                        send_to = map( lambda m:m.email_address, managers )
                        cc_to = config.get( "sample_email_approve_cc", "" ).split( ";" )

                        templatePath = os.path.join( config.get( "template_dir" ), "SAMPLE_EMAIL_TEMPLATE.html" )
                        template = open( templatePath )
                        html = "".join( template.readlines() )
                        template.close()

                        url = "%s/sample/viewRequest?id=%d" % ( config.get( 'website_url', 'http://service.r-pac.com.hk' ), main_obj.id )
                        content = html % ( main_obj.create_by, main_obj, main_obj.team, main_obj.contact_person, main_obj.customer, main_obj.program, main_obj.project, main_obj.item_code, main_obj.item_description, url, url, "".join( reasons_html ) )

                        if config.get( "is_test", None ) != 'true':  # if it's test, don't send email out
                            advancedSendMail( send_from, send_to, subject, None, content, cc_to )

                for o in send_email_obj : o.send_email = 1

            '''
            # update the main form's percentage

            status_list = [c.status for c in main_obj.getChildrenForm()]
            completed_list = filter( lambda v: v == COMPLETED_REQUEST, status_list )
            main_obj.percentage = float( len( completed_list ) ) / len( status_list ) if len( status_list ) else 0
            if len( completed_list ) != len( status_list ) and main_obj.status == COMPLETED_REQUEST : main_obj.status = UNDER_DEVELOPMENT
            elif len( completed_list ) == len( status_list ) and main_obj.status != COMPLETED_REQUEST : main_obj.status = COMPLETED_REQUEST
            '''

        def _before_update( main_obj ):
            # save the main obj and children history
            main_obj_copy = main_obj
            main_obj_copy.project_own = main_obj.project_own
            main_obj_copy.team = main_obj.team
            main_obj_copy.customer = main_obj.customer
            main_obj_copy.program = main_obj.program
            main_obj_copy.project = main_obj.project
            main_obj_copy.item_category = main_obj.item_category
            main_obj_copy.cowork_team = main_obj.cowork_team
            DBSession.add( FormVersion( **{'main_id': main_obj.id, 'version': "%s-RC%.2d" % ( main_obj.system_no, main_obj.revision ) if main_obj.revision else main_obj.system_no, 'serialize': {'main':main_obj_copy, 'subs': main_obj.getChildrenForm()}} ) )

        token = kw['token']
        is_draft = True if kw['is_draft'] == 'true' else False
        try:
            # forms = session['form'][token]
            forms = FormSerialize.find_by_token( kw['token'] )
            action = kw['action']
            main_obj = None

            childfroms_new_or_update = []  # mark which child form is new added or updated
            old_job_status = None

            sort_forms = sorted( forms, cmp = lambda x, y : cmp( x.serialize.get( 'tab_index', 0 ), y.serialize.get( 'tab_index', 0 ) ) )

            for form in sort_forms:
                if form.type == 'main':  # save the main form
                    main_kw = form.serialize
                    if action == 'new' or action == 'copy':
                        main_obj = MainForm.create( is_draft = is_draft, **main_kw )
                        DBSession.flush()
                    elif main_kw.get( 'id', None ):
                        main_obj = getOr404( MainForm, main_kw["id"], "/sample/index" )

                        if not is_draft:
                            _before_update( main_obj )

                        old_sub_forms = main_obj.getChildrenDict()
                        log.debug( 'old_sub_forms initialize: %s' % old_sub_forms )
                        new_sub_forms = []
                        for i in main_kw['tab_ids'].split( '|' ):
                            if len( i.split( '-' ) ) == 5:
                                new_sub_forms.append( int( i.split( '-' )[4] ) )

                        log.debug( 'old_sub_forms will be inactive: %s' % old_sub_forms )
                        for k, v in old_sub_forms.iteritems():
                            if v.keys():
                                for _k, _v in v.iteritems():
                                    if int( _k ) not in new_sub_forms:
                                        _v.active = 1

                        old_job_status = main_obj.status
                        main_obj.update( is_draft = is_draft, **main_kw )

                else:  # save the sub form
                    sub_kw = form.serialize
                    obj_id = sub_kw['tab_id'].split( '-' )[1]
                    sub_kw['is_draft'] = is_draft
                    main_id = main_obj.id
                    formPrefix = "%s-" % obj_id
                    dbclz = self._getDBClzByID( obj_id )
                    if not sub_kw.get( 'id', None ):  # when sub form is new
                        log.debug( 'create sub action %s: %s' % ( sub_kw['action'], obj_id ) )
                        obj = dbclz.saveNewWithDict( sub_kw, formPrefix )
                        obj.main_id = main_id
                        attachment_copy_ids = sub_kw.get( '%sattachment_copy' % formPrefix )
                        if action == 'copy' and attachment_copy_ids:
                            copy_attachments = [str( i ) for i in dbclz.copyAttachments( attachment_copy_ids )]
                            obj.attachment = '%s|%s' % ( obj.attachment, '|'.join( copy_attachments ) ) if obj.attachment else '|'.join( copy_attachments )
                        DBSession.add( obj )
                        DBSession.flush()
                        childfroms_new_or_update.append( "%s-%s" % ( obj_id, obj.id ) )
                    else:  # when the sub form is update
                        sub_id = sub_kw['id']
                        log.debug( 'update sub action %s: %s id: %s' % ( sub_kw['action'], obj_id, sub_id ) )
                        if old_job_status != DRAFT and obj_id in ['SFSampling', 'SFPrintout'] : continue  # if it's not draft and it's 'sample' or 'printout' form ,don't save!

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
                        if log_str :  # if there is update
                            if old_job_status != DRAFT:
                                DBSession.add( DevelopmentLog( system_no = str( sfForm.main ), main_form_id = sfForm.main_id, sub_form_id = sfForm.id, sub_form_type = dbclz.__name__, action_type = 'UPDATE', remark = " .\n".join( log_str ) ) )
                            sfForm.status = WAIT_FOR_APPROVAL if sfForm.why_need_approve() else NEW_REQUEST
                            sfForm.send_email = 0  # reset the send mail flag
                            childfroms_new_or_update.append( "%s-%s" % ( obj_id, sub_id ) )
                        else:
                            if not is_draft and old_job_status == DRAFT:  # if the form is changed from draft to save, all the tabs should be views as 'new'!
                                childfroms_new_or_update.append( "%s-%s" % ( obj_id, sub_id ) )

            if not is_draft:
                main_obj.new_or_update = childfroms_new_or_update
                _after_save( main_obj )
                if childfroms_new_or_update:
                    self.calculate_status( main_obj )
            self._removeSession( token )
        except Exception, e:
            log.exception( str( e ) )
            log.exception( 'Save sample form success exception!!! %s' % kw )
            transaction.doom()
            flash( "Error occur on the server side!", "warn" )
            redirect( "/sample/index" )
        else:
            if is_draft:
                flash( "Job draft has been successfully saved, Job No.: %s" % str( main_obj ) )
                redirect( "/sample/index" )
            else:
                flash( "Job request has been successfully submitted, Job No.: %s" % str( main_obj ) )
                redirect( "/sample/viewRequest?id=%s" % main_obj.id )

    @expose()
    def saveFormFail( self, **kw ):
        log.exception( 'Save sample form failure!!! %s' % kw )
        flash( "Error occur on the server side!", "warn" )
        redirect( "/sample/index" )

    @expose( "json" )
    def ajaxProjectInfo( self, ** kw ):
        try:
            ps = DBSession.query( Project ).filter( and_( Project.active == 0, Project.program_id == kw["program_id"] ) ).order_by( Project.name ).all()
            data = [( p.id, p.name ) for p in ps]
            return {"flag": 0, "data": data}
        except:
#            traceback.print_exc()
            logError()
            return {"flag": 1}

    @expose( 'tribal.templates.sample.list_customer' )
    def ajaxListCustomer( self ):
        return {'data':DBSession.query( Customer ).filter( Customer.active == 0 ).order_by( Customer.name ).all()}

    @expose( 'tribal.templates.sample.list_item_category' )
    def ajaxListItemCategory( self ):
        return {'data':DBSession.query( ItemCategory ).filter( ItemCategory.active == 0 ).order_by( ItemCategory.name ).all()}

    @expose( "json" )
    def ajaxField( self, **kw ):
        fieldName = kw.get( "fieldName", None )
        if not fieldName: return []
        try:
            result = []
            if fieldName == 'customer_name':
                rs = DBSession.query( Customer ).filter( and_( Customer.active == 0,
                                                          Customer.__table__.c.name.op( 'ilike' ) \
                                                          ( "%%%s%%" % unicode( kw["q"] ).strip() ) ) ).all()
                result = [( "%s|%s|customer_name|%s" ) % ( row.name, row.name, row.id ) for row in rs]
            elif fieldName == 'program_name':
                rs = DBSession.query( Program ).filter( and_( Program.active == 0,
                                                          Program.__table__.c.name.op( 'ilike' ) \
                                                          ( "%%%s%%" % unicode( kw["q"] ).strip() ) ) ).all()
                result = [( "%s|%s|program_name|%s" ) % ( row.name, row.name, row.id ) for row in rs]
            elif fieldName in ['user', 'create_by', 'contact_person', 'project_owner'] :
                rs = DBSession.query( User ).filter( User.__table__.c.display_name.op( 'ilike' ) \
                                                          ( "%%%s%%" % unicode( kw["q"] ).strip() ) ).all()
                result = [( "%s|%s|user_name|%s" ) % ( row, row.email_address, row.user_id ) for row in rs]

            return "\n".join( result )
        except:
#            traceback.print_exc()
            logError()
            return []

    @expose( 'json' )
    def ajaxAddCustomer( self, ** kw ):
        try:
            if DBSession.query( Customer ).filter( Customer.name == kw.get( 'name' ) ).first():
                return {'flag': 2}
            customer = Customer( name = kw.get( 'name' ) )
            DBSession.add( customer )
            DBSession.flush()
            return {'flag':0, 'customer':customer, 'data':[[i.id, i.name] for i in DBSession.query( Customer ).filter( Customer.active == 0 ).order_by( Customer.name ).all()]}
        except:
#            traceback.print_exc()
            logError()
            return {"flag": 1}

    @expose( 'json' )
    def ajaxAddItemCategory( self, ** kw ):
        try:
            if DBSession.query( ItemCategory ).filter( ItemCategory.name == kw.get( 'name' ) ).first():
                return {'flag': 2}
            it = ItemCategory( name = kw.get( 'name' ) )
            DBSession.add( it )
            DBSession.flush()
            return {'flag':0, 'item_category':it, 'data':[[i.id, i.name] for i in DBSession.query( ItemCategory ).filter( ItemCategory.active == 0 ).order_by( ItemCategory.name ).all()]}
        except:
#            traceback.print_exc()
            logError()
            return {"flag": 1}

    @expose( 'json' )
    def ajaxUpdateCustomer( self, ** kw ):
        try:
            if DBSession.query( Customer ).filter( Customer.name == kw.get( 'name' ) ).first():
                return {'flag': 2}
            DBSession.merge( Customer( name = kw.get( 'name' ), id = kw.get( 'customer_id' ) ) )
            DBSession.flush()
            return {'flag':0, 'data':[[i.id, i.name] for i in DBSession.query( Customer ).filter( Customer.active == 0 ).order_by( Customer.name ).all()]}
        except:
#            traceback.print_exc()
            logError()
            return {"flag": 1}


    @expose( 'json' )
    def ajaxUpdateItemCategory( self, ** kw ):
        try:
            if DBSession.query( ItemCategory ).filter( ItemCategory.name == kw.get( 'name' ) ).first():
                return {'flag': 2}
            DBSession.merge( ItemCategory( name = kw.get( 'name' ), id = kw.get( 'item_category_id' ) ) )
            DBSession.flush()
            return {'flag':0, 'data':[[i.id, i.name] for i in DBSession.query( ItemCategory ).filter( ItemCategory.active == 0 ).order_by( ItemCategory.name ).all()]}
        except:
            traceback.print_exc()
            logError()
            return {"flag": 1}

    @expose( 'json' )
    def ajaxDeleteCustomer( self, ** kw ):
        try:
            DBSession.merge( Customer( name = kw.get( 'id' ), active = 1 ) )
        except:
#            traceback.print_exc()
            logError()
            return {"flag": 1}

    @expose( 'tribal.templates.sample.list_program' )
    def ajaxListProgram( self ):
        return {'data':DBSession.query( Program ).filter( Program.active == 0 ).order_by( Program.name ).all()}

    @expose( 'json' )
    def ajaxAddProgram( self, ** kw ):
        try:
            if DBSession.query( Program ).filter( Program.name == kw.get( 'program_name' ) ).first():
                return {'flag': 2}
            program = Program( name = kw.get( 'program_name' ) )
            DBSession.add( program )
            DBSession.flush()
            return {'flag':0, 'program':program, 'data':[[i.id, i.name] for i in DBSession.query( Program ).filter( Program.active == 0 ).order_by( Program.name ).all()]}
        except:
#            traceback.print_exc()
            logError()
            return {"flag": 1}

    @expose( 'json' )
    def ajaxUpdateProgram( self, ** kw ):
        try:
            if DBSession.query( Program ).filter( Program.name == kw.get( 'program_name' ) ).first():
                return {'flag': 2}
            DBSession.merge( Program( name = kw.get( 'program_name' ), id = kw.get( 'program_id' ) ) )
            DBSession.flush()
            return {'flag':0, 'data':[[i.id, i.name] for i in DBSession.query( Program ).filter( Program.active == 0 ).order_by( Program.name ).all()]}
        except:
#            traceback.print_exc()
            logError()
            return {"flag": 1}

    @expose( 'json' )
    def ajaxDeleteProgram( self, ** kw ):
        try:
            DBSession.merge( Program( name = kw.get( 'id' ), active = 1 ) )
        except:
#            traceback.print_exc()
            logError()
            return {"flag": 1}

    @expose( 'tribal.templates.sample.list_project' )
    def ajaxListProject( self, **kw ):
        program_id = kw.get( 'program_id' )
        return {'program_id':program_id, 'data':DBSession.query( Project ).filter( Project.active == 0 ).filter( Project.program_id == program_id ).order_by( Project.name ).all()}

    @expose( 'json' )
    def ajaxAddProject( self, ** kw ):
        try:
            if DBSession.query( Project ).filter( and_( Project.name == kw.get( 'project_name' ), Project.program_id == kw.get( 'program_id' ) ) ).first():
                return {'flag': 2}
            project = Project( name = kw.get( 'project_name' ), program_id = kw.get( 'program_id' ) )
            DBSession.add( project )
            DBSession.flush()
            return {'flag':0, 'data':[[i.id, i.name] for i in DBSession.query( Project ).filter( Project.active == 0 ).filter( Project.program_id == project.program_id ).order_by( Project.name ).all()], 'project':project}
        except:
#            traceback.print_exc()
            logError()
            return {"flag": 1}

    @expose( 'json' )
    def ajaxUpdateProject( self, ** kw ):
        try:
            if DBSession.query( Project ).filter( and_( Project.name == kw.get( 'project_name' ), Project.program_id == kw.get( 'program_id' ), Project.id != kw.get( 'project_id' ) ) ).first():
                return {'flag': 2}
            project = DBSession.merge( Project( name = kw.get( 'project_name' ), id = kw.get( 'project_id' ) ) )
            DBSession.flush()
            return {'flag':0, 'data':[[i.id, i.name] for i in DBSession.query( Project ).filter( Project.active == 0 ).filter( Project.program_id == project.program_id ).order_by( Project.name ).all()]}
        except:
#            traceback.print_exc()
            logError()
            return {"flag": 1}

    @expose( 'json' )
    def ajaxDeleteProject( self, ** kw ):
        try:
            DBSession.merge( Project( name = kw.get( 'id' ), active = 1 ) )
        except:
#            traceback.print_exc()
            logError()
            return {"flag": 1}

    def _getDBClzByID( self, id ):
        try:
            return getattr( sampleDB, id )
        except:
#            traceback()
            logError()
            return None

    @expose( "json" )
    def ajaxJobForm( self, **kw ):
        subFormType = kw.get( "t", None )
        if not subFormType:
            return {
                    "success" : False,
                    "msg" : "No sub form type supply!"
                    }
        try:
            extraInfo = DBSession.query( FormExtraInfo ).filter( and_( FormExtraInfo.active == 0, FormExtraInfo.name == subFormType ) ).first()
            formConfig = []
            if extraInfo.job_config:
                mapping = sample_dict.getFormTypeMapping()
                for c in extraInfo.job_config.split( "|" ):
                    if c in mapping : formConfig.append( mapping[c] )

            return {
                    "success" : True,
                    "need_stock" : extraInfo.need_stock == 0,
                    "formConfig" : formConfig,
                    }
        except:
#            traceback.print_exc()
            logError()
            return {
                    "success" : False,
                    "msg" : "The service is not avaiable now, please try it later."
                    }


    @expose( "json" )
    def ajaxJobInfo( self, **kw ):
        jobid = kw.get( "job_id", None )
        if not jobid :
            return {
                    "success" : False,
                    "msg" : "No job id supply!"
                    }
        try:
            job = DBSession.query( Job ).get( jobid )
            return {
                    "success" : True,
                    "other_spend" : job.populateOtherSpend(),
                    "materials" : [( m.id, m.stock_id, m.qty ) for m in job.suform_job_materials],
                    "remark" : job.remark,
                    "time_spand" : job.time_spand,
                    }
        except:
            logError()
            return {
                    "success" : False,
                    "msg" : "The service is not avaiable now, please try it later."
                    }


    @expose( "json" )
    def ajaxMark( self, **kw ):
        statusType = {
                      "A" : ( NEW_REQUEST, "Approve" ),
                      "C" : ( COMPLETED_REQUEST, "Complete" ) ,
                      "D" : ( DISAPPROVAL, "Disapprove" ) ,
                      "G" : ( UNDER_DEVELOPMENT, "Restart" ),  # need to send email
                      "R" : ( WAIT_FOR_APPROVAL, "Wait for approve" ) ,
                      "X" : ( CANCELED_REQUEST, "Cancel" ),  # need to send email
                      "P" : ( PENDING, "Pending" ),  # need to send email
                      "U" : ( NEW_REQUEST, "Revision" ),
                      "S" : ( UNDER_DEVELOPMENT, "Start work" ) ,
                      }


        if kw["action"] not in statusType : return {"flag" : 2}

        try:
            task_labels = []
            task_clz = set()
            for form_id in kw["form_ids"].split( "|" ):
                ( formType, id ) = form_id.replace( "-", "_" ).split( "_" )[:2]
                dbclz = self._getDBClzByID( formType )
                task_labels.append( dbclz.getWidget().label )  # used to send email for cancel and pending
                task_clz.add( dbclz.__name__ )
                dbobj = DBSession.query( dbclz ).get( id )
                dbobj.status_back , dbobj.status = dbobj.status, statusType[kw["action"]][0]
                l = DevelopmentLog( main = dbobj.main, system_no = str( dbobj.main ), sub_form_id = dbobj.id, sub_form_type = dbclz.__name__,
                                   action_type = "UPDATE", remark = statusType[kw["action"]][1] )
                DBSession.add( l )
                if kw["action"] == "C":
                    dbobj.complete_time = dt.now()
                    dbobj.complete_by_id = request.identity["user"].user_id
                    flag = "%s-%s" % ( formType, id )
                    if  flag in dbobj.main.new_or_update : dbobj.main.new_or_update = dbobj.main.new_or_update.remove( flag )


            #==================================================================
            header = dbobj.main
            header.update_time = dt.now()
            self.calculate_status( header )
            #==================================================================


            if kw["action"] in ['X', 'P', 'G', 'U']:  # send email
#                def _sendNotifyEmail(self, h,type='NORMAL',task_label = None):
#                type = 'CANCELLED' if kw['action'] == 'X' else 'PENDING'
                action_type = {
                        'X' : 'CANCELLED',
                        'P' : 'PENDING',
                        'G' : 'RESTART',
                        'U' : 'RESTART',
                        }.get( kw['action'], '' )
                self._sendNotifyEmail( header, action_type, ",".join( task_labels ), extra = {'tasks' : list( task_clz )} )


            return {"flag" : 0, "percentage" : int( header.percentage * 100 ) , "whole_status" : header.status, "status" : dbobj.status}
        except:
            traceback.print_exc()
            logError()
            return {"flag" : 1}


    def calculate_status( self, header ):
        # check the whold request's status
        childrenStatus = []
        for c in header.getChildren():
            clildClz = self._getDBClzByID( c )
            for sf in DBSession.query( clildClz ).filter( and_( clildClz.active == 0, clildClz.main_id == header.id ) ) : childrenStatus.append( sf.status )


        new = childrenStatus.count( NEW_REQUEST )
        completed = childrenStatus.count( COMPLETED_REQUEST )
        pending = childrenStatus.count( PENDING )
        wait = childrenStatus.count( WAIT_FOR_APPROVAL )
        develop = childrenStatus.count( UNDER_DEVELOPMENT )
        disapprove = childrenStatus.count( DISAPPROVAL )
        cancel = childrenStatus.count( CANCELED_REQUEST )
        header.percentage = float( completed + cancel ) / len( childrenStatus )

        # update the job's status
        #===================================================================
        # S1 Wait for Approval
        # S2 New
        # S3 Under Development
        # S4 Pending
        # S5 Complete
        # S6 Disapproved
        # S7 Cancel
        #===================================================================

        def _markComplete():
            header.status = COMPLETED_REQUEST
            header.complete_time = dt.now()
            header.complete_by_id = request.identity["user"].user_id

        if wait == len( childrenStatus ) : header.status = NEW_REQUEST  # ALL S1
        elif new == len( childrenStatus ) : header.status = NEW_REQUEST  # ALL S2
        elif develop == len( childrenStatus ) : header.status = UNDER_DEVELOPMENT  # ALL S3
        elif pending == len( childrenStatus ) : header.status = UNDER_DEVELOPMENT  # ALL S4
        elif cancel == len( childrenStatus ) : header.status = CANCELED_REQUEST  # ALL S7
        elif disapprove == len( childrenStatus ) : header.status = CANCELED_REQUEST  # ALL S6
        elif completed == len( childrenStatus ) : _markComplete()  # ALL S5

        elif wait + new == len( childrenStatus ) : header.status = NEW_REQUEST  # S1 + S2
        elif disapprove + completed == len( childrenStatus ) : _markComplete()  # S5+S6
        elif disapprove + cancel == len( childrenStatus ) : header.status = CANCELED_REQUEST  # S6+S7
        elif wait + disapprove == len( childrenStatus ) : header.status = NEW_REQUEST  # S1 + S6
        elif wait + cancel == len( childrenStatus ) : header.status = NEW_REQUEST  # S1 + S7
        elif new + disapprove == len( childrenStatus ) : header.status = NEW_REQUEST  # S2 + S6
        elif new + cancel == len( childrenStatus ) : header.status = NEW_REQUEST  # S2 + S7
        elif completed + cancel == len( childrenStatus ) : _markComplete()  # S5 + S7

        elif disapprove + completed + cancel == len( childrenStatus ) : _markComplete()  # S5+S6+S7
        elif wait + new + disapprove == len( childrenStatus ) : header.status = NEW_REQUEST  # S1 + S2 + S6
        elif wait + new + cancel == len( childrenStatus ) : header.status = NEW_REQUEST  # S1 + S2 + S7
        elif wait + disapprove + cancel == len( childrenStatus ) : header.status = NEW_REQUEST  # S1 + S6 + S7
        elif new + disapprove + cancel == len( childrenStatus ) : header.status = NEW_REQUEST  # S2 + S6 + S7

        elif wait + new + disapprove + cancel == len( childrenStatus ) : header.status = NEW_REQUEST  # S1 + S2 + S6 + S7

        else: header.status = UNDER_DEVELOPMENT

    @expose( "json" )
    def ajaxTodoList( self, **kw ):
        try:
            if not has_permission( "SAMPLE_VIEW_ALL" ):
                teams = map( lambda t:t.id, getUserTeams( request.identity["user"] ) )
                _orws = [MainForm.team_id.in_( teams ),
                         MainForm.request_team_id.in_( teams ),
                         MainForm.cowork_team_id.in_( teams )]
                base_condition = [MainForm.active == 0, or_( *_orws )]
            else:
                base_condition = [MainForm.active == 0, ]

            draft = DBSession.query( MainForm ).filter( and_( MainForm.active == 0, MainForm.status == DRAFT, MainForm.create_by_id == request.identity['user'].user_id ) ).order_by( desc( MainForm.create_time ) )
            cs = DBSession.query( MainForm ).filter( and_( MainForm.status == CANCELED_REQUEST, MainForm.update_time > ( dt.now() - timedelta( days = 90 ) ), *base_condition ) ).order_by( desc( MainForm.update_time ) )
            def _s( statusType ):
                union_clause = []
                for n in sampleDB.__all__:
                    if n.startswith( "SF" ) and n != 'SFTabLabel':
                        dbclz = getattr( sampleDB, n )
                        union_clause.append( select( [dbclz.main_id], and_( dbclz.active == 0, dbclz.status == statusType ) ) )
                return DBSession.query( MainForm ).filter( and_( MainForm.status != DRAFT, MainForm.id.in_( union( *union_clause ) ), *base_condition ) ).order_by( desc( MainForm.update_time ) )

            ns = _s( NEW_REQUEST )
            devs = _s( UNDER_DEVELOPMENT )
            ws = _s( WAIT_FOR_APPROVAL )
            ps = _s( PENDING )

            return {"flag" : 0,
                    'draft': [( d.id, str( d ) ) for d in draft[:5]],
                    'draft_count': draft.count(),
                    "new" : [( n.id, str( n ) ) for n in ns[:5]],
                    "new_count" : ns.count(),
                    "wait" : [( w.id, str( w ) ) for w in ws[:5]],
                    "wait_count" : ws.count(),
                    "cancel" : [( c.id, str( c ) ) for c in cs[:5]],
                    "cancel_count" : cs.count(),
                    "pending" : [( p.id, str( p ) ) for p in ps[:5]],
                    "pending_count" : ps.count(),
                    "dev" : [( p.id, str( p ) ) for p in devs[:5]],
                    "dev_count" : devs.count(),
                    }
        except:
            traceback.print_exc()
            logError()
            return {"flag" : 1}


    @expose( "tribal.templates.sample.view_todolist" )
    @paginate( "result", items_per_page = 20 )
    @tabFocus( tab_type = "main" )
    def viewToDoList( self, **kw ):
        try:
            statusType = int( kw["statusType"] )
            if not has_permission( "SAMPLE_VIEW_ALL" ):
                teams = map( lambda t:t.id, getUserTeams( request.identity["user"] ) )
                _orws = [MainForm.team_id.in_( teams ),
                         MainForm.request_team_id.in_( teams ),
                         MainForm.cowork_team_id.in_( teams ), ]
                base_condition = [MainForm.active == 0, or_( *_orws )]
            else:
                base_condition = [MainForm.active == 0, ]

            def _s( statusType ):
                union_clause = []
                for n in sampleDB.__all__:
                    if n.startswith( "SF" ) and n != 'SFTabLabel':
                        dbclz = getattr( sampleDB, n )
                        union_clause.append( select( [dbclz.main_id], and_( dbclz.active == 0, dbclz.status == statusType ) ) )
                return DBSession.query( MainForm ).filter( and_( MainForm.status != DRAFT, MainForm.id.in_( union( *union_clause ) ), *base_condition ) ).order_by( desc( MainForm.update_time ) ).all()

            if statusType == DRAFT:
                result = DBSession.query( MainForm ).filter( and_( MainForm.active == 0, MainForm.status == DRAFT, MainForm.create_by_id == request.identity['user'].user_id ) ).order_by( desc( MainForm.create_time ) ).all()
            elif statusType == CANCELED_REQUEST:
                result = DBSession.query( MainForm ).filter( and_( MainForm.status == CANCELED_REQUEST, MainForm.update_time > ( dt.now() - timedelta( days = 90 ) ), *base_condition ) ).order_by( desc( MainForm.update_time ) ).all()
            else:
                result = _s( statusType )
            return {"result" : result, "statusType" : statusType}
        except Exception, e:
            log.exception( str( e ) )
            flash( "Error occur on the server side!" )
            redirect( "/sample/index" )

    @expose( "tribal.templates.sample.view_development" )
    @tabFocus( tab_type = "main" )
    def viewDevelopmentLog( self, **kw ):
        h = getOr404( MainForm, kw["id"], "/sample/index", "The record is not exist!" )
        field = kw.get( 'f', 'create_time' )
        direction = kw.get( 'd', 'desc' )
        try:
            query = DBSession.query( DevelopmentLog ).filter( and_( DevelopmentLog.active == 0, DevelopmentLog.main_form_id == kw["id"] ) )
            if direction == 'desc' :
                result = query.order_by( desc( getattr( DevelopmentLog, field ) ) )
            else:
                result = query.order_by( getattr( DevelopmentLog, field ) )
            return {"result" : result , "main" : h, "field" : field, "direction" : direction}
        except:
#            traceback.print_exc()
            logError()
            flash( "Error occur on the serve side!" )
            redirect( "/sample/index" )

    @expose( 'tribal.templates.sample.list_history' )
    @tabFocus( tab_type = 'main' )
    def listHistory( self, **kw ):
        return {'result': FormVersion.find_by_main_id( kw['id'] ), 'id': kw['id']}

    @expose( 'tribal.templates.sample.view_history' )
    @tabFocus( tab_type = 'main' )
    def viewHistory( self, **kw ):
        try:
            form_version = FormVersion.get( kw['id'] )
            h = form_version.main
            subs = form_version.subs
            rpt = None
            for g in h.create_by.groups:
                for profile in g.sample_profiles:
                    if profile.team :
                        rpt = profile.team
            childrenForms = []
            groupFormDict = {}
            for i in range( h.group_no or 1 ):
                groupFormDict[i + 1] = []
            for c in subs:
                form_name = c.__class__.__name__
                group_no = c.group_no or 1
                groupFormDict[group_no].append( {'id': c.id,
                    'form_name': form_name,
                    'form_label': SFTabLabel[form_name],
                    'group_no': group_no} )
                childrenForms.append( self._getSubFormFlag( c ) )
            try:
                cowork_team = h.cowork_team
            except:
                cowork_team = None

            return {'id':form_version.id, "main": h,
                'groupFormDict': groupFormDict,
                "childrenForms": json.dumps( childrenForms ), "rpt": rpt, "updatedChildrenForms" : json.dumps( h.new_or_update ),
                "cowork_team" : cowork_team}

        except Exception, e:
            log.exception( str( e ) )
            flash( "Error occor on the server side!", 'warn' )
            redirect( "/sample/index" )

    @expose( 'tribal.templates.sample.view_history_sub' )
    def getHistorySubForm( self, **kw ):
        try:
            tab_id = kw["tab_id"]
            form_id = tab_id.split( '-' )[1]
            index = int( tab_id.split( '-' )[2] ) - 1
            form_version = FormVersion.get( kw['history_id'] )
            sub_form = form_version.subs[index]
            dbObject = sub_form.__class__
            widget = dbObject.getWidget()()
            prefix = "%s-" % form_id
            result = {"flag": 0, "js_url": widget.js_url, 'tab_id':tab_id}
            cf = sub_form
            html = widget( cf.populateAsDict( prefix ), formPrefix = prefix, isDisable = True, dbObject = cf )
            result.update( {'main_id': cf.main_id, 'html': html, 'cf': cf} )
            return result
        except Exception, e:
            log.exception( str( e ) )
            return {"flag" : 1}

    def _filterAndSorted( self, prefix, kw ):
        return sorted( filter( lambda ( k, v ): k.startswith( prefix ), kw.iteritems() ), cmp = lambda x, y:cmp( x[0], y[0] ) )


    @expose( "json" )
    def ajaxAddJob( self, **kw ):
        try:
            clz = self._getDBClzByID( kw["form_clz"] )

            obj = DBSession.query( clz ).get( kw["form_id"] )

            params = dict( 
                      main_form_id = obj.main_id,
                      sub_form_id = obj.id,
                      sub_form_type = kw["form_clz"],
                      time_spand = kw.get( "time_spand", None ),
                      remark = kw["remark"],
                      designers = kw.get( "designers", "HK" ),
                      )
            other_spend = []
            other_spend_data = []
            extra = clz.getFormExtra()

            mapping = sample_dict.getFormTypeMapping()
            if extra and extra.job_config:
                for c in extra.job_config.split( "|" ):
                    other_spend.append( ( c, kw.get( c, None ) ) )
                    other_spend_data.append( ( mapping[c]['label'], kw.get( c, None ) ) )
            params["other_spend"] = json.dumps( other_spend )
            h = Job( **params )
            DBSession.add( h )
            DBSession.flush()
            data = {
                    "id" : h.id,
                    "time_spand" : kw["time_spand"],
                    "material" : [],
                    "create_by" : request.identity["user"].user_name,
                    "create_time" : dt.now().strftime( "%Y-%m-%d %H:%M" ),
                    "other_spend" : other_spend_data,
                    "remark" : kw["remark"] or '',
                    }


            stocks = self._filterAndSorted( "stock_", kw )
            qtys = self._filterAndSorted( "qty_", kw )
            for ( skey, sval ), ( qkey, qval ) in zip( stocks, qtys ):
                if not sval or not qval:continue
                st = DBSession.query( Stock ).get( sval )
                DBSession.add( JobMaterial( main_form_id = obj.main_id, job = h, stock_id = sval, qty = qval, cost = st.cost ) )
                data["material"].append( {"stock" : st.name, "qty" : qval} )

            return {"flag" : 0, "data":data}
        except:
#            traceback.print_exc()
            logError()
            transaction.doom()
            return {"flag" : 1}


    @expose( "json" )
    def ajaxReviseJob( self, **kw ):
        jobid = kw.get( "job_id", None )
        if not jobid : return {
                               "flag" : 1,
                               "msg" : "No job id supply!"
                               }
        try:
            job = DBSession.query( Job ).get( jobid )
            job.remark = kw.get( "remark", None )
            job.time_spand = kw.get( "time_spand", None )

            other_spend = []
            other_spend_data = []
            extra = job.sub_form().getFormExtra()

            mapping = sample_dict.getFormTypeMapping()
            if extra and extra.job_config:
                for c in extra.job_config.split( "|" ):
                    other_spend.append( ( c, kw.get( c, None ) ) )
                    other_spend_data.append( ( mapping[c]['label'], kw.get( c, None ) ) )
            job.other_spend = json.dumps( other_spend )

            data = {
                    "id" : job.id,
                    "time_spand" : kw["time_spand"],
                    "material" : [],
                    "create_by" : request.identity["user"].user_name,
                    "create_time" : dt.now().strftime( "%Y-%m-%d %H:%M" ),
                    "other_spend" : other_spend_data,
                    }


            existing_stocks = {}
            for m in job.suform_job_materials: existing_stocks[str( m.id )] = m

            stocks = self._filterAndSorted( "oldstock_", kw )
            qtys = self._filterAndSorted( "oldqty_", kw )
            for ( skey, sval ), ( qkey, qval ) in zip( stocks, qtys ):
                tmp, id = skey.split( "_" )

                m = existing_stocks.get( id, None )
                if not m : continue
                if not sval or not qval:
                    m.active = 1
                else:
                    m.stock_id = sval
                    m.qty = qval
                    m.cost = DBSession.query( Stock ).get( sval ).cost
                    data["material"].append( {"stock" : m.stock.name, "qty" : qval} )
                del existing_stocks[id]

            for v in existing_stocks.values() : v.active = 1

            new_stocks = self._filterAndSorted( "stock_", kw )
            new_qtys = self._filterAndSorted( "qty_", kw )
            for ( skey, sval ), ( qkey, qval ) in zip( new_stocks, new_qtys ):
                if not sval or not qval: continue
                st = DBSession.query( Stock ).get( sval )
                DBSession.add( JobMaterial( main_form_id = job.main_form_id, job = job, stock_id = sval, qty = qval, cost = st.cost ) )
                data["material"].append( {"stock" : st.name, "qty" : qval} )

            return {
                    "flag" : 0, "data" : data
                    }
        except:
#            traceback.print_exc()
            logError()
            transaction.doom()
            return {"flag" : 1}


    @expose( "json" )
    def ajaxDeleteJob( self, **kw ):
        try:
            job = DBSession.query( Job ).get( kw.get( "id", None ) )
            l = DevelopmentLog( main = job.main, sub_form_id = job.sub_form_id, sub_form_type = job.sub_form_type, action_type = "Update",
                             remark = '%s delete the job[id=%s].' % ( request.identity["user"], job.id ) )
            DBSession.add( l )
            job.active = 1
            return {"flag" : 0}
        except:
#            traceback.print_exc()
            logError()
            return {"flag" : 1}



    def _sendNotifyEmail( self, h, type = 'NORMAL', task_label = None, extra = None ):
        if config.get( "is_test", None ) == 'true':
            send_from = "r-tracktest@r-pac.com.hk"
            if type == 'NORMAL':
                subject = "[TESTING] %s / %s / %s / %s / %s" % ( h, h.reference_code, h.customer, h.program, h.item_code or '' )
                templatePath = os.path.join( config.get( "template_dir" ), "SAMPLE_NORMAL_EMAIL_TEMPLATE.html" )
            elif type == 'CANCELLED':
                subject = "[TESTING][CANCELLED] %s / %s / %s / %s / %s" % ( h, h.reference_code, h.customer, h.program, h.item_code or '' )
                templatePath = os.path.join( config.get( "template_dir" ), "SAMPLE_CANCEL_PENDING_EMAIL_TEMPLATE.html" )
            elif type == 'PENDING':
                subject = "[TESTING][PENDING] %s / %s / %s / %s / %s" % ( h, h.reference_code, h.customer, h.program, h.item_code or '' )
                templatePath = os.path.join( config.get( "template_dir" ), "SAMPLE_CANCEL_PENDING_EMAIL_TEMPLATE.html" )
            elif type == 'RESTART':
                subject = "[TESTING][RESTART] %s / %s / %s / %s / %s" % ( h, h.reference_code, h.customer, h.program, h.item_code or '' )
                templatePath = os.path.join( config.get( "template_dir" ), "SAMPLE_CANCEL_PENDING_EMAIL_TEMPLATE.html" )
        else:
            send_from = "r-track@r-pac.com.hk"
            if type == 'NORMAL':
                subject = "%s / %s / %s / %s / %s" % ( h, h.reference_code, h.customer, h.program, h.item_code or '' )
                templatePath = os.path.join( config.get( "template_dir" ), "SAMPLE_NORMAL_EMAIL_TEMPLATE.html" )
            elif type == 'CANCELLED':
                subject = "[CANCELLED] %s / %s / %s / %s / %s" % ( h, h.reference_code, h.customer, h.program, h.item_code or '' )
                templatePath = os.path.join( config.get( "template_dir" ), "SAMPLE_CANCEL_PENDING_EMAIL_TEMPLATE.html" )
            elif type == 'PENDING':
                subject = "[PENDING] %s / %s / %s / %s / %s" % ( h, h.reference_code, h.customer, h.program, h.item_code or '' )
                templatePath = os.path.join( config.get( "template_dir" ), "SAMPLE_CANCEL_PENDING_EMAIL_TEMPLATE.html" )
            elif type == 'RESTART':
                subject = "[RESTART] %s / %s / %s / %s / %s" % ( h, h.reference_code, h.customer, h.program, h.item_code or '' )
                templatePath = os.path.join( config.get( "template_dir" ), "SAMPLE_CANCEL_PENDING_EMAIL_TEMPLATE.html" )

        subject = subject.replace( "\n", ' ' )

        send_to = set()
        shtm = DBSession.query( Team ).filter( Team.short_name == 'SH' ).one()

        #=======================================================================
        # if the request belong to the Shangehai office
        # update by CL.Lam ,required by Stella at 2013-10-9
        #=======================================================================
        if h.team_id == shtm.id or h.request_team_id == shtm.id:
            tmpChildren = set()
            for c in h.new_or_update:
                childForm, cid = c.split( "-" )
                tmpChildren.add( childForm )
            tmpChildren = list( tmpChildren )
            for e in DBSession.query( FormExtraInfo ).filter( FormExtraInfo.name.in_( tmpChildren ) ):
                if e.sh_email_to:
                    for email in e.sh_email_to.split( ";" ): send_to.add( email )

        elif h.program_id:
            if h.project_id and h.program.email_rule == 1 and h.project.email_rule == 1 :
                # check if the job's project is Wal-mark and project is ONN/ONN – Phase I/ONN – Phase II/ONN – Phase III/ONN – Project II/ONN – Project III
                # then send e-mail to Teen.Wong
                for t in config.get( "sample_email_rule_1", '' ).split( ";" ): send_to.add( t )
            elif h.project_id and h.program.email_rule == 10 and h.project.email_rule == 10 :
                # if the Corporate Customer is Techpoint and the brand is Pantone ,send to Lendo , Mankit , Mars , Stella , Teen
                # required by Wind.Kwok at 2013-11-06
                for t in config.get( "sample_email_rule_10", '' ).split( ";" ): send_to.add( t )
            elif h.project_id and h.program.email_rule == 11 and h.project.email_rule == 11 :
                for t in config.get( "sample_email_rule_11", '' ).split( ";" ): send_to.add( t )
            elif h.project_id and h.program.email_rule == 12 and h.project.email_rule == 12 :
                for t in config.get( "sample_email_rule_12", '' ).split( ";" ): send_to.add( t )
            elif h.program.email_rule == 2 :  # if the program is target ,send to XXX
                for t in config.get( "sample_email_rule_2", '' ).split( ";" ): send_to.add( t )
            elif h.program.email_rule == 3 :  # if the program is avon ,send to XXX
                for t in config.get( "sample_email_rule_3", '' ).split( ";" ): send_to.add( t )
            elif h.program.email_rule == 4 :  # if the program is bby ,send to XXX
                for t in config.get( "sample_email_rule_4", '' ).split( ";" ): send_to.add( t )
            elif h.program.email_rule == 7 :  # if the program is TT Micro ,send to XXX
                for t in config.get( "sample_email_rule_7", '' ).split( ";" ): send_to.add( t )
            elif h.program.email_rule == 8 :  # if the program is Maideform or HBI/Maidenform ,send to XXX
                for t in config.get( "sample_email_rule_8", '' ).split( ";" ): send_to.add( t )
            elif h.program.email_rule == 9 :  # if the program is Lowes ,send to XXX
                for t in config.get( "sample_email_rule_9", '' ).split( ";" ): send_to.add( t )
            else:
                tmpChildren = set()
                for c in h.new_or_update:
                    childForm, cid = c.split( "-" )
                    tmpChildren.add( childForm )
                tmpChildren = list( tmpChildren )
                for e in DBSession.query( FormExtraInfo ).filter( FormExtraInfo.name.in_( tmpChildren ) ):
                    if e.email_to:
                        for email in e.email_to.split( ";" ): send_to.add( email )

        if type != 'NORMAL' and extra:
            for e in DBSession.query( FormExtraInfo ).filter( FormExtraInfo.name.in_( extra.get( 'tasks', [] ) ) ):
                if e.email_to:
                    for email in e.email_to.split( ";" ): send_to.add( email )


        send_to = list( send_to )

        if request.identity["user"].email_address : send_to.append( request.identity["user"].email_address )
        cc_to = config.get( "sample_email_cc", '' ).split( ";" )
        if h.cc_to :
            cc_to.extend( filter( lambda c : bool( c ), h.cc_to.split( ";" ) ) )
#        templatePath = os.path.join(config.get("template_dir"),"SAMPLE_NORMAL_EMAIL_TEMPLATE.html")
        template = open( templatePath )
        html = "".join( template.readlines() )
        template.close()

        url = "%s/sample/viewRequest?id=%d" % ( config.get( 'website_url', 'http://service.r-pac.com.hk' ), h.id )

        if type == 'NORMAL' :
            labels = [c.getWidget().label for c in h.getChildrenForm() if "%s-%s" % ( c.__class__.__name__, c.id ) in h.new_or_update]
            content = html % ( h, h.rpt, h.create_by, h.update_by, h.customer, h.program, h.project, h.item_code or '', h.item_description or '', "/".join( labels ), url, url )
        else:
            content = html % ( task_label, type, h, h.rpt, h.create_by, h.update_by, h.customer, h.program, h.project, h.item_code or '', h.item_description or '', url, url )

        if config.get( "is_test", None ) != 'true':  # if it's test, don't send email out
            advancedSendMail( send_from, send_to, subject, None, content, cc_to )


    @expose( "tribal.templates.sample.report" )
    @tabFocus( tab_type = "report" )
    def report( self, **kw ):
        teams = DBSession.query( Team ).filter( and_( Team.active == 0 ) ).order_by( Team.name )
        return {"widget":report_form, "teams" : teams}

    @expose()
    def export( self, **kw ):
        if kw.get( "report_type", None ) not in ["SUMMARY", "INDIVIDAL", "DETAIL", "DETAIL_FORMAT2"]:
            flash( "No such report type!" )
            return redirect( "/sample/report" )

        baseYear = kw.get( "create_time_from", None ) or kw.get( "create_time_to", None ) or dt.now().year
        baseYear = baseYear[:4]

        CDispatch.__setattr__ = wrap_text_setattr_
        if kw["report_type"] == "SUMMARY":
            md, mtd, mcost = self._getMonthData( kw, baseYear )
            td, ttd, tcost = self._getTeamData( kw, baseYear )
            return serveFile( self._genSummaryReport( kw, md, mtd, mcost, td, ttd, tcost, baseYear ) )
        elif kw["report_type"] == "INDIVIDAL":
            teamData = self._getTeamIndividalData( kw, baseYear )
            return serveFile( self._genTeamIndividalReport( teamData, baseYear ) )
        elif kw["report_type"] == "DETAIL":
            teamData = self._getSummaryDetailReport( kw, baseYear )
            return serveFile( self._genSummaryDetailReport( teamData, baseYear ) )
        elif kw["report_type"] == "DETAIL_FORMAT2":
            teamData = self._getSummaryDetailReportByTeam( kw, baseYear )
            return serveFile( self._genSummaryDetailByTeamReport( teamData, baseYear ) )
        # CDispatch.__setattr__ = _setattr_



    def _getMonthData( self, kw, baseYear ):
        team_header = {}
        designer_x_header = []
        designer_y_header = []
        material_x_header = []
        material_y_header = []
        form_type_mapping = {}


        def _convert_y_offset( team_id ):
            return team_header.get( team_id, team_header[-1] )["index"]

        # prepare the header for the table
        index = 0
        for t in DBSession.query( Team ).filter( Team.active == 0 ).order_by( Team.name ):
            if t.report_category : continue
            team_header[t.id] = {
                              "index" : index,
                              "name"  : t.name,
                              }
            designer_y_header.append( t.name )
            material_y_header.append( t.name )
            index += 1

        team_header[-1] = { "index" : index, "name"  : "Other" }
        designer_y_header.append( "Other" )
        material_y_header.append( "Other" )

        material_header = {}
        for index, m in enumerate( DBSession.query( Stock ).filter( Stock.active == 0 ).order_by( Stock.index ) ):
            material_header[m.id] = {
                              "index" : index,
                              "name"  : m.reportName,  # update by CL on 2014/4/25
                              "cost"  : m.cost,
                              }
            material_x_header.append( m.reportName )

        index = 0
        category_index_mapping = {}
        for m in DBSession.query( FormTypeMapping ).filter( FormTypeMapping.active == 0 ).order_by( FormTypeMapping.categoryindex ):
            form_type_mapping[m.name] = {
                                        "category" : m.category,
                                        }

            if m.category not in category_index_mapping:
                form_type_mapping[m.name]["index"] = index
                category_index_mapping[m.category] = {
                                               "name" : m.report_header,
                                               "index" : index,
                                               }
                index += 1
                designer_x_header.append( m.report_header )
            else:
                form_type_mapping[m.name]["index"] = category_index_mapping[m.category]["index"]

        designer_x_header.append( "Time Spend(min)" )
        timming_index = index
        # start to fill in the data table
        monthData = [[] for i in range( 12 )]

        baseDay = dt.strptime( "%s0115" % baseYear , "%Y%m%d" )
        for i, row in enumerate( monthData ):
            if kw.get( "designers", "BOTH" ) == "BOTH":
                row.extend( [{
                        "x_header" : designer_x_header,
                        "y_header" : designer_y_header,
                        "x_title"    : ( baseDay + timedelta( days = 30 * i ) ).strftime( "%B" ).upper(),
                        "y_title" :  "HK Designers",
                        "content"  : [[0 for j in range( len( designer_x_header ) )] for i in  range( len( designer_y_header ) )  ]
                        }, {
                        "x_header" : designer_x_header,
                        "y_header" : designer_y_header,
                        "x_title"    : ( baseDay + timedelta( days = 30 * i ) ).strftime( "%B" ).upper(),
                        "y_title" :  "SZ Designers",
                        "content"  : [[0 for j in range( len( designer_x_header ) )] for i in  range( len( designer_y_header ) )  ]
                        }] )
            else:
                row.append( {
                            "x_header" : designer_x_header,
                            "y_header" : designer_y_header,
                            "x_title"    : ( baseDay + timedelta( days = 30 * i ) ).strftime( "%B" ).upper(),
                            "y_title" :  "HK Designers" if kw.get( "designers", "HK" ) == "HK" else "SZ Designers",
                            "content"  : [[0 for j in range( len( designer_x_header ) )] for i in  range( len( designer_y_header ) )  ]
                            } )



            row.append( {
                        "x_header" : material_x_header,
                        "y_header" : material_y_header,
                        "x_title"    : ( baseDay + timedelta( days = 30 * i ) ).strftime( "%B" ).upper(),
                        "y_title" : "Used Material",
                        "content"  : [[0 for j in range( len( material_x_header ) )] for i in  range( len( material_y_header ) )  ]
                        } )

        totalData = [
                     {
                      "x_header" : designer_x_header,
                      "content"  : [[0 for i in designer_x_header], ],
                      }, {
                      "x_header" : designer_x_header,
                      "content"  : [[0 for i in designer_x_header], ],
                      },
                     {
                      "x_header" : material_x_header,
                      "content"  : [[0 for i in material_x_header],
                                    [v["cost"] for v in sorted( material_header.values(), cmp = lambda v1, v2:cmp( v1["index"], v2["index"] ) )]
                                   ],
                      }
                    ]
        if kw.get( "designers", "BOTH" ) != "BOTH" : totalData = totalData[1:]

        totalTeamCost = {
                          "x_header" : designer_y_header + ["Total"],
                          "content"  : [[0 for i in range( len( designer_y_header ) + 1 )], ],
                          }

        # fill the designer table
        for m, j in self._getRawData( kw, "DESIGNER" ):
            if kw.get( "designers", "BOTH" ) == "BOTH":
                # hk is 0 ,sz is 1
                if j.designers == "HK":
                    team_designer_content = monthData[j.create_time.month - 1][0]["content"]
                    total_designer_content = totalData[0]["content"]
                else:
                    team_designer_content = monthData[j.create_time.month - 1][1]["content"]
                    total_designer_content = totalData[1]["content"]
            else:
                team_designer_content = monthData[j.create_time.month - 1][0]["content"]
                total_designer_content = totalData[0]["content"]

#            y_offset = team_header[m.team_id]["index"]
            y_offset = _convert_y_offset( m.team_id )
            if j.time_spand :
                team_designer_content[y_offset][timming_index] += float( j.time_spand )
                total_designer_content[0][timming_index] += float( j.time_spand )
            if not j.other_spend: continue
            for n, q in json.loads( j.other_spend ):
                if not q : continue
                q = q.strip()
                if not q : continue
                x_offset = form_type_mapping[n]["index"]
                team_designer_content[y_offset][x_offset] += float( q )
                total_designer_content[0][x_offset] += float( q )

        # fill the material table
        for m, jm in self._getRawData( kw, "MATERIAL" ):
            team_material_content = monthData[jm.create_time.month - 1][-1]["content"]
#            y_offset = team_header[m.team_id]["index"]
            y_offset = _convert_y_offset( m.team_id )
            x_offset = material_header[jm.stock_id]["index"]
            team_material_content[y_offset][x_offset] += jm.qty
            totalData[-1]["content"][0][x_offset] += jm.qty
            # count the cost
            totalTeamCost["content"][0][y_offset] += jm.qty * jm.cost
            totalTeamCost["content"][0][-1] += jm.qty * jm.cost


        return monthData, totalData, totalTeamCost



    def _getTeamData( self, kw, baseYear ):
        baseDay = dt.strptime( "%s0115" % baseYear, "%Y%m%d" )
        designer_y_header = material_y_header = [( baseDay + timedelta( days = 30 * i ) ).strftime( "%b" ) for i in range( 12 )]
        designer_x_header = []
        material_x_header = []

        # prepare the header for the table
        material_header = {}
        for index, m in enumerate( DBSession.query( Stock ).filter( Stock.active == 0 ).order_by( Stock.index ) ):
            material_header[m.id] = {
                              "index" : index,
                              "name"  : m.reportName,  # update by CL on 2014/4/25
                              "cost"  : m.cost,
                              }
            material_x_header.append( m.reportName )

        index = 0
        form_type_mapping = {}
        category_index_mapping = {}
        for m in DBSession.query( FormTypeMapping ).filter( FormTypeMapping.active == 0 ).order_by( FormTypeMapping.categoryindex ):
            form_type_mapping[m.name] = {
                                        "category" : m.category,
                                        }

            if m.category not in category_index_mapping:
                form_type_mapping[m.name]["index"] = index
                category_index_mapping[m.category] = {
                                               "name" : m.report_header,
                                               "index" : index,
                                               }
                index += 1
                designer_x_header.append( m.report_header )
            else:
                form_type_mapping[m.name]["index"] = category_index_mapping[m.category]["index"]

        designer_x_header.append( "Time Spend(min)" )
        timming_index = index

        team_index_mapping = {}
        teamData = []

        def _create_tmp( name ):
            tmp = [{
                  "x_header" : designer_x_header,
                  "y_header" : designer_y_header,
                  "x_title"    : name,
                  "y_title" : "HK Designers",
                  "content"  : [[0 for j in designer_x_header] for i in designer_y_header]
                  }, {
                  "x_header" : designer_x_header,
                  "y_header" : designer_y_header,
                  "x_title"    : name,
                  "y_title" : "SZ Designers",
                  "content"  : [[0 for j in designer_x_header] for i in designer_y_header]
                  },
                  {
                  "x_header" : material_x_header,
                  "y_header" : material_y_header,
                  "x_title"    : name,
                  "y_title" : "Used Material",
                  "content"  : [[0 for j in material_x_header] for i in material_y_header],
                  }]
            if kw.get( "designers", "BOTH" ) != "BOTH" :
                if kw.get( "designers", "HK" ) != "HK":
                    tmp.pop( 0 )
                else:
                    tmp.pop( 1 )
            return tmp

        index = 0
        for t in DBSession.query( Team ).filter( Team.active == 0 ).order_by( Team.name ):
            if t.report_category : continue
            team_index_mapping[t.id] = {
                              "index" : index,
                              "name"  : t.name,
                              }
            teamData.append( _create_tmp( t.name ) )
            index += 1


        # add the "Other" group
        team_index_mapping[-1] = {
                                  "index" : index,
                                  "name" : "Other"
                                  }
        teamData.append( _create_tmp( "Other" ) )


        totalData = [
                      {
                      "x_header" : designer_x_header,
                      "content"  : [[0 for i in designer_x_header], ],
                      },
                      {
                      "x_header" : designer_x_header,
                      "content"  : [[0 for i in designer_x_header], ],
                      },
                      {
                      "x_header" : material_x_header,
                      "content"  : [[0 for i in material_x_header],
                                    [v["cost"] for v in sorted( material_header.values(), cmp = lambda v1, v2:cmp( v1["index"], v2["index"] ) )],
                                    ],
                      }
                     ]

        if kw.get( "designers", "BOTH" ) != "BOTH" : totalData = totalData[1:]

        totalTeamCost = {
                          "x_header" : [v["name"] for v in sorted( team_index_mapping.values(), cmp = lambda v1, v2:cmp( v1["index"], v2["index"] ) )] + ["Total"],
                          "content"  : [[0 for i in range( len( team_index_mapping ) + 1 )], ],
                          }

        def _get_team_index( team_id ):
            return ( team_index_mapping.get( team_id, None ) or team_index_mapping[-1] )["index"]

        # fill the designer table
        for m, j in self._getRawData( kw, "DESIGNER" ):
            if kw.get( "designers", "BOTH" ) != "BOTH":
                team_designer_content = teamData[_get_team_index( m.team_id )][0]["content"]
                total_content = totalData[0]["content"]
            else:
                if j.designers == "HK":
                    team_designer_content = teamData[_get_team_index( m.team_id )][0]["content"]
                    total_content = totalData[0]["content"]
                else:
                    team_designer_content = teamData[_get_team_index( m.team_id )][1]["content"]
                    total_content = totalData[1]["content"]

            y_offset = j.create_time.month - 1
            if j.time_spand :
                team_designer_content[y_offset][timming_index] += float( j.time_spand )
                total_content[0][timming_index] += float( j.time_spand )
            if not j.other_spend: continue
            for n, q in json.loads( j.other_spend ):
                if not q : continue
                q = q.strip()
                if not q : continue
                x_offset = form_type_mapping[n]["index"]
                team_designer_content[y_offset][x_offset] += float( q )
                total_content[0][x_offset] += float( q )


        # fill the material table
        for m, jm in self._getRawData( kw, "MATERIAL" ):
            team_material_content = teamData[_get_team_index( m.team_id )][-1]["content"]
            y_offset = jm.create_time.month - 1
            x_offset = material_header[jm.stock_id]["index"]
            team_material_content[y_offset][x_offset] += jm.qty
            totalData[-1]["content"][0][x_offset] += jm.qty
            totalTeamCost["content"][0][_get_team_index( m.team_id )] += jm.qty * jm.cost
            totalTeamCost["content"][0][-1] += jm.qty * jm.cost

        return teamData, totalData, totalTeamCost


    def _genSummaryReport( self, kw, monthData, monthTotalData, monthTeamCost,
                          teamData, teamTotalData, teamTeamCost, baseYear ):
        templatePath = os.path.join( config.get( "template_dir" ), "SD_SUMMERY_TEMPLATE.xls" )
        tempFileName, realFileName = self._getReportFilePath( templatePath )
        try:
            sdexcel = SampleJobSummary( templatePath = tempFileName, destinationPath = realFileName )
            sdexcel.inputData( monthData, monthTotalData, monthTeamCost, teamData, teamTotalData, teamTeamCost, baseYear , kw )
            sdexcel.outputData()
            return realFileName
        except:
#            traceback.print_exc()
            logError()
            if sdexcel:sdexcel.clearData()
            raise ReportGenerationException()



    def _getRawData( self, kw, dataType ):
        begin = kw.get( "create_time_from", None )
        end = kw.get( "create_time_to", None )

        condition = [MainForm.active == 0, Job.active == 0, MainForm.id == Job.main_form_id]

        if begin :
#            condition.append(MainForm.create_time >= dt.strptime(kw["create_time_from"]+"00:00:00", "%Y-%m-%d%H:%M:%S"))
            condition.append( Job.create_time >= dt.strptime( kw["create_time_from"] + "00:00:00", "%Y-%m-%d%H:%M:%S" ) )
        if end:
#            condition.append(MainForm.create_time <= dt.strptime(kw["create_time_to"]+"23:59:59", "%Y-%m-%d%H:%M:%S"))
            condition.append( Job.create_time <= dt.strptime( kw["create_time_to"] + "23:59:59", "%Y-%m-%d%H:%M:%S" ) )

        if dataType in ["DESIGNER", "MATERIAL"]:
            if kw.get( "designers", "BOTH" ) != "BOTH":
                condition.append( Job.designers == kw["designers"] )

            if dataType == "DESIGNER":
#                condition.extend([MainForm.id == Job.main_form_id,])
                return DBSession.query( MainForm, Job ).filter( and_( *condition ) )

            elif dataType == "MATERIAL":
                condition.extend( [
#                                  MainForm.id==Job.main_form_id,
                                  Job.id == JobMaterial.job_id,
                                  JobMaterial.active == 0,
                                  ] )
                return DBSession.query( MainForm, JobMaterial ).filter( and_( *condition ) )

        elif dataType == "DETAIL":
            condition.extend( [
#                              MainForm.id == Job.main_form_id,
                              MainForm.program_id == Program.id,
                              MainForm.project_id == Project.id,
                              Program.active == 0,
                              Project.active == 0,
                              ] )
            return DBSession.query( MainForm, Program, Project, Job ).filter( and_( *condition ) )


    def _getRawDataByTeam( self, kw ):
        begin = kw.get( "create_time_from", None )
        end = kw.get( "create_time_to", None )

        condition = [MainForm.active == 0, Job.active == 0, MainForm.id == Job.main_form_id]

        if begin :
            condition.append( Job.create_time >= dt.strptime( kw["create_time_from"] + "00:00:00", "%Y-%m-%d%H:%M:%S" ) )
        if end:
            condition.append( Job.create_time <= dt.strptime( kw["create_time_to"] + "23:59:59", "%Y-%m-%d%H:%M:%S" ) )

        condition.extend( [
                          MainForm.team_id == kw['team_id'],
                          MainForm.program_id == Program.id,
                          MainForm.project_id == Project.id,
                          Program.active == 0,
                          Project.active == 0,
                          ] )
        return DBSession.query( MainForm, Program, Project, Job ).filter( and_( *condition ) )




    def _getTeamIndividalData( self, kw, baseYear ):
        baseDay = dt.strptime( "%s0115" % baseYear, "%Y%m%d" )
        designer_y_header = material_y_header = [( baseDay + timedelta( days = 30 * i ) ).strftime( "%b" ) for i in range( 12 )]
        designer_x_header = []
        material_x_header = []
        material_header = {}
        for index, m in enumerate( DBSession.query( Stock ).filter( Stock.active == 0 ).order_by( Stock.index ) ):
            material_header[m.id] = {
                              "index" : index,
                              "name"  : m.reportName,  # update by CL on 2014/4/25
                              "cost"  : m.cost,
                              }
            material_x_header.append( m.reportName )

        index = 0
        form_type_mapping = {}
        category_index_mapping = {}
        for m in DBSession.query( FormTypeMapping ).filter( FormTypeMapping.active == 0 ).order_by( FormTypeMapping.categoryindex ):
            form_type_mapping[m.name] = {
                                        "category" : m.category,
                                        }

            if m.category not in category_index_mapping:
                form_type_mapping[m.name]["index"] = index
                category_index_mapping[m.category] = {
                                               "name" : m.report_header,
                                               "index" : index,
                                               }
                index += 1
                designer_x_header.append( m.report_header )
            else:
                form_type_mapping[m.name]["index"] = category_index_mapping[m.category]["index"]

        designer_x_header.append( "Time Spend(min)" )
        timming_index = index
        team_index_mapping = {}
        teamData = []


        def _create_data_list( name ):
            if kw.get( "designers", "BOTH" ) == "BOTH":
                return    [{
                              "x_header" : designer_x_header,
                              "y_header" : designer_y_header,
                              "x_title"    : name,
                              "y_title" : "HK Designers",
                              "content"  : [[0 for j in designer_x_header] for i in designer_y_header]
                              }, {
                              "x_header" : designer_x_header,
                              "y_header" : designer_y_header,
                              "x_title"    : name,
                              "y_title" : "SZ Designers",
                              "content"  : [[0 for j in designer_x_header] for i in designer_y_header]
                              },
                              {
                              "x_header" : material_x_header,
                              "y_header" : material_y_header,
                              "x_title"    : name,
                              "y_title" : "Used Material",
                              "content"  : [[0 for j in material_x_header] for i in material_y_header],
                              }]
            else:
                return [{
                              "x_header" : designer_x_header,
                              "y_header" : designer_y_header,
                              "x_title"    : name,
                              "y_title" : "HK Designers" if kw.get( "designers", "HK" ) == "HK" else "SZ Designers",
                              "content"  : [[0 for j in designer_x_header] for i in designer_y_header]
                              },
                              {
                              "x_header" : material_x_header,
                              "y_header" : material_y_header,
                              "x_title"    : name,
                              "y_title" : "Used Material",
                              "content"  : [[0 for j in material_x_header] for i in material_y_header],
                              }]


        def _create_total_list():
            if kw.get( "designers", "BOTH" ) == "BOTH":
                return [{
                              "x_header" : designer_x_header,
                              "content"  : [[0 for i in designer_x_header], ],
                              },
                              {
                              "x_header" : designer_x_header,
                              "content"  : [[0 for i in designer_x_header], ],
                              },
                              {
                              "x_header" : material_x_header,
                              "content"  : [[0 for i in material_x_header],
                                            [v["cost"] for v in sorted( material_header.values(), cmp = lambda v1, v2:cmp( v1["index"], v2["index"] ) )],
                                            ],
                              }]
            else:
                return [{
                              "x_header" : designer_x_header,
                              "content"  : [[0 for i in designer_x_header], ],
                              },
                              {
                              "x_header" : material_x_header,
                              "content"  : [[0 for i in material_x_header],
                                            [v["cost"] for v in sorted( material_header.values(), cmp = lambda v1, v2:cmp( v1["index"], v2["index"] ) )],
                                            ],
                              }]

        index = 0
        for t in DBSession.query( Team ).filter( Team.active == 0 ).order_by( Team.name ):
            if t.report_category : continue
            team_index_mapping[t.id] = {
                          "index" : index,
                          "name"  : t.name,
                          }
            teamData.append( {
                   "name" : t.name,
                   "data" : _create_data_list( t.name ),
                   "total" : _create_total_list(),
                   "totalSpend" : 0,
                   } )
            index += 1


        team_index_mapping[-1] = {
                          "index" : index,
                          "name"  :"Other",
                          }
        teamData.append( {
                   "name" : "Other",
                   "data" : _create_data_list( "Other" ),
                   "total" : _create_total_list(),
                   "totalSpend" : 0,
                   } )


        def _get_team_data_index( team_id ):
            return ( team_index_mapping.get( team_id, None ) or team_index_mapping[-1] )["index"]


        # fill the designer table
        for m, j in self._getRawData( kw, "DESIGNER" ):
            oneTeam = teamData[_get_team_data_index( m.team_id )]
            if kw.get( "designers", "BOTH" ) != "BOTH":
                team_designer_content = oneTeam["data"][0]["content"]
                total_content = oneTeam["total"][0]["content"]
            else:
                if j.designers == "HK":
                    team_designer_content = oneTeam["data"][0]["content"]
                    total_content = oneTeam["total"][0]["content"]
                else:
                    team_designer_content = oneTeam["data"][1]["content"]
                    total_content = oneTeam["total"][1]["content"]

            y_offset = j.create_time.month - 1
            if j.time_spand :
                team_designer_content[y_offset][timming_index] += float( j.time_spand )
                total_content[0][timming_index] += float( j.time_spand )
            if not j.other_spend: continue
            for n, q in json.loads( j.other_spend ):
                if not q : continue
                x_offset = form_type_mapping[n]["index"]
                team_designer_content[y_offset][x_offset] += float( q )
                total_content[0][x_offset] += float( q )



        # fill the material table
        for m, jm in self._getRawData( kw, "MATERIAL" ):
            oneTeam = teamData[_get_team_data_index( m.team_id )]
            team_material_content = oneTeam["data"][-1]["content"]
            totalData = oneTeam["total"]
            y_offset = jm.create_time.month - 1
            x_offset = material_header[jm.stock_id]["index"]
            team_material_content[y_offset][x_offset] += jm.qty
            totalData[-1]["content"][0][x_offset] += jm.qty
#            oneTeam["totalSpend"] += jm.qty * material_header[jm.stock_id]["cost"]
            oneTeam["totalSpend"] += jm.qty * jm.cost
        return teamData


    def _genTeamIndividalReport( self, teamData, baseYear ):
        templatePath = os.path.join( config.get( "template_dir" ), "SD_TEAM_INDIVIDAL_TEMPLATE.xls" )
        tempFileName, realFileName = self._getReportFilePath( templatePath )
        try:
            sdexcel = SampleJobSummary( templatePath = tempFileName, destinationPath = realFileName )
            sdexcel.inputData2( teamData, baseYear )
            sdexcel.outputData()
            return realFileName
        except:
#            traceback.print_exc()
            logError()
            if sdexcel:sdexcel.clearData()
            raise ReportGenerationException()



    def _getReportFilePath( self, templatePath ):
        current = dt.now()
        dateStr = current.strftime( "%Y%m%d" )
        fileDir = os.path.join( config.get( "download_dir" ), "sample", dateStr )
        if not os.path.exists( fileDir ): os.makedirs( fileDir )
        tempFileName = os.path.join( fileDir, "%s_%s_%d.xls" % ( request.identity["user"].user_name,
                                                           current.strftime( "%Y%m%d%H%M%S" ), random.randint( 0, 1000 ) ) )
        realFileName = os.path.join( fileDir, "%s_%s.xls" % ( request.identity["user"].user_name, current.strftime( "%Y%m%d%H%M%S" ) ) )
        shutil.copy( templatePath, tempFileName )
        return tempFileName, realFileName



    def _getSummaryDetailReport( self, kw, baseYear ):
#        test = [{
#                 "name" : "test team",
#                 "data" : [{
#                             "title" : "test",
#                             "x_header" : ["A1","A2","A3","A4"],
#                             "y_header" : [
#                                           ["y1",["y11","y12","y13"]],["y2",["y21","y22"]],["y3",["y31","y32"]]
#                                           ],
#                             "content"  : [["%d%d" %(i,j) for j in range(4)] for i in range(7)],
#                             "total"    : [ j for j in range(4) ],
#                           },]
#                 },]
#        return test

        beginMonth = dt.strptime( kw["create_time_from"], "%Y-%m-%d" ).month if kw.get( "create_time_from", None ) else 1
        endMonth = dt.strptime( kw["create_time_to"], "%Y-%m-%d" ).month if kw.get( "create_time_to", None ) else 12

#        if kw.get("create_time_from",None):
#            beginMonth = dt.strptime(kw["create_time_from"],"%Y-%m-%d").month

        baseDay = dt.strptime( "%s0115" % baseYear, "%Y%m%d" )
        monthList = [( baseDay + timedelta( days = 30 * i ) ).strftime( "%B" ) for i in range( 12 )]
        designer_x_header = []
        index = 0
        form_type_mapping = {}
        category_index_mapping = {}


        for m in DBSession.query( FormTypeMapping ).filter( FormTypeMapping.active == 0 ).order_by( FormTypeMapping.category2index ):
            form_type_mapping[m.name] = {
                                        "category" : m.category2,
                                        }

            if m.category2 not in category_index_mapping:
                form_type_mapping[m.name]["index"] = index
                category_index_mapping[m.category2] = {
                                               "name" : m.report_header2,
                                               "index" : index,
                                               }
                index += 1
                designer_x_header.append( m.report_header2 )
            else:
                form_type_mapping[m.name]["index"] = category_index_mapping[m.category2]["index"]
        designer_x_header.append( "Time Spend(min)" )
        timming_index = index


        team_index_mapping = {}
        teamData = []
        index = 0

        def _create_data( name ):
            return [{
                     "title" : "%s (%s,%s)" % ( name, monthList[beginMonth + i - 1], baseYear ),
                     "x_header" : designer_x_header,
                     "y_header" : [],
                     "content"  : [],
                     "total"    : [0 for i in designer_x_header],
                     "y_index_mapping" : {},
                     } for i in range( endMonth - beginMonth + 1 )]

        for t in DBSession.query( Team ).filter( Team.active == 0 ).order_by( Team.name ):
            if t.report_category : continue
            team_index_mapping[t.id] = {
                              "index" : index,
                              "name"  : t.name,
                              }
            teamData.append( {
                             "name" : t.name,
                             "data" : _create_data( t.name ),
                             } )
            index += 1

        team_index_mapping[-1] = {"index" : index, "name" : "Other"}
        teamData.append( { "name" : "Other", "data" : _create_data( "Other" ) } )


        def _getOneTeamOneMonth( team_id ):
            return teamData[( team_index_mapping.get( m.team_id, None ) or team_index_mapping[-1] )["index"]]["data"]

        # fill the designer table
        for m, program, project, j in self._getRawData( kw, "DETAIL" ):
            oneTeamOneMonth = _getOneTeamOneMonth( m.team_id )[j.create_time.month - beginMonth]
            team_designer_content = oneTeamOneMonth["content"]
            total_content = oneTeamOneMonth["total"]

            total_content[timming_index] += j.time_spand

            y_index_mapping = oneTeamOneMonth["y_index_mapping"]
            if m.project_id in y_index_mapping:
                y_offset = y_index_mapping[m.project_id]  # to count out
            else:
                insert_location = 0
                for header, sub_header in oneTeamOneMonth["y_header"]:
                    insert_location += len( sub_header )
                    if header == program.name:
                        sub_header.append( project.name )  # error here

                        for y_index_key, y_index_val in y_index_mapping.items() :
                            if y_index_val >= insert_location :  y_index_mapping[y_index_key] += 1

                        break
                else:
                    oneTeamOneMonth["y_header"].append( [program.name, [project.name, ]] )
                y_offset = y_index_mapping[m.project_id] = insert_location
                team_designer_content.insert( insert_location, [0 for i in designer_x_header] )

            team_designer_content[y_offset][timming_index] += j.time_spand
            if not j.other_spend: continue
            for n, q in json.loads( j.other_spend ):
                if not q : continue
                x_offset = form_type_mapping[n]["index"]
                team_designer_content[y_offset][x_offset] += float( q )
                total_content[x_offset] += float( q )

        return teamData


    def _genSummaryDetailReport( self, teamData, baseYear ):
        templatePath = os.path.join( config.get( "template_dir" ), "SD_SUMMERY_DETAIL_TEMPLATE.xls" )
        tempFileName, realFileName = self._getReportFilePath( templatePath )
        try:
            sdexcel = SampleJobSummary( templatePath = tempFileName, destinationPath = realFileName )
            sdexcel.inputData3( teamData, baseYear )
            sdexcel.outputData()
            return realFileName
        except:
            logError()
            if sdexcel:sdexcel.clearData()
            raise ReportGenerationException()



    def _getSummaryDetailReportByTeam( self, kw, baseYear ):
        beginMonth = dt.strptime( kw["create_time_from"], "%Y-%m-%d" ).month if kw.get( "create_time_from", None ) else 1
        endMonth = dt.strptime( kw["create_time_to"], "%Y-%m-%d" ).month if kw.get( "create_time_to", None ) else 12
        team = DBSession.query( Team ).get( kw["team_id"] )

        baseDay = dt.strptime( "%s0115" % baseYear, "%Y%m%d" )
        monthList = [( baseDay + timedelta( days = 30 * i ) ).strftime( "%B" ) for i in range( 12 )]
        designer_x_header = []
        index = 0
        form_type_mapping = {}
        category_index_mapping = {}
        for m in DBSession.query( FormTypeMapping ).filter( FormTypeMapping.active == 0 ).order_by( FormTypeMapping.category3index ):
            form_type_mapping[m.name] = {
                                        "category" : m.category3,
                                        }

            if m.category3 not in category_index_mapping:
                form_type_mapping[m.name]["index"] = index
                category_index_mapping[m.category3] = {
                                               "name" : m.report_header3,
                                               "index" : index,
                                               }
                index += 1
                designer_x_header.append( m.report_header3 )
            else:
                form_type_mapping[m.name]["index"] = category_index_mapping[m.category3]["index"]
        designer_x_header.append( "Time Spend(min)" )
        timming_index = index

        def _create_data( name ):
            return [{
                 "month" : monthList[beginMonth + i - 1],
                 "title" : "%s (%s,%s)" % ( name, monthList[beginMonth + i - 1], baseYear ),
                 "x_header" : designer_x_header,
                 "hk_y_header" : [],
                 "sz_y_header" : [],
                 "hk_content"  : [],
                 "sz_content"  : [],
                 "total"    : [0 for i in designer_x_header],
                 "hk_y_index_mapping" : {},
                 "sz_y_index_mapping" : {},
                 } for i in range( endMonth - beginMonth + 1 )]


        oneTeamData = {
                         "name" : team.name,
                         "data" : _create_data( team.name ),
                         }

        # fill the designer table
        for m, program, project, j in self._getRawDataByTeam( kw ):
            if not j.designers : continue
            oneTeamOneMonth = oneTeamData["data"][j.create_time.month - beginMonth]

            if j.designers == "HK" :
                team_designer_content = oneTeamOneMonth["hk_content"]
                y_index_mapping = oneTeamOneMonth["hk_y_index_mapping"]
                y_header = oneTeamOneMonth["hk_y_header"]
            else:
                team_designer_content = oneTeamOneMonth["sz_content"]
                y_index_mapping = oneTeamOneMonth["sz_y_index_mapping"]
                y_header = oneTeamOneMonth["sz_y_header"]

            total_content = oneTeamOneMonth["total"]
            total_content[timming_index] += j.time_spand
            if m.project_id in y_index_mapping:
                y_offset = y_index_mapping[m.project_id]  # to count out
            else:
                insert_location = 0
                for header, sub_header in y_header:
                    insert_location += len( sub_header )
                    if header == program.name:
                        sub_header.append( project.name )  # error here

                        for y_index_key, y_index_val in y_index_mapping.items() :
                            if y_index_val >= insert_location :  y_index_mapping[y_index_key] += 1

                        break
                else:
                    y_header.append( [program.name, [project.name, ]] )
                y_offset = y_index_mapping[m.project_id] = insert_location
                team_designer_content.insert( insert_location, [0 for i in designer_x_header] )

            team_designer_content[y_offset][timming_index] += j.time_spand
            if not j.other_spend: continue
            for n, q in json.loads( j.other_spend ):
                if not q : continue
                x_offset = form_type_mapping[n]["index"]
                team_designer_content[y_offset][x_offset] += float( q )
                total_content[x_offset] += float( q )

        return oneTeamData



    def _genSummaryDetailByTeamReport( self, teamData, baseYear ):
        templatePath = os.path.join( config.get( "template_dir" ), "SD_SUMMERY_DETAIL_TEAM_TEMPLATE.xls" )
        tempFileName, realFileName = self._getReportFilePath( templatePath )
        try:
            sdexcel = SampleJobSummary( templatePath = tempFileName, destinationPath = realFileName )
            sdexcel.inputData4( teamData, baseYear )
            sdexcel.outputData()
            return realFileName
        except:
            logError()
            if sdexcel:sdexcel.clearData()
            raise ReportGenerationException()



    @expose( "json" )
    def ajaxDeleteAttachment( self, **kw ):
        try:
            clz = self._getDBClzByID( kw["form_id"] )
            obj = DBSession.query( clz ).get( kw["id"] )
            atts = obj.getAttachment()
            del atts[atts.index( kw["a_id"] )]
            obj.attachment = "|".join( atts )
            DBSession.add( DevelopmentLog( main_form_id = obj.main_id, sub_form_id = obj.id,
                                         sub_form_type = clz.__name__, action_type = 'UPDATE',
                                         remark = "user[%s] delete the attachment[id=%s]." % ( request.identity["user"], kw["a_id"] ) ) )
            DBSession.flush()
            return {"flag":0}
        except:
#            traceback.print_exc()
            logError()
            return {"flag":1}

    @expose()
    def downloadAllAttachment( self, **kw ):
        try:
            obj_id = kw['form_id']
            dbclz = self._getDBClzByID( obj_id )
            paths = []
            for i in dbclz.get( int( kw['sub_id'] ) ).getAttachment( wrapper = True ):
                paths.append( [i.file_path, i.file_name] )
            zip_folder = os.path.join( config.download_dir, 'sample' )
            if not os.path.exists( zip_folder ):
                os.makedirs( zip_folder )
            zip_path = os.path.join( zip_folder, '%s_%s.zip' % ( obj_id, dt.now().strftime( "%Y%m%d%H%M%S" ) ) ).replace( '\\', '/' )
            create_zip( zip_path, paths )
            return serveFile( zip_path )
        except:
            logError()
            flash( "Error occor on the server side!", 'warn' )
            redirect( "/sample/index" )

    @expose()
    def upload( self, **kw ):
        ( flag, objs ) = sysUpload( kw["attachment"], kw["attachment_name"] )

        if flag != 0 :
            flash( "error" )
        else:
            flash( ",".join( [str( id ) for id in objs if id] ) )

        redirect( "/sample/test" )

        try:
            file_path = kw["attachment"].filename
            ( pre, ext ) = os.path.splitext( file_path )

            path_prefix = os.path.join( config.download_dir, "sys" )
            if not os.path.exists( path_prefix ) : os.makedirs( path_prefix )

            file_name = "%s%.4d%s" % ( dt.now().strftime( "%Y%m%d%H%M%S" ), random.randint( 1, 1000 ), ext )
            full_path = os.path.join( path_prefix, file_name )

            f = open( full_path, "wb" )
            f.write( kw["attachment"].file.read() )
            f.close()

            db_file_name = kw.get( "attachment_name", None ) or file_name
            if db_file_name.find( "." ) < 0 : db_file_name = db_file_name + ext

            obj = UploadObject( file_name = db_file_name, file_path = os.path.join( "sys", file_name ) )
            DBSession.add( obj )
            DBSession.flush()
#            return obj.id
            flash( obj.id )
        except:
#            traceback.print_exc()
            logError()
            flash( "Error" )
        redirect( "/sample/test" )

    @expose( "json" )
    def ajaxRegionTeam( self, **kw ):
        try:
            if kw.get( "id" ):
                curr = DBSession.query( SampleGroupProfile ).filter( SampleGroupProfile.active == 0 )
                if kw.get( 'key' ) == 'project_own':curr = curr.filter( SampleGroupProfile.region_id == kw["id"] )
                else:curr = curr.filter( SampleGroupProfile.team_id == kw["id"] )
                curr = curr.all()
                users = []
                for a in curr:
                    if a and a.group:
                        for b in a.group.users:
                            objs = {'id':b.user_id, 'display_name':b.display_name}
                            if objs not in users: users.append( objs )
                # excluded = DBSession.query(Group).filter(~Group.users.any(User.user_id == u.user_id)).order_by(Group.group_name)
                sorted_x = sorted( users.__iter__(), key = operator.itemgetter( 'display_name' ) )
                return dict( user = sorted_x, cur = kw.get( 'key' ) , active = 0 )
            else:
                return dict( msg = "fail" , active = 1 )
        except:
#            traceback.print_exc()
            logError()
            return dict( msg = "fail" , active = 1 )


    @expose()
    def actionFromEmail( self, type, id, result ):
        try:
            dbObj = self._getDBClzByID( type )
            form = DBSession.query( dbObj ).filter( and_( dbObj.active == 0, dbObj.id == id ) ).one()

            if form.status != WAIT_FOR_APPROVAL :
                flash( "No approve/disapprove action need to be done on this record!" )
            else:
                form.status = NEW_REQUEST if result == "Y" else DISAPPROVAL
                action = "Approve" if result == "Y" else "Disapprove"
                d = DevelopmentLog( main_form_id = form.main_id, sub_form_id = form.id, sub_form_type = type, action_type = action, remark = "[%s]%s %s the form[id : %s]" % ( type, request.identity["user"], action, id ) )
                DBSession.add( d )
                DBSession.flush()  # fix the strange problem
                flash( "Update the record successfully!" )
        except:
#            traceback.print_exc()
            logError()
            transaction.doom()
            flash( "The record doesn't exist!" )
        redirect( "/sample/index" )


    @expose()
    def snapshot( self, **kw ):
        """snapshot 
        logging using picture
        2011-11-04
        """
        try:
#            host = '127.0.0.1'
#            port = '1312'
            host_url = request.headers.get( 'Host' )
            positions = kw.get( 'positions', '' )
            url = kw.get( "snapshot_url" )
            jobno = kw.get( "jobno", '' ).strip()
            files = kw.get( "file_exts", '' )
#            log_id = int(kw.get("id", 0))
#            qty = int(kw.get("qty", 0))
            if url and positions and files:
                http_url = 'http://%s/sample/%s' % ( host_url, url )
                phantomjs = os.path.join( config.get( 'public_dir' ), 'phantomjs', 'phantomjs.exe' )
                snapshotjs = os.path.join( config.get( 'public_dir' ), 'phantomjs', 'snapshot.js' )
                img_dir = os.path.join( config.get( 'public_dir' ), 'upload', 'snapshot' )
                if not os.path.exists( img_dir ):
                    os.makedirs( img_dir )
                # Usage: phantomjs.exe snapshot.js URL positions   img_dir
                sp = subprocess.Popen( "%s %s %s %s %s %s" % ( phantomjs, snapshotjs, http_url, positions, img_dir, files ),
                         stdout = subprocess.PIPE, stderr = subprocess.STDOUT )
                file_list = []
                dlzipFile = os.path.join( img_dir, "%s_%s%d.zip" % ( jobno, dt.now().strftime( "%Y%m%d%H%M%S" ),
                                                                         random.randint( 1, 1000 ) ) )
                while 1:
                    if sp.poll() is not None:
                        # print 'exec command completed.'
                        break
                    else:
                        line = sp.stdout.readline().strip()
                        # print line
                        if line.endswith( '.pdf' ) or line.endswith( '.png' ):
                            # zip to download
                            file_list.append( line )
                if file_list:
                    dlzip = zipfile.ZipFile( dlzipFile, "w", zlib.DEFLATED )
                    for fl in file_list:
                        dlzip.write( os.path.abspath( str( fl ) ), os.path.basename( str( fl ) ) )
                    dlzip.close()
                    try:
                        for fl in file_list:
                            os.remove( fl )
                    except:
                        pass
                    return serveFile( unicode( dlzipFile ) )
                else:
                    raise Exception( 'No file generated!' )
        except Exception, e:
            log.exception( str( e ) )
            flash( "Error occor on the server side!", 'warn' )
            redirect( "/sample/%s" % url )


    @expose( "json" )
    def checkDuplicate( self, **kw ):
        if not kw.get( "project", None ) or not kw.get( "item_code", None ) : return {"flag" : 1}
        _query = DBSession.query( MainForm ).filter( and_( MainForm.active == 0, MainForm.item_code == kw["item_code"], MainForm.status != DRAFT ) )
        if kw.get( 'main_id', None ):
            _query = _query.filter( MainForm.id != int( kw['main_id'] ) )
        if _query.filter( MainForm.project_id == kw["project"] ).count() > 0 or _query.filter( MainForm.program_id == kw["program"] ).count() > 0:
            return {"flag": 1}
        else:
            return {"flag": 0}

    @expose()
    def release( self, **kw ):
        h = getOr404( MainForm, kw["id"], "/sample/index" )
        if h.child_form:
            for sfClz in  h.child_form.split( "|" ):
                clz = self._getDBClzByID( sfClz )
                for obj in DBSession.query( clz ).filter( clz.main_id == h.id ): obj.active = 0
        DBSession.add( DevelopmentLog( main_form_id = h.id, sub_form_id = None, sub_form_type = None, action_type = 'RELEASE', remark = "%s release the tabs." % request.identity["user"] ) )
        flash( "Release the tabs successfully!" )
        redirect( "/sample/viewRequest?id=%s" % h.id )


    @expose()
    def resend_email( self, **kw ):
        h = getOr404( MainForm, kw["id"], "/sample/index" )
        reasons_html = []
        html_template = '<tr><td style="width:300px">%s</td><td style="width:100px"><a href="%s" target="_blank">Approve</a></td><td style="width:100px"><a href="%s" target="_blank">NOT Approve</a></td></tr>'

        for c in h.getChildrenForm():
            if c.send_email != 0 and c.status == WAIT_FOR_APPROVAL:
                yes_url = "%s/sample/actionFromEmail?type=%s&id=%s&result=Y" % ( config.get( "website_url" ), c.__class__.__name__, c.id, )
                no_url = "%s/sample/actionFromEmail?type=%s&id=%s&result=N" % ( config.get( "website_url" ), c.__class__.__name__, c.id, )
                reasons_html.append( html_template % ( c.why_need_approve(), yes_url, no_url ) )

        if reasons_html:
            managers = getManagerByTeam( h.team_id, False )
            if managers:
                if config.get( "is_test", False ):
                    send_from = "r-tracktest@r-pac.com.hk"
                    subject = "[TESTING]Need your approval on the job : %s" % str( h )
                else:
                    send_from = "r-track@r-pac.com.hk"
                    subject = "Need your approval on the job : %s" % str( h )
                send_to = map( lambda m:m.email_address, managers )
                cc_to = config.get( "sample_email_cc", "" ).split( ";" )

                templatePath = os.path.join( config.get( "template_dir" ), "SAMPLE_EMAIL_TEMPLATE.html" )
                template = open( templatePath )
                html = "".join( template.readlines() )
                template.close()

                url = "%s/sample/viewRequest?id=%d" % ( config.get( 'website_url', 'http://service.r-pac.com.hk' ), h.id )
                content = html % ( h.create_by, h, h.team, h.contact_person, h.customer, h.program, h.project, h.item_code, h.item_description, url, "".join( reasons_html ) )
                if config.get( "is_test", None ) != 'true':  # if it's test, don't send email out
                    advancedSendMail( send_from, send_to, subject, None, content, cc_to )

                DBSession.add( DevelopmentLog( main_form_id = h.id, sub_form_id = None, sub_form_type = None, action_type = 'RESEND', remark = "%s re-send the approve e-mail." % request.identity["user"] ) )
            flash( "Resend the approve e-mail successfully!" )
        else:
            flash( "No need to resend the approve e-mail!" )
        redirect( "/sample/viewRequest?id=%s" % h.id )


    def _removeSession( self, token ):
        FormSerialize.delete_by_token( token )


    @expose()
    def deleteJob( self, **kw ):
        h = getOr404( MainForm, kw.get( 'id', None ), '/sample/index' )
        h.active = 1
        DevelopmentLog( main = h, system_no = str( h ), sub_form_id = None, sub_form_type = None, action_type = "DELETE", remark = None )
        flash( 'The record has been deleted successfully!' )
        redirect( '/sample/index' )


    @expose( 'tribal.templates.sample.combine' )
    def combine( self, **kw ):
        result = []
        if not kw: return {'result' : result, 'values' : kw }

        jobs = kw.get( 'jobs', None )
        if jobs:
            ws = [MainForm.__table__.c.system_no.op( "ilike" )( "%%%s%%" % job ) for job in jobs.split( "," )]
            result = DBSession.query( MainForm ).filter( or_( *ws ) ).order_by( MainForm.create_time )

        return {'result' : result, 'values' : kw}




    @expose()
    def combineSave( self, **kw ):
        ids = kw.get( 'ids', None )
        tid = kw.get( 'target', None )
        reason = kw.get( 'reason', None )

        if not ids or not tid :
            flash( 'No job to combine ,or not target supplied !' )
            return redirect( '/sample/combine' )

        target = DBSession.query( MainForm ).get( tid )
        if not target :
            flash( 'The target job does not exist!' )
            return redirect( '/sample/combine' )

        try:
            subformType = set()
            done = []
            for jid in ids:
                obj = DBSession.query( MainForm ).get( jid )
                if not obj : continue
                if obj.id == target.id : continue
            # transfer the subtask
                for c in obj.getChildrenForm():
                    c.main_id = target.id
            # transfer the job
                rs = DBSession.query( Job ).filter( Job.main_form_id == obj.id )
                for r in rs:
                    r.main_form_id = target.id

                for c in obj.child_form.split( '|' ) : subformType.add( c )
            # inactive the jobs except the target
            # required by Wing.Kwok. ask to search the combined job
#                obj.active = 1
            # transfer the job log
                DBSession.query( DevelopmentLog ).filter( DevelopmentLog.main_form_id == obj.id ).update( {"main_form_id": target.id} )
            # transfer the version
                DBSession.query( FormVersion ).filter( FormVersion.main_id == obj.id ).update( {'main_id' : target.id} )
            # add the redirect job ID to the delete job
                obj.combine_to_id = target.id
                done.append( unicode( obj ) )

                DBSession.add( DevelopmentLog( main_form_id = obj.id, action_type = 'COMBINE', remark = 'Combine this job into %s. Reason : %s' % ( target, reason ) ) )


            for c in target.child_form.split( "|" ) : subformType.discard( c )
            if subformType:
                target.child_form = '%s|%s' % ( target.child_form, "|".join( list( subformType ) ) )

            # make the job
            DBSession.add( DevelopmentLog( main_form_id = target.id, action_type = 'COMBINE', remark = 'Combine the jobs[%s] into it. Reason : %s' % ( ','.join( done ), reason ) ) )
            flash( 'Succ!' )
        except:
            traceback.print_exc()
            transaction.doom()
            flash( 'Error on the server!' )
        return redirect( '/sample/combine' )
