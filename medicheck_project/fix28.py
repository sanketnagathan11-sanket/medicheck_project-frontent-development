import os, re

content = open('MediCheck.html', encoding='utf-8').read()

def replace_func(func_name, text, new_impl):
    pattern = r"function\s+" + func_name + r"\s*\(\)\s*\{"
    match = re.search(pattern, text)
    if not match:
        print(f"Could not find {func_name}")
        return text
    start = match.start()
    idx = text.find('{', start)
    stack = 1
    i = idx + 1
    while i < len(text) and stack > 0:
        if text[i] == '{': stack += 1
        elif text[i] == '}': stack -= 1
        i += 1
    
    return text[:start] + new_impl + text[i:]


update_profile_new = """function updateProfile() {
      const session = ls('session');
      if(!session || session.type !== 'patient') return;
      const newName = document.getElementById('prof-name').value.trim();
      const newEmail = document.getElementById('prof-email').value.trim();
      const newAddress = document.getElementById('prof-address').value.trim();
      const newPass = document.getElementById('prof-password').value;
      if(!newName) { flash('Name cannot be empty', 'danger'); return; }
      let patients = getPatients();
      let p = patients.find(p => p.patient_id === session.id);
      if(p) {
        p.full_name = newName;
        p.email = newEmail;
        p.address = newAddress;
        if(newPass) p.password = newPass;
        lsSet('patients', patients);
        session.name = newName;
        lsSet('session', session);
        flash('Profile updated successfully!', 'success');
        renderProfile();
      }
    }"""

content = replace_func('updateProfile', content, update_profile_new)

open('MediCheck.html', 'w', encoding='utf-8').write(content)
print("updateProfile fixed!")
