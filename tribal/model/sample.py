# -*- coding: utf-8 -*-
from datetime import date, datetime as dt
import json, traceback, itertools, logging, copy
import urllib

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
from tribal.model import DBSession, DB_DATE_FORMAT
from tribal.model import DeclarativeBase
from tribal.model import metadata
from tribal.model.auth import *
from tribal.model.sysutil import *
from tribal.util.common import sysUpload
from tribal.util.sql_helper import *



__all__ = ["NEW_REQUEST", "WAIT_FOR_APPROVAL", "DISAPPROVAL", "UNDER_DEVELOPMENT", "CANCELED_REQUEST", "COMPLETED_REQUEST", "PENDING", "DRAFT",
    "SysMixin",
    "Region", "Customer", "Program", "Project", "Team", "SampleGroupProfile", "Stock", "ItemCategory",
    "MainForm", "SFTarget", "SFAvon", "SFBestBuy",
    "SFBox", "SFTray", "SFFloor", "SFGeneral", "SFLabel", "SFArtwork", "SFSampling", "SFPrintout", "SF3DImage",
    "SFAssembly", "SFDrop", "SFUpload", "SFContainer", "SFFileConvert", "SFPhoto",
    "DevelopmentLog", "Job", "JobMaterial", "FormExtraInfo", "FormTypeMapping",
    "uploadAttachments", "FormSerialize", "FormVersion", 'SFTabLabel']

log = logging.getLogger( __name__ )


##############################################################################################################
#
#        Form status define
#
##############################################################################################################


NEW_REQUEST = 0
WAIT_FOR_APPROVAL = -1
DISAPPROVAL = -2
CANCELED_REQUEST = -9
DRAFT = -10
COMPLETED_REQUEST = 1
UNDER_DEVELOPMENT = 2
PENDING = 3


SFTabLabel = {
    "SFTarget":"Target",
    "SFTray":"Tray",
    "SFAvon":"Avon",
    "SFBestBuy":"Best Buy",
    "SFBox":"Box",
    "SFFloor":"Floor/Pallet Display/Sidekick",
    "SFGeneral":"General packaging Design",
    "SFLabel":"Barcode Label",
    "SFArtwork":"Artwork",
    "SFPrintout":"Printout",
    "SFSampling":"Sampling",
    "SF3DImage":"3D Image",
    "SFAssembly":"Assembly Sheet",
    "SFDrop":"Drop Test",
    "SFUpload":"Upload/Download/File checking",
    "SFContainer":"Container Loading",
    "SFFileConvert":"File Convert",
    "SFPhoto":"Photo Shot"
}

##############################################################################################################
#
#        Mixin Object define
#
##############################################################################################################


def getUserID():
    user_id = 1
    try:
        user_id = request.identity["user"].user_id
    except:
        pass
    finally:
        return user_id

def uploadAttachments( kw ):
    for k, v in kw.iteritems():
        if k.endswith( 'attachment' ):
            ( flag, ids ) = sysUpload( v, kw["%s_name" % k] )
            print '#' * 40, 'upload file: flag: %s, ids: %s' % ( flag, ids )
            if flag != 0: raise "Error when upload the file(s)"
            else:
                del kw[k]
                kw['%s_ids' % k] = ids

class EasyMixin( object ):

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
        if ids:  # update sub form attachment id after save sub form success
            self.attachment = "%s|%s" % ( self.attachment, "|".join( map( str, ids ) ) ) if self.attachment else "|".join( map( str, ids ) )


    @classmethod
    def _makeRemark( clz, v ):
        return '%s Remark Added At %s %s\n%s' % ( '*' * 10, dt.now().strftime( DB_DATE_FORMAT ), '*' * 10, v )


    def saveUpdateWithDict( self, kw, prefix = "" ):
        is_draft = True if kw.get( 'is_draft', None ) == 'true' else False
        refinedValue = self._refineValue( kw, prefix, "UPDATE" )
        for c in self.getColumns():
            key = "%s%s" % ( prefix, c )
            if key in refinedValue:
                if not is_draft and c == 'remark' :
                    if self.remark and refinedValue[key]:
                        refinedValue[key] = '%s\n\n%s' % ( self.remark, self._makeRemark( refinedValue[key] ) )
                    elif refinedValue[key]:
                        refinedValue[key] = self._makeRemark( refinedValue[key] )
                    elif self.remark:
                        refinedValue[key] = self.remark
                setattr( self, c, refinedValue[key] )
        self.saveAttachment( kw, prefix )


    @classmethod
    def saveNewWithDict( clz, kw, prefix = "" ):
        vs = {}
        action = kw.get( 'action', None )
        is_draft = kw.get( 'is_draft', False )
        refinedValues = clz._refineValue( kw, prefix, "NEW" )
        for c in clz.getColumns():
            key = "%s%s" % ( prefix, c )
            if refinedValues.has_key( key ):
                if action == 'copy' or is_draft or c != 'remark':
                    if refinedValues[key] or refinedValues[key] == 0: vs[c] = refinedValues[key]
                elif refinedValues[key]:
                    vs[c] = clz._makeRemark( refinedValues[key] )
        obj = clz( ** vs )
        obj.saveAttachment( kw, prefix )
        return obj


    def serialize( self, valueFromDB = True, exclude_field = [] ):
        result = {}
        excluded = ['id', 'create_time', 'create_by_id', 'update_time',
                    'update_by_id', 'active', 'status', 'status_back',
                    'complete_time', 'send_email', 'revision', 'group_no']

        if exclude_field:
            excluded.extend( exclude_field )

        m = self.__mapper__.columns
        for cname in m.keys():
            colClz = m[cname]
            if isinstance( colClz, Column ) and cname not in excluded:
                v = getattr( self, cname )
#                if valueFromDB:
#                    if v is None:
#                        v = ''
#                    elif isinstance(colClz.type, (DateTime, Date)):  #the sql date time field
#                        v = v.strftime('%Y-%m-%d') if v else ''
#                    elif isinstance(colClz.type, CheckBoxCol):  #the sql checkbox field
#                        v = str(sorted(v))
#                    elif cname in ['material_widgets','shoot_widgets']: #special handle for the material widget info
#                        v = ",".join(sorted([d['SHOW_TEXT'] for d in v])) if v else ''
# #                    elif cname == 'insert_material': #special value for the box material info
# #                        v = v['SHOW_TEXT'] if v else ''
#                    elif (cname == 'insert_material' and isinstance(self, SFBox)) or \
#                         (cname == 'material' and isinstance(self, SFBestBuy)) or \
#                         (cname == 'material_other' and isinstance(self, SFTarget)) :
#                        v = v['SHOW_TEXT'] if v else ''
#
#                else:
#                    if v is None: v = ''
#
#                    elif isinstance(colClz.type, CheckBoxCol):  #the sql checkbox field
#                        v = unicode([v]) if type(v) != list else unicode(sorted(v))
#                    elif cname in ['material_widgets','shoot_widgets']: #special handle for the material widget info
#                        v = ",".join(sorted([d['SHOW_TEXT'] for d in v])) if v else ''
# #                    elif cname == 'insert_material': #special value for the box material info
# #                        v = v['SHOW_TEXT'] if v else ''
#                    elif (cname == 'insert_material' and isinstance(self, SFBox)) or \
#                         (cname == 'material' and isinstance(self, SFBestBuy)) or \
#                         (cname == 'material_other' and isinstance(self, SFTarget)) :
#                        v = v['SHOW_TEXT'] if v else ''


                if v is None: v = ''
                elif isinstance( v, ( dt, date ) ): v = v.strftime( '%Y-%m-%d' )
                elif isinstance( colClz.type, CheckBoxCol ):  # the sql checkbox field
                    if type( v ) != list : v = str( v )
                    else:  v = " , ".join( map( str, sorted( v ) ) )
                elif isinstance( colClz.type, MultiTextCol ):  # the sql multitext field
                    if type( v ) != list : v = str( v )
                    else:  v = ",".join( map( str, v ) )
                elif cname in ['material_widgets', 'shoot_widgets']:  # special handle for the material widget info
                    v = ",".join( sorted( [urllib.unquote( d['SHOW_TEXT'] ) for d in v] ) ) if v else ''
                elif ( cname == 'insert_material' and isinstance( self, SFBox ) ) or \
                         ( cname == 'material' and isinstance( self, SFBestBuy ) ) or \
                         ( cname == 'material_other' and isinstance( self, SFTarget ) ) :
                        v = urllib.unquote( v['SHOW_TEXT'] ) if v else ''


                result[cname] = ( v, colClz.doc or cname )
        return result


class SysMixin( object ):
    create_time = Column( DateTime, default = dt.now )
    create_by_id = Column( Integer, default = getUserID )
    update_time = Column( DateTime, default = dt.now, onupdate = dt.now )
    update_by_id = Column( Integer, default = getUserID, onupdate = getUserID )
    active = Column( Integer, default = 0 )  # 0 is active ,1 is inactive

    @property
    def create_by( self ):
        return DBSession.query( User ).get( self.create_by_id )

    @property
    def update_by( self ):
        return DBSession.query( User ).get( self.update_by_id )



