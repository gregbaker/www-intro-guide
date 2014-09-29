#!/usr/bin/env python

import sys
import html5lib

def html5_validate(infiles):
    for infile in infiles:
        if not infile.endswith('.html'):
            continue
        html = open(infile).read()
        parser = html5lib.HTMLParser(tree=html5lib.treebuilders.getTreeBuilder("dom"))
        parser.parse(html)
        if parser.errors:
            print '=' * 70
            print "Validation error in %s." % (infile)
            print parser.errors
            sys.exit(1)

if __name__ == '__main__':
    html5_validate(sys.argv[1:])
