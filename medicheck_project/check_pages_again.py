import re
c = open('MediCheck.html', encoding='utf-8').read()
for p in re.findall(r'<div id="page-[^"]+"', c):
    print(p)