class FormMixin( object ):
    status = Column( Integer, default = 0 )
    overall_result = Column( Unicode( 5 ), default = None )  # 0 is fail ,1 is pass
    attachment = Column( Unicode( 999 ) )
    complete_time = Column( DateTime )
    complete_by_id = Column( Integer )
    status_back = Column( Integer, default = 0 )  # to store the last status
    send_email = Column( Integer, default = 0 )  # 0 is not send email ,1 is send email already

    group_no = Column( Integer, default = 0 )



    @classmethod
    def getWidget( clz ):
        from tribal.widgets import sample as sampleWidget
        return getattr( sampleWidget, "%sWidget" % clz.__name__ )

    def showStatus( self ):
        if self.status == NEW_REQUEST: return "New"
        if self.status == UNDER_DEVELOPMENT: return "Under Development"
        if self.status == CANCELED_REQUEST: return "Cancelled"
        if self.status == WAIT_FOR_APPROVAL: return "Wait For Approval"
        if self.status == DISAPPROVAL: return "Disapproval"
        if self.status == COMPLETED_REQUEST: return "Completed"
        if self.status == PENDING: return "Pending"
        return ""

    def getDevelopmentLog( self ):
        if self.__class__.name == "MainForm":
            col = DevelopmentLog.main_form_id == self.id
        else:
            col = DevelopmentLog.sub_form_type == self.__class__.__name__
        return DBSession.query( DevelopmentLog ).filter( and_( DevelopmentLog.active == 0, col ) ).order_by( DevelopmentLog.update_time )


    @classmethod
    def getEstimateTime( clz ):
        try:

            return DBSession.query( FormExtraInfo ).filter( and_( FormExtraInfo.active == 0,
                                                         FormExtraInfo.name == clz.__name__ ) ).first().estimate_time
        except:
            # traceback.print_exc()
            return None

    @classmethod
    def getFormExtra( clz ):
        try:
            return DBSession.query( FormExtraInfo ).filter( and_( FormExtraInfo.active == 0, FormExtraInfo.name == clz.__name__ ) ).first()
        except:
            # traceback.print_exc()
            return None

    def getAttachment( self, wrapper = False ):
        try:
            if not wrapper: return [id for id in self.attachment.split( "|" ) if id]
            m = lambda id: DBSession.query( UploadObject ).get( id )
            return map( m, [id for id in self.attachment.split( "|" ) if id] )
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
            return DBSession.query( Job ).filter( and_( Job.active == 0, Job.sub_form_type == self.__class__.__name__,
                                               Job.sub_form_id == self.id ) ).order_by( Job.create_time ).all()
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
                'kw': SFTabLabel
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
                        # diff = lambda l1,l2: [x for x in l1 if x not in l2]
                else:
                    result['update'].append( ( old_obj[key][1], old_obj[key][0], new_obj[key][0] ) )
        '''
        for key in list(set(old_obj).difference(set(new_obj))):
            result['delete'].append((old_obj[key][1], old_obj[key][0]))

        for key in list(set(new_obj).difference(set(old_obj))):
            result['new'].append((old_obj[key][1], new_obj[key][0]))
        '''
        return result

    def why_need_approve( self ):
        return None

##############################################################################################################
#
#        Logic Object define
#
##############################################################################################################

class Region( DeclarativeBase, EasyMixin, SysMixin ):
    __tablename__ = 'sample_region'

    id = Column( Integer, primary_key = True )
    name = Column( Unicode( 20 ) )
    code = Column( Unicode( 5 ) )

    def __str__( self ):
        return self.name


class Customer( DeclarativeBase, EasyMixin, SysMixin ):
    __tablename__ = 'sample_customer'

    id = Column( Integer, primary_key = True )
    name = Column( Unicode( 100 ) )

    def __str__( self ):
        return self.name



class Program( DeclarativeBase, EasyMixin, SysMixin ):
    __tablename__ = 'sample_program'

    id = Column( Integer, primary_key = True )
    name = Column( Unicode( 50 ) )
    email_rule = Column( Integer )

    def __str__( self ):
        return self.name


class Project( DeclarativeBase, EasyMixin, SysMixin ):
    __tablename__ = 'sample_project'

    id = Column( Integer, primary_key = True )
    name = Column( Unicode( 50 ) )

    program_id = Column( Integer, ForeignKey( 'sample_program.id' ) )
    program = relation( Program )
    email_rule = Column( Integer )

    def __str__( self ):
        return self.name

    @classmethod
    def find_by_program( cls, program_id ):
        return DBSession.query( cls ).filter( cls.program_id == program_id ).all()

class Team( DeclarativeBase, EasyMixin, SysMixin ):
    __tablename__ = 'sample_team'

    id = Column( Integer, primary_key = True )
    name = Column( Unicode( 20 ) )
    short_name = Column( Unicode( 10 ) )
    manager = Column( Unicode( 100 ) )
    report_category = Column( Unicode( 20 ) )
    need_approval = Column( Integer, default = 0 )  # 0 don't need approval, 1 need approval

    def __str__( self ):
        return self.name



class Stock( DeclarativeBase, EasyMixin, SysMixin ):
    __tablename__ = 'sample_stock'

    id = Column( Integer, primary_key = True )
    name = Column( Unicode( 100 ) )
    cost = Column( Float, default = 0 )
    reportName = Column( "report_name", Text )
    index = Column( Integer )

    def __str__( self ):
        return self.name



class ItemCategory( DeclarativeBase, EasyMixin, SysMixin ):
    __tablename__ = 'sample_item_category'

    id = Column( Integer, primary_key = True )
    name = Column( Unicode( 100 ) )

    def __str__( self ):
        return self.name



class MainForm( DeclarativeBase, EasyMixin, SysMixin, FormMixin ):
    __tablename__ = 'sample_main_form'

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
    program_id = Column( Integer, ForeignKey( 'sample_program.id' ), doc = 'Corporate Customer' )
    program = relation( Program )
    project_id = Column( Integer, ForeignKey( 'sample_project.id' ) )
    project = relation( Project, doc = 'Brand' )

    item_category_id = Column( Integer, ForeignKey( 'sample_item_category.id' ), doc = 'Item Category' )
    item_category = relation( ItemCategory, primaryjoin = item_category_id == ItemCategory.id )

    reference_code = Column( Text, doc = 'Reference Code' )
    item_description = Column( Text, doc = 'Item Description' )
    item_code = Column( Text, doc = 'Item Code' )
    child_form = Column( Text, doc = 'Task' )
    request_contact_number = Column( Text, doc = 'Contact number' )
    cc_to = Column( Text, doc = 'E-mail CC to' )

    request_type = Column( Unicode( 10 ) )
    revision = Column( Integer, default = 0 )
    rpt = Column( Unicode( 100 ) )  # kevin add
    project_owner = Column( Unicode( 100 ) )  # kevin add
#    history = Column(Unicode(500))
    percentage = Column( Float, default = 0 )

    _new_or_update = Column( 'new_or_update', Unicode( 500 ), doc = 'new or update' )

    combine_to_id = Column( Integer, default = None )
    cowork_team_id = Column( Integer, ForeignKey( 'sample_team.id' ), doc = 'Access Rights' )
    cowork_team = relation( Team, primaryjoin = cowork_team_id == Team.id )

    def get_new_or_update( self ):
        if self._new_or_update is None : return []
        return self._new_or_update.split( "|" )
#        return (self._new_or_update or "").split("|")

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
#        try:
#            return list(itertools.chain(*map(m, map(k, self.getChildren()))))
#        except:
#            traceback.print_exc()
#            return []

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
            return DBSession.query( Job ).filter( and_( Job.active == 0, Job.main_form_id == self.id ) ).all()
        except Exception, e:
            log.exception( str( e ) )
            return []

    def update( self, **kw ):
        old_object = self.serialize()
        old_object_status = self.status

        for key, dbobj in [( "project_own", Region ), ( "team", Team ), ( "customer", Customer ), ( "program", Program ), ( "request_team", Team ),
                          ( "project", Project ), ( "item_category", ItemCategory ), ( "cowork_team", Team )]:
            if key in kw :
                val = DBSession.query( dbobj ).get( kw[key] ) if kw[key] else None
                setattr( self, key, val )

        for key in ["contact_person", "reference_code", "item_description", "item_code", "project_owner", "request_contact_number", 'group_no']:
            if key in kw :
                val = kw[key].strip() if kw[key] else None
                setattr( self, key, val )

        if "cc_to" in kw: self.cc_to = ( kw["cc_to"] or '' ).replace( "\n", '' )

        self.child_form = kw.get( "form_ids" )
        # add the update log
        if old_object_status != DRAFT:
            self.revision += 1
        # if update from draft and save to status: new
        if old_object_status == DRAFT and not kw['is_draft']:
            self.status = NEW_REQUEST
        new_object = self.serialize( False )

        new_object['cowork_team_id'] = ( kw['cowork_team'], 'Access Rights' )  # to fix the cowork_team not log down problem.

        check_log = MainForm.compareObject( old_object, new_object )

        log_str = []
        for ( key, old_val, new_val ) in check_log['update']:
            log_str.append( "Change [%s] from '%s' to '%s' " % ( key, old_val, new_val ) )
        for ( key, new_val ) in check_log['new']:
            log_str.append( "New [%s] '%s' " % ( key, new_val ) )
        if log_str and old_object_status != DRAFT: DBSession.add( DevelopmentLog( system_no = str( self ), main_form_id = self.id, sub_form_id = None, sub_form_type = None, action_type = 'UPDATE', remark = " .\n".join( log_str ) ) )



    @classmethod
    def create( cls, **kw ):
        requiredFields = ["project_own", "contact_person", "team", "program", "project", "project_own"]
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
                  "item_category" : DBSession.query( ItemCategory ).get( kw["item_category"] ) if kw.get( "item_category", False ) else None,
                  "program" : DBSession.query( Program ).get( kw["program"] ) if kw.get( "program", False ) else None,
                  "project" : DBSession.query( Project ).get( kw["project"] ) if kw.get( "project", False ) else None,
                  "project_own" : DBSession.query( Region ).get( kw["project_own"] ) if kw.get( "project_own", False ) else None,
                  "request_team" : DBSession.query( Team ).get( kw["request_team"] ) if kw.get( "request_team", None ) else None,
                  "project_owner" : kw.get( "project_owner", None ),
                  "rpt" : kw.get( "rpt", None ) or None,
                  "cc_to" : kw.get( "cc_to", None ) or None,
                  "status": DRAFT if is_draft else NEW_REQUEST,
                  "cowork_team" : DBSession.query( Team ).get( kw["cowork_team"] ) if kw.get( "cowork_team", None ) else None,
                  'group_no': kw.get( 'group_no', 0 )}
        if hParam['cc_to'] : hParam['cc_to'] = hParam['cc_to'].strip().replace( "\n", '' )

        hParam["request_type"] = "New"

        def _getSystemNo( regionCode, teamShortName ):
            c = DBSession.query( MainForm ).count()
            if teamShortName :
                return "PD-%s-%s-%.6d" % ( regionCode, teamShortName, c + 1 )
            else:
                return "PD-%s-%.6d" % ( regionCode, c + 1 )

        hParam["system_no"] = _getSystemNo( hParam["project_own"].code, hParam["team"].short_name )
        h = MainForm( **hParam )
        DBSession.add( h )
        return h



