import os

content = open('MediCheck.html', encoding='utf-8').read()

# 1. Update Nav
nav_old = """      <div class="nav-links">
        <a id="nav-tests" onclick="showPage('tests')">Tests &amp; Packages</a>
        <a id="nav-bookings" onclick="showPage('bookings')" style="display:none">My Bookings</a>
        <a id="nav-contact" onclick="showPage('contact')">Contact</a>
      </div>"""
nav_new = """      <div class="nav-links">
        <a id="nav-tests" onclick="showPage('tests')">Tests &amp; Packages</a>
        <a id="nav-bookings" onclick="showPage('bookings')" style="display:none">My Bookings</a>
        <a id="nav-profile" onclick="showPage('profile')" style="display:none; cursor:pointer;">My Profile</a>
        <a id="nav-contact" onclick="showPage('contact')">Contact</a>
      </div>"""
content = content.replace(nav_old, nav_new)

# 2. Add #page-profile before #page-admin
page_old = """  <!--  ADMIN PAGE  -->
  <div id="page-admin" class="page">"""
page_new = """  <!-- MY PROFILE PAGE -->
  <div id="page-profile" class="page">
    <div class="wrap" style="padding-top:2.5rem; max-width:600px;">
      <h1 class="section-title" style="text-align:left; margin-bottom: 0.5rem">My Profile</h1>
      <p class="section-sub" style="text-align:left; margin-bottom: 2rem;">Manage your personal details and portal password.</p>
      <div class="form-card" style="padding:2rem">
        <div class="fg" style="margin-bottom:1.2rem"><label>Full Name</label><input id="prof-name"></div>
        <div class="fg" style="margin-bottom:1.2rem"><label>Phone Number</label><input id="prof-phone" disabled style="background:#f1f5f9; cursor:not-allowed;" title="Phone number cannot be changed."></div>
        <div class="fg" style="margin-bottom:1.5rem"><label>Change Password</label><input id="prof-password" type="password" placeholder="Leave blank to keep current password"></div>
        <button class="btn btn-primary" style="width:100%" onclick="updateProfile()">Save Changes</button>
      </div>
    </div>
  </div>

  <!--  ADMIN PAGE  -->
  <div id="page-admin" class="page">"""
if "<!--  ADMIN PAGE  -->" in content:
    content = content.replace(page_old, page_new)
else:
    # Try the emoji version
    page_old = """  <!-- 🛠 ADMIN PAGE 🛠 -->
  <div id="page-admin" class="page">"""
    page_new = """  <!-- MY PROFILE PAGE -->
  <div id="page-profile" class="page">
    <div class="wrap" style="padding-top:2.5rem; max-width:600px;">
      <h1 class="section-title" style="text-align:left; margin-bottom: 0.5rem">My Profile</h1>
      <p class="section-sub" style="text-align:left; margin-bottom: 2rem;">Manage your personal details and portal password.</p>
      <div class="form-card" style="padding:2rem">
        <div class="fg" style="margin-bottom:1.2rem"><label>Full Name</label><input id="prof-name"></div>
        <div class="fg" style="margin-bottom:1.2rem"><label>Phone Number</label><input id="prof-phone" disabled style="background:#f1f5f9; cursor:not-allowed;" title="Phone number cannot be changed."></div>
        <div class="fg" style="margin-bottom:1.5rem"><label>Change Password</label><input id="prof-password" type="password" placeholder="Leave blank to keep current password"></div>
        <button class="btn btn-primary" style="width:100%" onclick="updateProfile()">Save Changes</button>
      </div>
    </div>
  </div>

  <!-- 🛠 ADMIN PAGE 🛠 -->
  <div id="page-admin" class="page">"""
    content = content.replace(page_old, page_new)

# 3. Update updateAuthNav
auth_nav_old = """function updateAuthNav(){
  const session=ls('session');
  const btn=document.getElementById('nav-auth-btn');
  const bnav=document.getElementById('nav-bookings');
  if(session){
    if(session.type==='patient'){
      bnav.style.display='inline-block';
      btn.textContent='Logout';
      btn.onclick=logout;
    } else {
      bnav.style.display='none';
      btn.textContent='Staff Dashboard';
      btn.onclick=()=>showPage('admin');
    }
  } else {
    bnav.style.display='none';
    btn.textContent='Login / Register';
    btn.onclick=openAuth;
  }
}"""
auth_nav_new = """function updateAuthNav(){
  const session=ls('session');
  const btn=document.getElementById('nav-auth-btn');
  const bnav=document.getElementById('nav-bookings');
  const pnav=document.getElementById('nav-profile');
  if(session){
    if(session.type==='patient'){
      bnav.style.display='inline-block';
      if(pnav) pnav.style.display='inline-block';
      btn.textContent='Logout';
      btn.onclick=logout;
    } else {
      bnav.style.display='none';
      if(pnav) pnav.style.display='none';
      btn.textContent='Staff Dashboard';
      btn.onclick=()=>showPage('admin');
    }
  } else {
    bnav.style.display='inline-block';
    if(pnav) pnav.style.display='none';
    btn.textContent='Login / Register';
    btn.onclick=openAuth;
  }
}"""
content = content.replace(auth_nav_old, auth_nav_new)

