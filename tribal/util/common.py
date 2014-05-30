# -*- coding: utf-8 -*-
import sys, os, random, cStringIO, urllib
reload( sys )
sys.setdefaultencoding( 'utf8' )
import base64
import sha
from datetime import date, datetime as dt
import traceback, os, smtplib, StringIO, base64, hashlib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
from email.header import Header

import ho.pisa as pisa

from tg import expose, redirect, validate, flash, config, response, request
from tribal.model import *
from tribal.model.sysutil import *

DISPLAY_DATE_FORMAT = "%Y-%m-%d"


__all__ = ["tabFocus", "Date2Text", "getOr404", "sendEmail", "advancedSendMail", "number2alphabet", "alphabet2number", "serveFile", "null2blank",
           "HTML2PDF", "sysUpload", "rpacEncrypt", "rpacDecrypt", "OrderedDict", "makeException", "logError",
           "OrderedSet", "ReportGenerationException", "createToken", "isWorkTime"]


def tabFocus( tab_type = "" ):
    def decorator( fun ):
        def returnFun( *args, **keywordArgs ):
            returnVal = fun( *args, **keywordArgs )
            if type( returnVal ) == dict and "tab_focus" not in returnVal:
                returnVal["tab_focus"] = tab_type
            return returnVal
        return returnFun
    return decorator


def Date2Text( value = None, dateTimeFormat = DISPLAY_DATE_FORMAT, defaultNow = False ):
    if not value and defaultNow : value = dt.now()

    format = dateTimeFormat
    result = value

    if isinstance( value, date ):
        try:
            result = value.strftime( format )
        except:
            traceback.print_exc()
    elif hasattr( value, "strftime" ):
        try:
            result = value.strftime( format )
        except:
            traceback.print_exc()

    if not result:
        result = ""

    return result

def getOr404( obj, id, redirect_url = "/index", message = "The record deosn't exist!" ):
    try:
        v = DBSession.query( obj ).get( id )
        if v : return v
#        else : raise "No such obj"
        else : raise makeException( "No such obj!" )
    except:
        traceback.print_exc()
        flash( message )
        redirect( redirect_url )

# This method is used in MS Excel to convert the header column from number to alphalbet
# def number2alphabet(n):
#    result = []
#    while n >= 0:
#        if n > 26:
#            result.insert(0, n % 26)
#            n /= 26
#        else:
#            result.insert(0, n)
#            break
#    return "".join([chr(r + 64) for r in result ]) if result else None



def number2alphabet( n ):
    result = []
    while n > 0 :
        x , y = n / 26, n % 26
        result.append( y )
        if x > 0 :
            n = x
        else:
            break

    p = 0
    for i in range( len( result ) ):
        result[i] += p
        if result[i] <= 0 and i + 1 < len( result ):
            result[i] += 26
            p = -1
        else:
            p = 0

    if result[-1] <= 0 : result = result[:-1]
    result.reverse()
    return "".join( map( lambda v:chr( v + 64 ), result ) )



def alphabet2number( str ):
    if not str or not isinstance( str, basestring ) : raise TypeError
    if not str.isalpha() : raise ValueError
    return  reduce( lambda a, b:  ( a * 26 ) + ord( b ) - ord( "a" ) + 1, str.lower(), 0 )



def sendEmail( send_from, send_to, subject, text, cc_to = [], files = [], server = "192.168.42.14" ):
    assert type( send_to ) == list
    assert type( files ) == list

    msg = MIMEMultipart()
    msg.set_charset( "utf-8" )
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join( send_to )

    if cc_to:
        assert type( cc_to ) == list
        msg['cc'] = COMMASPACE.join( cc_to )
        send_to.extend( cc_to )

    msg['Date'] = formatdate( localtime = True )
    msg['Subject'] = subject.replace( "\n", ' ' )

    msg.attach( MIMEText( text ) )

    for f in files:
        part = MIMEBase( 'application', "octet-stream" )
        if isinstance( f, basestring ):
            part.set_payload( open( f, "rb" ).read() )
            Encoders.encode_base64( part )
            part.add_header( 'Content-Disposition', 'attachment; filename="%s"' % Header( os.path.basename( f ), 'utf-8' ) )
        elif hasattr( f, "file_path" ) and hasattr( f, "file_name" ):
            part.set_payload( open( f.file_path, "rb" ).read() )
            Encoders.encode_base64( part )
            part.add_header( 'Content-Disposition', 'attachment; filename="%s"' % Header( f.file_name, 'utf-8' ) )
        msg.attach( part )

    smtp = smtplib.SMTP( server )
    smtp.sendmail( send_from, send_to, msg.as_string() )
    smtp.close()