class SFTarget( DeclarativeBase, EasyMixin, SysMixin, FormMixin ):
    __tablename__ = 'sample_sub_form_target'

    id = Column( Integer, primary_key = True )
    main_id = Column( Integer, ForeignKey( 'sample_main_form.id' ) )
    main = relation( MainForm )

    dept_id = Column( Text, doc = 'Dept#' )
    promo_id = Column( Text )
    dpci = Column( Text, doc = 'DPCI#' )
    packaging_style = Column( Text, doc = 'Packaging Style' )
    vendor_style = Column( Text, doc = 'Vendor Style#' )
    spg = Column( Text, doc = 'SPG#' )
    dimension = Column( Text, doc = 'Dimension/Size' )

    insert = Column( CheckBoxCol( 99 ), doc = 'Insert' )
    material = Column( CheckBoxCol( 99 ), doc = 'Material' )
    material_other = Column( JSONCol( 1000 ), doc = 'Material other content' )

    submitted_item = Column( CheckBoxCol( 99 ) )  # kevin add
    submitted_item_other = Column( Text, doc = 'Submitted item other content' )

    file_from = Column( CheckBoxCol( 99 ), doc = 'Artwork File From' )
    file_from_ftp_location = Column( Text, doc = 'Artwork File From Ftp Location' )
    file_from_files_location = Column( Text, doc = 'Artwork File From Files Location' )

    factory_code = Column( Unicode( 99 ), doc = 'Artwork Info-Factory Code(Artwork)' )
    size_w = Column( Text, doc = 'Artwork attachment size width' )
    size_h = Column( Text, doc = 'Artwork attachment size height' )
    size_unit = Column( CheckBoxCol( 99 ), doc = 'Artwork attachment size unit' )
    color = Column( CheckBoxCol( 99 ), doc = 'Artwork attachment color' )
    color_spot_content = Column( Text, doc = 'Artwork attachment spot color content' )
    color_other_content = Column( Text, doc = 'Artwork attachment other color content' )

    die = Column( CheckBoxCol( 99 ), doc = 'Requirements die line' )  # kevin add
    file_format = Column( CheckBoxCol( 99 ), doc = 'Requirements die line for production' )
    target_format = Column( CheckBoxCol( 99 ), doc = 'Requirements die line for production with target format' )
    file_protection = Column( CheckBoxCol( 99 ), doc = 'Requirements die line for production security file protection' )

    expected_date = Column( DateTime )
    remark = Column( Text )
#    target_vendor_id = Column(Integer, doc='Vendor Name')
#    product_name = Column(Unicode(200))
#    material_other = Column(Unicode(100), doc='Material other content')
#    submitted_item = Column(Unicode(50))
#    requirement = Column(CheckBoxCol(100))
#    requirement_other = Column(Unicode(100), doc='Requirement other content')
#    sample = Column(Unicode(50), doc='Requirements sample')
#    sample_qty = Column(Integer, doc='Requirements sample quality')
#    sketch = Column(Unicode(5000), )

    @classmethod
    def _refineValue( cls, kw, prefix, actionType ):
        kw = super( SFTarget, cls )._refineValue( kw, prefix, actionType )
        needApprove = False
        # weber: super do it, except qty validation
#        intFields = ["sample_qty", ]
#        for f in intFields:
#            key = "%s%s" % (prefix, f)
#            if kw.get(key, None):
#                if actionType == "NEW" and kw[key] > 5: needApprove = True
            # key = "%s%s" % (prefix, f)
            # if kw.get(key, None):
            #    kw[key] = int(kw[key])
            #    if actionType == "NEW" and kw[key] > 5: needApprove = True
            # elif key in kw:  kw[key] = None

        material_other_key = ( "%s%s" ) % ( prefix, 'material_other' )
        if material_other_key in kw and kw[material_other_key]:
            kw[material_other_key] = json.loads( kw[material_other_key] )

        if actionType == "NEW" and needApprove: kw["%sstatus" % prefix] = WAIT_FOR_APPROVAL

        return kw
#
#    def why_need_approve(self):
#        if self.sample_qty > 5 :
#            return '[%s]No. of sampling: %s' % (self.getWidget().label, self.sample_qty)
#        else:
#            return None


class SFAvon( DeclarativeBase, EasyMixin, SysMixin, FormMixin ):
    __tablename__ = 'sample_sub_form_avon'

    id = Column( Integer, primary_key = True )
    main_id = Column( Integer, ForeignKey( 'sample_main_form.id' ) )
    main = relation( MainForm )

    pp_no = Column( Text, doc = 'PP#' )
    category = Column( CheckBoxCol( 99 ), doc = 'Design Category' )
    sample = Column( CheckBoxCol( 99 ), doc = 'Submitted items Sample Reference' )
    artwork = Column( CheckBoxCol( 99 ), doc = 'Submitted items Artworks' )
    dimension_type = Column( CheckBoxCol( 99 ), doc = 'Dimension Type' )

    product_width = Column( Text, doc = 'Product Dimension width' )
    product_depth = Column( Text, doc = 'Product Dimension depth' )
    product_height = Column( Text, doc = 'Product Dimension height' )
    product_unit = Column( CheckBoxCol( 99 ), doc = 'Product Dimension unit' )
    product_as_sample = Column( CheckBoxCol( 99 ), doc = 'Product Dimension as sample' )

    dimension_width = Column( Text, doc = 'Styrofoam Dimension width' )
    dimension_depth = Column( Text, doc = 'Styrofoam Dimension depth' )
    dimension_height = Column( Text, doc = 'Styrofoam Dimension height' )
    dimension_unit = Column( CheckBoxCol( 99 ), doc = 'Styrofoam Dimension unit' )
    dimension_as_sample = Column( CheckBoxCol( 99 ), doc = 'Styrofoam Dimension as sample' )

    box_width = Column( Text, doc = 'Box Dimension width' )
    box_depth = Column( Text, doc = 'Box Dimension depth' )
    box_height = Column( Text, doc = 'Box Dimension height' )
    box_unit = Column( CheckBoxCol( 99 ), doc = 'Box Dimension unit' )
    box_as_sample = Column( CheckBoxCol( 99 ), doc = 'Box Dimension  as sample' )
    box_size = Column( CheckBoxCol( 99 ), doc = 'Box Dimension size type' )

    product_weight = Column( Text, doc = 'Product Weight' )
    product_weight_unit = Column( Unicode( 49 ), doc = 'Product Weight unit' )
    product_weight_as_sample = Column( CheckBoxCol( 99 ), doc = 'Product Weight as sample' )

    top = Column( CheckBoxCol( 99 ), doc = 'Top & Bottom Closure type' )
    top_other = Column( Text, doc = 'Top & Bottom Closure other content' )

    mp_width = Column( Text, doc = 'Specified MP size width' )
    mp_depth = Column( Text, doc = 'Specified MP size depth' )
    mp_height = Column( Text, doc = 'Specified MP size height' )
    mp_size = Column( CheckBoxCol( 99 ), doc = 'Specified MP size type' )
    mp_unit = Column( CheckBoxCol( 99 ), doc = 'Specified MP size unit' )

    quantity = Column( CheckBoxCol( 99 ), doc = 'MP quantity' )
    quantity_pcs = Column( MultiTextCol, doc = 'MP Fixed Quantity' )

    country = Column( CheckBoxCol( 99 ) )
    country_other = Column( Text, doc = 'MP Country other content' )

    product = Column( CheckBoxCol( 99 ), doc = 'Product Orientation' )
    design_criteria = Column( CheckBoxCol( 99 ) )

    artwork_file_from = Column( CheckBoxCol( 99 ), doc = 'Files from' )
    artwork_file_from_ftp_location = Column( Text, doc = 'Files from FTP Location' )
    artwork_file_from_files_location = Column( Text, doc = 'Files from Files Location' )

    artwork_factory_code = Column( Unicode( 49 ), doc = 'Artwork Info-Factory Code(Artwork)' )
    artwork_size_w = Column( Text, doc = 'Artwork Info-Size Width' )
    artwork_size_h = Column( Text, doc = 'Artwork Info-Size Height' )
    artwork_size_unit = Column( CheckBoxCol( 99 ), doc = 'Artwork Info-Size Unit' )
    artwork_color = Column( CheckBoxCol( 99 ), doc = 'Artwork Info-Color' )
    artwork_color_spot_content = Column( MultiTextCol, doc = 'Artwork Info-No. of spot color' )
    artwork_color_other_content = Column( Text, doc = 'Artwork Info-Color-Other' )

    artwork_output = Column( CheckBoxCol( 99 ), doc = 'Output' )
    artwork_protection = Column( CheckBoxCol( 99 ), doc = 'Security File Protction' )
    artwork_output_other_content = Column( Text, doc = 'Output-Other' )

    label_size_w = Column( Text, doc = 'Label Info size width' )
    label_size_h = Column( Text, doc = 'Label Info size height' )
    label_size_unit = Column( CheckBoxCol( 99 ), doc = 'Label Info size unit' )

    label_material = Column( Text, doc = 'Label Info material' )
    label_country = Column( Text, doc = 'Label Info country' )
    label_item_code = Column( Text, doc = 'Label Info item code' )
    label_item_name = Column( Text, doc = 'Label Info item name' )
    label_barcode = Column( Unicode( 49 ), doc = 'Label Info barcode' )
    label_font = Column( Text, doc = 'Label Info font' )
    label_content_color = Column( Text, doc = 'Label Info content color' )
    label_color = Column( CheckBoxCol( 99 ), doc = 'Label Info color' )
    label_color_other = Column( Text, doc = 'Label Info color other' )

    remark = Column( Text, doc = 'remark' )
    expected_date = Column( DateTime )
    material_widgets = Column( JSONCol( 10000 ), doc = "Material" )

