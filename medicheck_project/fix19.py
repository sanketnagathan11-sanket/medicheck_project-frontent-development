import os

content = open('MediCheck.html', encoding='utf-8').read()

auth_old = """  if(adminNav) adminNav.style.display = (session && session.type === 'staff') ? 'inline-block' : 'none';
  if(patientsNav) patientsNav.style.display = (session && session.type === 'staff' && session.role === 'Admin') ? 'inline-block' : 'none';
  if(profileNav) profileNav.style.display = (session && session.type === 'patient') ? 'inline-block' : 'none';"""

auth_new = """  let isStaff = (session && session.type === 'staff');
  let isAdmin = false;
  if (isStaff) {
    let staff = getStaff().find(s => s.staff_id === session.id);
    if (staff && staff.role === 'Admin') isAdmin = true;
  }

  if(adminNav) adminNav.style.display = isStaff ? 'inline-block' : 'none';
  if(patientsNav) patientsNav.style.display = isAdmin ? 'inline-block' : 'none';
  if(profileNav) profileNav.style.display = (session && session.type === 'patient') ? 'inline-block' : 'none';"""

if auth_old in content:
    content = content.replace(auth_old, auth_new)
    print("Patched Auth Nav logic")
else:
    print("Failed Auth Nav logic patch")

open('MediCheck.html', 'w', encoding='utf-8').write(content)
