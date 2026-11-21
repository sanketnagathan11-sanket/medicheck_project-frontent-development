import os

content = open('MediCheck.html', encoding='utf-8').read()

# 1. Update <nav>
nav_old = """      <a id="nav-profile" onclick="showPage('profile')" style="display:none; cursor:pointer;">My Profile</a>
      <a id="nav-admin" onclick="showPage('admin')">Staff Portal</a>"""
nav_new = """      <a id="nav-profile" onclick="showPage('profile')" style="display:none; cursor:pointer;">My Profile</a>
      <a id="nav-patients" onclick="showPage('patients')" style="display:none; cursor:pointer;">Patient DB</a>
      <a id="nav-admin" onclick="showPage('admin')">Staff Portal</a>"""
if nav_old in content:
    content = content.replace(nav_old, nav_new)
    print("Nav replaced")
else:
    print("Failed nav replace")

# 2. Update updateAuthNav()
auth_old = """  const adminNav = document.getElementById('nav-admin');
  const profileNav = document.getElementById('nav-profile');
  const bookingsNav = document.getElementById('nav-bookings');

  if(adminNav) adminNav.style.display = (session && session.type === 'staff') ? 'inline-block' : 'none';
  if(profileNav) profileNav.style.display = (session && session.type === 'patient') ? 'inline-block' : 'none';
  // Customers can only see their bookings if logged in OR logged out (logged out redirects to login on click)
  // But wait, if staff is logged in, hide bookings
  if(bookingsNav) bookingsNav.style.display = (session && session.type === 'staff') ? 'none' : 'inline-block';"""

auth_new = """  const adminNav = document.getElementById('nav-admin');
  const profileNav = document.getElementById('nav-profile');
  const bookingsNav = document.getElementById('nav-bookings');
  const patientsNav = document.getElementById('nav-patients');

  if(adminNav) adminNav.style.display = (session && session.type === 'staff') ? 'inline-block' : 'none';
  if(patientsNav) patientsNav.style.display = (session && session.type === 'staff' && session.role === 'Admin') ? 'inline-block' : 'none';
  if(profileNav) profileNav.style.display = (session && session.type === 'patient') ? 'inline-block' : 'none';
  // Customers can only see their bookings if logged in OR logged out (logged out redirects to login on click)
  // But wait, if staff is logged in, hide bookings
  if(bookingsNav) bookingsNav.style.display = (session && session.type === 'staff') ? 'none' : 'inline-block';"""
if auth_old in content:
    content = content.replace(auth_old, auth_new)
    print("Auth Nav replaced")
else:
    print("Failed Auth Nav")

# 3. Add page-patients
# Find where page-admin starts and insert page-patients before it
admin_page_start = """    <!-- 🧪 ADMIN PAGE 🧪 -->
    <div id="page-admin" class="page">"""
page_patients = """    <!-- PATIENT DB PAGE -->
    <div id="page-patients" class="page">
      <div class="wrap" style="padding-top:2.5rem; max-width:1200px;">
        <h1 class="section-title" style="text-align:left; margin-bottom: 0.5rem">Customer & Patient Database</h1>
        <p class="section-sub" style="text-align:left; margin-bottom: 2rem;">Authorized Admin Access Only.</p>
        <div id="patients-table-container"></div>
      </div>
    </div>

    <!-- 🧪 ADMIN PAGE 🧪 -->
    <div id="page-admin" class="page">"""
if admin_page_start in content:
    content = content.replace(admin_page_start, page_patients)
    print("Page Patients injected")
else:
    print("Failed Page Patients injected")
    
# 4. update showPage
showpage_old = """  if(name==='bookings') lookupBookings();
  if(name==='profile') renderProfile();
}"""
showpage_new = """  if(name==='bookings') lookupBookings();
  if(name==='profile') renderProfile();
  if(name==='patients') renderPatients();
}"""
if showpage_old in content:
    content = content.replace(showpage_old, showpage_new)
    print("Show Page replaced")
