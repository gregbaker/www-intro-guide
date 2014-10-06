from jinja2 import Environment, FileSystemLoader, Template, Markup, \
    contextfilter, contextfunction, escape
import json
import os.path
from collections import OrderedDict

def get_context(infile):
    depth = infile.count('/')
    rellink = '../' * depth
    return {'rellink': rellink, 'input_file': infile}

svg_template = Template("""<figure id="fig-{{ filebase }}" class="{{ figureclass }}"><img src="../{{ directory }}/{{ filebase }}.{{ extension }}" alt="{{ caption }}"><figcaption>{{ caption }}{{ reference_link }}</figcaption></figure>""")

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
    return svg_template.render(context)

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
        
@contextfunction
def xref(context, chap):
    """
    Output a cross-reference to another section
    """
    data = json.load(open('contents.json'))
    contents = _read_contents()
    title = contents[chap]
    return '<a href="%s.html" class="xref">%s</a>' % (chap, title)
    

def include_output(name):
    return '<blockquote class="output">%s</blockquote>' % (loader.get_source(environment, name)[0])

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
        preclass = codeclass
    return '<blockquote%s>\n<pre class="%s">%s</pre>\n</blockquote>' % (figid, preclass, escape(content))

def quoted_code(filename, codeclass='html', syntaxhighlight=True):
    content = file(filename).read()
    figid = 'code-' + os.path.splitext(filename)[0]
    return block_code(content, ident=figid, codeclass=codeclass, syntaxhighlight=syntaxhighlight)



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

