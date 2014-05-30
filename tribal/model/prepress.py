# -*- coding: utf-8 -*-
from datetime import date, datetime as dt
import json, traceback, itertools, logging, copy

from sqlalchemy import *
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import backref
from sqlalchemy.orm import mapper
from sqlalchemy.orm import relation
from sqlalchemy.schema import Column
from sqlalchemy.schema import Table
from sqlalchemy.types import Integer
from sqlalchemy.types import Unicode
from sqlalchemy.types import PickleType
from tg import request
from tribal.model import DBSession
from tribal.model import DeclarativeBase
from tribal.model import metadata
from tribal.model.auth import *
from tribal.model.sysutil import *
from tribal.util.common import sysUpload
from tribal.util.sql_helper import *
from tribal.model.sample import SysMixin, Region, Team, Customer, Program, \
    Project


__all__ = [
           'PS_NEW_REQUEST', 'PS_ASSIGNED', 'PS_UNDER_DEVELOPMENT', 'PS_COMPLETED_REQUEST', 'PS_PENDING',
           'PS_CANCELED_REQUEST', 'PS_DRAFT',
           'PS_JOB_COMPLETE', 'PS_JOB_NEW', 'PS_JOB_PENDING',
           'PSAppTeam', 'PSItemCategory', 'PSMainForm', 'PSSFUpload', 'PSSFBarcode', 'PSJob',
           'PSDevelopmentLog', 'PSFormVersion']


log = logging.getLogger( __name__ )

PS_NEW_REQUEST = 0
PS_ASSIGNED = 1
PS_UNDER_DEVELOPMENT = 2
PS_COMPLETED_REQUEST = 3
PS_PENDING = 4
PS_CANCELED_REQUEST = 9
PS_DRAFT = -10

PS_JOB_COMPLETE = 0
PS_JOB_NEW = 1
PS_JOB_PENDING = 2


class PSEasyMixin( object ):

    __excluded__ = ["id"]

    @classmethod
    def get( cls, id ):
        id = int( id ) if type( id ) != int else id
        return DBSession.query( cls ).get( id )

    @classmethod
    def find_all( cls ):
        return DBSession.query( cls ).filter( cls.active == 0 ).order_by( cls.name ).all()

    @classmethod
    def getColumns( cls, excluded = None ):
        excluded = excluded or cls.__excluded__
        colums = []
        m = cls.__mapper__.columns
        for cname in m.keys():
            if isinstance( m[cname], Column ) and cname not in excluded:
                colums.append( cname )
        return colums

    def populateAsDict( self, prefix = "" ):
        vs = {}
        for c in self.getColumns(): vs["%s%s" % ( prefix, c )] = getattr( self, c )
        return self._fineTune( vs, prefix )

    def _fineTune( self, vs, prefix ):
        # this method should be overwritten by the subclass if some special fields need to format beform vendor to outside.
        return vs


    @classmethod
    def _refineValue( clz, kw, prefix, actionType = None ):
        # this method need to be overwrite by the subclass to handle the
        for i in clz.__table__.columns:
            if type( i.type ) == Integer or type( i.type ) == DateTime:
                key = '%s%s' % ( prefix, i.key )
                if kw.has_key( key ):
                    if kw[key] == None or kw[key] == '':
                        kw[key] = None
                    elif type( i.type ) == Integer:
                        kw[key] = int( kw[key] )
        return kw

    def saveAttachment( self, kw, prefix ):
        ids = kw.get( "%s%s" % ( prefix, "attachment_ids" ), None )
        if ids:    # update sub form attachment id after save sub form success
            self.attachment = "%s|%s" % ( self.attachment, "|".join( map( str, ids ) ) ) if self.attachment else "|".join( map( str, ids ) )

    def saveUpdateWithDict( self, kw, prefix = "" ):
        refinedValue = self._refineValue( kw, prefix, "UPDATE" )
        for c in self.getColumns():
            key = "%s%s" % ( prefix, c )
            if key in refinedValue:
                setattr( self, c, refinedValue[key] )
        self.saveAttachment( kw, prefix )

    @classmethod
    def saveNewWithDict( clz, kw, prefix = "" ):
        vs = {}
        refinedValues = clz._refineValue( kw, prefix, "NEW" )
        for c in clz.getColumns():
            key = "%s%s" % ( prefix, c )
            if refinedValues.has_key( key ):
                if refinedValues[key] or refinedValues[key] == 0:
                    vs[c] = refinedValues[key]
        obj = clz( ** vs )
        obj.saveAttachment( kw, prefix )
        return obj

    def serialize( self, valueFromDB = True, exclude_field = [] ):
        result = {}
        excluded = ['id', 'create_time', 'create_by_id', 'update_time',
                    'update_by_id', 'active', 'status', 'status_back',
                    'complete_time', 'send_email', 'revision']

        if exclude_field:
            excluded.extend( exclude_field )

        m = self.__mapper__.columns
        for cname in m.keys():
            colClz = m[cname]
            if isinstance( colClz, Column ) and cname not in excluded:
                v = getattr( self, cname )

                if v is None: v = ''
                elif isinstance( v, ( dt, date ) ): v = v.strftime( '%Y-%m-%d' )
                elif isinstance( colClz.type, CheckBoxCol ):    # the sql checkbox field
                    if type( v ) != list : v = str( v )
                    else:  v = " , ".join( map( str, sorted( v ) ) )
                elif isinstance( colClz.type, MultiTextCol ):    # the sql multitext field
                    if type( v ) != list : v = str( v )
                    else:  v = ",".join( map( str, v ) )

                result[cname] = ( v, colClz.doc or cname )
        return result




