# -*- coding: utf-8 -*-
import traceback
from datetime import datetime as dt, timedelta
from sqlalchemy.sql.expression import and_
from tribal.model import DBSession
from tribal.model.prepress import PSGroupProfile



__all__ = ['getPSUserTeams', 'getPSUserRegions', 'checkPSSameTeam', 'countTime']



def getPSUserTeams( user, type = "team" ):
    teams = set()
    for g in user.groups:
        if "PREPRESS_SYSTEM" not in map( lambda p:p.permission_name, g.permissions ):continue
        profiles = DBSession.query( PSGroupProfile ).filter( and_( PSGroupProfile.active == 0, PSGroupProfile.group_id == g.group_id ) )

        for p in profiles :
            if type == "team":
                    if p.team_id : teams.add( p.team )
            elif type == "appteam":
                if p.app_team_id : teams.add( p.app_team )

    return list( teams )



def getPSUserRegions( user, nameOrId = 'name' ):
    regions = set()
    for g in user.groups:
        for profile in g.prepress_profiles:
            if profile.region : regions.add( profile.region )

    if nameOrId == 'name' : return map( lambda v : str( v ), list( regions ) )
    if nameOrId == 'id'   : return map( lambda v : v.id, list( regions ) )

    return regions



def checkPSSameTeam( user, header ):
    user_belong_teams = [team.id for team in getPSUserTeams( user )]

    check_teams = [team.id for team in getPSUserTeams( header.create_by )]
    check_teams.append( header.team_id )

    for t in check_teams:
        if t in user_belong_teams : return True
    return False



def countTime( timestr ):
    totalmins = 0
    TIME_FORMAT = "%Y/%m/%d %H:%M"

    if not timestr : return totalmins
    times = timestr.split( "|" )
    if len( times ) < 2 : return totalmins
    if len( times ) % 2 != 0 : times = times[:-1]


    def _countSameDay( begin, end ):
        if begin >= end : return timedelta( seconds = 0 )
        pm1 = dt( begin.year, begin.month, begin.day, 13, )    # lunch start at 1PM
        pm2 = dt( begin.year, begin.month, begin.day, 14, )    # lunch end at 2PM
        if end < pm1 or begin > pm2 : spend = end - begin
        else: spend = max( [end, pm2] ) - min( [begin, pm1] ) - timedelta( hours = 1 )
        return spend

    totalspend = timedelta( seconds = 0 )
    for i in range( len( times ) / 2 ):
        try:
            b = dt.strptime( times[i * 2 ], TIME_FORMAT )
            e = dt.strptime( times[i * 2 + 1], TIME_FORMAT )
            b, e = min( [b, e] ), max( [b, e] )
            # if it's the same day
            if b.day == e.day :
                totalspend += _countSameDay( b, e )
            else:
                pm6 = dt( b.year, b.month, b.day, 18, )    # company start at 6 PM
                totalspend += _countSameDay( b, pm6 )

                am9 = dt( e.year, e.month, e.day, 9, )    # company start at 9 AM
                totalspend += _countSameDay( am9, e )

                for i in range( 1, b.day - e.day ):
                    if ( b + timedelta( days = i ) ).weekday not in [5, 6] :
                        totalspend += timedelta( hours = 8 )
        except:
            traceback.print_exc()
    totalmins = totalspend.seconds / 60
    return totalmins



if __name__ == '__main__':
    print countTime( '2013/07/03 9:00|2013/07/03 10:00' )    # 60
    print countTime( '2013/07/03 14:00|2013/07/03 18:00' )    # 240
    print countTime( '2013/07/03 9:00|2013/07/03 18:00' )    # 480
    print countTime( '2013/07/03 8:00|2013/07/03 19:00' )    # 600

    print countTime( '2013/07/03 9:00|2013/07/04 18:00' )    # 960
    print countTime( '2013/07/03 14:00|2013/07/04 18:00' )    # 720
    print countTime( '2013/07/03 9:00|2013/07/04 13:00' )    # 720
    print countTime( '2013/07/03 8:00|2013/07/04 19:00' )    # 1080

    print countTime( '2013/07/05 9:00|2013/07/08 18:00' )    # 960
    print countTime( '2013/07/05 14:00|2013/07/08 18:00' )    # 720
    print countTime( '2013/07/05 9:00|2013/07/08 13:00' )    # 720
    print countTime( '2013/07/05 14:00|2013/07/08 13:00' )    # 480
    print countTime( '2013/07/05 8:00|2013/07/08 19:00' )    # 1080
