import os

content = open('MediCheck.html', encoding='utf-8').read()

# Replace HTML
old_html = """      <!-- New Login Section on Home Page -->
      <div class="split-login-section" style="margin-top: 5rem; display: flex; flex-wrap: wrap; background: #fff; border: 1px solid var(--border); border-radius: 20px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,.05);">
        <div style="flex: 1; min-width: 320px; padding: 3rem; display: flex; flex-direction: column; justify-content: center;">
          <h2 class="section-title" style="text-align:left; margin-bottom: 0.5rem; font-size:1.6rem">Patient Portal Login</h2>
          <p class="section-sub" style="text-align:left; margin-bottom: 2rem; max-width: 100%;">Log in to view your diagnostic reports, track active bookings, and manage your health.</p>
          <div class="fg" style="margin-bottom:1.2rem;"><label>Phone Number</label><input id="page-login-phone" type="tel" maxlength="10" placeholder="Enter registered 10-digit number"></div>
          <div class="fg" style="margin-bottom:1.5rem;"><label>Password</label><input id="page-login-password" type="password" placeholder="Enter password"></div>
          <button class="btn btn-primary" style="width:100%" onclick="pagePatientLogin()">Login to My Account</button>
          
          <div style="margin-top:1.5rem; text-align:center; font-size:.9rem; color:var(--muted)">
            <p style="margin-bottom:.6rem;">New patient? <button style="background:none;border:none;color:var(--primary);cursor:pointer;font-weight:600" onclick="openAuth(); switchAuth('register')">Create an account</button></p>
            <p><button style="background:none;border:none;color:var(--muted);cursor:pointer;text-decoration:underline" onclick="openAuth(); switchAuth('staff')">Are you a staff member? Staff Login &rarr;</button></p>
          </div>

        </div>"""

new_html = """      <!-- New Login Section on Home Page -->
      <div class="split-login-section" style="margin-top: 5rem; display: flex; flex-wrap: wrap; background: #fff; border: 1px solid var(--border); border-radius: 20px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,.05);">
        <div style="flex: 1; min-width: 320px; padding: 3rem; display: flex; flex-direction: column; justify-content: center;">
          
          <div id="page-auth-login" class="page-auth-pane active">
            <h2 class="section-title" style="text-align:left; margin-bottom: 0.5rem; font-size:1.6rem">Patient Portal Login</h2>
            <p class="section-sub" style="text-align:left; margin-bottom: 2rem; max-width: 100%;">Log in to view your diagnostic reports, track active bookings, and manage your health.</p>
            <div class="fg" style="margin-bottom:1.2rem;"><label>Phone Number</label><input id="page-login-phone" type="tel" maxlength="10" placeholder="Enter registered 10-digit number"></div>
            <div class="fg" style="margin-bottom:1.5rem;"><label>Password</label><input id="page-login-password" type="password" placeholder="Enter password"></div>
            <button class="btn btn-primary" style="width:100%" onclick="pagePatientLogin()">Login to My Account</button>
            <div style="margin-top:1.5rem; text-align:center; font-size:.9rem; color:var(--muted)">
              <p style="margin-bottom:.6rem;">New patient? <button style="background:none;border:none;color:var(--primary);cursor:pointer;font-weight:600" onclick="switchPageAuth('register')">Create an account</button></p>
              <p><button id="page-staff-switch" style="background:none;border:none;color:var(--muted);cursor:pointer;text-decoration:underline" onclick="switchPageAuth('staff')">Are you a staff member? Staff Login &rarr;</button></p>
            </div>
          </div>

          <div id="page-auth-register" class="page-auth-pane">
            <h2 class="section-title" style="text-align:left; margin-bottom: 0.5rem; font-size:1.6rem">Create Patient Account</h2>
            <p class="section-sub" style="text-align:left; margin-bottom: 2rem; max-width: 100%;">Register a new account to book tests and access your health dashboard.</p>
            <div class="fg" style="margin-bottom:1.2rem"><label>Full Name *</label><input id="page-reg-name" placeholder="Your full name"></div>
            <div class="fg" style="margin-bottom:1.2rem"><label>Phone *</label><input id="page-reg-phone" type="tel" maxlength="10" placeholder="10-digit number"></div>
            <div class="fg" style="margin-bottom:1.5rem"><label>Create Password *</label><input id="page-reg-password" type="password" placeholder="Minimum 4 characters"></div>
            <button class="btn btn-teal" style="width:100%" onclick="pagePatientRegister()">Create Patient Account</button>
            <div style="margin-top:1.5rem; text-align:center; font-size:.9rem; color:var(--muted)">
              <p><button style="background:none;border:none;color:var(--primary);cursor:pointer;font-weight:600" onclick="switchPageAuth('login')">&larr; Back to Login</button></p>
            </div>
          </div>

          <div id="page-auth-staff" class="page-auth-pane">
            <h2 class="section-title" style="text-align:left; margin-bottom: 0.5rem; font-size:1.6rem">Staff Portal Login</h2>
            <p class="section-sub" style="text-align:left; margin-bottom: 2rem; max-width: 100%;">Authorized personnel only. Access your tasks and system settings.</p>
            <div class="fg" style="margin-bottom:1.2rem"><label>Staff ID</label><input id="page-staff-id" type="number" placeholder="e.g. 6"></div>
            <div class="fg" style="margin-bottom:1.5rem"><label>Password</label><input id="page-staff-password" type="password" placeholder="Enter staff password"></div>
            <button class="btn btn-primary" style="width:100%" onclick="pageStaffLogin()">Login to Staff Portal</button>
            <div style="margin-top:1.5rem; text-align:center; font-size:.9rem; color:var(--muted)">
              <p style="margin-bottom:.6rem;">Demo password: <strong>medicheck123</strong></p>
              <p><button style="background:none;border:none;color:var(--primary);cursor:pointer;font-weight:600" onclick="switchPageAuth('login')">&larr; Back to Patient Login</button></p>
            </div>
          </div>

        </div>"""

# Replace CSS
old_css = """    /* Test tube image animation */"""
new_css = """    /* Page Auth Pane CSS */
    .page-auth-pane { display: none; flex-direction: column; height: 100%; justify-content: center; animation: authFade 0.25s ease; }
    .page-auth-pane.active { display: flex; }

    /* Test tube image animation */"""

# Replace JS
old_js = """function pagePatientLogin(){"""
new_js = """function switchPageAuth(type) {
  document.querySelectorAll('.page-auth-pane').forEach(p => p.classList.remove('active'));
  document.getElementById('page-auth-' + type).classList.add('active');
}

function pagePatientRegister() {
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
}

function pageStaffLogin() {
  const id=parseInt(document.getElementById('page-staff-id').value);
  const password=document.getElementById('page-staff-password').value;
  const staff=getStaff().find(s=>s.staff_id===id);
  if(!staff){ flash('Invalid Staff ID.', 'danger'); return; }
  if(password!=='medicheck123'){ flash('Incorrect staff password.', 'danger'); return; }
  lsSet('session',{type:'staff',id:staff.staff_id,name:staff.full_name,role:staff.role});
  updateAuthNav(); showPage('admin');
  flash('Logged into staff portal as '+staff.full_name,'success');
}

function pagePatientLogin(){"""

if old_html in content and old_css in content and old_js in content:
    content = content.replace(old_html, new_html).replace(old_css, new_css).replace(old_js, new_js)
    open('MediCheck.html', 'w', encoding='utf-8').write(content)
    print('Replaced ALL')
else:
    print('Failed to find targets')