class PSFormMixin( object ):
    status = Column( Integer, default = 0 )
    overall_result = Column( Unicode( 5 ), default = None )    # 0 is fail ,1 is pass
    attachment = Column( Unicode( 999 ) )
    complete_time = Column( DateTime )
    complete_by_id = Column( Integer )
    status_back = Column( Integer, default = 0 )    # to store the last status
    send_email = Column( Integer, default = 0 )    # 0 is not send email ,1 is send email already
#     worktime = Column( Text )
#     spendmins = Column( Integer, default = 0 )


    @classmethod
    def getWidget( clz ):
        from tribal.widgets import prepress as prepressWidget
        return getattr( prepressWidget, "%sWidget" % clz.__name__ )



    def showStatus( self ):
        if self.status == PS_NEW_REQUEST: return "New"
        if self.status == PS_ASSIGNED: return "Assigned"
        if self.status == PS_UNDER_DEVELOPMENT: return "Under Development"
        if self.status == PS_COMPLETED_REQUEST: return "Completed"
        if self.status == PS_CANCELED_REQUEST: return "Cancelled"
        if self.status == PS_PENDING : return "Pending"
        return ""


    def getAttachment( self, wrapper = False, attach_type = "attachment" ):
        '''获取sub_form附件
        Args:
            attach_type: 附件类型，attachment或complete_attachment
        '''
        try:
            attachment = getattr( self, attach_type )
            if not wrapper: return [id for id in attachment.split( "|" ) if id]
            m = lambda id: DBSession.query( UploadObject ).get( id )
            return map( m, [id for id in attachment.split( "|" ) if id] )
        except:
            return []


    @classmethod
    def copyAttachments( cls, ids ):
        if isinstance( ids, str ) or isinstance( ids, unicode ):
            ids = [ids]
        objs = [DBSession.query( UploadObject ).get( int( id ) ) for id in ids if id]
        attachments = []
        for obj in objs:
            if obj:
                attachment = UploadObject( **{'file_name': obj.file_name, 'file_path': obj._file_path} )
                DBSession.add( attachment )
                DBSession.flush()
                attachments.append( attachment.id )
        return attachments

    @property
    def jobs( self ):
        try:
            return DBSession.query( PSJob ).filter( and_( PSJob.active == 0, PSJob.sub_form_type == self.__class__.__name__,
                                               PSJob.sub_form_id == self.id, PSJob.status == PS_JOB_COMPLETE ) ).all()
        except Exception, e:
            log.exception( str( e ) )
            return []

    @property
    def complete_by( self ):
        try:
            return DBSession.query( User ).get( self.complete_by_id )
        except:
            return None


    @classmethod
    def compareObject( cls, old_obj, new_obj ):
        kw_master = {
            'child_form': {
                'type': list,
                'seperator': '|',
                'kw': {
                    "PSSFUpload":"Prepress",
                    "PSSFBarcode":"Barcode",
                }
            }
        }

        old_keys = old_obj.keys()
        new_keys = new_obj.keys()
        result = {
                  "new" : [],
                  "update" : [],
                  "delete" : [],
                  }

        for key in list( set( old_keys ).intersection( set( new_keys ) ) ):
            old_val = old_obj[key][0]
            new_val = new_obj[key][0]

            if old_val is None : old_val = ''
            if new_val is None : new_val = ''

            old_val = unicode( old_val )
            new_val = unicode( new_val )

            if old_val != new_val:
                if kw_master.has_key( key ):
                    val_master = kw_master[key]['kw']
                    if kw_master[key]['type'] == list:
                        old_list = old_obj[key][0].split( kw_master[key].get( 'seperator', '|' ) )
                        new_list = new_obj[key][0].split( kw_master[key].get( 'seperator', '|' ) )
                        old_list_copy = copy.copy( old_list )
                        new_list_copy = copy.copy( new_list )

                        for i in new_list:
                            if i in old_list_copy:
                                new_list_copy.remove( i )
                                old_list_copy.remove( i )
                        for val in old_list_copy:
                            if val:
                                result['delete'].append( ( old_obj[key][1], val_master[val] ) )
                        for val in new_list_copy:
                            if val:
                                result['new'].append( ( new_obj[key][1], val_master[val] ) )
                else:
                    result['update'].append( ( old_obj[key][1], old_obj[key][0], new_obj[key][0] ) )

        return result




