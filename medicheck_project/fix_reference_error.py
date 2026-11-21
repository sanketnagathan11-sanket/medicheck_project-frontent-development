import re

c = open('MediCheck.html', encoding='utf-8').read()

c = re.sub(r'^\s*if\(patientsNav\).*?$\n', '', c, flags=re.MULTILINE)
c = re.sub(r'^\s*if\(profileNav\).*?$\n', '', c, flags=re.MULTILINE)

open('MediCheck.html', 'w', encoding='utf-8').write(c)
print("Fixed undeclared variables!")
