from jinja2 import Environment, FileSystemLoader, Template, contextfilter
import json
import os.path
from collections import OrderedDict

def get_context(infile):
    depth = infile.count('/')
    rellink = '../' * depth
    return {'rellink': rellink, 'input_file': infile}

svg_template = Template("""<figure id="fig-{{ filebase }}" class="{{ figureclass }}"><img src="../{{ directory }}/{{ filebase }}.{{ extension }}" alt="{{ caption }}"><figcaption>{{ caption }}&nbsp;<a href="{{rellink}}references.html">*</a></figcaption></figure>""")

@contextfilter
def figure(context, filebase, caption, figureclass='block', extension='png', directory='figures'):
    """
    Output the markup for an image figure
    """
    context = {
        'rellink': context['rellink'],
        'directory': directory,
        'filebase': filebase,
        'caption': caption,
        'figureclass': figureclass,
        'extension': extension,
    }
    return svg_template.render(context)

@contextfilter
def floatfigure(context, filebase, caption, figureclass=None, extension='png'):
    cls = 'floating'
    if figureclass:
        cls += ' ' + figureclass

    return figure(context, filebase=filebase, caption=caption, figureclass=cls, extension=extension,
        directory='floats')


def contents(_):
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

@contextfilter
def subcontents(context, _):
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

@contextfilter
def pagetitle(context, _):
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
        
@contextfilter
def xref(context, chap):
    """
    Output a cross-reference to another section
    """
    data = json.load(open('contents.json'))
    contents = _read_contents()
    title = contents[chap]
    return '<a href="%s.html" class="xref">%s</a>' % (chap, title)
    


environment = Environment(
        loader=FileSystemLoader(['.', '_layouts']),
        )
environment.filters['figure'] = figure
environment.filters['floatfigure'] = floatfigure
environment.filters['contents'] = contents
environment.filters['subcontents'] = subcontents
environment.filters['pagetitle'] = pagetitle
environment.filters['xref'] = xref


  