#    material_type = Column(Unicode(20))
#    folding_cards_type = Column(Unicode(20), doc='Material Folding Cards type')
#    folding_cards_other = Column(Unicode(100), doc='Material Folding Cards Other Content')
#    paper_thickness_type = Column(Unicode(20), doc='Material Folding Cards Paper thickness')
#    paper_thickness_unit = Column(Unicode(5), doc='Material Folding Cards Paper thickness unit')
#    gramage_gsm = Column(Unicode(10), doc='Material Folding Cards Gramage')
#    flute = Column(Unicode(20), doc='Material Corrugated type')
#    flute_type = Column(Unicode(20), doc='Material Corrugated flute')
#    flute_type_gsm = Column(Unicode(10), doc='Material Corrugated CCNB Top gsm')
#    bursting = Column(Unicode(10), doc='Material Corrugated Specification Bursting')
#    ect = Column(Unicode(10), doc='Material Corrugated Specification ECT')
#    gramage = Column(Unicode(10), doc='Material Corrugated Specification Gramage')
#    material_provided = Column(Unicode(50))
#    material_type_other_content = Column(Unicode(50))
#    white_box = Column(Unicode(5), doc='White-Box Sample Required')
#    white_box_qty = Column(Integer, doc='White-Box Sample Required pcs')
#    material_type_content = Column(Unicode(100)) #kevin add
#    urgency = Column(Unicode(20), )
#    urgency_request = Column(Unicode(500))

    @classmethod
    def _refineValue( cls, kw, prefix, actionType ):
        kw = super( SFAvon, cls )._refineValue( kw, prefix, actionType )
        needApproval = False
        # weber: super do it, except pcs validation
#        fs = ["white_box_qty","quantity_pcs" ]
        # fs = ["quantity_pcs",]
        # for f in fs:
        #    key = "%s%s" % (prefix, f)
        #    if kw.get(key, None):
        #        if actionType == "NEW" and kw[key] > 5: needApproval = True
            # key = "%s%s" % (prefix, f)
            # if kw.get(key, None):
            #    kw[key] = int(kw[key])
            #    if actionType == "NEW" and kw[key] > 5: needApproval = True
            # elif key in kw:  kw[key] = None
#
#        column = '%squantity_pcs' % prefix
#        if kw.has_key(column) and type(kw[column]) == list:
#            kw[column] = ','.join(kw[column])
#
#        column = '%artwork_color_spot_content' % prefix
#        if kw.has_key(column) and type(kw[column]) == list:
#            kw[column] = ','.join(kw[column])
#
        # for the material_widgets
        material_widgets_key = ( "%s%s" ) % ( prefix, 'material_widgets' )
        if material_widgets_key in kw and kw[material_widgets_key]:
            kw[material_widgets_key] = json.loads( kw[material_widgets_key] )

        if actionType == "NEW" and needApproval:
            kw["%sstatus" % prefix] = WAIT_FOR_APPROVAL

        return kw

#    def why_need_approve(self):
#        if self.white_box_qty > 5 :
#            return '[%s]No. of sampling: %d' % (self.getWidget().label, self.white_box_qty)
#        else:
#            return None


class SFBestBuy( DeclarativeBase, EasyMixin, SysMixin, FormMixin ):
    __tablename__ = 'sample_sub_form_bestbuy'

    id = Column( Integer, primary_key = True )
    main_id = Column( Integer, ForeignKey( 'sample_main_form.id' ) )
    main = relation( MainForm )

    job_purpose = Column( CheckBoxCol( 99 ), doc = 'job purpose' )
    job_presentation = Column( CheckBoxCol( 99 ), doc = 'job presentation' )

    submit_items = Column( CheckBoxCol( 99 ), doc = 'Submitted Items' )
    submit_items_other = Column( Text, doc = 'Submitted Items Other Content' )

    size_w = Column( Text, doc = 'Product and packaging details size width' )
    size_d = Column( Text, doc = 'Product and packaging details size depth' )
    size_h = Column( Text, doc = 'Product and packaging details size height' )
    size_unit = Column( CheckBoxCol( 99 ), doc = 'Product and packaging details size unit' )
    size_type = Column( CheckBoxCol( 99 ), doc = 'Product and packaging details size type' )
    size_as_sample = Column( CheckBoxCol( 99 ), doc = 'Product and packaging details size as sample' )

    weight = Column( Text, doc = 'Packaging Weight' )
    weight_unit = Column( Unicode( 49 ), doc = 'Packaging Weight unit' )
    weight_as_sample = Column( CheckBoxCol( 99 ), doc = 'Packaging Weight as sample' )

    material = Column( JSONCol( 1000 ), doc = 'Packaging Material' )
    material_as_sample = Column( CheckBoxCol( 99 ), doc = 'Packaging Material as sample' )

    material_type = Column( CheckBoxCol( 999 ), doc = 'Packaging Material type' )
    window_size_w = Column( Text, doc = 'Packaging Style Window Box size width' )
    window_size_d = Column( Text, doc = 'Packaging Style Window Box size depth' )
    window_size_unit = Column( CheckBoxCol( 99 ), doc = 'Packaging Style Window Box size unit' )
    material_other = Column( Text, doc = 'Packaging Material other' )

    requirement = Column( CheckBoxCol( 99 ), doc = 'Requirements' )

    expected_date = Column( DateTime )
    remark = Column( Text )

#    material = Column(Unicode(100), doc='Packaging Material')
#    window_size=Column(Unicode(100))
#    job_type = Column(CheckBoxCol(500), doc='Job type')
#    job_type_other = Column(Unicode(100), doc='Job type other')
#    job_type_sampling = Column(Unicode(100))
#    job_type_printout = Column(Unicode(100))
    @classmethod
    def _refineValue( cls, kw, prefix, actionType ):
        kw = super( SFBestBuy, cls )._refineValue( kw, prefix, actionType )
        material_key = ( "%s%s" ) % ( prefix, 'material' )
        if material_key in kw and kw[material_key]:
            kw[material_key] = json.loads( kw[material_key] )
        return kw

class SFBox( DeclarativeBase, EasyMixin, SysMixin, FormMixin ):
    __tablename__ = 'sample_sub_form_box'

    id = Column( Integer, primary_key = True )
    main_id = Column( Integer, ForeignKey( 'sample_main_form.id' ) )
    main = relation( MainForm )

    job_perpose = Column( CheckBoxCol( 99 ), doc = 'Job Purpose' )
    presentation = Column( CheckBoxCol( 99 ), doc = 'Presentation' )

    product_or_box = Column( CheckBoxCol( 99 ), doc = 'Product Details as sample' )
    product_w = Column( Text, doc = 'Product Details Product width' )
    product_d = Column( Text, doc = 'Product Details Product depth' )
    product_h = Column( Text, doc = 'Product Details Product height' )
    product_unit = Column( CheckBoxCol( 99 ), doc = 'Product Details Product unit' )

    product_weight = Column( Text, doc = 'Product Details weight' )
    product_weight_unit = Column( Unicode( 49 ), doc = 'Product Details unit' )

    box_w = Column( Text, doc = 'Product Details box width' )
    box_d = Column( Text, doc = 'Product Details box depth' )
    box_h = Column( Text, doc = 'Product Details box height' )
    box_unit = Column( CheckBoxCol( 99 ), doc = 'Product Details box unit' )
    box_size = Column( CheckBoxCol( 99 ), doc = 'Product Details box size' )

    top_closure = Column( CheckBoxCol( 99 ), doc = 'Box Style top closure' )
    top_closure_other = Column( Text, doc = 'Box Style top closure other content' )
    top_locking = Column( CheckBoxCol( 99 ), doc = 'Box Style top locking' )
    top_locking_other = Column( Text, doc = 'Box Style top locking other content' )
    bottom_closure = Column( CheckBoxCol( 99 ), doc = 'Box Style bottom closure' )
    bottom_closure_other = Column( Text, doc = 'Box Style bottom closure other content' )
    bottom_locking = Column( CheckBoxCol( 99 ), doc = 'Box Style bottom locking' )
    bottom_locking_other = Column( Text, doc = 'Box Style bottom locking other content' )

    insert = Column( CheckBoxCol( 99 ), doc = 'Box Style insert' )
    insert_material = Column( JSONCol( 1000 ), doc = "Insert Material" )

    loading = Column( CheckBoxCol( 99 ), doc = 'Box Style material loading' )
    window_type = Column( CheckBoxCol( 99 ), doc = 'Box Style material window' )
    window_with = Column( CheckBoxCol( 99 ), doc = 'Box Style material window width' )
    pvc_thickness = Column( Text, doc = 'Box Style pvc thickness' )
    pet_thickness = Column( Text, doc = 'Box Style pet thickness' )
    pp_thickness = Column( Text, doc = 'Box Style pp thickness' )
    window_with_other_content = Column( Text, doc = 'Box Style window other content' )
    window_with_other_unit = Column( Text, doc = 'Box Style window other content unit' )
    window_size_w = Column( Text, doc = 'Box Style window size width' )
    window_size_h = Column( Text, doc = 'Box Style window size height' )
    window_size_unit = Column( CheckBoxCol( 99 ), doc = 'Box Style window size unit' )
    suggested_by_pd_team = Column( CheckBoxCol( 99 ), doc = 'Box Style suggested by PD Team' )

    remark = Column( Text, doc = 'remark ' )
    expected_date = Column( DateTime, doc = 'expected date' )

    material_widgets = Column( JSONCol( 10000 ), doc = "Material" )

