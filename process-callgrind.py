#! /usr/bin/python3

import getopt
import html
import sys

def cmdline_help():
    print('-i x   callgrind output file to process')
    print('-c     include context')
    print('-f     filter output')
    print('-h     this output')

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:cfh')
except getopt.GetoptError as err:
    print(err)
    cmdline_help()
    sys.exit(2)

input_file = None
filter_output = False
incl_context = False

for o, a in opts:
    if o == '-i':
        input_file = a
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
func = None

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
    elif line[0:3] == 'fn=':
        func = line[3:]
#    elif line[0:4] == 'cfn=':
#        func = line[4:]
    elif line[0] >= '0' and line[0] <= '9':
        if func[0:2] == '0x':
            continue

        parts = line.split()
        if len(parts) == 1:
            continue

        ln = int(parts[0])
        cost = int(parts[1])

        #curfile = cfile if cfile != None else file
        curfile = file

        if not curfile in data:
            data[curfile] = dict()

        if not func in data[curfile]:
            data[curfile][func] = dict()

        if ln in data[curfile][func]:
            #print(f'Duplicate definition for {curfile} {func} {ln} @ line {lnr}')
            pass
        else:
            data[curfile][func][ln] = cost
fh.close()

for file in data:
    try: 
        if file != None:
            data[file][' contents '] = [l.strip('\n') for l in open(file, 'r').readlines()]
    except FileNotFoundError as e:
        pass

print('<html>')
print('<body>')

for file in data:
    header_emitted = False
    for func in data[file]:
        if func != ' contents ':
            max_nr = 0
            suppress = False
            if " contents " in data[file]:
                for ln in data[file][func]:
                    if ln > len(data[file][" contents "]):
                        suppress = True
                        break
                    max_nr = max(max_nr, ln)
            else:
                suppress = True

            if suppress == False or filter_output == False:
                if header_emitted == False:
                    print(f'<h2>{file}</h2>')
                    header_emitted = True

                print(f'<h3>{func}</h3>')
                print(f'<table><tr><th>line number</th><th>const</th><th>contents</th></tr>')
                for ln in range(1, max_nr + 1):
                    text = html.escape(data[file][" contents "][ln - 1] if " contents " in data[file] and ln <= len(data[file][" contents "]) else "")
                    if ln in data[file][func]:
                        print(f'<tr><td>{ln}</td><td>{data[file][func][ln]}</td><td><pre>{text}</pre></td></tr>')
                    else:
                        print(f'<tr><td>{ln}</td><td></td><td><pre>{text}</pre></td></tr>')

                print('</table>')

print('</body>')
print('</html>')
