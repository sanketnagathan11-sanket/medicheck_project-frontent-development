import re

c = open('MediCheck.html', encoding='utf-8').read()

old_logic = """    if(adminNav) adminNav.style.display = isStaff ? 'inline-block' : 'none';
    if(patientsNav) patientsNav.style.display = isAdmin ? 'inline-block' : 'none';
    if(profileNav) profileNav.style.display = (session && session.type === 'patient') ? 'inline-block' : 'none';"""

new_logic = """    if(adminNav) adminNav.style.display = isStaff ? 'inline-block' : 'none';
    if(patientsNav) patientsNav.style.display = 'none'; // Removed from admin as requested
    if(profileNav) profileNav.style.display = 'none'; // Removed from customer login as requested"""

c = c.replace(old_logic, new_logic)
open('MediCheck.html', 'w', encoding='utf-8').write(c)
print("Updated nav logic!")