#    product_weight_as_sample = Column(Unicode(5), doc='Product Details as sample')
#    material_type = Column(Unicode(20), doc='Material')
#    folding_cards_type = Column(Unicode(20), doc='Material Folding Cards')
#    folding_cards_other = Column(Unicode(100), doc='Material Folding Cards other')
#    paper_thickness_type = Column(Unicode(20), doc='Material Paper thickness')
#    paper_thickness_unit = Column(Unicode(5), doc='Material Paper thickness unit')
#    gramage_gsm = Column(Unicode(10), doc='Material gramage')
#    flute = Column(Unicode(20), doc='Material Corrugated fluth')
#    flute_type = Column(Unicode(20), doc='Material Corrugated fluth type')
#    flute_type_gsm = Column(Unicode(10), doc='Material Corrugated fluth gsm')
#    bursting = Column(Unicode(10), doc='Material Corrugated bursting')
#    ect = Column(Unicode(10), doc='Material Corrugated etc')
#    gramage = Column(Unicode(10), doc='Material Corrugated gramage')
#    material_provided = Column(Unicode(50), doc='Material provided')
#    material_type_other_content = Column(Unicode(50), doc='Material other content')
#    insert_material = Column(Unicode(20), doc='Box Style insert material')

    @classmethod
    def _refineValue( cls, kw, prefix, actionType ):
        kw = super( SFBox, cls )._refineValue( kw, prefix, actionType )
        # for the material_widgets
#        material_widgets_key = ("%s%s") % (prefix,'material_widgets')
#        if material_widgets_key in kw and kw[material_widgets_key]:
#            kw[material_widgets_key] = json.loads(kw[material_widgets_key])

        json_mapping = {
                        'material_widgets_key' : ( "%s%s" ) % ( prefix, 'material_widgets' ),
                        'insert_material_key'  : ( "%s%s" ) % ( prefix, 'insert_material' ),
                        }
        for v in json_mapping.values():
            if v in kw and kw[v]:
                kw[v] = json.loads( kw[v] )
        return kw

class SFTray( DeclarativeBase, EasyMixin, SysMixin, FormMixin ):
    __tablename__ = 'sample_sub_form_tray'

    id = Column( Integer, primary_key = True )
    main_id = Column( Integer, ForeignKey( 'sample_main_form.id' ) )
    main = relation( MainForm )

    job_purpose = Column( CheckBoxCol( 99 ), doc = 'job purpose' )
    presentation = Column( CheckBoxCol( 99 ), doc = 'presentation' )

    product_dimension_type = Column( CheckBoxCol( 99 ), doc = 'Product Details' )
    product_dimension_option_text = Column( Text, doc = 'Refer to Packaging Option' )  # new added by CL on 2014/05/26
    product_dimension_w = Column( Text, doc = 'Product Details product dimension width' )
    product_dimension_d = Column( Text, doc = 'Product Details product dimension depth' )
    product_dimension_h = Column( Text, doc = 'Product Details product dimension height' )
    product_dimension_unit = Column( CheckBoxCol( 99 ), doc = 'Product Details product dimension unit' )
    product_dimension_as_sample = Column( CheckBoxCol( 99 ), doc = 'product dimension as sample' )
    weight = Column( Text, doc = 'Product Details product dimension weight' )
    weight_unit = Column( Unicode( 49 ), doc = 'Product Details product dimension weight unit' )
    product_weight_as_sample = Column( CheckBoxCol( 99 ), doc = 'product weight as sample' )

    product_tray_size = Column( CheckBoxCol( 99 ), doc = 'Product Details product dimension size' )
    tray_dimension_w = Column( Text, doc = 'Tray Size dimension width' )
    tray_dimension_d = Column( Text, doc = 'Tray Size dimension depth' )
    tray_dimension_bh = Column( Text, doc = 'Tray Size dimension DH' )
    tray_dimension_fh = Column( Text, doc = 'Tray Size dimension FH' )
    tray_size_unit = Column( CheckBoxCol( 99 ), doc = 'Tray Size  unit' )
    box_size = Column( CheckBoxCol( 99 ), doc = 'box size' )
    tray_pack_left = Column( Text, doc = 'Tray Size pcs left to right' )
    tray_pack_front = Column( Text, doc = 'Tray Size pcs front to back' )
    tray_pack_top = Column( Text, doc = 'Tray Size pcs top to bottom' )

    stackable = Column( CheckBoxCol( 99 ), doc = 'stackable' )
    style = Column( CheckBoxCol( 99 ), doc = 'style' )
    tray_detail = Column( CheckBoxCol( 99 ), doc = 'tray detail' )
    tray_detail_pcs = Column( Integer, doc = 'tray detail pcs' )
    tray_detail_hook_qty = Column( Text, doc = 'Tray Style Details Hooks pcs' )
    tray_detail_thickness = Column( Text, doc = 'tray detail thickness' )
    tray_detail_thickness_unit = Column( CheckBoxCol( 99 ), doc = 'Tray Size thickness unit' )
    shipper = Column( CheckBoxCol( 99 ), doc = 'shipper' )
    shipper_other_content = Column( Text, doc = 'shipper other content' )
    shipper_loading = Column( CheckBoxCol( 99 ), doc = 'Tray Style Shipper Loading' )

    remark = Column( Text, doc = 'remark' )
    expected_date = Column( DateTime, doc = 'expected date' )

    material_widgets = Column( JSONCol( 10000 ), doc = "Material" )
#    tray_size_type = Column(Unicode(50), doc='Tray Size')
#    other = Column(Unicode(100), doc='other content')

#    tray_dimension_fh=Column(Float)

#    material = Column(Unicode(20), doc='material')
#    material_type = Column(Unicode(20), doc='material folding cards')
#    material_other = Column(Unicode(100), doc='material folding cards other content')
#    paper_thickness_type = Column(Unicode(20), doc='material folding cards paper thickness type')
#    paper_thickness_unit = Column(Unicode(5), doc='material folding cards paper thickness unit')
#    gramages = Column(Unicode(10), doc='material folding cards gramages')
#    specification_burst = Column(CheckBoxCol(100), doc='material Corrugated specification burst')

#    flute = Column(Unicode(20), doc='Material corrugated fluth')
#    flute_type = Column(Unicode(20), doc='Material corrugated fluth type')
#    flute_type_gsm = Column(Unicode(10), doc='Material corrugated fluth gsm')
#    bursting = Column(Unicode(10), doc='Material corrugated fluth bursting')
#    ect = Column(Unicode(10), doc='Material corrugated fluth bursting etc')
#    material_type_content = Column(Unicode(100), doc='material type content')
#    material_type_other_content = Column(Unicode(100), doc='material type other content')

    @classmethod
    def _refineValue( cls, kw, prefix, actionType ):
        kw = super( SFTray, cls )._refineValue( kw, prefix, actionType )
        # weber: super do it
        # intFields = ["tray_detail_pcs", ]
        # for f in intFields:
        #    key = "%s%s" % (prefix, f)
        #    if kw.get(key, None): kw[key] = int(kw[key])
        #    elif key in kw:  kw[key] = None
        # for the material_widgets
        material_widgets_key = ( "%s%s" ) % ( prefix, 'material_widgets' )
        if material_widgets_key in kw and kw[material_widgets_key]:
            kw[material_widgets_key] = json.loads( kw[material_widgets_key] )
        return kw

class SFFloor( DeclarativeBase, EasyMixin, SysMixin, FormMixin ):
    __tablename__ = 'sample_sub_form_floor'

    id = Column( Integer, primary_key = True )
    main_id = Column( Integer, ForeignKey( 'sample_main_form.id' ) )
    main = relation( MainForm )

    job_purpose = Column( CheckBoxCol( 99 ), doc = 'job purpose' )
    presentation = Column( CheckBoxCol( 99 ), doc = 'presentation' )
    diagram_for_approval = Column( CheckBoxCol( 99 ), doc = 'diagram for approval' )

    dimension_type = Column( CheckBoxCol( 99 ), doc = 'Product Details type' )
    dimension_type_option_text = Column( Text, doc = 'Refer to Packaging Option' )
    dimension_w = Column( Text, doc = 'Product Details width' )
    dimension_d = Column( Text, doc = 'Product Details depth' )
    dimension_h = Column( Text, doc = 'Product Details height' )
    dimension_unit = Column( CheckBoxCol( 99 ), doc = 'Product Details unit' )
    dimension_as_sample = Column( CheckBoxCol( 99 ), doc = 'Product Details as sample' )
    weight = Column( Text, doc = 'Product Details weight' )
    weight_unit = Column( Unicode( 49 ), doc = 'Product Details weight unit' )
    weight_as_sample = Column( CheckBoxCol( 99 ), doc = 'Product Details weight as sample' )

    pallet_size = Column( CheckBoxCol( 99 ), doc = 'Display Size' )
    full_pallet = Column( CheckBoxCol( 99 ), doc = 'Display Size full pallet' )
    full_pallet_height_limit = Column( Text, doc = 'Display Size full pallet height limit' )
    full_pallet_height_limit_unit = Column( CheckBoxCol( 99 ), doc = 'Display Size full pallet height limit unit' )
    half_pallet = Column( CheckBoxCol( 99 ), doc = 'Display Size half pallet' )
    half_pallet_height_limit = Column( Text, doc = 'Display Size half pallet height limit' )
    half_pallet_height_limit_unit = Column( CheckBoxCol( 99 ), doc = 'Display Size half pallet height limit unit' )
    display_pack_left = Column( Text, doc = 'Display Size display pack left' )
    display_pack_front = Column( Text, doc = 'Display Size display pack front' )
    display_pack_top = Column( Text, doc = 'Display Size display pack top' )
    other_size_w = Column( Text, doc = 'Display Size other size weight' )
    other_size_d = Column( Text, doc = 'Display Size other size depth' )
    other_size_h = Column( Text, doc = 'Display Size other size height' )
    other_size_unit = Column( CheckBoxCol( 99 ), doc = 'Display Size other size unit' )

    front_lip_height = Column( Text, doc = 'Pallet Size front lip height' )
    front_lip_unit = Column( CheckBoxCol( 99 ), doc = 'Pallet Size front lip unit' )
    shelves_left = Column( Text, doc = 'Display Size shelves left' )
    shelves_top = Column( Text, doc = 'Display Size shelves top' )
    pack_left = Column( Text, doc = 'Display Size pack left' )
    pack_front = Column( Text, doc = 'Display Size pack front' )
    top_to_bottom = Column( Text, doc = 'Pallet Size top to bottom' )

    style = Column( CheckBoxCol( 99 ), doc = 'Pallet Style ' )
    facing = Column( CheckBoxCol( 99 ), doc = 'Pallet Style facing' )
    facing_other = Column( Text, doc = 'Pallet Style facing other' )
    detail_type = Column( CheckBoxCol( 99 ), doc = 'Pallet Style detail type' )
    detail_height = Column( Text, doc = 'Pallet Style detail height' )
    detail_height_unit = Column( CheckBoxCol( 99 ), doc = 'Pallet Style detail height unit' )
    detail_type_hook_qty = Column( Text, doc = 'Pallet Style detail hook qty' )
    detail_type_other_content = Column( Text, doc = 'Pallet Style detail type other content' )
    shipper_type1 = Column( CheckBoxCol( 99 ), doc = 'Pallet Style shipper type1' )
    shipper_type2 = Column( CheckBoxCol( 99 ), doc = 'Pallet Style shipper type2' )
    transit = Column( CheckBoxCol( 99 ), doc = 'Pallet Style transit' )

    remark = Column( Text, doc = 'remark' )
    expected_date = Column( DateTime, doc = 'expected date' )

    material_widgets = Column( JSONCol( 10000 ), doc = "Material" )
