import os

content = open('MediCheck.html', encoding='utf-8').read()

# 1. Update #auth-register modal
modal_old = """    <div id="auth-register" class="auth-pane">
      <div class="fg"><label>Full Name *</label><input id="reg-name" placeholder="Your full name"></div>
      <div class="fg"><label>Phone *</label><input id="reg-phone" type="tel" maxlength="10" placeholder="10-digit number"></div>
      <div class="fg"><label>Create Password *</label><input id="reg-password" type="password" placeholder="Minimum 4 characters"></div>
      <button class="btn btn-teal" style="width:100%;margin-top:1rem" onclick="patientRegister()">Create Patient Account</button>
    </div>"""
modal_new = """    <div id="auth-register" class="auth-pane">
      <div class="fg"><label>Full Name *</label><input id="reg-name" placeholder="Your full name"></div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px">
        <div class="fg"><label>DOB *</label><input id="reg-dob" type="date"></div>
        <div class="fg"><label>Gender *</label><select id="reg-gender"><option>Male</option><option>Female</option><option>Other</option></select></div>
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px">
        <div class="fg"><label>Phone *</label><input id="reg-phone" type="tel" maxlength="10" placeholder="10 digits"></div>
        <div class="fg"><label>Email</label><input id="reg-email" type="email" placeholder="Optional"></div>
      </div>
      <div class="fg"><label>Address *</label><input id="reg-address" placeholder="Residential address"></div>
      <div class="fg"><label>Create Password *</label><input id="reg-password" type="password" placeholder="Min 4 chars"></div>
      <button class="btn btn-teal" style="width:100%;margin-top:1rem" onclick="patientRegister()">Create Patient Account</button>
    </div>"""
if modal_old in content:
    content = content.replace(modal_old, modal_new)

# 2. Update #page-auth-register
page_old = """          <div id="page-auth-register" class="page-auth-pane">
            <h2 class="section-title" style="text-align:left; margin-bottom: 0.5rem; font-size:1.6rem">Create Patient Account</h2>
            <p class="section-sub" style="text-align:left; margin-bottom: 2rem; max-width: 100%;">Register a new account to book tests and access your health dashboard.</p>
            <div class="fg" style="margin-bottom:1.2rem"><label>Full Name *</label><input id="page-reg-name" placeholder="Your full name"></div>
            <div class="fg" style="margin-bottom:1.2rem"><label>Phone *</label><input id="page-reg-phone" type="tel" maxlength="10" placeholder="10-digit number"></div>
            <div class="fg" style="margin-bottom:1.5rem"><label>Create Password *</label><input id="page-reg-password" type="password" placeholder="Minimum 4 characters"></div>
            <button class="btn btn-teal" style="width:100%" onclick="pagePatientRegister()">Create Patient Account</button>
            <div style="margin-top:1.5rem; text-align:center; font-size:.9rem; color:var(--muted)">
              <p><button style="background:none;border:none;color:var(--primary);cursor:pointer;font-weight:600" onclick="switchPageAuth('login')">&larr; Back to Login</button></p>
            </div>
          </div>"""
page_new = """          <div id="page-auth-register" class="page-auth-pane">
            <h2 class="section-title" style="text-align:left; margin-bottom: 0.5rem; font-size:1.6rem">Create Patient Account</h2>
            <p class="section-sub" style="text-align:left; margin-bottom: 1.5rem; max-width: 100%;">Register a new account to book tests and access your health dashboard.</p>
            <div class="fg" style="margin-bottom:1rem"><label>Full Name *</label><input id="page-reg-name" placeholder="Your full name"></div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:1rem">
              <div class="fg" style="margin-bottom:0"><label>DOB *</label><input id="page-reg-dob" type="date"></div>
              <div class="fg" style="margin-bottom:0"><label>Gender *</label><select id="page-reg-gender" style="width:100%;padding:.65rem;border:1px solid var(--border);border-radius:4px"><option>Male</option><option>Female</option><option>Other</option></select></div>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:1rem">
              <div class="fg" style="margin-bottom:0"><label>Phone *</label><input id="page-reg-phone" type="tel" maxlength="10" placeholder="10 digits"></div>
              <div class="fg" style="margin-bottom:0"><label>Email</label><input id="page-reg-email" type="email" placeholder="Optional"></div>
            </div>
            <div class="fg" style="margin-bottom:1rem"><label>Address *</label><input id="page-reg-address" placeholder="Residential address"></div>
            <div class="fg" style="margin-bottom:1.5rem"><label>Create Password *</label><input id="page-reg-password" type="password" placeholder="Min 4 chars"></div>
            <button class="btn btn-teal" style="width:100%" onclick="pagePatientRegister()">Create Patient Account</button>
            <div style="margin-top:1.5rem; text-align:center; font-size:.9rem; color:var(--muted)">
              <p><button style="background:none;border:none;color:var(--primary);cursor:pointer;font-weight:600" onclick="switchPageAuth('login')">&larr; Back to Login</button></p>
            </div>
          </div>"""
if page_old in content:
    content = content.replace(page_old, page_new)