class PSAppTeam( DeclarativeBase, PSEasyMixin, SysMixin ):
    __tablename__ = 'prepress_app_team'

    id = Column( Integer, primary_key = True )
    name = Column( Unicode( 20 ) )

    def __str__( self ):
        return self.name

    @property
    def users( self ):
        user_list = []
        try:
            for profile in self.prepress_profiles:
                user_list.extend( profile.group.users )
            return set( user_list )
        except Exception, e:
            log.exception( str( e ) )
            return []


class PSItemCategory( DeclarativeBase, PSEasyMixin, SysMixin ):
    __tablename__ = 'prepress_item_category'

    id = Column( Integer, primary_key = True )
    name = Column( Unicode( 100 ) )

    def __str__( self ):  return self.name



class PSMainForm( DeclarativeBase, SysMixin, PSFormMixin, PSEasyMixin ):
    __tablename__ = 'prepress_main_form'

    id = Column( Integer, primary_key = True )
    system_no = Column( Unicode( 50 ), doc = 'System No' )
    project_own_id = Column( Integer, ForeignKey( 'sample_region.id' ), doc = 'Project Owner Name' )
    project_own = relation( Region )
    contact_person = Column( Unicode( 50 ), doc = 'Division in Charge Contact Person' )
#    request_person = Column(Unicode(50))
    team_id = Column( Integer, ForeignKey( 'sample_team.id' ), doc = 'Division in Charge Team' )
    team = relation( Team, primaryjoin = team_id == Team.id )

    request_team_id = Column( Integer, ForeignKey( 'sample_team.id' ), doc = 'Request Team' )
    request_team = relation( Team, primaryjoin = request_team_id == Team.id )

    customer_id = Column( Integer, ForeignKey( 'sample_customer.id' ), doc = 'Vendor/Customer' )
    customer = relation( Customer )