else:
    print("Failed Show Page")

# 5. Extract table logic from renderAdmin and move to renderPatients
admin_db_old = """  if (isAdmin) {
    let customerHTML = `<h2 style="font-size:1.3rem;margin:2rem 0 1rem 0">Customer / Patient Database</h2>
      <div style="background:#fff;border:1px solid var(--border);border-radius:var(--r);padding:1.25rem;box-shadow:0 1px 3px rgba(0,0,0,.05);overflow-x:auto;">
        <table style="width:100%; border-collapse:collapse; font-size:.9rem;">
          <thead>
            <tr style="border-bottom:2px solid var(--border);text-align:left;">
              <th style="padding:.5rem">ID</th>
              <th style="padding:.5rem">Name</th>
              <th style="padding:.5rem">Phone</th>
              <th style="padding:.5rem">Email</th>
              <th style="padding:.5rem">Gender/DOB/Blood</th>
              <th style="padding:.5rem">Address</th>
              <th style="padding:.5rem">Tier</th>
            </tr>
          </thead>
          <tbody>
            ${getPatients().map(p => `
              <tr style="border-bottom:1px solid var(--border);">
                <td style="padding:.5rem;color:var(--primary)">#${p.patient_id}</td>
                <td style="padding:.5rem"><strong>${p.full_name}</strong></td>
                <td style="padding:.5rem">${p.phone}</td>
                <td style="padding:.5rem">${p.email || '-'}</td>
                <td style="padding:.5rem">${p.gender || '-'} (${p.dob || '-'}) [${p.blood_group || '-'}]</td>
                <td style="padding:.5rem">${p.address || '-'}</td>
                <td style="padding:.5rem"><span class="badge ${p.membership_tier==='Premium'?'b-ready':'b-scheduled'}">${p.membership_tier || 'Standard'}</span></td>
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

admin_db_new = """  }
}

function renderPatients() {
  const session = ls('session');
  if(!session || session.type !== 'staff' || session.role !== 'Admin') { showPage('home'); return; }
  
  let customerHTML = `
      <div style="background:#fff;border:1px solid var(--border);border-radius:var(--r);padding:1.25rem;box-shadow:0 1px 3px rgba(0,0,0,.05);overflow-x:auto;">
        <table style="width:100%; border-collapse:collapse; font-size:.9rem;">
          <thead>
            <tr style="border-bottom:2px solid var(--border);text-align:left;">
              <th style="padding:.5rem">ID</th>
              <th style="padding:.5rem">Name</th>
              <th style="padding:.5rem">Phone</th>
              <th style="padding:.5rem">Email</th>
              <th style="padding:.5rem">Gender/DOB/Blood</th>
              <th style="padding:.5rem">Address</th>
              <th style="padding:.5rem">Tier</th>
            </tr>
          </thead>
          <tbody>
            ${getPatients().map(p => `
              <tr style="border-bottom:1px solid var(--border);">
                <td style="padding:.5rem;color:var(--primary)">#${p.patient_id}</td>
                <td style="padding:.5rem"><strong>${p.full_name}</strong></td>
                <td style="padding:.5rem">${p.phone}</td>
                <td style="padding:.5rem">${p.email || '-'}</td>
                <td style="padding:.5rem">${p.gender || '-'} (${p.dob || '-'}) [${p.blood_group || '-'}]</td>
                <td style="padding:.5rem">${p.address || '-'}</td>
                <td style="padding:.5rem"><span class="badge ${p.membership_tier==='Premium'?'b-ready':'b-scheduled'}">${p.membership_tier || 'Standard'}</span></td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>`;
      
  const container = document.getElementById('patients-table-container');
  if(container) container.innerHTML = customerHTML;
}

function addStaff() {"""

if admin_db_old in content:
    content = content.replace(admin_db_old, admin_db_new)
    print("Admin DB successfully split into renderPatients")
else:
    print("Failed Admin DB split")

open('MediCheck.html', 'w', encoding='utf-8').write(content)
