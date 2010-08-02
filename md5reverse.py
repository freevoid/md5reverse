#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup

from urllib import urlencode
from urllib2 import Request, urlopen

MD5DB_URL = 'http://md5.noisette.ch/md5.php'

__all__ = ['md5reverse']

def make_md5_lookup_url(hash):
    return '?'.join([MD5DB_URL, urlencode({'hash': hash})])

def parse_response(xml_string):
    xml = BeautifulSoup(xml_string)
    answer = xml.find('string')
    if answer is None:
        error = xml.find('error')
        if error:
            raise ValueError(error.contents)
        else:
            raise ValueError("Parse error occured")
    else:
        return answer.string

def md5reverse(hash):
    """
    Reverse md5 hash using XML-service from md5.noisette.ch
    Pretty straightforward:

    >>> import md5
    >>> md5sum = lambda hash: md5.md5(hash).hexdigest()
    >>> md5lookup(md5sum("admin"))
    u'admin'
    """
    assert isinstance(hash, basestring)
    assert len(hash) == 32
    r = Request(url=make_md5_lookup_url(hash))
    f = urlopen(r)
    return parse_response(f.read())

def graceful_md5lookup(hash):
    try:
        md5reverse(hash)
    except BaseException, e:
        return ('error', e)

#raise RuntimeError("Error while requesting %s" % MD5DB_URL)

if __name__=='__main__':
    import sys
    assert len(sys.argv) == 2
    hash = sys.argv[1]
    try:
        sys.stdout.write(md5reverse(hash))
    except:
        sys.exit(1)
    sys.exit(0)

