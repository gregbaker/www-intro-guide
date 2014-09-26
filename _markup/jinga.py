#!/usr/bin/env python

import fileinput, sys
from jinja_environment import environment, get_context

def main(infile, outfile):
    template = environment.get_template(infile)
    context = get_context(infile)
    output = template.render(context)
    
    with file(outfile, 'wb') as fh:
        fh.write(output)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