# 4. Add renderProfile and updateProfile, and modify showPage
show_page_old = """  if(name==='admin') renderAdmin();
  if(name==='report' && extra) renderReport(extra);
}"""
show_page_new = """  if(name==='admin') renderAdmin();
  if(name==='profile') renderProfile();
  if(name==='report' && extra) renderReport(extra);
}

function renderProfile() {
  const session = ls('session');
  if(!session || session.type !== 'patient') { showPage('home'); return; }
  const patient = getPatients().find(p => p.patient_id === session.id);
  if(patient) {
    document.getElementById('prof-name').value = patient.full_name;
    document.getElementById('prof-phone').value = patient.phone;
    document.getElementById('prof-password').value = ''; // leave blank
  }
}

function updateProfile() {
  const session = ls('session');
  if(!session || session.type !== 'patient') return;
  const newName = document.getElementById('prof-name').value.trim();
  const newPass = document.getElementById('prof-password').value;
  if(!newName) { flash('Name cannot be empty', 'danger'); return; }
  let patients = getPatients();
  let p = patients.find(p => p.patient_id === session.id);
  if(p) {
    p.full_name = newName;
    if(newPass) p.password = newPass;
    lsSet('patients', patients);
    session.name = newName;
    lsSet('session', session);
    flash('Profile updated successfully!', 'success');
  }
}"""
content = content.replace(show_page_old, show_page_new)

# 5. Hide Home Page login section if logged in
render_home_old = """function renderHome(){
  document.getElementById('test-search').value = '';
}"""
render_home_new = """function renderHome(){
  document.getElementById('test-search').value = '';
  const loginSec = document.querySelector('.split-login-section');
  if(loginSec) {
    const session = ls('session');
    if(session) {
      loginSec.style.display = 'none';
    } else {
      loginSec.style.display = 'flex';
    }
  }
}"""
content = content.replace(render_home_old, render_home_new)

# 6. Admin: Add Customer Profiles list
# Look for where staff workload ends in renderAdmin
render_admin_old = """    }
  }
}

function addStaff() {"""
render_admin_new = """    }
  }
  
  if (isAdmin) {
    let customerHTML = `<h2 style="font-size:1.3rem;margin:2rem 0 1rem 0">Customer / Patient Database</h2>
      <div style="background:#fff;border:1px solid var(--border);border-radius:var(--r);padding:1.25rem;box-shadow:0 1px 3px rgba(0,0,0,.05);overflow-x:auto;">
        <table style="width:100%; border-collapse:collapse; font-size:.9rem;">
          <thead>
            <tr style="border-bottom:2px solid var(--border);text-align:left;">
              <th style="padding:.5rem">ID</th>
              <th style="padding:.5rem">Name</th>
              <th style="padding:.5rem">Phone</th>
            </tr>
          </thead>
          <tbody>
            ${patients.map(p => `
              <tr style="border-bottom:1px solid var(--border);">
                <td style="padding:.5rem;color:var(--primary)">#${p.patient_id}</td>
                <td style="padding:.5rem"><strong>${p.full_name}</strong></td>
                <td style="padding:.5rem">${p.phone}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>`;
    let workloadDiv = document.getElementById('staff-workload');
    if(workloadDiv && workloadDiv.parentElement) {
      // Append it below staff workload
      const existingDb = document.getElementById('customer-db-section');
      if(existingDb) existingDb.remove();
      const div = document.createElement('div');
      div.id = 'customer-db-section';
      div.innerHTML = customerHTML;
      workloadDiv.parentElement.appendChild(div);
    }
  }
}

function addStaff() {"""
content = content.replace(render_admin_old, render_admin_new)

open('MediCheck.html', 'w', encoding='utf-8').write(content)
print("Fix8 complete")