#     program_id = Column( Integer, ForeignKey( 'sample_program.id' ), doc = 'Corporate Customer' )
#     program = relation( Program )
    project = Column( Unicode( 50 ), doc = 'Brand' )

    item_category_id = Column( Integer, ForeignKey( 'prepress_item_category.id' ), doc = 'Item Category' )
    item_category = relation( PSItemCategory, primaryjoin = item_category_id == PSItemCategory.id )

    reference_code = Column( Text, doc = 'Reference Code' )
    item_description = Column( Text, doc = 'Item Description' )
    item_code = Column( Text, doc = 'Item Code' )
    child_form = Column( Text, doc = 'Task' )
    request_contact_number = Column( Text, doc = 'Contact number' )
    cc_to = Column( Text, doc = 'E-mail CC to' )

    request_type = Column( Unicode( 10 ) )
    revision = Column( Integer, default = 0 )
    rpt = Column( Unicode( 100 ) )    # kevin add
    project_owner = Column( Unicode( 100 ) )    # kevin add
    percentage = Column( Float, default = 0 )
    _new_or_update = Column( 'new_or_update', Unicode( 500 ), doc = 'new or update' )

    app_team_id = Column( Integer, ForeignKey( 'prepress_app_team.id' ) )
    app_team = relation( PSAppTeam, doc = 'Applicable Team ' )

    assign_users = Column( Unicode( 500 ) )

    def get_new_or_update( self ):
        if self._new_or_update is None : return []
        return self._new_or_update.split( "|" )


    def set_new_or_update( self, content ):
        if not content :
            self._new_or_update = None
        else:
            self._new_or_update = "|".join( content )


    new_or_update = property( fget = get_new_or_update, fset = set_new_or_update )


    def __str__( self ):
        return "%s-RC%.2d" % ( self.system_no, self.revision ) if self.revision else self.system_no

    def getChildren( self ):
        return [] if  not self.child_form else list( set( self.child_form.split( "|" ) ) )


    def getChildrenForm( self ):
        k = lambda n: globals()[n]
        m = lambda d: DBSession.query( d ).filter( and_( d.active == 0, d.main_id == self.id ) ).order_by( d.id ).all()

        result = []
        try:
            for c in self.getChildren(): result.extend( m( k( c ) ) )
            return sorted( result, cmp = lambda x, y : cmp( x.create_time, y.create_time ) )
        except Exception, e:
            log.exception( str( e ) )
            return result

    def getChildrenDict( self ):
        childrenDict = {}
        for i in self.getChildrenForm():
            clzName = i.__class__.__name__
            if not childrenDict.has_key( clzName ):
                childrenDict[clzName] = {}
            childrenDict[clzName].update( {str( i.id ): i} )
        return childrenDict

    @property
    def jobs( self ):
        try:
            return DBSession.query( PSJob ).filter( and_( PSJob.active == 0, PSJob.main_form_id == self.id ) ).all()
        except Exception, e:
            log.exception( str( e ) )
            return []


    def update( self, **kw ):
        old_object = self.serialize()
        old_object_status = self.status
        for key, dbobj in [( "project_own", Region ), ( "team", Team ), ( "customer", Customer ), ( "request_team", Team ),
                          ( "item_category", PSItemCategory )]:
            if key in kw :
                val = DBSession.query( dbobj ).get( kw[key] ) if kw[key] else None
                setattr( self, key, val )

        for key in ["contact_person", "reference_code", "item_description", "item_code", "project_owner", "request_contact_number", "project"]:
            if key in kw :
                val = kw[key].strip() if kw[key] else None
                setattr( self, key, val )

        if "cc_to" in kw:
            self.cc_to = ( kw["cc_to"] or '' ).replace( "\n", '' )

        self.child_form = kw.get( "form_ids" )
        # add the update log
        if old_object_status != PS_DRAFT:
            self.revision += 1
        # if update from draft and save to status: new
        if old_object_status == PS_DRAFT and not kw['is_draft']:
            self.status = PS_NEW_REQUEST
        new_object = self.serialize( False )
        check_log = PSMainForm.compareObject( old_object, new_object )
        log_str = []
        for ( key, old_val, new_val ) in check_log['update']:
            log_str.append( "Change [%s] from '%s' to '%s' " % ( key, old_val, new_val ) )
        for ( key, new_val ) in check_log['new']:
            log_str.append( "New [%s] '%s' " % ( key, new_val ) )
        if log_str and old_object_status != PS_DRAFT: DBSession.add( PSDevelopmentLog( system_no = str( self ), main_form_id = self.id, sub_form_id = None, sub_form_type = None, action_type = 'UPDATE', remark = " .\n".join( log_str ) ) )




    @classmethod
    def create( cls, **kw ):
        requiredFields = ["project_own", "contact_person", "team", "project", "project_own"]
        is_draft = kw['is_draft']
        if not is_draft:
            for f in requiredFields:
                if not kw.get( f, False ) :
                    raise Exception( 'Please Fill in the required field(s) before you submit the request!' )
        hParam = {
                  'child_form': kw.get( "form_ids", '' ),
                  "contact_person" : kw.get( "contact_person", None ),
                  "reference_code" : kw.get( "reference_code", None ),
                  "item_description" : kw.get( "item_description", None ),
                  "item_code" : kw.get( "item_code", None ),
                  "request_contact_number" : kw.get( "request_contact_number", None ),
                  "team" : DBSession.query( Team ).get( kw["team"] ) if kw.get( "team", None ) else None,
                  "customer" : DBSession.query( Customer ).get( kw["customer"] ) if kw.get( "customer", False ) else None,
                  "item_category" : DBSession.query( PSItemCategory ).get( kw["item_category"] ) if kw.get( "item_category", False ) else None,
                  "project" : kw.get( "project", None ),
                  "project_own" : DBSession.query( Region ).get( kw["project_own"] ) if kw.get( "project_own", False ) else None,
                  "request_team" : DBSession.query( Team ).get( kw["request_team"] ) if kw.get( "request_team", None ) else None,
                  "project_owner" : kw.get( "project_owner", None ),
                  "rpt" : kw.get( "rpt", None ) or None,
                  "cc_to" : kw.get( "cc_to", None ) or None,
                  "status": PS_DRAFT if is_draft else PS_NEW_REQUEST,
                  "status_back": PS_DRAFT if is_draft else PS_NEW_REQUEST,
                  }
        if hParam['cc_to'] : hParam['cc_to'] = hParam['cc_to'].strip().replace( "\n", '' )

        hParam["request_type"] = "New"

        def _getSystemNo():
            s = Sequence( 'rp_main_form_seq' )
            s.create( DBSession.bind, checkfirst = True )    # if the seq is existed ,don't create again
            c = DBSession.execute( s )
            prefix = 'OTHER'
            for g in request.identity["user"].groups:
                for profile in g.prepress_profiles:
                    if profile.region_id :
                        prefix = profile.region.code
                        break
