import os, re
content = open('MediCheck.html', encoding='utf-8').read()

pattern = r"\s*if \(isAdmin\) \{\s*let customerHTML = `<h2.*?workloadDiv\.parentElement\.appendChild\(div\);\s*\}\s*\}\s*\}\s*\}\s*"
match = re.search(pattern, content, re.DOTALL)
if match:
    # Just close the renderAdmin function with a single bracket
    new_content = content[:match.start()] + "\n}\n\n" + content[match.end():]
    open('MediCheck.html', 'w', encoding='utf-8').write(new_content)
    print("Syntax fixed successfully via regex!")
else:
    print("Could not find regex pattern!")
