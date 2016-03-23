import os, subprocess
import re

gm_output = re.compile(r'^.* (\d+)x(\d+)\+0\+0 .*$')

def image_size(imgpath):
    imgpath = os.path.join('_site', imgpath)
    if imgpath.endswith('.svg'):
        # gm can't process SVG, but we already converted to PNG anyway
        imgpath = imgpath[:-4] + '.png'
    if imgpath.endswith('.svgz'):
        # gm can't process SVG, but we already converted to PNG anyway
        imgpath = imgpath[:-5] + '.png'

    cmd = subprocess.Popen(
            ['gm', 'identify', imgpath],
            stdout=subprocess.PIPE)
    output = cmd.stdout.read()
    
    match = gm_output.match(output)
    w = int(match.group(1))
    h = int(match.group(2))
    return w,h

def img_width_height(imgpath, scale=1.0):
    wh = image_size(imgpath)
    if not wh:
        return ''
    w, h = wh
    return 'width="%i" height="%i"' % (w*scale, h*scale)
