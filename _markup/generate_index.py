#!/usr/bin/env python

import sys
import html5lib
from jinja_environment import _read_contents, basename, process_jinga
from cgi import escape

TEMPLATE_START = """{% extends "base.html" %}
{% block title %}Index of Terms{% endblock %}
{% block h1 %}Index of Terms{% endblock %}
{% block pageclass %}termindex{% endblock %}

{% block content %}
<ul id="index">
"""

TEMPLATE_END = """
</ul>
{% endblock %}"""

CONTEXT = {'rellink': './', 'indexlink': './'}

def extract_text(elt):
    """
    Get the plain-text from this element
    """
    if elt.nodeType == elt.TEXT_NODE:
        return elt.data
    elif elt.nodeType == elt.ELEMENT_NODE:
        return ''.join(extract_text(e) for e in elt.childNodes)
    else:
        raise ValueError, "unknown node type %i" % (elt.nodeType)

def index_dfn(contents, terms, fname, dfn):
    """
    Add entry to index data structure for this <dfn>
    """
    elt = dfn
    depth = 0
    while not elt.hasAttribute('id'):
        if elt.tagName == 'section':
            raise ValueError, '<section> without id in %s' % (fname)

        if elt.tagName == 'dd':
            # special case id-finder for stuff in a <dd>: link to the <dt>
            elt = elt.previousSibling
            while elt.nodeType != elt.ELEMENT_NODE or elt.tagName != 'dt':
                elt = elt.previousSibling
        else:
            elt = elt.parentNode
        depth += 1

    ident = elt.getAttribute('id')
    good_id = depth < 2 or elt.tagName == 'dt'    

    if dfn.hasAttribute('data-term'):
       text = dfn.getAttribute('data-term')
    else:
       text = extract_text(dfn)

    # kind of suggest that the <dfn> or at least its parent has an id to link to
    if not good_id:
        sys.stderr.write("<dfn> for '%s' in %s has no id.\n" % (text, fname))

    entry = terms.get(text, [])
    topic = contents[basename(fname)]
    entry.append((fname + '#' + ident, topic))
    terms[text] = entry

def collect_terms(infiles):
    """
    Collect all <dfn>s in the documents into a data structure
    """
    terms = {}
    contents = _read_contents()
    for f in infiles:
        assert f.startswith('_site/')
        doc = html5lib.parse(open(f).read(), treebuilder="dom")
        dfns = doc.getElementsByTagName('dfn')
        for d in dfns:
            index_dfn(contents, terms, f[6:], d)
    
    return terms

def build_index(terms):
    """
    Build the HTML for the index list
    """
    words = terms.keys()
    words.sort(key=lambda x: x.lower())
    items = []
    for w in words:
        out = []
        for url,txt in terms[w]:
            out.append('<a href="%s">%s</a>' % (escape(url), escape(txt)))
        items.append('<li><span class="term">' + escape(w) + '</span>: ' + ('; '.join(out)) + '</li>')
    return '\n'.join(items)

def render_index(content):
    """
    Render the index into a page
    """
    template_text = TEMPLATE_START + content + TEMPLATE_END
    return process_jinga(template_text, CONTEXT)

def generate_index(outfile, infiles):
    terms = collect_terms(infiles)
    index_content = build_index(terms)
    content = render_index(index_content)
    with open(outfile, 'w') as fh:
        fh.write(content)


if __name__ == '__main__':
    generate_index(sys.argv[1], sys.argv[2:])