#    othter_style = Column(Unicode(100), doc='Pallet Style other')

#    other_size_bh = Column(Text, doc='Display Size other size bh')
#    other_size_fh = Column(Text, doc='Display Size other size fh')

#    material_type = Column(Unicode(20), doc='Material')
#    folding_cards_type = Column(Unicode(20), doc='Material folding cards type')
#    folding_cards_other = Column(Unicode(100), doc='Material folding cards other content')
#    paper_thickness_type = Column(Unicode(20), doc='Material paper thickness type')
#    paper_thickness_unit = Column(Unicode(5), doc='Material paper thickness unit')
#    gramage_gsm = Column(Unicode(10), doc='Material gramage gsm')
#    flute = Column(Unicode(20), doc='Material flute')
#    flute_type = Column(Unicode(20), doc='Material flute type')
#    flute_type_gsm = Column(Unicode(10), doc='Material flute type gsm')
#    bursting = Column(Unicode(10), doc='Material bursting')
#    ect = Column(Unicode(10), doc='Material etc')
#    gramage = Column(Unicode(10), doc='Material gramage')
#    material_provided = Column(Unicode(50), doc='Material provided')
#    material_type_other_content = Column(Unicode(50), doc='Material type other content')
#    flute_type_gsm_gsm = Column(Unicode(50), doc='Pallet Size flute_ ype gsm')

    @classmethod
    def _refineValue( cls, kw, prefix, actionType ):
        kw = super( SFFloor, cls )._refineValue( kw, prefix, actionType )
        # for the material_widgets
        material_widgets_key = ( "%s%s" ) % ( prefix, 'material_widgets' )
        if material_widgets_key in kw and kw[material_widgets_key]:
            kw[material_widgets_key] = json.loads( kw[material_widgets_key] )
        return kw


class SFGeneral( DeclarativeBase, EasyMixin, SysMixin, FormMixin ):
    __tablename__ = 'sample_sub_form_general'

    id = Column( Integer, primary_key = True )
    main_id = Column( Integer, ForeignKey( 'sample_main_form.id' ) )
    main = relation( MainForm )

    job_purpose = Column( CheckBoxCol( 99 ), doc = 'job purpose' )
    job_presentation = Column( CheckBoxCol( 99 ), doc = 'job presentation' )

    size_w = Column( UnicodeText, doc = 'Product Details size width' )
    size_d = Column( UnicodeText, doc = 'Product Details size depth' )
    size_h = Column( UnicodeText, doc = 'Product Details size height' )
    size_unit = Column( CheckBoxCol( 99 ), doc = 'Product Details size unit' )
    size_type = Column( CheckBoxCol( 99 ), doc = 'Product Details size' )
    size_as_sample = Column( CheckBoxCol( 99 ), doc = 'Product Details size as sample' )
    weight = Column( UnicodeText, doc = 'Product Details product width' )
    weight_unit = Column( Unicode( 49 ), doc = 'Product Details product width unit' )
    weight_as_sample = Column( CheckBoxCol( 99 ), doc = 'Product Details product weight as sample' )

    submit_item = Column( CheckBoxCol( 99 ), doc = 'Submitted Items' )
    submit_item_other = Column( UnicodeText, doc = 'Submitted Items other content' )

    item_type = Column( CheckBoxCol( 99 ), doc = 'item type' )
    item_type_other = Column( UnicodeText, doc = 'item type other content' )

    remark = Column( UnicodeText, doc = 'remark' )
    expected_date = Column( DateTime, doc = 'expected date' )
    material_widgets = Column( JSONCol( 10000 ), doc = "Material" )
#    material_type = Column(Unicode(20), doc='Material')
#    folding_cards_type = Column(Unicode(20), doc='Material folding cards type')
#    folding_cards_other = Column(Unicode(100), doc='Material folding cards other content')
#    paper_thickness_type = Column(Unicode(20), doc='Material paper thickness type')
#    paper_thickness_unit = Column(Unicode(5), doc='Material paper thickness unit')
#    gramage_gsm = Column(Unicode(100), doc='Material gramage gsm')
#    flute = Column(Unicode(100), doc='Material fluth')
#    flute_type = Column(Unicode(20), doc='Material fluth type')
#    flute_type_gsm = Column(Unicode(100), doc='Material type gsm')
#    bursting = Column(Unicode(100), doc='Material bursting')
#    ect = Column(Unicode(100), doc='Material etc')
#    gramage = Column(Unicode(100), doc='Material  gramage')
#    material_provided = Column(Unicode(50), doc='Material provided')
#    material_type_other_content = Column(Unicode(50), doc='Material folding card other content')
    # material = Column(Unicode(100))
    # material_sample = Column(Unicode(5))
    # material_type_content = Column(Unicode(100)) #kevin add

    @classmethod
    def _refineValue( cls, kw, prefix, actionType ):
        kw = super( SFGeneral, cls )._refineValue( kw, prefix, actionType )
        # for the material_widgets
        material_widgets_key = ( "%s%s" ) % ( prefix, 'material_widgets' )
        if material_widgets_key in kw and kw[material_widgets_key]:
            kw[material_widgets_key] = json.loads( kw[material_widgets_key] )

        return kw


class SFLabel( DeclarativeBase, EasyMixin, SysMixin, FormMixin ):
    __tablename__ = 'sample_sub_form_label'

    id = Column( Integer, primary_key = True )
    main_id = Column( Integer, ForeignKey( 'sample_main_form.id' ) )
    main = relation( MainForm )

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
    color_other = Column( Text, doc = 'Label Info color other' )

    output = Column( CheckBoxCol( 99 ), doc = 'Output' )
    protection = Column( CheckBoxCol( 99 ), doc = 'Security File Protction' )
    output_other_content = Column( Text, doc = 'Output other content' )

    remark = Column( Text, doc = 'remark' )
    expected_date = Column( DateTime, doc = 'expected date' )
#    other = Column(Text, doc='Label Info other')

class SFArtwork( DeclarativeBase, EasyMixin, SysMixin, FormMixin ):
    __tablename__ = 'sample_sub_form_artwork'

    id = Column( Integer, primary_key = True )
    main_id = Column( Integer, ForeignKey( 'sample_main_form.id' ) )
    main = relation( MainForm )

    file_from = Column( CheckBoxCol( 99 ), doc = 'Files from' )
    file_from_ftp_location = Column( Text, doc = 'Files from FTP Location' )
    file_from_files_location = Column( Text, doc = 'Files from Files Location' )

    factory_code = Column( Unicode( 49 ), doc = 'Artwork Info-Factory Code(Artwork)' )
    size_w = Column( Text, doc = 'Artwork Info-Size Width' )
    size_h = Column( Text, doc = 'Artwork Info-Size Height' )
    size_unit = Column( CheckBoxCol( 99 ), doc = 'Artwork Info-Size Unit' )
    color = Column( CheckBoxCol( 99 ), doc = 'Artwork Info-Color' )
    color_spot_content = Column( MultiTextCol, doc = 'Artwork Info-No. of spot color' )
    color_other_content = Column( Text, doc = 'Artwork Info-Color-Other' )

    output = Column( CheckBoxCol( 99 ), doc = 'Output' )
    protection = Column( CheckBoxCol( 99 ), doc = 'Security File Protction' )
    output_other_content = Column( Text, doc = 'Output-Other' )

    remark = Column( Text, doc = 'Remark' )
    expected_date = Column( DateTime, doc = 'Expected date' )

class SFSampling( DeclarativeBase, EasyMixin, SysMixin, FormMixin ):
    __tablename__ = 'sample_sub_form_sampling'

    id = Column( Integer, primary_key = True )
    main_id = Column( Integer, ForeignKey( 'sample_main_form.id' ) )
    main = relation( MainForm )

    file_from = Column( CheckBoxCol( 99 ), doc = 'Files from' )
    file_from_ftp_location = Column( Text, doc = 'Files from FTP Location' )
    file_from_files_location = Column( Text, doc = 'Files from Files Location' )
    file_from_task_name = Column( Text, doc = 'Files from New Design Task Name' )

    output = Column( CheckBoxCol( 99 ), doc = 'Output' )
    output_white_pcs = Column( Integer, doc = 'Output-White mock up pcs' )
    output_woodfree_pcs = Column( Integer, doc = 'Output-Color Mock up in woodfree paper pcs' )
    output_semi_pcs = Column( Integer, doc = 'Output-Color Mock up in semi gloss paper pcs' )
    output_label_pcs = Column( Integer, doc = 'Output-Color Mock up in label pcs' )

    delivery = Column( CheckBoxCol( 99 ), doc = 'Expected date type' )
    expected_date = Column( DateTime, doc = 'Expected date' )
    expected_time = Column( Unicode( 49 ), doc = 'Same Day Delivery' )
    collection_point = Column( CheckBoxCol( 99 ), doc = 'Collection Point' )

    remark = Column( Text, doc = 'Remark' )

    material_widgets = Column( JSONCol( 10000 ), doc = "Material" )

