#!/usr/bin/env python

import sys
import html5lib
from jinja_environment import _read_contents, basename, environment

TEMPLATE_START = """{% extends "base.html" %}
{% block title %}Index of Terms{% endblock %}
{% block h1 %}Index of Terms{% endblock %}
{% block pageclass %}term_index{% endblock %}

{% block content %}
<ul id="index">
"""

TEMPLATE_END = """
</ul>
{% endblock %}"""

CONTEXT = {'rellink': './'}


def index_dfn(contents, terms, fname, dfn):
    """
    Add entry to index data structure for this <dfn>
    """
    elt = dfn
    while not elt.hasAttribute('id'):
        if elt.tagName == 'section':
            raise ValueError, '<section> without id in %s' % (fname)
        elt = elt.parentNode
    
    ident = elt.getAttribute('id')
    assert len(dfn.childNodes) == 1 # handle other cases later if we need to
    text = dfn.childNodes[0].data
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
            out.append('<a href="%s">%s</a>' % (url, txt))
        items.append('<li>' + w + ': ' + ('; '.join(out)) + '</li>')
    return '\n'.join(items)

def render_index(content):
    """
    Render the index into a page
    """
    template_text = TEMPLATE_START + content + TEMPLATE_END
    template = environment.from_string(template_text)
    return template.render(CONTEXT)

def generate_index(infiles):
    terms = collect_terms(infiles)
    index_content = build_index(terms)
    print render_index(index_content)


if __name__ == '__main__':
    generate_index(sys.argv[1:])