# 3. Update patientRegister
reg1_old = """function patientRegister(){
  const name=document.getElementById('reg-name').value.trim();
  const phone=document.getElementById('reg-phone').value.trim();
  const password=document.getElementById('reg-password').value;
  if(!name||!phone||!password){ flash('Please fill in all fields.', 'danger'); return; }
  let patients=getPatients();
  if(patients.some(p=>p.phone===phone)){ flash('Phone number already registered. Please login.', 'danger'); switchAuth('login'); document.getElementById('login-phone').value=phone; return; }
  const newId=patients.length>0 ? Math.max(...patients.map(p=>p.patient_id))+1 : 1;
  const patient={patient_id:newId, full_name:name, phone:phone, password:password};
  patients.push(patient);
  lsSet('patients',patients);
  lsSet('session',{type:'patient',id:patient.patient_id,name:patient.full_name});
  authLocked=false; closeAuth(); updateAuthNav();
  flash('Account created successfully. Welcome, '+patient.full_name+'!','success');
}"""
reg1_new = """function patientRegister(){
  const name=document.getElementById('reg-name').value.trim();
  const phone=document.getElementById('reg-phone').value.trim();
  const password=document.getElementById('reg-password').value;
  const dob=document.getElementById('reg-dob').value;
  const gender=document.getElementById('reg-gender').value;
  const email=document.getElementById('reg-email').value.trim();
  const address=document.getElementById('reg-address').value.trim();

  if(!name||!phone||!password||!dob||!gender||!address){ flash('Please fill in all required fields.', 'danger'); return; }
  let patients=getPatients();
  if(patients.some(p=>p.phone===phone)){ flash('Phone number already registered. Please login.', 'danger'); switchAuth('login'); document.getElementById('login-phone').value=phone; return; }
  const newId=patients.length>0 ? Math.max(...patients.map(p=>p.patient_id))+1 : 1;
  
  const patient={
    patient_id:newId, full_name:name, phone:phone, password:password,
    dob:dob, gender:gender, email:email, address:address, membership_tier:'Standard'
  };
  patients.push(patient);
  lsSet('patients',patients);
  lsSet('session',{type:'patient',id:patient.patient_id,name:patient.full_name});
  authLocked=false; closeAuth(); updateAuthNav();
  flash('Account created successfully. Welcome, '+patient.full_name+'!','success');
}"""
if reg1_old in content:
    content = content.replace(reg1_old, reg1_new)

# 4. Update pagePatientRegister
reg2_old = """function pagePatientRegister() {
  const name=document.getElementById('page-reg-name').value.trim();
  const phone=document.getElementById('page-reg-phone').value.trim();
  const password=document.getElementById('page-reg-password').value;
  if(!name||!phone||!password){ flash('Please fill in all fields.', 'danger'); return; }
  let patients=getPatients();
  if(patients.some(p=>p.phone===phone)){ flash('Phone number already registered. Please login.', 'danger'); switchPageAuth('login'); document.getElementById('page-login-phone').value=phone; return; }
  const newId=patients.length>0 ? Math.max(...patients.map(p=>p.patient_id))+1 : 1;
  const patient={patient_id:newId, full_name:name, phone:phone, password:password};
  patients.push(patient);
  lsSet('patients',patients);
  lsSet('session',{type:'patient',id:patient.patient_id,name:patient.full_name});
  updateAuthNav(); showPage('bookings');
  flash('Account created successfully. Welcome, '+patient.full_name+'!','success');
}"""
reg2_new = """function pagePatientRegister() {
  const name=document.getElementById('page-reg-name').value.trim();
  const phone=document.getElementById('page-reg-phone').value.trim();
  const password=document.getElementById('page-reg-password').value;
  const dob=document.getElementById('page-reg-dob').value;
  const gender=document.getElementById('page-reg-gender').value;
  const email=document.getElementById('page-reg-email').value.trim();
  const address=document.getElementById('page-reg-address').value.trim();

  if(!name||!phone||!password||!dob||!gender||!address){ flash('Please fill in all required fields.', 'danger'); return; }
  let patients=getPatients();
  if(patients.some(p=>p.phone===phone)){ flash('Phone number already registered. Please login.', 'danger'); switchPageAuth('login'); document.getElementById('page-login-phone').value=phone; return; }
  const newId=patients.length>0 ? Math.max(...patients.map(p=>p.patient_id))+1 : 1;
  
  const patient={
    patient_id:newId, full_name:name, phone:phone, password:password,
    dob:dob, gender:gender, email:email, address:address, membership_tier:'Standard'
  };
  patients.push(patient);
  lsSet('patients',patients);
  lsSet('session',{type:'patient',id:patient.patient_id,name:patient.full_name});
  updateAuthNav(); showPage('bookings');
  flash('Account created successfully. Welcome, '+patient.full_name+'!','success');
}"""
if reg2_old in content:
    content = content.replace(reg2_old, reg2_new)

open('MediCheck.html', 'w', encoding='utf-8').write(content)
print("Done fix 11")
