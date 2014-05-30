import traceback
from sqlalchemy.sql import *
from repoze.what.predicates import in_any_group,in_group,has_permission


from tribal.model import DBSession,FormTypeMapping,SampleGroupProfile,Permission


__all__ = ["getSampleMaster","getUserTeams","getUserRegions","getAllSampleUsers","checkSameTeam","getManagerByTeam","sample_dict"]

def getSampleMaster(clz):
    try:
        return DBSession.query(clz).filter(clz.active == 0).order_by(clz.name).all()
    except:
        traceback.print_exc()
    return []


def getUserTeams(user):
    teams = set()
    for g in user.groups:
        if "SAMPLE_DEVELOPMENT" not in map(lambda p:p.permission_name,g.permissions):continue
        profiles = DBSession.query(SampleGroupProfile).filter(and_(SampleGroupProfile.active==0,SampleGroupProfile.group_id==g.group_id))
        for p in profiles : teams.add(p.team)
    return list(teams)



def getUserRegions(user,nameOrId='name'):
    regions = set()
    for g in user.groups:
        for profile in g.sample_profiles:
            if profile.region : regions.add(profile.region)
    
    if nameOrId == 'name' : return map(lambda v : str(v),list(regions))
    if nameOrId == 'id'   : return map(lambda v : v.id,list(regions))
    
    return regions


            
def getAllSampleUsers():
    try:
        users = set()
        p = DBSession.query(Permission).filter(Permission.permission_name=="SAMPLE_DEVELOPMENT").one()
        for g in p.groups :
            for u in g.users: users.add(u)
        return sorted(list(users),key=lambda o:o.user_name)
    except:
        traceback.print_exc()
        return []


#def checkSameTeam(user,header):       
#    return header.team_id in [team.id for team in getUserTeams(user)]



def checkSameTeam(user,header):
    user_belong_teams = [team.id for team in getUserTeams(user)]
    
    check_teams = [team.id for team in getUserTeams(header.create_by)]
    check_teams.append(header.team_id)
    
    for t in check_teams:
        if t in user_belong_teams : return True
    return False
    

def getManagerByTeam(tid,idOnly=True):
    try:
        users = []
        for p in DBSession.query(SampleGroupProfile).filter(and_(SampleGroupProfile.active==0,SampleGroupProfile.team_id==tid)):
            if p.manager_group_id : users.extend(p.manager_group.users)
        return [u.user_id for u in users] if idOnly else users
        
    except:
        traceback.print_exc()
        return []


class SampleDict(object):
    
    _formTypeMapping = None
    
    def getFormTypeMapping(self):
        if self._formTypeMapping is None:
            self._formTypeMapping = {}
            for m in DBSession.query(FormTypeMapping).filter(FormTypeMapping.active==0):
                self._formTypeMapping[m.name] = {
                                          "name" : m.name,
                                          "label" : m.label,
                                          "category" : m.category,
                                          "report_header" : m.report_header,
                                          }
        return self._formTypeMapping
    
    
sample_dict = SampleDict()


