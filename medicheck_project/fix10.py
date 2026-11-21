import os

content = open('MediCheck.html', encoding='utf-8').read()

# 1. Update <nav>
nav_old = """    <nav>
      <a id="nav-home" class="active" onclick="showPage('home')">Home</a>
      <a id="nav-tests" onclick="showPage('tests')">Tests &amp; Packages</a>
      <a id="nav-bookings" onclick="showPage('bookings')">My Bookings</a>
      <a id="nav-admin" onclick="showPage('admin')">Staff Portal</a>
      <a id="nav-contact" onclick="showPage('contact')">Contact</a>
      <a id="nav-book" onclick="showPage('book')" style="cursor:pointer">Book a Test</a>
      <a id="auth-nav" class="nav-btn btn" onclick="openAuth()" style="cursor:pointer">Login</a>
    </nav>"""
nav_new = """    <nav>
      <a id="nav-home" class="active" onclick="showPage('home')">Home</a>
      <a id="nav-tests" onclick="showPage('tests')">Tests &amp; Packages</a>
      <a id="nav-bookings" onclick="showPage('bookings')">My Bookings</a>
      <a id="nav-profile" onclick="showPage('profile')" style="display:none; cursor:pointer;">My Profile</a>
      <a id="nav-admin" onclick="showPage('admin')">Staff Portal</a>
      <a id="nav-contact" onclick="showPage('contact')">Contact</a>
      <a id="nav-book" onclick="showPage('book')" style="cursor:pointer">Book a Test</a>
      <a id="auth-nav" class="nav-btn btn" onclick="openAuth()" style="cursor:pointer">Login</a>
    </nav>"""
if nav_old in content:
    content = content.replace(nav_old, nav_new)
    print("Nav replaced")
else:
    print("Failed Nav replace")

# 2. Add #page-profile before #page-admin
# Let's just find the closing div of bookings and start of admin
admin_old = """    <!-- 🧪 ADMIN PAGE 🧪 -->
    <div id="page-admin" class="page">"""
admin_new = """    <!-- MY PROFILE PAGE -->
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

    <!-- 🧪 ADMIN PAGE 🧪 -->
    <div id="page-admin" class="page">"""
# Try different emojis if needed
if "id=\"page-admin\"" in content:
    idx = content.find('<div id="page-admin"')
    # Find the preceding comment
    idx_comment = content.rfind('<!--', 0, idx)
    if idx_comment != -1:
        content = content[:idx_comment] + admin_new[admin_new.find('<!-- MY PROFILE PAGE'):] + content[idx + len('<div id="page-admin" class="page">'):]
        print("Profile page inserted")
else:
    print("Failed Profile page")

# 3. Update updateAuthNav
authnav_old = """function updateAuthNav(){
  const nav=document.getElementById('auth-nav');
  const session=ls('session');
  
  const adminNav = document.getElementById('nav-admin');
  if(adminNav){
    adminNav.style.display = (session && session.type === 'staff') ? 'inline-block' : 'none';
  }

  if(!nav) return;
  if(session){
    nav.textContent='Logout';
    nav.onclick=logout;
  }else{
    nav.textContent='Login';
    nav.onclick=()=>openAuth('login', false);
  }
}"""
authnav_new = """function updateAuthNav(){
  const nav=document.getElementById('auth-nav');
  const session=ls('session');
  
  const adminNav = document.getElementById('nav-admin');
  const profileNav = document.getElementById('nav-profile');
  const bookingsNav = document.getElementById('nav-bookings');

  if(adminNav) adminNav.style.display = (session && session.type === 'staff') ? 'inline-block' : 'none';
  if(profileNav) profileNav.style.display = (session && session.type === 'patient') ? 'inline-block' : 'none';
  // Customers can only see their bookings if logged in OR logged out (logged out redirects to login on click)
  // But wait, if staff is logged in, hide bookings
  if(bookingsNav) bookingsNav.style.display = (session && session.type === 'staff') ? 'none' : 'inline-block';

  if(!nav) return;
  if(session){
    nav.textContent='Logout';
    nav.onclick=logout;
  }else{
    nav.textContent='Login';
    nav.onclick=()=>openAuth('login', false);
  }
}"""
if authnav_old in content:
    content = content.replace(authnav_old, authnav_new)
    print("Auth Nav replaced")
else:
    print("Failed Auth Nav")

# 4. showPage additions
showpage_old = """  if(name==='report' && extra) renderReport(extra);
  if(name==='bookings') lookupBookings();
}"""
showpage_new = """  if(name==='report' && extra) renderReport(extra);
  if(name==='bookings') lookupBookings();
  if(name==='profile') renderProfile();
}

function renderProfile() {
  const session = ls('session');
  if(!session || session.type !== 'patient') { showPage('home'); return; }
  const patient = getPatients().find(p => p.patient_id === session.id);
  if(patient) {
    document.getElementById('prof-name').value = patient.full_name;
    document.getElementById('prof-phone').value = patient.phone;
    document.getElementById('prof-password').value = ''; 
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
if showpage_old in content:
    content = content.replace(showpage_old, showpage_new)
    print("Show Page replaced")
else:
    print("Failed Show Page")

# 5. Admin Patient DB
admin_db_old = """    }
  }
}

function addStaff() {"""
admin_db_new = """    }
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
            ${getPatients().map(p => `
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
if admin_db_old in content:
    content = content.replace(admin_db_old, admin_db_new)
    print("Admin DB replaced")
else:
    print("Failed Admin DB")

open('MediCheck.html', 'w', encoding='utf-8').write(content)
