import re

c = open('MediCheck.html', encoding='utf-8').read()

# 1. Remove nav links
c = re.sub(r'<a id="nav-profile".*?</a>', '', c)
c = re.sub(r'<a id="nav-patients".*?</a>', '', c)

# 2. Remove from updateAuthNav logic
c = re.sub(r'const profileNav\s*=\s*document\.getElementById\(\'nav-profile\'\);', '', c)
c = re.sub(r'const patientsNav\s*=\s*document\.getElementById\(\'nav-patients\'\);', '', c)
c = re.sub(r'if\(patientsNav\)\s*patientsNav\.style\.display\s*=\s*\'none\';.*?\n', '', c)
c = re.sub(r'if\(profileNav\)\s*profileNav\.style\.display\s*=\s*\'none\';.*?\n', '', c)

# 3. Remove showPage calls
c = re.sub(r'if\(name===\'profile\'\)\s*renderProfile\(\);', '', c)
c = re.sub(r'if\(name===\'patients\'\)\s*renderPatients\(\);', '', c)

# 4. Remove HTML pages
def remove_page(html, page_id):
    start = html.find(f'<div id="{page_id}"')
    if start == -1: return html
    # find the next page
    end = html.find('<div id="page-', start + 5)
    if end == -1:
        end = html.find('</main>', start)
    # let's try to grab up to the next <!-- PAGE comment if it exists
    end_comment = html.rfind('<!--', start, end)
    if end_comment != -1 and "PAGE" in html[end_comment:end]:
        end = end_comment
    return html[:start] + html[end:]

c = remove_page(c, 'page-profile')
c = remove_page(c, 'page-patients')

open('MediCheck.html', 'w', encoding='utf-8').write(c)
print("Removed pages!")