#             return "RP%s%.6d" % ( prefix, c )
            return "RP%s%s" % ( prefix, c )

        hParam["system_no"] = _getSystemNo()
        h = PSMainForm( **hParam )
        DBSession.add( h )
        return h



class PSSFUpload( DeclarativeBase, SysMixin, PSFormMixin, PSEasyMixin ):
    __tablename__ = 'prepress_sub_form_upload'

    id = Column( Integer, primary_key = True )
    main_id = Column( Integer, ForeignKey( 'prepress_main_form.id' ) )
    main = relation( PSMainForm )

    # job_nature = Column(CheckBoxCol(99), doc='Job Nature ')
    checking = Column( CheckBoxCol( 99 ), doc = 'Artwork Pre-Flight/Die-line Pre-Flight' )

    file_from = Column( CheckBoxCol( 99 ), doc = 'Files From' )
    from_ftp_location = Column( Text, doc = 'Files From FTP Location' )
    from_public_location = Column( Text, doc = 'Files From Public Location' )

    file_to = Column( CheckBoxCol( 99 ), doc = 'File to' )
    to_ftp_location = Column( Text, doc = 'File to FTP Location' )
    to_public_location = Column( Text, doc = 'File to Public Location' )

    output = Column( CheckBoxCol( 99 ), doc = 'Output' )
    output_other_content = Column( Text, doc = 'Output other content' )

    expected_date = Column( DateTime, doc = 'Expected date' )
    remark = Column( Text, doc = 'Remark' )

#     complete_items = Column( Integer )
    complete_attachment = Column( Text )



class PSSFBarcode( DeclarativeBase, SysMixin, PSFormMixin, PSEasyMixin ):
    __tablename__ = 'prepress_sub_form_barcode'

    id = Column( Integer, primary_key = True )
    main_id = Column( Integer, ForeignKey( 'prepress_main_form.id' ) )
    main = relation( PSMainForm )

    file_from = Column( CheckBoxCol( 99 ), doc = 'Files From ' )
    file_from_ftp_location = Column( Text, doc = 'Files From ftp location' )
    file_from_files_location = Column( Text, doc = 'Files From files location' )

    size_w = Column( Text, doc = 'Label Info size width' )
    size_h = Column( Text, doc = 'Label Info size height' )
    size_unit = Column( CheckBoxCol( 99 ), doc = 'Label Info size unit' )

    material = Column( Text, doc = 'Label Info material' )
    country = Column( Text, doc = 'Label Info country' )
    item_code = Column( Text, doc = 'Label Info item code' )
    item_name = Column( Text, doc = 'Label Info item name' )
    barcode = Column( Unicode( 49 ), doc = 'Label Info barcode' )
    font = Column( Text, doc = 'Label Info font' )
    content_color = Column( Text, doc = 'Label Info content color' )
    color = Column( CheckBoxCol( 99 ), doc = 'Label Info color' )
    color_other_content = Column( Text, doc = 'Label Info color other' )

    output = Column( CheckBoxCol( 99 ), doc = 'Output' )
    protection = Column( CheckBoxCol( 99 ), doc = 'Security File Protction' )
    output_other_content = Column( Text, doc = 'Output other content' )

