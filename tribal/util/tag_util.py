# -*- coding: utf-8 -*-
from tribal.model import *

def returnIds(poNo, style, soNo, soRemark, tagNo, brand, attachmentSet, ediFile, latest=0):
    try:
        items = DBSession.query(TAGItem).filter(and_(TAGItem.poNo==poNo, TAGItem.style==style, TAGItem.soNo==soNo, \
                        TAGItem.soRemark==soRemark, TAGItem.tagNo==tagNo,TAGItem.brand==brand, TAGItem.attachmentSet==attachmentSet, \
                                                    TAGItem.active==0, TAGItem.ediFile==ediFile, TAGItem.latest==latest)).all() or []
        return '_'.join([str(i.id) for i in items if i])
    except:
        return '_'.join([])


def returnFormat(brand, tagNo):
    b = str(brand).strip()
    t = str(tagNo).strip()
    if 'Flapdoodles'==b:
        """
        if 'INF' == t:
            return 'Flapdoodles_905'
        elif 'ING' == t:
            return 'Flapdoodles_940'
        else:
            return 'Flapdoodles'
	    """
        return 'Flapdoodles'
    elif 'Little Me'==b:
        return 'LittleMe'
    elif 'GUESS' == b.upper():
        return 'Guess'
    elif 'KENSIE GIRL' == b.upper():
        return 'KENSIEGIRL'
    else:
        return 'LittleMe'