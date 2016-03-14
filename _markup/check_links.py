#!/usr/bin/env python

import sys, os
import html5lib
import itertools
import urllib
import urlparse
from jinja_environment import _read_contents, basename, process_jinja
from cgi import escape

def find_links(elt):
    if elt.nodeType == elt.ELEMENT_NODE:
        if elt.tagName == 'a':
            yield elt.getAttribute('href')
        elif elt.tagName == 'link':
            yield elt.getAttribute('href')
        elif elt.tagName == 'script':
            yield elt.getAttribute('src')
        elif elt.tagName == 'img':
            yield elt.getAttribute('src')
        
        for c in elt.childNodes:
            for l in find_links(c):
                yield l

def collect_links(infile):
    doc = html5lib.parse(open(infile).read(), treebuilder="dom")
    for l in find_links(doc.documentElement):
        # get absolute URL, and split off fragment.
        absurl = urlparse.urljoin(infile, l)
        sp = urlparse.urlsplit(absurl)
        frag = sp.fragment
        sp_nofrag = urlparse.SplitResult(sp.scheme, sp.netloc, sp.path, sp.query, '')
        absurl = urlparse.urlunsplit(sp_nofrag)
        yield absurl, frag

def collect_all_links(infiles):
    links = set()
    for f in infiles:
        links |= set(collect_links(f))
    return links

def fetch(url):
    if url.startswith('http://') or url.startswith('https://'):
        return urllib.urlopen(url).read()
    else:
        try:
            return open(url).read()
        except IOError:
            return open(os.path.join(url, 'index.html')).read()

def check_all_links(infiles):
    links = collect_all_links(infiles)
    contents = {}
    for url, frag in links:
        if url in contents:
            data = contents[url]
        else:
            data = fetch(url)
            contents[url] = data

        if not frag:
            # fetched without error: good enough with no fragment.
            continue
        
        # TODO: check fragments
        #print ('id="%s"' % frag) in data


if __name__ == '__main__':
    check_all_links(sys.argv[1:])
