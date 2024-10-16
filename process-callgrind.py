#! /usr/bin/python3

import getopt
import html
import sys

def cmdline_help():
    print('-i x   callgrind output file to process')
    print('-o x   output directory (must exist)')
    print('-c     include context')
    print('-f     filter output')
    print('-h     this output')

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:o:cfh')
except getopt.GetoptError as err:
    print(err)
    cmdline_help()
    sys.exit(2)

output_dir = None
input_file = None
filter_output = False
incl_context = False

for o, a in opts:
    if o == '-i':
        input_file = a
    elif o == '-o':
        output_dir = a
    elif o == '-f':
        filter_output = True
    elif o == '-c':
        incl_context = True
    elif o == '-h':
        cmdline_help()
        sys.exit(0)
    else:
        cmdline_help()
        sys.exit(1)

if input_file == None:
    print('No file selected')
    print()
    cmdline_help()
    sys.exit(1)

data = dict()
mcnt = 0

file = None
cfile = None

lnr = 0
fh = open(input_file, 'r')
for line in fh.readlines():
    lnr += 1
    line = line.strip()
    if line == '':
        continue
    if line[0:3] == 'fl=':
        cfile = file = line[3:]
    elif line[0:4] == 'cfl=' or line[0:4] == 'cfi=':
        cfile = line[4:]
    elif line[0] >= '0' and line[0] <= '9':
        parts = line.split()
        if len(parts) == 1:
            continue

        ln = int(parts[0])
        cost = int(parts[1])

        #curfile = cfile if cfile != None else file
        curfile = file

        if not curfile in data:
            data[curfile] = dict()

        if ln in data[curfile]:
            #print(f'Duplicate definition for {curfile} {ln} @ line {lnr}')
            pass
        else:
            data[curfile][ln] = cost
fh.close()

contents = dict()
for file in data:
    try: 
        if file != None:
            contents[file] = [l.strip('\n') for l in open(file, 'r').readlines()]
    except FileNotFoundError as e:
        pass

fhi = open(output_dir + '/index.html', 'w')
fhi.write('<html>\n')
fhi.write('<body>\n')
fhi.write('<ul>\n')

fho = None

for file in sorted(data):
    max_nr = 0
    suppress = False
    if file in contents:
        n_lines = len(contents[file])
        for ln in data[file]:
            if ln > n_lines:
                suppress = True
                break
            max_nr = max(max_nr, ln)
    else:
        suppress = True

    if suppress == False or filter_output == False:
        fname = str(abs(hash(file))) + '.html'
        fhi.write(f'<li><a href="{fname}">{file}</a>\n')
        fho = open(output_dir + '/' + fname, 'w')
        fho.write('<html>\n')
        fho.write('<body>\n')
        fho.write(f'<h2>{file}</h2>\n')
        header_emitted = True

        fho.write(f'<table><tr><th>line number</th><th>const</th><th>contents</th></tr>\n')
        for ln in range(1, max_nr + 1):
            text = html.escape(contents[file][ln - 1] if file in contents and ln <= len(contents[file]) else "")
            if ln in data[file] and data[file][ln] > 0:
                fho.write(f'<tr><td>{ln}</td><td>{data[file][ln]}</td><td><pre>{text}</pre></td></tr>\n')
            else:
                fho.write(f'<tr><td>{ln}</td><td>-</td><td><pre>{text}</pre></td></tr>\n')

        fho.write('</table>\n')

        fho.write('</body>\n')
        fho.write('</html>\n')
        fho.close()
        fho = None

fhi.write('</body>\n')
fhi.write('</html>\n')
fhi.close()