def advancedSendMail( send_from, send_to, subject, text, html, cc_to = [], files = [], server = "192.168.42.14" ):
    assert type( send_to ) == list
    assert type( files ) == list

    if not text and not html:
        raise "No content to send!"
    elif text and not html :
        msg = MIMEText( text, "plain", _charset = 'utf-8' )    # fix the default encoding problem
    elif not text and html:
        msg = MIMEText( html, "html", _charset = 'utf-8' )    # fix the default encoding problem
    else:
        msg = MIMEMultipart( "alternative" )
        msg.attach( MIMEText( text, "plain", _charset = 'utf-8' ) )
        msg.attach( MIMEText( html, "html", _charset = 'utf-8' ) )

    msg.set_charset( "utf-8" )
    if len( files ) > 0 :
        tmpmsg = msg
        msg = MIMEMultipart()
        msg.attach( tmpmsg )

    msg['From'] = send_from
    msg['To'] = COMMASPACE.join( send_to )

    if cc_to:
        assert type( cc_to ) == list
        msg['cc'] = COMMASPACE.join( cc_to )
        send_to.extend( cc_to )

    msg['Date'] = formatdate( localtime = True )
    msg['Subject'] = subject

    for f in files:
        part = MIMEBase( 'application', "octet-stream" )
        if isinstance( f, basestring ):
            part.set_payload( open( f, "rb" ).read() )
            Encoders.encode_base64( part )
            part.add_header( 'Content-Disposition', 'attachment; filename="%s"' % Header( os.path.basename( f ), 'utf-8' ) )
        elif hasattr( f, "file_path" ) and hasattr( f, "file_name" ):
            part.set_payload( open( f.file_path, "rb" ).read() )
            Encoders.encode_base64( part )
            part.add_header( 'Content-Disposition', 'attachment; filename="%s"' % Header( f.file_name, 'utf-8' ) )
        msg.attach( part )

    smtp = smtplib.SMTP( server )
    smtp.sendmail( send_from, send_to, msg.as_string() )
    smtp.close()


def serveFile( filePath, fileName = None, contentType = "application/x-download", contentDisposition = "attachment" ):
    response.headers['Content-type'] = 'application/x-download' if not contentType else contentType

    if not fileName:
        response.headers['Content-Disposition'] = "%s;filename=%s" % ( contentDisposition, os.path.basename( filePath ) )
    else:
        if request.headers["User-Agent"].find( "MSIE" ) > -1:
            response.headers['Content-Disposition'] = "%s;filename=%s" % ( contentDisposition, urllib.quote( fileName.encode( 'utf-8' ) ) )
        elif request.headers["User-Agent"].find( "Firefox" ) > -1:
            response.headers['Content-Disposition'] = "%s;filename=%s" % ( contentDisposition, "=?utf-8?B?%s?=" % base64.b64encode( fileName ) )
        else:
            response.headers['Content-Disposition'] = "%s;filename=%s" % ( contentDisposition, fileName )

    response.headers['Pragma'] = 'public'    # for IE
    response.headers['Cache-control'] = 'max-age=0'    # for IE
    f = open( filePath, 'rb' )
    content = "".join( f.readlines() )
    f.close()
    return content



def defaultIfNone( blackList = [None, ], default = "" ):
    def returnFun( value ):
        defaultValue = default() if callable( default ) else default
        if value in blackList:
            return defaultValue
        else:
            try:
                return str( value )
            except:
                try:
                    return repr( value )
                except:
                    pass
        return defaultValue
    return returnFun

null2blank = defaultIfNone( blackList = [None, "NULL", "null", "None"] )


