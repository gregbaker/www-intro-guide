from jinja2 import Environment, FileSystemLoader, Template, Markup, \
    contextfilter, contextfunction
from cgi import escape
import json
import os.path
import codecs, sys
from collections import OrderedDict
from img_process import img_width_height

GLOBALS = {
    'htmlref_url': 'https://developer.mozilla.org/en/docs/Web/Guide/HTML/HTML5/HTML5_element_list', # see also html_tag_ref_url() below
    'cssref_url': 'https://developer.mozilla.org/en-US/docs/Web/CSS/Reference', # see also css_prop_ref_url() below
    'jquery_url': 'https://code.jquery.com/jquery-2.2.0.min.js',
    'raphael_url': 'https://bit.ly/raphael-212_js',
    'raphref_url': 'http://dmitrybaranovskiy.github.io/raphael/reference.html', # see also raph_ref_url() below
    'raph': 'Rapha&euml;l',
    'jqueryui_version': '1.11.4',
    'copyright_year': '2015&ndash;2016',
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

figure_template = Template("""<figure id="fig-{{ filebase }}" class="{{ figureclass }}"><img src="{{rellink}}{{ imgpath }}" alt="{{ caption }}" {{widthheight}} />{% if caption %}<figcaption>{{ caption }}{{ reference_link }}</figcaption>{% endif %}</figure>""")

@contextfunction
def figure(context, filebase, caption, figureclass='block', extension='png', directory='figures', referenced=True):
    """
    Output the markup for an image figure
    """
    if referenced:
        reference_link = '&nbsp;<a href="%sreferences.html">*</a>' % (context['rellink'])
    else:
        reference_link = ''
    
    imgpath = '%s/%s.%s' % (directory, filebase, extension)
    wh = img_width_height(imgpath)
        
    context = {
        'rellink': context['rellink'],
        'widthheight': wh,
        'filebase': filebase,
        'imgpath': imgpath,
        'filebase': filebase,
        'caption': caption,
        'figureclass': figureclass,
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


def _section_parts(sections):
    for secparts in sections:
        try:
            sec_slug, sec_title = secparts
            cls = None
        except ValueError:
            sec_slug, sec_title, cls = secparts
        
        yield (sec_slug, sec_title, cls)


def contents():
    """
    Output the Table of Contents from the contents.json data.
    """
    from wordcount import wordcount
    total_wc = 0
    data = json.load(open('contents.json'))
    section = 'pre'
    res = ['<ol class="toc" id="preface">']
    for chapter in data:
        if section == 'pre' and 'preface' not in chapter:
            res.append('</ol>')
            res.append('<ol class="toc" id="contents">')
            section = 'contents'
        if section == 'contents' and 'appendix' in chapter and chapter['appendix']:
            res.append('</ol>')
            res.append('<ol class="toc" id="appendix">')
            section = 'appendix'

        chap_slug = chapter['chapter'][0]
        chap_title = chapter['chapter'][1]
        res.append('<li><a href="content/%s.html">%s</a>' % (chap_slug, chap_title))
        
        sections = chapter.get('contents', [])
        if sections:
            res.append('<ol>')
            for sec_slug, sec_title, cls in _section_parts(sections):
                slug = '%s-%s' % (chap_slug, sec_slug)
                wc = wordcount('content/%s.html' % (slug))
                total_wc += wc
                clscode = ''
                if cls:
                    clscode = ' class="%s"' % (cls,)
                res.append('<li%s><a href="content/%s.html">%s</a> <span class="wc">(%i; %i)</span></li>\n' % (clscode, slug, sec_title, wc, total_wc))
            res.append('</ol>')

        res.append('</li>\n')

    res.append('<li><a href="term_index.html">Index of Terms</a></li>')
    res.append('<li><a href="references.html">References</a></li>')
    res.append('<li><a href="copyright.html">Copyright Information</a></li>')
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
        sections = chapter.get('contents', [])
        if chap_slug == chapter_slug:
            res.append('<h2 id="contents">Contents</h2>')
            res.append('<ol class="chapter-toc toc">')
            for sec_slug, sec_title, cls in _section_parts(sections):
                clscode = ''
                if cls:
                    clscode = ' class="%s"' % (cls,)
                res.append('<li%s><a href="%s-%s.html">%s</a></li>' % (clscode, chap_slug, sec_slug, sec_title))
            res.append('</ol>')

    return ''.join(res)

@contextfunction
def pagetitle(context):
    infile = context['input_file']
    fn = os.path.split(infile)[-1]
    basename = os.path.splitext(fn)[0]
    
    if basename.startswith('exer'):
        return 'Exercise ' + basename[4:]
    elif basename.startswith('assign'):
        return 'Assignment ' + basename[6:]
    elif basename == 'term_index':
        return 'Index of Terms'
    elif basename == 'references':
        return 'References and Sources'
    elif basename == 'copyright':
        return 'Copyright Information'
    elif basename == 'intro':
        return 'Course Introduction'
    
    data = json.load(open('contents.json'))
    for chapter in data:
        chap_slug = chapter['chapter'][0]
        if chap_slug == basename:
            return chapter['chapter'][1]
        sections = chapter.get('contents', [])
        for sec_slug, sec_title, cls in _section_parts(sections):
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
        sections = chapter.get('contents', [])
        for sec_slug, sec_title, cls in _section_parts(sections):
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
    return '<a href="%scontent/%s.html%s" class="xref">%s</a>' % (context['rellink'], chap, frag, text)
    
@contextfunction
def chapterlabel(context):
    infile = context['input_file']
    fn = os.path.split(infile)[-1]
    basename = os.path.splitext(fn)[0]
    
    if '-' in basename:
        return basename.split('-')[0]
    else:
        return basename


def include_output(name, cls=''):
    text = loader.get_source(environment, name)[0].rstrip()
    return u'<blockquote class="output %s">%s</blockquote>' % (cls, text)

def check_line_len(filename, text):
    maxlen = max(len(line.rstrip()) for line in text.splitlines())
    if maxlen > 70:
        sys.stderr.write("%s has long lines (%i chars)." % (filename, maxlen))

def include_escaped(name):
    text = loader.get_source(environment, name)[0]
    check_line_len(name, text)
    return escape(text.rstrip())

def block_code(content, ident=None, codeclass='html', syntaxhighlight=True):
    if ident:
        figid = ' id="%s"' % (ident,)
    else:
        figid = ''

    if codeclass == 'svg':
        codeclass = 'xml svg'

    if syntaxhighlight:
        preclass = 'brush: ' + codeclass
    else:
        preclass = codeclass + " code"
    
    text = content.rstrip()
    check_line_len(ident, text)
    res = u'<blockquote%s>\n<pre class="%s">%s</pre>\n</blockquote>' % (figid, preclass, escape(text))
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
    
    content = process_jinja(content).rstrip()

    return block_code(content, ident=figid, codeclass=codeclass, syntaxhighlight=syntaxhighlight)

def html_tag_ref_url(elt):
    return 'https://developer.mozilla.org/en/docs/Web/HTML/Element/%s' % (elt)

def css_prop_ref_url(prop):
    return 'https://developer.mozilla.org/en-US/docs/Web/CSS/%s' % (prop)

def css_dt(prop):
    # avoid repetition on css-properties.html
    return '<dt id="%s"><a href="%s"><code class="css dfn">%s</code></a></dt>' % (prop, css_prop_ref_url(prop), prop)

def raph_ref_url(obj, meth):
    return GLOBALS['raphref_url'] + '#%s.%s' % (obj, meth)

def timing(semester, week):
    """Timing note for lecture notes"""
    return '<aside class="timing t%s">%s end of week %i</aside>' % (semester, semester, week)

@contextfilter
def markdown(context, value):
    from markdown import markdown as md
    return md(value, output_format='xhtml5')

def process_jinja(template_text, context={}):
    """
    Return result of processing template text in our standard environment.
    """
    template = environment.from_string(template_text)
    return template.render(context).rstrip()


loader = FileSystemLoader(['.', '_layouts'])
environment = Environment(
        loader=loader,
        )
environment.filters['markdown'] = markdown
environment.globals['figure'] = figure
environment.globals['floatfigure'] = floatfigure
environment.globals['contents'] = contents
environment.globals['subcontents'] = subcontents
environment.globals['pagetitle'] = pagetitle
environment.globals['chapterlabel'] = chapterlabel
environment.globals['xref'] = xref
environment.globals['include_output'] = include_output
environment.globals['include_escaped'] = include_escaped
environment.globals['quoted_code'] = quoted_code
environment.globals['block_code'] = block_code
environment.globals['html_tag_ref_url'] = html_tag_ref_url
environment.globals['css_prop_ref_url'] = css_prop_ref_url
environment.globals['css_dt'] = css_dt
environment.globals['raph_ref_url'] = raph_ref_url
environment.globals['timing'] = timing
environment.globals['crumbsep'] = ' &rarr; '
environment.globals.update(GLOBALS)