#    material = Column(Unicode(20), doc='Material')
#    paper_thickness_type = Column(Unicode(20), doc='Material-Folding Cards')
#    paper_thickness_unit = Column(Unicode(5), doc='Material-Folding Cards-Paper thickness Unit')
#    gramage = Column(Unicode(10), doc='Material-Folding Cards-Gramage')
#    flute = Column(Unicode(20), doc='Material-Corrugated-Flute')
#    flute_type = Column(Unicode(20), doc='Material-Corrugated-Flute Type')
#    flute_type_gsm = Column(Unicode(10), doc='Material-Corrugated-Flute Type-gsm')
#    bursting = Column(Unicode(10), doc='Material-Corrugated-Bursting')
#    ect = Column(Unicode(10), doc='Material-Corrugated-ECT')
#    gramages = Column(Unicode(10), doc='Material-Corrugated-Gramage')

#    others = Column(Unicode(100), doc='Material-Other')
#    material_type = Column(Unicode(100), doc='Material-Folding Cards')
#    material_provided = Column(CheckBoxCol(50), doc='Material-Material provided')
#    according_files = Column(CheckBoxCol(50))
#    material_type_content = Column(Unicode(100), doc='Material-Folding Cards-')
#    material_type_other_content = Column(Unicode(100), doc='Material-Folding Cards-Other')

    @classmethod
    def _refineValue( cls, kw, prefix, actionType ):
        kw = super( SFSampling, cls )._refineValue( kw, prefix, actionType )
        needApprove = False
        # weber: super do it, except pcs validation
        intFields = ["output_white_pcs", "output_woodfree_pcs", "output_semi_pcs", "output_label_pcs"]
        for f in intFields:
            key = "%s%s" % ( prefix, f )
            if kw.get( key, None ):
                if actionType == "NEW" and kw[key] > 5: needApprove = True
            # key = "%s%s" % (prefix, f)
            # if kw.get(key, None):
            #    kw[key] = int(kw[key])
            #    if actionType == "NEW" and kw[key] > 5: needApprove = True
            # elif key in kw:  kw[key] = None


        # weber:super do it
        # if kw.has_key("%s%s" % (prefix, 'expected_date')) and not kw["%s%s" % (prefix, 'expected_date')]:
        #    kw["%s%s" % (prefix, 'expected_date')] = None

        material_widgets_key = ( "%s%s" ) % ( prefix, 'material_widgets' )
        if material_widgets_key in kw and kw[material_widgets_key]:
            kw[material_widgets_key] = json.loads( kw[material_widgets_key] )

        if actionType == "NEW" and needApprove: kw["%sstatus" % prefix] = WAIT_FOR_APPROVAL
        return kw

    def why_need_approve( self ):
        intFields = [( "output_white_pcs", "White mock up" ),
                     ( "output_woodfree_pcs", "Color Mock up in woodfree paper" ),
                     ( "output_semi_pcs", "Color Mock up in semi gloss paper" ),
                     ( "output_label_pcs", "Color Mock up in label" )]
        reasons = []
        for f, n in intFields:
            v = getattr( self, f )
            if v > 5: reasons.append( "No. of %s: %d." % ( n, v ) )
        return None if not reasons else "[%s] %s" % ( self.getWidget().label, " ".join( reasons ) )

class SFPrintout( DeclarativeBase, EasyMixin, SysMixin, FormMixin ):
    __tablename__ = 'sample_sub_form_printout'

    id = Column( Integer, primary_key = True )
    main_id = Column( Integer, ForeignKey( 'sample_main_form.id' ) )
    main = relation( MainForm )

    file_from = Column( CheckBoxCol( 99 ), doc = 'Files from' )
    file_from_ftp_location = Column( Text, doc = 'Files from FTP Location' )
    file_from_files_location = Column( Text, doc = 'Files from Files Location' )
    file_from_task_name = Column( Text, doc = 'Files from New Design Task Name' )

    output = Column( CheckBoxCol( 99 ), doc = 'Output' )
    output_dupont_pcs = Column( Integer, doc = 'Output Dupont pcs' )
    output_woodfree_pcs = Column( Integer, doc = 'Dupont Epson - Woodfree Paper pcs' )
    output_semi_pcs = Column( Integer, doc = 'Epson - Semi Gloss Paper pcs' )
    output_label_pcs = Column( Integer, doc = 'Epson - Label pcs' )
    output_normal_pcs = Column( Integer, doc = 'Laser Proof pcs' )

    delivery = Column( CheckBoxCol( 99 ), doc = 'Same Day Delivery/Expected date' )
    collection_point = Column( CheckBoxCol( 99 ), doc = 'Collection Point' )

    expected_date = Column( DateTime, doc = 'Expected date' )
    expected_time = Column( Unicode( 49 ), doc = 'Same Day Delivery' )
    remark = Column( Text, doc = 'Remark' )

    @classmethod
    def _refineValue( cls, kw, prefix, actionType ):
        kw = super( SFPrintout, cls )._refineValue( kw, prefix, actionType )
        needApproval = False
        # weber: super do it, except pcs validation
        fs = ["output_dupont_pcs", "output_woodfree_pcs", "output_semi_pcs", "output_label_pcs", "output_normal_pcs"]
        for f in fs:
            key = "%s%s" % ( prefix, f )
            if kw.get( key, None ):
                if actionType == "NEW" and kw[key] > 5: needApproval = True
            # key = "%s%s" % (prefix, f)
            # if kw.get(key, None):
            #    kw[key] = int(kw[key])
            #    if actionType == "NEW" and kw[key] > 5: needApproval = True
            # elif key in kw:  kw[key] = None

        # weber: super do it
        # if kw.has_key("%s%s" % (prefix, 'expected_date')) and not kw["%s%s" % (prefix, 'expected_date')]:
        #    kw["%s%s" % (prefix, 'expected_date')] = None

        if actionType == "NEW" and needApproval:
            kw["%sstatus" % prefix] = WAIT_FOR_APPROVAL

        return kw


    def why_need_approve( self ):
        intFields = [( "output_dupont_pcs", "Dupont" ),
                     ( "output_woodfree_pcs", "Epson - Woodfree Paper" ),
                     ( "output_semi_pcs", "Epson - Semi Gloss Paper" ),
                     ( "output_label_pcs", "Epson - Label" ),
                     ( "output_normal_pcs", "Normal Printer" )]
        reasons = []
        for f, n in intFields:
            v = getattr( self, f )
            if v > 5: reasons.append( "No. of %s: %d." % ( n, v ) )
        return None if not reasons else "[%s] %s" % ( self.getWidget().label, " ".join( reasons ) )

class SF3DImage( DeclarativeBase, EasyMixin, SysMixin, FormMixin ):
    __tablename__ = 'sample_sub_form_3dimage'

    id = Column( Integer, primary_key = True )
    main_id = Column( Integer, ForeignKey( 'sample_main_form.id' ) )
    main = relation( MainForm )

    file_from = Column( CheckBoxCol( 99 ), doc = 'Files from' )
    file_from_ftp_location = Column( Text, doc = 'Files from FTP Location' )
    file_from_files_location = Column( Text, doc = 'Files from Files Location' )

    output = Column( Unicode( 99 ), doc = 'Output' )
    details = Column( CheckBoxCol( 99 ), doc = 'Details' )

    expected_date = Column( DateTime, doc = 'Expected date' )
    remark = Column( Text, doc = 'Remark' )

class SFAssembly( DeclarativeBase, EasyMixin, SysMixin, FormMixin ):
    __tablename__ = 'sample_sub_form_assembly'

    id = Column( Integer, primary_key = True )
    main_id = Column( Integer, ForeignKey( 'sample_main_form.id' ) )
    main = relation( MainForm )

    file_from = Column( CheckBoxCol( 99 ), doc = 'Files from' )
    file_from_ftp_location = Column( Text, doc = 'Files from FTP Location' )
    file_from_files_location = Column( Text, doc = 'Files from Files Location' )

    output = Column( CheckBoxCol( 99 ), doc = 'Output' )
    expected_date = Column( DateTime, doc = 'Expected date' )
    remark = Column( Text, doc = 'Remark' )

class SFDrop( DeclarativeBase, EasyMixin, SysMixin, FormMixin ):
    __tablename__ = 'sample_sub_form_drop_test'

    id = Column( Integer, primary_key = True )
    main_id = Column( Integer, ForeignKey( 'sample_main_form.id' ) )
    main = relation( MainForm )

    submit_items = Column( CheckBoxCol( 99 ), doc = 'Submitted Items' )
    submit_items_location = Column( Text, doc = 'Submitted Items Location' )

    test_info = Column( CheckBoxCol( 99 ), doc = 'Test Info' )
    condition = Column( CheckBoxCol( 99 ), doc = 'Conditions' )
    condition_other_content = Column( Text, doc = 'Conditions Others' )

    remark = Column( Text, doc = 'Remark' )
    expected_date = Column( DateTime, doc = 'Expected date' )

class SFUpload( DeclarativeBase, EasyMixin, SysMixin, FormMixin ):
    __tablename__ = 'sample_sub_form_upload'

    id = Column( Integer, primary_key = True )
    main_id = Column( Integer, ForeignKey( 'sample_main_form.id' ) )
    main = relation( MainForm )

    # job_nature = Column(CheckBoxCol(99), doc='Job Nature ')
    checking = Column( CheckBoxCol( 99 ), doc = 'Artwork Pre-Flight/Die-line Pre-Flight' )

    file_from = Column( CheckBoxCol( 99 ), doc = 'Files From' )
    from_ftp_location = Column( Text, doc = 'Files From FTP Location' )
    from_public_location = Column( Text, doc = 'Files From Public Location' )

    file_to = Column( CheckBoxCol( 99 ), doc = 'File to' )
    to_ftp_location = Column( Text, doc = 'File to FTP Location' )
    to_public_location = Column( Text, doc = 'File to Public Location' )

    expected_date = Column( DateTime, doc = 'Expected date' )
    remark = Column( Text, doc = 'Remark' )


