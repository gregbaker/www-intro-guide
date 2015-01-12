#!/usr/bin/env python

import sys
import html5lib
import collections

def all_ids(elt):
    ids_deep = [all_ids(e) for e in elt.childNodes if e.nodeType==e.ELEMENT_NODE]
    ids = [i for ids in ids_deep for i in ids]
    if elt.hasAttribute('id'):
        ids.append(elt.getAttribute('id'))
    return ids

def html5_validate(infiles):
    for infile in infiles:
        if not infile.endswith('.html'):
            continue
        html = open(infile).read()
        parser = html5lib.HTMLParser(tree=html5lib.treebuilders.getTreeBuilder("dom"))
        tree = parser.parse(html)
        if parser.errors:
            print '=' * 70
            print "Validation error in %s." % (infile)
            print parser.errors
            sys.exit(1)
        
        ids = all_ids(tree.documentElement)
        if len(ids) != len(set(ids)):
            repeats = [i for i,n in collections.Counter(ids).items() if n>1]
            print '=' * 70
            print "Repeated id in %s." % (infile)
            print repeats
            sys.exit(1)
            

if __name__ == '__main__':
    html5_validate(sys.argv[1:])
