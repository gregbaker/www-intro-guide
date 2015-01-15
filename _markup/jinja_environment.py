from jinja2 import Environment, FileSystemLoader, Template, Markup, \
    contextfilter, contextfunction
from cgi import escape
import json
import os.path
import codecs, sys
from collections import OrderedDict

GLOBALS = {
    'htmlref_url': 'https://developer.mozilla.org/en/docs/Web/Guide/HTML/HTML5/HTML5_element_list',
    'jquery_url': 'https://code.jquery.com/jquery-2.1.3.min.js',
}

# https://stackoverflow.com/questions/5040532/python-ascii-codec-cant-decode-byte
reload(sys)
sys.setdefaultencoding('utf-8')

def get_context(infile):
    depth = infile.count('/')
    rellink = '../' * depth
    if depth == 0:
        indexlink = './'
    else:
        indexlink = rellink

    return {'rellink': rellink, 'indexlink': indexlink, 'input_file': infile}

figure_template = Template("""<figure id="fig-{{ filebase }}" class="{{ figureclass }}"><img src="../{{ directory }}/{{ filebase }}.{{ extension }}" alt="{{ caption }}"><figcaption>{{ caption }}{{ reference_link }}</figcaption></figure>""")

@contextfunction
def figure(context, filebase, caption, figureclass='block', extension='png', directory='figures', referenced=True):
    """
    Output the markup for an image figure
    """
    if referenced:
        reference_link = '&nbsp;<a href="%sreferences.html">*</a>' % (context['rellink'])
    else:
        reference_link = ''
    context = {
        'directory': directory,
        'filebase': filebase,
        'caption': caption,
        'figureclass': figureclass,
        #'extension': 'png' if extension=='svg' else extension,
        'extension': extension,
        'reference_link': reference_link,
    }
    return figure_template.render(context)

@contextfunction
def floatfigure(context, filebase, caption, figureclass=None, extension='png'):
    cls = 'floating'
    if figureclass:
        cls += ' ' + figureclass

    return figure(context, filebase=filebase, caption=caption, figureclass=cls, extension=extension,
        directory='floats')


def contents():
    """
    Output the Table of Contents from the contents.json data.
    """
    data = json.load(open('contents.json'))
    res = ['<ol id="toc">']
    for chapter in data:
        chap_slug = chapter['chapter'][0]
        chap_title = chapter['chapter'][1]
        sections = chapter['contents']
        res.append('<li><a href="content/%s.html">%s</a>' % (chap_slug, chap_title))
        if sections:
            res.append('<ol>')
            for sec_slug, sec_title in sections:
                res.append('<li><a href="content/%s-%s.html">%s</a></li>' % (chap_slug, sec_slug, sec_title))
            res.append('</ol>')

        res.append('</li>')
    res.append('</ol>')
    return ''.join(res)

@contextfunction
def subcontents(context):
    """
    Output one chapter's Contents from the contents.json data.
    """
    infile = context['input_file']
    fn = os.path.split(infile)[-1]
    chapter_slug = os.path.splitext(fn)[0]

    data = json.load(open('contents.json'))
    res = []
    for chapter in data:
        chap_slug = chapter['chapter'][0]
        sections = chapter['contents']
        if chap_slug == chapter_slug:
            res.append('<h2 id="contents">Contents</h2>')
            res.append('<ol class="chapter-toc">')
            for sec_slug, sec_title in sections:
                res.append('<li><a href="%s-%s.html">%s</a></li>' % (chap_slug, sec_slug, sec_title))
            res.append('</ol>')

    return ''.join(res)

@contextfunction
def pagetitle(context):
    infile = context['input_file']
    fn = os.path.split(infile)[-1]
    basename = os.path.splitext(fn)[0]
    
    data = json.load(open('contents.json'))
    for chapter in data:
        chap_slug = chapter['chapter'][0]
        if chap_slug == basename:
            return chapter['chapter'][1]
        sections = chapter['contents']
        for sec_slug, sec_title in sections:
            if chap_slug + '-' + sec_slug == basename:
                return sec_title
    
    return ''

def _read_contents():
    data = json.load(open('contents.json'))
    contents = OrderedDict()
    for chapter in data:
        chap_slug = chapter['chapter'][0]
        chap_title = chapter['chapter'][1]
        contents[chap_slug] = chap_title
        sections = chapter['contents']
        for sec_slug, sec_title in sections:
            contents[chap_slug + '-' + sec_slug] = sec_title
    return contents

def basename(fn):
    return os.path.splitext(os.path.split(fn)[1])[0]

@contextfunction
def xref(context, chap, text=None, fragment=None):
    """
    Output a cross-reference to another section
    """
    data = json.load(open('contents.json'))
    if text is None:
        contents = _read_contents()
        text = contents[chap]
    frag = ''
    if fragment:
        frag = '#' + fragment    
    return '<a href="%s.html%s" class="xref">%s</a>' % (chap, frag, text)
    

def include_output(name):
    return u'<blockquote class="output">%s</blockquote>' % (loader.get_source(environment, name)[0])

def include_escaped(name):
    text = loader.get_source(environment, name)[0]
    return escape(text)

def block_code(content, ident=None, codeclass='html', syntaxhighlight=True):
    if ident:
        figid = ' id="%s"' % (ident,)
    else:
        figid = ''
    if syntaxhighlight:
        preclass = 'brush: ' + codeclass
    else:
        preclass = codeclass + " code"
    
    res = u'<blockquote%s>\n<pre class="%s">%s</pre>\n</blockquote>' % (figid, preclass, escape(content))
    return res.encode('utf8')

def quoted_code(filename, codeclass=None, syntaxhighlight=True, ident=None):
    content = codecs.open(filename, encoding='utf-8').read()
    if not codeclass:
        _, ext = os.path.splitext(filename)
        codeclass = ext[1:]
    if ident:
        figid = ident
    else:
        figid = 'code-' + os.path.splitext(os.path.split(filename)[-1])[0]
    
    content = process_jinga(content)
        
    return block_code(content, ident=figid, codeclass=codeclass, syntaxhighlight=syntaxhighlight)


def process_jinga(template_text, context={}):
    """
    Return result of processing template text in our standard environment.
    """
    template = environment.from_string(template_text)
    return template.render(context)


loader = FileSystemLoader(['.', '_layouts'])
environment = Environment(
        loader=loader,
        )
environment.globals['figure'] = figure
environment.globals['floatfigure'] = floatfigure
environment.globals['contents'] = contents
environment.globals['subcontents'] = subcontents
environment.globals['pagetitle'] = pagetitle
environment.globals['xref'] = xref
environment.globals['include_output'] = include_output
environment.globals['include_escaped'] = include_escaped
environment.globals['quoted_code'] = quoted_code
environment.globals['block_code'] = block_code
environment.globals.update(GLOBALS)
