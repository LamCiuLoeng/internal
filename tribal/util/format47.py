# -*- coding: utf-8 -*-
import re

_DeptList = [
        ("BOYS", u"GARÇONS"),
        ("GIRLS", u"FILLES"),
        ("TODDLER BOYS", u"TOUT-PETITS GARÇONS"),
        ("TODDLER GIRLS", u"TOUT-PETITS FILLES"),
        ("INFANT BOYS", u"NOURRISSONS GARÇONS"),
        ("INFANT GIRLS", u"NOURRISSONS FILLES"),
        ("newborn girls".upper(), u"Nouveau-nées Filles"),
        ("newborn boys".upper(), u"Nouveau-nés Garçons"),
        ("newborn girl".upper(), u"Nouveau-née Gille"),
        ("newborn boy".upper(), u"Nouveau-né Garçon"),
        ("UNISEX".upper(), u"UNISEXE"),
        ('Infants'.upper(), u'Nourrissons'),  # 20120104
        ('Toddlers'.upper(), u'Tout-petits'),
        ('Infants-Toddlers'.upper(), u'Nourrissons/tout-petits'),
        ("BOY'S S-M-L".upper(), u"Garçons P-M-G"),
        ("GIRL'S S-M-L".upper(), u"Filles P-M-G"),
        ("One Size".upper(), u"Taille unique")
        ]
_Dept = dict(_DeptList)

## Color Dist
_ColorDescList = [
        ("AQUA".upper(), u"TURQUOISE"),
        ("ASSORTED".upper(), u"COORDONNÉ"), ## Check 20100202
        ("BEIGE".upper(), u"BEIGE"),
        ("BLACK".upper(), u"NOIR"),
        ("BLUE".upper(), u"BLEU"),
        ("BROWN".upper(), u"MARRON"),
        ("BRONZE".upper(), u"BRONZE"),
        ("BURGUNDY".upper(), u"BORDEAUX"),
        ("CAMEL".upper(), u"BRUN CHAMEAU"), ## Check 20100202
        ("CHECK".upper(), u"ÉTOFFE À CARREAUX"),
        ("CHAMBRAY".upper(), u"CHAMBRAY"),
        ("CORAL".upper(), u"CORAIL"),
        ("DARK BLUE".upper(), u"BLEU FONCÉ"),
        ("DARK BROWN".upper(), u"MARRON FONCÉ"),
        ("DENIM".upper(), u"JEAN"),
        ("DARK GREEN".upper(), u"VERT FONCÉ"),
        ("DARK GREY".upper(), u"GRIS FONCÉ"),
        ("DARK ORANGE".upper(), u"ORANGE FONCÉ"),
        ("DARK PINK".upper(), u"ROSE FONCÉ"),
        ("DARK PURPLE".upper(), u"VIOLET FONCÉ"),
        ("DARK STONE".upper(), u"TEINTE FONCÉE"), ## Check 20100202
        ("FUCHSIA".upper(), u"FUCHSIA"), ## Check 20100202
        ("GOLD".upper(), u"DORÉ"),
        ("GREY HEATHER".upper(), u"GRIS BRUYÈRE"), ## Check 20100202
        ("GREEN".upper(), u"VERT"),
        ("GREY".upper(), u"GRIS"),
        ("INDIGO".upper(), u"INDIGO"),
        ("IVORY".upper(), u"IVOIRE"),
        ("KHAKI".upper(), u"KAKI"),
        ("LAVENDER".upper(), u"LAVANDE"),
        ("LIGHT BLUE".upper(), u"BLEU CLAIR"),
        ("LIGHT GREEN".upper(), u"VERT CLAIR"),
        ("LIGHT DENlM".upper(), u"JEAN CLAIR"),
        ("LIGHT DENIM".upper(), u"JEAN CLAIR"),
        ("LIGHT GREY".upper(), u"GRIS CLAIR"),
        ("LILAC".upper(), u"LILAS"),
        ("LIME".upper(), u"LIME"), ## Check 20100202
        ("LIGHT PINK".upper(), u"ROSE CLAIR"), ## Check 20100202
        ("LIGHT PURPLE".upper(), u"VIOLET CLAIR"),
        ("LT STONE".upper(), u"TEINTE PÂLE"), ## Check 20100202
        ("LT TURQUOISE".upper(), u"TURQUOISE CLAIR"),
        ("LIGHT YELLOW".upper(), u"JAUNE CLAIR"),
        ("MED STONE".upper(), u"TEINTE ADOUCIE"), ## Check 20100202
        ("MULTI".upper(), u"MULTI"),
        ("NATURAL".upper(), u"NATUREL"),
        ("NAVY".upper(), u"BLEU MARIN"), ## Check 20100202
        ("OATMEAL".upper(), u"AVOINE"), ## Check 20100202
        ("OLIVE".upper(), u"OLIVE"),
        ("ORANGE".upper(), u"ORANGE"),
        ("OFF-WHITE".upper(), u"BLANC CASSÉ"),
        ("PEACH".upper(), u"PÊCHE"),
        ("PLAID".upper(), u"ÉTOFFE À CARREAUX"), ## Check 20100202
        ("PLUM".upper(), u"PRUNE"),
        ("PINK".upper(), u"ROSE"),
        ("PRINT".upper(), u"IMPRIMÉ"),
        ("PURPLE".upper(), u"VIOLET"),
        ("RASPBERRY".upper(), u"FRAMBOISE"),
        ("RED".upper(), u"ROUGE"),
        ("RINSE".upper(), u"TEINTE RINCÉE"), ## Check 20100202
        ("ROYAL BLUE".upper(), u"BLEU ROI"),
        ("RUST".upper(), u"ROUILLE"),
        ("SILVER".upper(), u"ARGENT"),
        ("SUPER STONE".upper(), u"PIERRE SUBLIME"), ## Check 20100202
        ("STONE".upper(), u"PIERRE"),
        ("STRIPE".upper(), u"RAYÉ"), ## Check 20100202
        ("TAN".upper(), u"FAUVE"), ## Check 20100202
        ("TICKING".upper(), u"COUTIL"), ## Check 20100202
        ("TEAL".upper(), u"SARCELLE"),
        ("TURQUOISE".upper(), u"TURQUOISE"),
        ("ULTRA STONE".upper(), u"PIERRE ULTRA"), ## Check 20100202
        ("VIOLET".upper(), u"VIOLET"),
        ("WHITE".upper(), u"BLANC"),
        ("YELLOW".upper(), u"JAUNE"),
        ("MULTI COLOR PACK".upper(), u"ENSEMBLE À PLUSIEURS COULEURS"), ## Check 20100202
        ("HOT PINK", u"ROSE INDIEN"), ## Check 20100202
        ("BLEACH DENIM",u"DENIM DÉLAVÉ"), ##20100202 Email
        ("Charcoal Gray Heather".upper(), u"Gris bruyère"), ##2010/04/16 email
        ("Charcoal Grey Heather".upper(), u"Gris bruyère"),
        ("Charcoal Grey H".upper(), u"Gris bruyère"),
        ("CHARCOAL", u"CHARBON"), ## 2011/04/26 email
        ("DARK RED", u"ROUGE FONCÉ"), ## 2011/04/26 email
        ('TAUPE', u'TAUPE'), # 20120104
#        ('Mint Print'.upper(), u'Monnaie Imprimer'.upper()), # 20120104
#        ('Morning Ray'.upper(), u'Ray Matin'.upper()), # 20120104
        ('CREAM'.upper(), u'CRÈME'),
        ("SANDBLAST", u"DENIM DÉLAVÉ AU SABLE"),
        ("TINT", u"TEINTE"),
        ("VIENNA WASH", u"TEINTE VIENNA"),
        ("PALE ORANGE", u"ORANGE PÂLE"),
        ("CHAPTER WASH", u"TEINTE CHAPTER"),
        ("DARK GREY HEATHER", u"ÉTOFFE CHINÉE GRIS FONCÉ"),
        ]

