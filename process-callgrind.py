#! /usr/bin/python3

import sys

data = dict()
mcnt = 0

file = None
cfile = None
func = None

lnr = 0
fh = open(sys.argv[1], 'r')
for line in fh.readlines():
    lnr += 1
    line = line.strip()
    if line == '':
        continue
    if line[0:3] == 'fl=':
        file = line[3:]
    elif line[0:4] == 'cfl=' or line[0:4] == 'cfi=':
        cfile = line[4:]
    elif line[0:3] == 'fn=':
        func = line[3:]
    elif line[0:4] == 'cfn=':
        func = line[4:]
    elif line[0] >= '0' and line[0] <= '9':
        parts = line.split()
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
            data[file][' contents '] = [l.strip() for l in open(file, 'r').readlines()]
    except FileNotFoundError as e:
        pass

for file in data:
    for func in data[file]:
        if func != ' contents ':
            for ln in data[file][func]:
                print(f'{file} {func} {ln} {data[file][" contents "][ln] if " contents " in data[file] and ln < len(data[file][" contents "]) else ""}')
