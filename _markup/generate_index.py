#!/usr/bin/env python

import sys
import html5lib
import itertools
from jinja_environment import _read_contents, basename, process_jinja
from html import escape

TEMPLATE_START = """{% extends "appendixbase.html" %}
{% block title %}Index of Terms{% endblock %}
{% block h1 %}Index of Terms{% endblock %}
{% block pageclass %}termindex appendix{% endblock %}

{% block content %}
<ul id="index">
"""

TEMPLATE_END = """
</ul>
{% endblock %}"""

CONTEXT = {'rellink': './', 'indexlink': './', 'input_file': 'term_index.html'}

class IndexTerm(object):
    def __init__(self, term, link, topic, alphaterm=None):
        self.term = term
        self.link = link
        self.topic = topic
        if alphaterm:
            self.alphaterm = alphaterm
        else:
            self.alphaterm = term
    
    def __repr__(self):
        return "'%s'@%s" % (self.term, self.link)
    
    @classmethod
    def indexkey(cls, term):
        return term.alphaterm
    @classmethod
    def sortkey(cls, term):
        return term.alphaterm.lower()

def extract_text(elt):
    """
    Get the plain-text from this element
    """
    if elt.nodeType == elt.TEXT_NODE:
        return elt.data
    elif elt.nodeType == elt.ELEMENT_NODE:
        return ''.join(extract_text(e) for e in elt.childNodes)
    else:
        raise ValueError("unknown node type %i" % (elt.nodeType))

def get_id(elt, fname):
    depth = 0
    origelt = elt
    while not elt.hasAttribute('id'):
        if elt.tagName == 'section':
            raise ValueError('<section> without id in %s' % (fname))

        if elt.tagName == 'dd':
            # special case id-finder for stuff in a <dd>: link to the <dt>
            elt = elt.previousSibling
            while elt.nodeType != elt.ELEMENT_NODE or elt.tagName != 'dt':
                elt = elt.previousSibling
        elif elt.tagName in ['h2', 'h3']:
            # special case headings: assume they're first child of a <section>
            depth -= 1
            elt = elt.parentNode
        elif elt.tagName == 'a':
            # special case links: the add a unimportant level of depth
            depth -= 1
            elt = elt.parentNode
        else:
            elt = elt.parentNode
        depth += 1

    ident = elt.getAttribute('id')
    good_id = depth < 2 or elt.tagName in ['dt', 'figure']

    # kind of suggest that the element or at least its parent has an id to link to
    if not good_id:
        sys.stderr.write("'%s' in %s has no id nearby.\n" % (origelt, fname))
    
    return ident


def index_elt(contents, fname, elt):
    """
    Add entry to index data structure for this element
    """
    ident = get_id(elt, fname)
    alphaterm = None

    if elt.tagName == 'code':
       if elt.hasAttribute('data-term'):
           text = elt.getAttribute('data-term')
       else:
           text = extract_text(elt)

       if u'\u2026' in text:
           pos = text.find(u'\u2026')
           text = text[:pos]
       alphaterm = text
       alphaterm = alphaterm.replace('<', '')
       alphaterm = alphaterm.replace('>', '')
       alphaterm = alphaterm.replace('&', '')
       alphaterm = alphaterm.replace('.', '')
       
       codetype = elt.getAttribute('class').split()[0]
       
       text = '<code class="%s">%s</code> <span class="codetype">(%s)</span>' % (codetype, escape(text), codetype.upper())

    elif elt.hasAttribute('data-term'):
       text = elt.getAttribute('data-term')
    else:
       text = extract_text(elt)

    link = fname + '#' + ident
    topic = contents[basename(fname)]

    term = IndexTerm(text, link, topic, alphaterm=alphaterm)
    return term

def find_elements(elt):
    if elt.nodeType == elt.ELEMENT_NODE:
        classes = elt.getAttribute('class').split()
        if 'dfn' in classes:
            yield elt
        if elt.tagName == 'dfn':
            yield elt
        else:
            for c in elt.childNodes:
                for e in find_elements(c):
                    yield e

def find_terms(infiles):
    contents = _read_contents()
    for f in infiles:
        if '/intro' in f:
            # don't index introduction material
            continue
        assert f.startswith('_site/')
        link = f[6:]
        doc = html5lib.parse(open(f).read(), treebuilder="dom")
        
        for d in find_elements(doc.documentElement):
            yield index_elt(contents, link, d)

def collect_terms(infiles):
    """
    Collect all <dfn>s in the documents into a data structure
    """
    terms = list(find_terms(infiles))
    terms.sort(key=IndexTerm.sortkey)
    collected = itertools.groupby(terms, key=IndexTerm.indexkey)
    return collected

def build_index(terms):
    """
    Build the HTML for the index list
    """
    items = []
    for key, kterms in terms:
        out = []
        for t in kterms:
            out.append('<a href="%s">%s</a>' % (escape(t.link), t.topic))
        items.append('<li><span class="term">' + t.term + '</span>: ' + ('; '.join(out)) + '</li>')
    return '\n'.join(items)

def render_index(content):
    """
    Render the index into a page
    """
    template_text = TEMPLATE_START + content + TEMPLATE_END
    return process_jinja(template_text, CONTEXT)

def generate_index(outfile, infiles):
    terms = collect_terms(infiles)
    index_content = build_index(terms)
    content = render_index(index_content)
    with open(outfile, 'w') as fh:
        fh.write(content)


if __name__ == '__main__':
    generate_index(sys.argv[1], sys.argv[2:])
