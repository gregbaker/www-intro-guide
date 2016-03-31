#!/usr/bin/env python

import sys, os
import html5lib
import itertools
import urllib2
import urlparse
import json
from jinja_environment import _read_contents, basename, process_jinja
from cgi import escape

CONTENT_CACHE = '.link_cache.json'

# a few links use the user-agent to filter bots, but we're trying to test real-user experience
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'

def is_absolute_url(url):
    return url.startswith('http://') or url.startswith('https://')

def find_links(elt):
    if elt.nodeType == elt.ELEMENT_NODE:
        if elt.tagName == 'a':
            yield elt.getAttribute('href'), elt
        elif elt.tagName == 'link':
            yield elt.getAttribute('href'), elt
        elif elt.tagName == 'script':
            yield elt.getAttribute('src'), elt
        elif elt.tagName == 'img':
            yield elt.getAttribute('src'), elt
        
        for c in elt.childNodes:
            for l in find_links(c):
                yield l

def collect_links(infile):
    doc = html5lib.parse(open(infile).read(), treebuilder="dom")
    for l, elt in find_links(doc.documentElement):
        # get canonical URL, and split off fragment.
        absurl = urlparse.urljoin(infile, l)
        sp = urlparse.urlsplit(absurl)
        frag = sp.fragment
        if elt.getAttribute('data-linkcheck') == 'nofrag':
            # ignore fragment if link explicitly says to
            frag = ''

        if is_absolute_url(absurl):
            sp_nofrag = urlparse.SplitResult(sp.scheme, sp.netloc,
                    sp.path, sp.query, '')
            absurl = urlparse.urlunsplit(sp_nofrag)
        else:
            # also strip query string for local files: handled by JS only
            sp_nofragquery = urlparse.SplitResult(sp.scheme, sp.netloc,
                    sp.path, '', '')
            absurl = urlparse.urlunsplit(sp_nofragquery)

        yield absurl, frag

def collect_all_links(infiles):
    links = set()
    for f in infiles:
        links |= set(collect_links(f))
    return links

def fetch(url):
    if is_absolute_url(url):
        try:
            req = urllib2.Request(url, headers={'User-Agent': 'USER_AGENT'})
            resp = urllib2.urlopen(req)
            status = resp.getcode()
            data = resp.read()
            return data, status
        except urllib2.HTTPError, e:
            return '', e.code
    else:
        try:
            return open(url).read(), 200
        except IOError:
            try:
                return open(os.path.join(url, 'index.html')).read(), 200
            except IOError:
                return '', 404

def get_content_cache():
    try:
        unicode_contents = json.load(file(CONTENT_CACHE, 'rb'))
    except (IOError, ValueError):
        return {}
    
    contents = {k: (v.decode('base64'), s) for k, (v,s) in unicode_contents.items()}
    return contents

def save_content_cache(contents):
    unicode_contents = {k: (v.encode('base64'), s) for k, (v,s) in contents.items()}
    json.dump(unicode_contents, file(CONTENT_CACHE, 'wb'), indent=2)

def check_all_links(infiles):
    links = collect_all_links(infiles)
    contents = get_content_cache()
    for url, frag in links:
        if url in contents:
            data, status = contents[url]
        else:
            data, status = fetch(url)
            contents[url] = (data, status)

        if status != 200:
            print url, status, len(data)

        if not frag:
            # fetched without error: good enough with no fragment.
            continue
        
        # TODO: check fragments
        if ('id="%s"' % frag) in data:
            # page contains the requested fragment as an id=""s
            continue
        print url, frag
        #print `data`

    save_content_cache(contents)


if __name__ == '__main__':
    check_all_links(sys.argv[1:])
