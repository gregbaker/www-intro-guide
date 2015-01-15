#!/usr/bin/env python

import sys
from jinja_environment import environment, get_context

def jinga_process(infile, outfile):
    template = environment.get_template(infile)
    context = get_context(infile)
    output = template.render(context).rstrip()
    
    with file(outfile, 'wb') as fh:
        fh.write(output)


if __name__ == '__main__':
    jinga_process(sys.argv[1], sys.argv[2])