#     complete_items = Column( Integer )
    complete_attachment = Column( Text )
    expected_date = Column( DateTime, doc = 'Expected date' )
    remark = Column( Text, doc = 'Remark' )



class PSJob( DeclarativeBase, SysMixin ):
    __tablename__ = 'prepress_job'

    id = Column( Integer, primary_key = True )
    main_form_id = Column( Integer, ForeignKey( 'prepress_main_form.id' ) )
    main = relation( PSMainForm, backref = "jobs", primaryjoin = "and_(PSMainForm.id == PSJob.main_form_id, PSJob.active == 0,PSJob.status == 0)" )
    sub_form_id = Column( Integer )
    sub_form_type = Column( Unicode( 50 ) )

#     time_spand = Column( Float, default = None )
    complete_time = Column( DateTime, default = None )
    item = Column( Integer, default = 0 )
    remark = Column( Text )

    #===========================================================================
    # added at 09-05
    #===========================================================================
    job_type = Column( Text )
    status = Column( Integer, default = PS_JOB_COMPLETE )    # 0 is completed, 1 is new , 2 is under development, 3 is pending
    status_bak = Column( Integer )    # to log down the orignal status before restart
    time_list = Column( Text )    # log out the start-end time ,its stucture is s1,e1|s2,e2
    time_count = Column( Integer, default = 0 )    # the system count time ,come from the time_list

    def sub_form( self ):
        try:
            return DBSession.query( globals()[self.sub_form_type] ).get( self.sub_form_id )
        except Exception, e:
            log.exception( str( e ) )
            return None


class PSDevelopmentLog( DeclarativeBase, SysMixin ):
    __tablename__ = 'prepress_development_log'

    id = Column( Integer, primary_key = True )
    system_no = Column( Text )
    main_form_id = Column( Integer, ForeignKey( 'prepress_main_form.id' ) )
    main = relation( PSMainForm, backref = "Logs" )
    sub_form_id = Column( Integer )
    sub_form_type = Column( Text )
    action_type = Column( Text )
    remark = Column( Text )

    @property
    def sub_form( self ):
        selfModule = __import__( "tribal.model.prepress" ).model.prepress
        dbclz = getattr( selfModule, self.sub_form_type )
        return DBSession.query( dbclz ).get( self.sub_form_id )



class PSFormVersion( DeclarativeBase ):

    __tablename__ = 'prepress_form_version'

    id = Column( Integer, primary_key = True )
    main_id = Column( Integer, ForeignKey( 'prepress_main_form.id' ) )
    version = Column( Unicode( 50 ) )
    serialize = Column( PickleType() )

    @classmethod
    def get( cls, id ):
        return DBSession.query( cls ).get( id )

    @classmethod
    def find_by_main_id( cls, main_id ):
        return DBSession.query( cls ).filter( cls.main_id == main_id ).order_by( desc( cls.version ) )

    @property
    def main( self ):
        return self.serialize['main']

    @property
    def subs( self ):
        return self.serialize['subs']


class PSGroupProfile( DeclarativeBase, SysMixin ):
    __tablename__ = 'prepress_group_profile'

    id = Column( Integer, primary_key = True )
    name = Column( Unicode( 50 ) )
    description = Column( Unicode( 1000 ) )
    group_id = Column( Integer, ForeignKey( 'tg_group.group_id' ) )
    group = relation( Group, backref = "prepress_profiles", primaryjoin = "PSGroupProfile.group_id == Group.group_id" )

    team_id = Column( Integer, ForeignKey( 'sample_team.id' ) )
    team = relation( Team )
    app_team_id = Column( Integer, ForeignKey( 'prepress_app_team.id' ) )
    app_team = relation( PSAppTeam, backref = "prepress_profiles", primaryjoin = "PSGroupProfile.app_team_id == PSAppTeam.id" )
    region_id = Column( Integer, ForeignKey( 'sample_region.id' ) )
    region = relation( Region )

    def __str__( self ):
        return self.name

