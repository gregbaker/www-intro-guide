import sys
import html5lib
from jinja_environment import _read_contents, basename, process_jinja

COUNTED_ELEMENTS = set(['h1', 'h2', 'h3', 'p', 'dt', 'dd', 'th', 'td'])
EXCLUDED_ELEMENTS = set(['blockquote'])

def count_words(elt, in_counted=False):
    """
    Count the words (that we care about)
    """
    if elt.nodeType == elt.ELEMENT_NODE and elt.tagName in EXCLUDED_ELEMENTS:
        return 0
    elif elt.nodeType == elt.ELEMENT_NODE and elt.tagName in COUNTED_ELEMENTS:
        child_counts = [count_words(e, in_counted=True) for e in elt.childNodes]
        return sum(child_counts)
    elif elt.nodeType == elt.ELEMENT_NODE:
        child_counts = [count_words(e) for e in elt.childNodes]
        return sum(child_counts)
    elif elt.nodeType == elt.TEXT_NODE and in_counted:
        txt = elt.data
        return len(txt.split())

    return 0
    
    return
    if elt.nodeType == elt.TEXT_NODE:
        return elt.data
    elif elt.nodeType == elt.ELEMENT_NODE:
        return ''.join(extract_text(e) for e in elt.childNodes)
    else:
        raise ValueError, "unknown node type %i" % (elt.nodeType)

def wordcount(infile):
    doc = html5lib.parse(open(infile).read(), treebuilder="dom")
    return count_words(doc.documentElement)
        
if __name__ == '__main__':
    print wordcount(sys.argv[1])
