import os
content = open('MediCheck.html', encoding='utf-8').read()

start_idx = content.find("    if (isAdmin) {\n      let customerHTML =")
if start_idx == -1:
    print("Could not find start_idx!")
else:
    end_idx = content.find("  function renderPatients() {", start_idx)
    if end_idx == -1:
        print("Could not find end_idx!")
    else:
        # We want to replace everything from start_idx to end_idx with just "}\n\n"
        # because renderAdmin should just end there.
        new_content = content[:start_idx] + "}\n\n" + content[end_idx:]
        open('MediCheck.html', 'w', encoding='utf-8').write(new_content)
        print("Syntax fixed successfully!")
