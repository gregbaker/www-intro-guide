import sys

def rstrip_file(infile, outfile):
    with open(infile, 'rb') as fh:
        data = fh.read()

    with open(outfile, 'wb') as fh:
        fh.write(data.rstrip())

if __name__ == '__main__':
    rstrip_file(sys.argv[1], sys.argv[2])
