import os, re

content = open('MediCheck.html', encoding='utf-8').read()

html_new = """            <!-- Editable Fields -->
            <div style="text-align:left; display:flex; flex-direction:column; gap:1rem;">
               <div style="background:#f8fafc; padding:1rem 1.25rem; border-radius:10px; border:1px solid #e2e8f0;">
                 <label style="font-size:.75rem; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:.3rem; display:block;">Full Name</label>
                 <input type="text" id="prof-name" style="width:100%; background:transparent; border:none; font-weight:600; font-size:.95rem; color:var(--text); outline:none;">
               </div>
               <div style="background:#f8fafc; padding:1rem 1.25rem; border-radius:10px; border:1px solid #e2e8f0;">
                 <label style="font-size:.75rem; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:.3rem; display:block;">Email</label>
                 <input type="email" id="prof-email" style="width:100%; background:transparent; border:none; font-weight:600; font-size:.95rem; color:var(--text); outline:none;">
               </div>
               
               <div style="display:flex; gap:1rem;">
                 <div style="flex:1; background:#f8fafc; padding:1rem 1.25rem; border-radius:10px; border:1px solid #e2e8f0; opacity:0.8;">
                   <label style="font-size:.75rem; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:.3rem; display:block;">Phone 🔒</label>
                   <input type="text" id="prof-phone" disabled style="width:100%; background:transparent; border:none; font-weight:600; font-size:.95rem; color:var(--muted); outline:none;">
                 </div>
                 <div style="flex:1; background:#f8fafc; padding:1rem 1.25rem; border-radius:10px; border:1px solid #e2e8f0; opacity:0.8;">
                   <label style="font-size:.75rem; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:.3rem; display:block;">DOB 🔒</label>
                   <input type="text" id="prof-dob" disabled style="width:100%; background:transparent; border:none; font-weight:600; font-size:.95rem; color:var(--muted); outline:none;">
                 </div>
               </div>
               
               <div style="display:flex; gap:1rem;">
                 <div style="flex:1; background:#f8fafc; padding:1rem 1.25rem; border-radius:10px; border:1px solid #e2e8f0; opacity:0.8;">
                   <label style="font-size:.75rem; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:.3rem; display:block;">Gender 🔒</label>
                   <input type="text" id="prof-gender" disabled style="width:100%; background:transparent; border:none; font-weight:600; font-size:.95rem; color:var(--muted); outline:none;">
                 </div>
                 <div style="flex:1; background:#f8fafc; padding:1rem 1.25rem; border-radius:10px; border:1px solid #e2e8f0; opacity:0.8;">
                   <label style="font-size:.75rem; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:.3rem; display:block;">Blood 🔒</label>
                   <input type="text" id="prof-blood" disabled style="width:100%; background:transparent; border:none; font-weight:600; font-size:.95rem; color:var(--muted); outline:none;">
                 </div>
               </div>
  
               <div style="background:#f8fafc; padding:1rem 1.25rem; border-radius:10px; border:1px solid #e2e8f0;">
                 <label style="font-size:.75rem; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:.3rem; display:block;">Address</label>
                 <input type="text" id="prof-address" style="width:100%; background:transparent; border:none; font-weight:600; font-size:.95rem; color:var(--text); outline:none;">
               </div>
               <div style="background:#f8fafc; padding:1rem 1.25rem; border-radius:10px; border:1px solid #e2e8f0;">
                 <label style="font-size:.75rem; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:.3rem; display:block;">Change Password</label>
                 <input type="password" id="prof-password" placeholder="Leave blank to keep..." style="width:100%; background:transparent; border:none; font-weight:600; font-size:.95rem; color:var(--text); outline:none;">
               </div>
            </div>"""

start_idx = content.find("<!-- Editable Fields -->")
end_idx = content.find("</button>", start_idx) # finds the first button after Editable Fields, wait.

# let's be more precise
end_idx = content.find('<button class="btn btn-teal"', start_idx)

if start_idx != -1 and end_idx != -1:
    new_content = content[:start_idx] + html_new + "\n            " + content[end_idx:]
    open('MediCheck.html', 'w', encoding='utf-8').write(new_content)
    print("Replaced HTML fields")
else:
    print("Failed to find boundaries")
    
# Also fix renderProfile logic!
def replace_func_renderProfile(text):
    pattern = r"function\s+renderProfile\s*\(\)\s*\{"
    match = re.search(pattern, text)
    if not match:
        return text
    start = match.start()
    idx = text.find('{', start)
    stack = 1
    i = idx + 1
    while i < len(text) and stack > 0:
        if text[i] == '{': stack += 1
        elif text[i] == '}': stack -= 1
        i += 1
    
    old_impl = text[start:i]
    new_impl = old_impl.replace(
        "document.getElementById('prof-phone').value = patient.phone;\n        document.getElementById('prof-password').value = '';",
        """document.getElementById('prof-phone').value = patient.phone;
        document.getElementById('prof-email').value = patient.email || '';
        document.getElementById('prof-dob').value = patient.dob || '';
        document.getElementById('prof-gender').value = patient.gender || '';
        document.getElementById('prof-blood').value = patient.blood_group || '';
        document.getElementById('prof-address').value = patient.address || '';
        document.getElementById('prof-password').value = '';"""
    )
    if new_impl == old_impl:
        # maybe spacing
        new_impl = re.sub(
            r"document\.getElementById\('prof-phone'\)\.value = patient\.phone;\s*document\.getElementById\('prof-password'\)\.value = '';",
            """document.getElementById('prof-phone').value = patient.phone;
        document.getElementById('prof-email').value = patient.email || '';
        document.getElementById('prof-dob').value = patient.dob || '';
        document.getElementById('prof-gender').value = patient.gender || '';
        document.getElementById('prof-blood').value = patient.blood_group || '';
        document.getElementById('prof-address').value = patient.address || '';
        document.getElementById('prof-password').value = '';""",
            old_impl
        )
    return text[:start] + new_impl + text[i:]

content = open('MediCheck.html', encoding='utf-8').read()
new_content = replace_func_renderProfile(content)
open('MediCheck.html', 'w', encoding='utf-8').write(new_content)
print("Fixed renderProfile logic")