def HTML2PDF( data, filename ):
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument( StringIO.StringIO( data.encode( 'UTF-8' ) ), result, encoding = "UTF-8" )
    f = open( filename, 'wb' )
    f.write( result.getvalue() )
    f.close()
    return pdf.err

def rpacEncrypt( v ):
    c = base64.b64encode( unicode( v ) )
    e = hashlib.md5()
    e.update( "r-pac%sorsay" % unicode( v ) )
    k = e.hexdigest()[5:15]
#    k = sha.new("r-pac%sorsay" % unicode(v)).hexdigest()[5:15]
    return c + k

def rpacDecrypt( enStr ):
    if not enStr or len( enStr ) < 10 : return ( False, None )
    k = enStr[-10:]
    c = base64.b64decode( enStr[:-10] )

    e = hashlib.md5()
    e.update( "r-pac%sorsay" % unicode( c ) )
    kk = e.hexdigest()[5:15]

    if k != kk : return ( False, None )
#    if sha.new("r-pac%sorsay" % c).hexdigest()[5:15] != k : return (False,None)
    return ( True, c )



def sysUpload( attachment_list, attachment_name_list = None, folder = "sys", return_obj = False ):

#    if not (attachment_list and attachment_name_list) : return (1,[])
    if type( attachment_list ) != list : attachment_list = [attachment_list]
    if not attachment_name_list: attachment_name_list = [getattr( i, 'filename', None ) for i in attachment_list]
    if type( attachment_name_list ) != list : attachment_name_list = [attachment_name_list]
    if len( attachment_list ) != len( attachment_name_list ) : return ( 2, [] )


    def _todo( a, n ):
        try:
            file_path = a.filename
            ( pre, ext ) = os.path.splitext( file_path )
            path_prefix = os.path.join( config.download_dir, folder )
            if not os.path.exists( path_prefix ) : os.makedirs( path_prefix )

            file_name = "%s%.4d%s" % ( dt.now().strftime( "%Y%m%d%H%M%S" ), random.randint( 1, 1000 ), ext )
            full_path = os.path.join( path_prefix, file_name )

            f = open( full_path, "wb" )
            f.write( a.file.read() )
            f.close()

            db_file_name = n or file_name
            if db_file_name.find( "." ) < 0 : db_file_name = db_file_name + ext

            obj = UploadObject( file_name = db_file_name, file_path = os.path.join( folder, file_name ) )
            DBSession.add( obj )
            DBSession.flush()
            return obj.id if not return_obj else obj
#            return obj.id
        except:
            traceback.print_exc()
            logError()
            return None

    return ( 0, [_todo( a, n ) for a, n in zip( attachment_list, attachment_name_list ) if hasattr( a, "filename" )] )


def makeException( msg ):
    class _ExceptionClz( Exception ):
        def __init__( self, msg = msg ):
            self.msg = msg
            self.is_customize = True

        def __str__( self ): return self.msg
        def __unicode__( self ): return self.msg
        def __repr__( self ): return self.msg

    return _ExceptionClz


def logError():
    try:
        content = cStringIO.StringIO()
        content.write( "\n\n%s  %s %s\n" % ( "*" * 10, dt.now(), request.identity["user"] ) )
        traceback.print_exc( file = content )
        if not os.path.exists( config.log_dir ):
            os.makedirs( config.log_dir )
        f = file( os.path.join( config.log_dir, "error-%s.txt" % Date2Text( defaultNow = True ) ), 'ab' )
        f.write( content.getvalue() )
        f.close()
        print traceback.format_exc().splitlines()[-1]
    except:
        pass


#===============================================================================
# Copy from Sqlalchemy by CL on 2010-06-11
#
#===============================================================================