_ColorDesc = dict(_ColorDescList)

_AttachSetList = [
        ("PC+HAT", u"M+BONNET"),
        ("PC+BELT", u"M+CEINTURE"),
        ("PC+SCARF", u"M+ÉCHARPE"),
        ("PC+SASH", u"M+CEINTURE-ÉCHARPE"),
        ("PC+SOCK", u"M+CHAUSSETTES"),  # 2010/04/16 email
        ("PC+SOCKS", u"M+CHAUSSETTES"),  # 2010/04/16 email
        ("PC+BIB", u"M+BAVETTE"),  # 2010/04/16 email
        ("PC+PANTY", u"M+CULOTTE"),  # 2010/09/21 email
        ("PC+BIB+SOCKS", u"M+BAVETTE+CHAUSSETTES"),  # 2010/09/21 email
        ("PC+HEADBAND", u"M+BANDEAU"),  # 2010/09/21 email
        ("PC+HEADSCARF", u"M+FOULARD"),
        ("PC+HAT+BOOTIE", u"M+BONNET+BOTTINES"),
        ("PC+TIGHT", u"M+LEGGING"),
        ("PC+BAG", u"M+SAC"),
        ("PC+HEADBAND+BOOTIE", u"M+BANDEAU+PANTOUFLES"),
        ("PCBAND+BOOTIE", u"M+BANDEAU+PANTOUFLES"),
        ("PC+SWAG", u"M+CHAÎNETTE"),
        ]
_AttachSet = dict(_AttachSetList)

def _convert(s,testDict):
    try:
        result = testDict[s.strip()]
    except:
        result = ''
    return result

# add by cz@20120104
def color_french(color):
    """color french convert"""
    if color:
        return _convert(color.upper().strip(), _ColorDesc)
    else:
        return ''

