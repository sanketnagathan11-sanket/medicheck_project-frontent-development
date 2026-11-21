import os, re

content = open('MediCheck.html', encoding='utf-8').read()

pattern = r"(lsSet\('session',\{type:'patient',id:patient\.patient_id,name:patient\.full_name\}\);\s*authLocked=false; closeAuth\(\); updateAuthNav\(\); showPage\(')home('\);)"
new_content = re.sub(pattern, r"\g<1>bookings\g<2>", content)

if content != new_content:
    print("Regex replaced")
    open('MediCheck.html', 'w', encoding='utf-8').write(new_content)
else:
    print("Regex failed")