class SFContainer( DeclarativeBase, EasyMixin, SysMixin, FormMixin ):
    __tablename__ = 'sample_sub_form_container'

    id = Column( Integer, primary_key = True )
    main_id = Column( Integer, ForeignKey( 'sample_main_form.id' ) )
    main = relation( MainForm )

    weight = Column( Text, doc = 'Loading Info Weight' )
    weight_unit = Column( Unicode( 49 ), doc = 'Loading Info Unit' )
    weight_as_sample = Column( CheckBoxCol( 99 ), doc = 'Loading Info As Sample' )

    size_according = Column( CheckBoxCol( 99 ), doc = 'Size according to the new deisgn with this request' )
    outer_w = Column( Text, doc = 'Overall outer size Width' )
    outer_d = Column( Text, doc = 'Overall outer size Depth' )
    outer_h = Column( Text, doc = 'Overall outer size Height' )
    outer_unit = Column( CheckBoxCol( 99 ), doc = 'Overall outer size Unit' )
    outer_as_sample = Column( CheckBoxCol( 99 ), doc = 'Overall outer size as sample' )

    pallet = Column( CheckBoxCol( 99 ), doc = 'Pallet' )
    pallet_w = Column( Text, doc = 'Pallet Width' )
    pallet_d = Column( Text, doc = 'Pallet Depth' )
    pallet_h = Column( Text, doc = 'Pallet Height' )
    pallet_unit = Column( CheckBoxCol( 99 ), doc = 'Pallet Unit' )
    orientation = Column( CheckBoxCol( 99 ), doc = 'Product Orientation' )
    info = Column( CheckBoxCol( 99 ), doc = 'Container Info' )
    info_other = Column( Text, doc = 'Container Info Others' )

    remark = Column( Text, doc = 'Remark' )
    expected_date = Column( DateTime, doc = 'Expected date' )
#    pallet_content=Column(Unicode(20))

class SFFileConvert( DeclarativeBase, EasyMixin, SysMixin, FormMixin ):
    __tablename__ = 'sample_sub_form_file_convert'

    id = Column( Integer, primary_key = True )
    main_id = Column( Integer, ForeignKey( 'sample_main_form.id' ) )
    main = relation( MainForm )

    file_from = Column( CheckBoxCol( 99 ), doc = 'Files From' )
    file_from_ftp_location = Column( Text, doc = 'FTP Location' )
    file_from_files_location = Column( Text, doc = 'Files Location' )

    output = Column( CheckBoxCol( 99 ), doc = 'Output' )
    output_pdf_protection = Column( CheckBoxCol( 99 ), doc = 'Output PDF Security File Protection' )
    output_other_content = Column( Text, doc = 'Other Output' )

    expected_date = Column( DateTime, doc = 'Expected date' )
    remark = Column( Text, doc = 'Remark' )

class SFPhoto( DeclarativeBase, EasyMixin, SysMixin, FormMixin ):
    __tablename__ = 'sample_sub_form_photo'

    id = Column( Integer, primary_key = True )
    main_id = Column( Integer, ForeignKey( 'sample_main_form.id' ) )
    main = relation( MainForm )

    job_purpose = Column( CheckBoxCol( 99 ), doc = 'job purpose' )
    submit_items = Column( CheckBoxCol( 99 ), doc = 'Submitted Items' )
    submit_items_other = Column( Text, doc = 'Submitted Items Others Content' )
    job_nature = Column( CheckBoxCol( 99 ), doc = 'Job Nature' )
    output = Column( CheckBoxCol( 99 ), doc = 'Output' )
    output_other_content = Column( Text, doc = 'Output other content' )
    shoot_widgets = Column( JSONCol( 10000 ), doc = "View Of Shoots" )

    expected_date = Column( DateTime, doc = 'Expected date' )
    remark = Column( Text, doc = 'Remark' )

    @classmethod
    def _refineValue( cls, kw, prefix, actionType ):
        kw = super( SFPhoto, cls )._refineValue( kw, prefix, actionType )
        shoot_widgets_key = ( "%s%s" ) % ( prefix, 'shoot_widgets' )
        if shoot_widgets_key in kw and kw[shoot_widgets_key]:
            kw[shoot_widgets_key] = json.loads( kw[shoot_widgets_key] )

        return kw

class DevelopmentLog( DeclarativeBase, SysMixin ):
    __tablename__ = 'sample_development_log'

    id = Column( Integer, primary_key = True )
    system_no = Column( Unicode( 50 ) )
    main_form_id = Column( Integer, ForeignKey( 'sample_main_form.id' ) )
    main = relation( MainForm, backref = "Logs" )
    sub_form_id = Column( Integer )
    sub_form_type = Column( Unicode( 50 ) )
    action_type = Column( Unicode( 50 ) )
    remark = Column( Unicode( 50000 ) )

    @property
    def sub_form( self ):
        selfModule = __import__( "tribal.model.sample" ).model.sample
        dbclz = getattr( selfModule, self.sub_form_type )
        return DBSession.query( dbclz ).get( self.sub_form_id )

class SampleGroupProfile( DeclarativeBase, SysMixin ):
    __tablename__ = 'sample_group_profile'

    id = Column( Integer, primary_key = True )
    name = Column( Unicode( 50 ) )
    description = Column( Unicode( 1000 ) )
    group_id = Column( Integer, ForeignKey( 'tg_group.group_id' ) )
    group = relation( Group, backref = "sample_profiles", primaryjoin = "SampleGroupProfile.group_id == Group.group_id" )

    team_id = Column( Integer, ForeignKey( 'sample_team.id' ) )
    team = relation( Team )
    region_id = Column( Integer, ForeignKey( 'sample_region.id' ) )
    region = relation( Region )

    manager_group_id = Column( Integer, ForeignKey( 'tg_group.group_id' ) )
    manager_group = relation( Group, backref = "sample_manager_profiles", primaryjoin = "SampleGroupProfile.manager_group_id == Group.group_id" )
    def __str__( self ):
        return self.name


class FormExtraInfo( DeclarativeBase, SysMixin ):
    __tablename__ = 'sample_form_extra_info'

    id = Column( Integer, primary_key = True )
    name = Column( Unicode( 50 ) )
    estimate_time = Column( Unicode( 50 ) )
    job_config = Column( Unicode( 500 ) )
    need_stock = Column( Integer, default = 0 )  # 0 is needed ,1 is not need
    email_to = Column( Text )
    sh_email_to = Column( Text )


class FormTypeMapping( DeclarativeBase, SysMixin ):
    __tablename__ = 'sample_form_type_mapping'

    id = Column( Integer, primary_key = True )
    name = Column( Unicode( 100 ) )
    label = Column( Unicode( 100 ) )
    category = Column( Unicode( 100 ) )
    categoryindex = Column( Integer )
    report_header = Column( Unicode( 100 ) )

    category2 = Column( Unicode( 100 ) )
    category2index = Column( Integer )
    report_header2 = Column( Unicode( 100 ) )

    category3 = Column( Unicode( 100 ) )
    category3index = Column( Integer )
    report_header3 = Column( Unicode( 100 ) )


class FormSerialize( DeclarativeBase, SysMixin ):
    __tablename__ = 'sample_form_serialize'

    id = Column( Integer, primary_key = True )
    token = Column( Unicode( 100 ) )
    type = Column( Unicode( 20 ) )
    serialize = Column( PickleType() )

    @classmethod
    def find_by_token( cls, token ):
        return DBSession.query( cls ).filter( cls.token == token ).order_by( cls.type ).all()

    @classmethod
    def delete_by_token( cls, token ):
        return DBSession.execute( "delete from sample_form_serialize where token='%s'" % token )

class FormVersion( DeclarativeBase ):

    __tablename__ = 'sample_form_version'

    id = Column( Integer, primary_key = True )
    main_id = Column( Integer, ForeignKey( 'sample_main_form.id' ) )
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

class Job( DeclarativeBase, SysMixin ):
    __tablename__ = 'sample_job'

    id = Column( Integer, primary_key = True )
    main_form_id = Column( Integer, ForeignKey( 'sample_main_form.id' ) )
    main = relation( MainForm, backref = "jobs", primaryjoin = "and_(MainForm.id == Job.main_form_id, Job.active == 0)" )
    sub_form_id = Column( Integer )
    sub_form_type = Column( Unicode( 50 ) )
    time_spand = Column( Float, default = None )
    complete_time = Column( DateTime, default = None )
    remark = Column( Unicode( 1000 ) )
    other_spend = Column( Unicode( 1000 ) )
    designers = Column( Unicode( 5 ) )


    def sub_form( self ):
        try:
            return DBSession.query( globals()[self.sub_form_type] ).get( self.sub_form_id )
        except Exception, e:
            log.exception( str( e ) )
            return None

    # add by cz@2010-11-01
    @property
    def materialQty( self ):
        try:
            return sum( [m.qty for m in self.suform_job_materials if m] )
        except Exception, e:
            log.exception( str( e ) )
            return None

    @property
    def materials( self ):
        try:
            return '+'.join( [m.stock.name for m in self.suform_job_materials if m] )
        except Exception, e:
            log.exception( str( e ) )
            return None

    def populateOtherSpend( self ):
        try:
            from tribal.util.sample_helper import sample_dict
            mapping = sample_dict.getFormTypeMapping()
            result = []
            for ( n, v ) in json.loads( self.other_spend ):
                result.append( ( n, v, mapping.get( n, None ) ) )
            return result
        except Exception, e:
            log.exception( str( e ) )
            return []

class JobMaterial( DeclarativeBase, SysMixin ):
    __tablename__ = 'sample_job_material'

    id = Column( Integer, primary_key = True )
    main_form_id = Column( Integer, ForeignKey( 'sample_main_form.id' ) )
    main = relation( MainForm, backref = "main_job_materials", primaryjoin = "and_(MainForm.id == JobMaterial.main_form_id, JobMaterial.active == 0)" )

    job_id = Column( Integer, ForeignKey( 'sample_job.id' ) )
    job = relation( Job, backref = "suform_job_materials", primaryjoin = "and_(Job.id == JobMaterial.job_id, JobMaterial.active == 0)" )

    stock_id = Column( Integer, ForeignKey( 'sample_stock.id' ) )
    stock = relation( Stock, backref = "stock_job_materials" )
    cost = Column( Float, default = 0 )

    qty = Column( Float )