def dept_french(dept):
    """dept french convert"""
    if dept:
        dept = dept.strip()
        _tmp = re.search("^\S{1,3}\-\S{1,3}\s?(.*)$", dept)
        if _tmp:
            _tmpS = _tmp.groups()[0]
        elif 'S-M-L' in dept:
            _tmpS = dept
        elif re.search("^(.*)\s?\S{1,3}\-\S{1,3}$", dept):
            _tmpS = re.search("^(.*)\s?\S{1,3}\-\S{1,3}$", dept).groups()[0]
        else:
            _tmpS = dept
        return _convert(_tmpS.upper(), _Dept)
    else:
        return ''

def attach_set_french(attach_set):
    """attach_set french convert"""
    if attach_set:
        attach_set = attach_set.strip().upper()
        _tmp = re.search("^(\d{1,3})\s?(PC)\s?(SET)?$", attach_set)
        if _tmp:
            _tmpS = _tmp.groups()[0]
            _attach_set = _tmpS + u" PIECE SET"
            return _attach_set, u"ENSEMBLE " + _tmpS + u" PIÈCES"
        elif re.search("^(\d{1,3})\s?(PC\+\S*)$", attach_set):
            _tmpS = re.search("^(\d{1,3})\s?(PC\+\S*)$", attach_set).groups()
            if int(_tmpS[0]) > 1 and _tmpS[1] == "PC+SOCK":
                return attach_set, _tmpS[0] + " " + _convert("PC+SOCKS", _AttachSet)
            else:
                return attach_set, _tmpS[0] + " " + _convert(_tmpS[1].strip(), _AttachSet)
        elif re.search("^(\d{1,3})\s?(PCBAND\+.*)$", attach_set):
            _tmpS = re.search("^(\d{1,3})\s?(PCBAND\+.*)$", attach_set).groups()
            return attach_set, _tmpS[0] + " " + _convert(_tmpS[1].strip(), _AttachSet)
        else:
            return attach_set, ''
    else:
        return '', ''



def format47_AfterPaser(lst):
    _lst = list(lst)
    _lst[14] = "0"
    _lst[2] = _convert(_lst[1].upper().strip(), _ColorDesc)

    _tmp = re.search("^\S{1,3}\-\S{1,3}\s?(.*)$", _lst[5])
    if _tmp :
        _tmpS = _tmp.groups()[0]
    else :
        _tmpS = _lst[5]
    _lst[6] = _convert( _tmpS.upper(), _Dept)

    _tmp = re.search("^(\d{1,3})\s?(PC)\s?(SET)?$", _lst[10].strip())
    if _tmp :
        _tmpS = _tmp.groups()[0]
        _lst[10] = _tmpS + u" PIECE SET"
        _lst[11] = u"ENSEMBLE " + _tmpS + u" PIÈCES"
    elif re.search("^(\d{1,3})\s?(PC\+\S*)$", _lst[10].strip()) :
        _tmpS = re.search("^(\d{1,3})\s?(PC\+\S*)$", _lst[10].strip()).groups()
        if int(_tmpS[0]) > 1 and _tmpS[1] == "PC+SOCK":
            _lst[11] = _tmpS[0] + " " + _convert("PC+SOCKS", _AttachSet)
        else :
            _lst[11] = _tmpS[0] + " " + _convert(_tmpS[1].strip(), _AttachSet)
    else :
        _lst[11] = ""

    _lst[13] = _lst[12]
    if len(_lst[13]) == 15:
        _13 = _lst[13].split("-")
        if _13[2] not in ("OWB", "STK", "ST1") :
            _lst[13] = _13[0]

    return _lst

def format47B_AfterPaser(lst):
    _lst = list(lst)
    _lst[14] = "0"
    _lst[2] = _convert(_lst[1].upper().strip(), _ColorDesc)

    _tmp = re.search("^\S{1,3}\-\S{1,3}\s?(.*)$", _lst[5])
    if _tmp :
        _tmpS = _tmp.groups()[0]
    else :
        _tmpS = _lst[5]
    _lst[6] = _convert( _tmpS.upper(), _Dept)

    _tmp = re.search("^(\d{1,3})\s?(PC)\s?(SET)?$", _lst[10].strip())
    if _tmp :
        _tmpS = _tmp.groups()[0]
        _lst[10] = _tmpS + u" PIECE SET"
        _lst[11] = u"ENSEMBLE " + _tmpS + u" PIÈCES"
    elif re.search("^(\d{1,3})\s?(PC\+\S*)$", _lst[10].strip()) :
        _tmpS = re.search("^(\d{1,3})\s?(PC\+\S*)$", _lst[10].strip()).groups()
        if int(_tmpS[0]) > 1 and _tmpS[1] == "PC+SOCK":
            _lst[11] = _tmpS[0] + " " + _convert("PC+SOCKS", _AttachSet)
        else :
            _lst[11] = _tmpS[0] + " " + _convert(_tmpS[1].strip(), _AttachSet)
    else :
        _lst[11] = ""

    return _lst


if __name__ == '__main__':
#    l =("5 PC+SASH", "3 PC+SCARF")
#    for a in l:
#        b = re.search("^(\d{1,3})\s?(PC\+\S*)$", a).groups()[1]
#        c = _convert(b,_AttachSet)
#        print c
    print attach_set_french('2 PCBAND+BOOTIE')
