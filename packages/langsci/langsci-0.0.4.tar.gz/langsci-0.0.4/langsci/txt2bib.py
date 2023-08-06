import sys 
import langsci
try:
    from langscibibtex import Record 
except ImportError:
    from langsci.langscibibtex import Record

filename = sys.argv[1]
lines = open(filename).readlines()
for l in lines: 
    if l.strip=='':
        continue
    r = Record(l) 
    print(r.bibstring) 