class OrderedDict( dict ):
    """A dict that returns keys/values/items in the order they were added."""

    def __init__( self, ____sequence = None, **kwargs ):
        self._list = []
        if ____sequence is None:
            if kwargs:
                self.update( **kwargs )
        else:
            self.update( ____sequence, **kwargs )

    def clear( self ):
        self._list = []
        dict.clear( self )

    def copy( self ):
        return self.__copy__()

    def __copy__( self ):
        return OrderedDict( self )

    def sort( self, *arg, **kw ):
        self._list.sort( *arg, **kw )

    def update( self, ____sequence = None, **kwargs ):
        if ____sequence is not None:
            if hasattr( ____sequence, 'keys' ):
                for key in ____sequence.keys():
                    self.__setitem__( key, ____sequence[key] )
            else:
                for key, value in ____sequence:
                    self[key] = value
        if kwargs:
            self.update( kwargs )

    def setdefault( self, key, value ):
        if key not in self:
            self.__setitem__( key, value )
            return value
        else:
            return self.__getitem__( key )

    def __iter__( self ):
        return iter( self._list )

    def values( self ):
        return [self[key] for key in self._list]

    def itervalues( self ):
        return iter( self.values() )

    def keys( self ):
        return list( self._list )

    def iterkeys( self ):
        return iter( self.keys() )

    def items( self ):
        return [( key, self[key] ) for key in self.keys()]

    def iteritems( self ):
        return iter( self.items() )

    def __setitem__( self, key, object ):
        if key not in self:
            self._list.append( key )
        dict.__setitem__( self, key, object )

    def __delitem__( self, key ):
        dict.__delitem__( self, key )
        self._list.remove( key )

    def pop( self, key, *default ):
        present = key in self
        value = dict.pop( self, key, *default )
        if present:
            self._list.remove( key )
        return value

    def popitem( self ):
        item = dict.popitem( self )
        self._list.remove( item[0] )
        return item

class OrderedSet( set ):
    def __init__( self, d = None ):
        set.__init__( self )
        self._list = []
        if d is not None:
            self.update( d )

    def add( self, element ):
        if element not in self:
            self._list.append( element )
        set.add( self, element )

    def remove( self, element ):
        set.remove( self, element )
        self._list.remove( element )

    def insert( self, pos, element ):
        if element not in self:
            self._list.insert( pos, element )
        set.add( self, element )

    def discard( self, element ):
        if element in self:
            self._list.remove( element )
            set.remove( self, element )

    def clear( self ):
        set.clear( self )
        self._list = []

    def __getitem__( self, key ):
        return self._list[key]

    def __iter__( self ):
        return iter( self._list )

    def __repr__( self ):
        return '%s(%r)' % ( self.__class__.__name__, self._list )

    __str__ = __repr__

    def update( self, iterable ):
        add = self.add
        for i in iterable:
            add( i )
        return self

    __ior__ = update

    def union( self, other ):
        result = self.__class__( self )
        result.update( other )
        return result

    __or__ = union

    def intersection( self, other ):
        other = set( other )
        return self.__class__( a for a in self if a in other )

    __and__ = intersection

    def symmetric_difference( self, other ):
        other = set( other )
        result = self.__class__( a for a in self if a not in other )
        result.update( a for a in other if a not in self )
        return result

    __xor__ = symmetric_difference

    def difference( self, other ):
        other = set( other )
        return self.__class__( a for a in self if a not in other )

    __sub__ = difference

    def intersection_update( self, other ):
        other = set( other )
        set.intersection_update( self, other )
        self._list = [ a for a in self._list if a in other]
        return self

    __iand__ = intersection_update

    def symmetric_difference_update( self, other ):
        set.symmetric_difference_update( self, other )
        self._list = [ a for a in self._list if a in self]
        self._list += [ a for a in other._list if a in self]
        return self

    __ixor__ = symmetric_difference_update

    def difference_update( self, other ):
        set.difference_update( self, other )
        self._list = [ a for a in self._list if a in self]
        return self

    __isub__ = difference_update



#===============================================================================
# exception define
#===============================================================================
class ReportGenerationException( Exception ):
    def __init__( self, msg = "Error when generate the report!" ):
        self.msg = msg

    def __str__( self ):
        return self.msg


def createToken():
    token = request.identity["user"].user_name + dt.now().strftime( "%y%m%d%H%M%S" ) + str( random.randint( 100, 999 ) )
    return sha.new( token ).hexdigest()


def isWorkTime():
    n = dt.now()
    return ( n.weekday() not in [5, 6] ) and ( 8 < n.hour < 18 )
