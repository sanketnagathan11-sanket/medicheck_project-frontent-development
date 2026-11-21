import os, re

content = open('MediCheck.html', encoding='utf-8').read()

col_old = r'<th style="padding:\.5rem">Gender/DOB/Blood</th>'
col_new = r'<th style="padding:.5rem">Gender</th>\n                <th style="padding:.5rem">DOB</th>\n                <th style="padding:.5rem">Blood</th>'

content = re.sub(col_old, col_new, content)

val_old = r"<td style=\"padding:\.5rem\">\$\{p\.gender \|\| '-'\} \(\$\{p\.dob \|\| '-'\}\) \[\$\{p\.blood_group \|\| '-'\}\]</td>"
val_new = r"<td style=\"padding:.5rem\">${p.gender || '-'}</td>\n                  <td style=\"padding:.5rem\">${p.dob || '-'}</td>\n                  <td style=\"padding:.5rem\">${p.blood_group || '-'}</td>"

content = re.sub(val_old, val_new, content)

open('MediCheck.html', 'w', encoding='utf-8').write(content)
print("Updated columns!")
