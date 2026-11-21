import os, re

content = open('MediCheck.html', encoding='utf-8').read()

# 1. Update HTML fields
html_old = """            <!-- Editable Fields -->
            <div style="text-align:left; display:flex; flex-direction:column; gap:1.25rem;">
               <div style="background:#f8fafc; padding:1rem 1.25rem; border-radius:10px; border:1px solid #e2e8f0;">
                 <label style="font-size:.75rem; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:.3rem; display:block;">Full Name</label>
                 <input type="text" id="prof-name" style="width:100%; background:transparent; border:none; font-weight:600; font-size:.95rem; color:var(--text); outline:none;">
               </div>
               <div style="background:#f8fafc; padding:1rem 1.25rem; border-radius:10px; border:1px solid #e2e8f0;">
                 <label style="font-size:.75rem; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:.3rem; display:block;">Phone Number (Locked)</label>
                 <input type="text" id="prof-phone" disabled style="width:100%; background:transparent; border:none; font-weight:600; font-size:.95rem; color:var(--muted); outline:none;">
               </div>
               <div style="background:#f8fafc; padding:1rem 1.25rem; border-radius:10px; border:1px solid #e2e8f0;">
                 <label style="font-size:.75rem; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:.3rem; display:block;">Change Password</label>
                 <input type="password" id="prof-password" placeholder="Leave blank to keep..." style="width:100%; background:transparent; border:none; font-weight:600; font-size:.95rem; color:var(--text); outline:none;">
               </div>
            </div>"""

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

content = content.replace(html_old, html_new)

# 2. Update renderProfile JS
js_render_old = """      document.getElementById('prof-name').value = patient.full_name;
        document.getElementById('prof-phone').value = patient.phone;
        document.getElementById('prof-password').value = '';"""
js_render_new = """      document.getElementById('prof-name').value = patient.full_name;
        document.getElementById('prof-phone').value = patient.phone;
        document.getElementById('prof-email').value = patient.email || '';
        document.getElementById('prof-dob').value = patient.dob || '';
        document.getElementById('prof-gender').value = patient.gender || '';
        document.getElementById('prof-blood').value = patient.blood_group || '';
        document.getElementById('prof-address').value = patient.address || '';
        document.getElementById('prof-password').value = '';"""
        
content = content.replace(js_render_old, js_render_new)

# 3. Update updateProfile JS
js_update_old = """    const newName = document.getElementById('prof-name').value.trim();
      const newPass = document.getElementById('prof-password').value;
      if(!newName) { flash('Name cannot be empty', 'danger'); return; }
      let patients = getPatients();
      let p = patients.find(p => p.patient_id === session.id);
      if(p) {
        p.full_name = newName;
        if(newPass) p.password = newPass;"""

js_update_new = """    const newName = document.getElementById('prof-name').value.trim();
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
        if(newPass) p.password = newPass;"""
        
content = content.replace(js_update_old, js_update_new)

open('MediCheck.html', 'w', encoding='utf-8').write(content)
print("Updated profile fields!")
