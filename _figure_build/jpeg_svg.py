#!/usr/bin/env python

import string, base64, os

output = '../figures/jpeg.svg'

qualities = [90, 70, 50, 30, 10]
n_samples = len(qualities)
sample_h = 80
sample_w = 300
sample_sep = 5
total_h = n_samples * (sample_h + sample_sep) - sample_sep
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
    img_filename = "photo-q%i-crop.png" % (q)
    jpeg_filename = "photo-q%i.jpeg" % (q)
    
    size = os.stat(jpeg_filename).st_size
    data = file(img_filename).read()
    url = "data:image/png;base64," + base64.b64encode(data)
    y = i*(sample_h + sample_sep)
    
    block = block_template.substitute({
        'sample_w': sample_w,
        'sample_h': sample_h,
        'text_x': sample_w + 10,

        'url': url,
        'img_y': y,

        'q': 'JPEG quality: %i' % (q),
        'q_y': y+35,

        'size': "File size: %i KB" % (size/1024),
        'size_y': y+55,
    })
    body.append(block)

with open(output, 'wb') as fh:
    fh.write(svg_template.substitute({
      'body': '\n'.join(body),
    }))

