import urllib
import urllib2

def get_post_response(url, post_params):
    postdata = urllib.urlencode(post_params)
    req = urllib2.Request(url=url, data=postdata)
    return urllib2.urlopen(req).read()