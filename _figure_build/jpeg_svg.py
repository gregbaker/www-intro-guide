#!/usr/bin/env python

import string, base64, os

output = '../figures/jpeg.svg'

qualities = [None, 90, 70, 50, 30, 10]
n_samples = len(qualities)
sample_h = 80 # double actual image size for visibility
sample_w = 360
sample_sep = 5
total_h = (n_samples) * (sample_h + sample_sep) - sample_sep
total_w = sample_w + 135

svg_template = string.Template("""<svg height="%i" width="%i" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
${body}
</svg>""" % (total_h, total_w))

block_template = string.Template("""
<image xlink:href="${url}" x="0" y="${img_y}" height="${sample_h}px" width="${sample_w}px"/>
<text style="font-family: &quot;Source Sans Pro&quot;,&quot;Helvetica&quot;,sans-serif; font-size: 14px;" x="${text_x}" y="${size_y}">${size}</text>
<text style="font-family: &quot;Source Sans Pro&quot;,&quot;Helvetica&quot;,sans-serif; font-size: 14px;" x="${text_x}" y="${q_y}">${q}</text>
""")

body = []
for i, q in enumerate(qualities):
    if q is None:
        img_filename = 'photo-crop.png'
        qtxt = 'Original Image'
        sztxt = ''
    else:
        img_filename = 'photo-q%i-crop.png' % (q)
        jpeg_filename = 'photo-q%i.jpeg' % (q)
        qtxt = 'JPEG quality: %i' % (q)
        size = os.stat(jpeg_filename).st_size
        sztxt = 'File size: %i KB' % (size/1024)
    
    data = file(img_filename).read()
    url = "data:image/png;base64," + base64.b64encode(data)
    y = i*(sample_h + sample_sep)
    
    
    block = block_template.substitute({
        'sample_w': sample_w,
        'sample_h': sample_h,
        'text_x': sample_w + 10,

        'url': url,
        'img_y': y,

        'q': qtxt,
        'q_y': y+35,

        'size': sztxt,
        'size_y': y+55,
    })
    body.append(block)

with open(output, 'wb') as fh:
    fh.write(svg_template.substitute({
      'body': '\n'.join(body),
    }))

