document.addEventListener('DOMContentLoaded', () => {
  const pageId = document.body.id;
  const pageContent = document.body.innerHTML;
  
  // Inject the App Shell (Sidebar, Header, Auth Modal, Footer)
  document.body.innerHTML = `
    <!-- AUTH MODAL -->
    <div id="auth-overlay" class="auth-overlay" role="dialog" aria-modal="true" aria-labelledby="auth-title" onclick="if(event.target===this) closeAuth()">
      <div class="auth-modal">
        <button class="auth-close" onclick="closeAuth()" aria-label="Close login">&times;</button>
        <div class="auth-logo">+</div>
        <h2 id="auth-title" class="auth-title">Welcome to MediCheck</h2>
        <p class="auth-sub">Sign in to manage bookings and access your healthcare dashboard.</p>
        <div class="auth-tabs">
          <button id="tab-login" class="auth-tab active" onclick="switchAuth('login')">Patient Login</button>
          <button id="tab-register" class="auth-tab" onclick="switchAuth('register')">Register</button>
        </div>
        <div id="auth-login" class="auth-pane active">
          <div class="fg"><label>Phone Number</label><input id="login-phone" type="tel" maxlength="10" placeholder="Enter registered 10-digit number"></div>
          <div class="fg"><label>Password</label><input id="login-password" type="password" placeholder="Enter password"></div>
          <button class="btn btn-primary" style="width:100%" onclick="patientLogin()">Login to MediCheck</button>
          <p class="auth-note">New patient? <button class="auth-link" onclick="switchAuth('register')">Create an account</button></p>
        </div>
        <div id="auth-register" class="auth-pane">
          <div class="fg"><label>Full Name *</label><input id="reg-name" placeholder="Your full name"></div>
          <div class="fg"><label>Phone *</label><input id="reg-phone" type="tel" maxlength="10" placeholder="10-digit number"></div>
          <div class="fg"><label>Create Password *</label><input id="reg-password" type="password" placeholder="Minimum 4 characters"></div>
          <button class="btn btn-teal" style="width:100%;margin-top:1rem" onclick="patientRegister()">Create Patient Account</button>
        </div>
        <div id="auth-staff" class="auth-pane">
          <div class="fg"><label>Staff ID</label><input id="staff-id" type="number" placeholder="e.g. 6"></div>
          <div class="fg"><label>Password</label><input id="staff-password" type="password" placeholder="Enter staff password"></div>
          <button class="btn btn-primary" style="width:100%" onclick="staffLogin()">Login to Staff Portal</button>
          <p class="auth-note">Demo password: <strong>medicheck123</strong></p>
        </div>
        <div class="auth-staff">
          <button id="staff-switch" class="auth-link" onclick="switchAuth('staff')">Are you a staff member? Staff Login →</button>
        </div>
      </div>
    </div>

    <div class="app-layout">
      <!-- SIDEBAR -->
      <aside class="sidebar" id="sidebar">
        <div class="sidebar-header">
          <a href="index.html" class="sidebar-brand">
            <span class="sidebar-brand-mark">+</span> MediCheck
          </a>
        </div>
        <nav class="sidebar-nav">
          <a href="index.html" class="${pageId === 'page-home' ? 'active' : ''}">🏠 Home</a>
          <a href="tests.html" class="${pageId === 'page-tests' ? 'active' : ''}">🧪 Tests & Packages</a>
          <a href="book.html" class="${pageId === 'page-book' ? 'active' : ''}">📅 Book a Test</a>
          <a href="bookings.html" class="${pageId === 'page-bookings' ? 'active' : ''}">📋 My Bookings</a>
          <a href="contact.html" class="${pageId === 'page-contact' ? 'active' : ''}">✉️ Contact</a>
          <a href="admin.html" id="nav-admin" class="${pageId === 'page-admin' ? 'active' : ''}" style="display:none; margin-top: 1rem; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 1rem;">⚙️ Staff Portal</a>
        </nav>
        <div class="sidebar-footer">
          <div style="font-size: 0.8rem; color: var(--muted)">© 2026 MediCheck.</div>
        </div>
      </aside>
      
      <!-- MAIN CONTENT -->
      <div class="main-content">
        <!-- HEADER -->
        <header>
          <div class="wrap hdr">
            <div class="hdr-left">
              <button class="mobile-toggle" onclick="toggleSidebar()">☰</button>
            </div>
            <nav>
              <button id="auth-nav" class="nav-btn" onclick="openAuth()">Login</button>
            </nav>
          </div>
        </header>

        <div id="flash-container"></div>
        
        <main>
          ${pageContent}
        </main>
        
        <!-- FOOTER -->
        <footer>
          <div class="wrap footer-inner">
            <div>
              <div class="footer-brand">+ MediCheck Diagnostics</div>
              <p>Leading Diagnostic Lab &amp; Home Sample Collection Network</p>
              <div class="fine-print" style="margin-top:.5rem">Field Project-I — Diagnostic Management System</div>
            </div>
            <div class="tag-strip">
              <span class="lab-tag">MASS WALK-IN TIER</span>
              <span class="lab-tag lab-tag-p">PREMIUM HOME COLLECTION TIER</span>
            </div>
          </div>
        </footer>
      </div>
    </div>
  `;

  // Re-bind any inline scripts that were destroyed by innerHTML replacement
  // For safety, we rely on the function calls below instead of inline scripts
  
  if (pageId === 'page-home') renderHome();
  if (pageId === 'page-tests') renderTests();
  if (pageId === 'page-book') initBookFromURL();
  if (pageId === 'page-bookings') {
    const session = ls('session');
    if(!session) {
      flash('Please log in to view your bookings.', 'danger');
      openAuth('login', false);
    } else {
      setTimeout(lookupBookings, 50);
    }
  }
  if (pageId === 'page-admin') {
    const session = ls('session');
    if(!session || session.type !== 'staff') {
      flash('Access Denied. Only staff members can view the Staff Portal.', 'danger');
      document.querySelector('main').innerHTML = '<div class="wrap"><div class="card" style="margin-top:2rem;text-align:center"><h2>Access Denied</h2><p>Please login as staff.</p></div></div>';
    } else {
      renderAdmin();
    }
  }
  if (pageId === 'page-report') {
    const params = new URLSearchParams(window.location.search);
    const id = parseInt(params.get('id'));
    if (id) renderReport(id);
  }

  updateAuthNav();
  if(!ls('session') && pageId !== 'page-report') setTimeout(()=>openAuth('login', false), 250);
});

function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
}

// Redirect helper to replace original showPage
function showPage(page, extra) {
  if (page === 'home') window.location.href = 'index.html';
  else if (page === 'report' && extra) window.location.href = `report.html?id=${extra}`;
  else if (page === 'book' && extra) {
     if (extra.pkg) window.location.href = `book.html?pkg=${extra.pkg}`;
     else if (extra.test) window.location.href = `book.html?test=${extra.test}`;
  }
  else window.location.href = page + '.html';
}

function flash(msg, type=''){
  const c = document.getElementById('flash-container');
  if(!c) return;
  const d = document.createElement('div');
  d.className='flash '+(type||'');
  d.innerHTML=`<span>${msg}</span><button onclick="this.parentElement.remove()" style="background:none;border:none;cursor:pointer;font-weight:700;font-size:1.1rem;color:inherit">&times;</button>`;
  c.appendChild(d);
  setTimeout(()=>{if(d.parentElement)d.remove()},6000);
}

// ═══════════════════════════════════════════════════════════════
//  HOME PAGE
// ═══════════════════════════════════════════════════════════════
function renderHome(){
  const patients = getPatients(), bookings = getBookings(), tests = getTests();
  const hs = document.getElementById('home-stats');
  if(hs) hs.innerHTML=`
    <div class="stat-item"><div class="stat-num">${patients.length}+</div><div class="stat-label">Registered Patients</div></div>
    <div class="stat-item"><div class="stat-num">${tests.length}</div><div class="stat-label">Lab Tests Offered</div></div>
    <div class="stat-item"><div class="stat-num">${bookings.length}</div><div class="stat-label">Bookings Completed</div></div>
    <div class="stat-item"><div class="stat-num">NABL</div><div class="stat-label">Certified Accreditation</div></div>
  `;
  const pkgs = getPackages().slice(0,3);
  const hp = document.getElementById('home-packages');
  if(hp) hp.innerHTML=pkgs.map(pkg=>`
    <div class="card">
      <div class="card-badge ${pkg.tier==='Premium'?'b-premium':'b-mass'}">${pkg.tier} Tier</div>
      <h3 style="font-size:1.2rem;margin-bottom:.5rem">${pkg.package_name}</h3>
      <p style="color:var(--muted);font-size:.88rem;margin-bottom:1.2rem;flex:1">${pkg.description}</p>
      <div class="card-price">₹${pkg.price} <span>/ package</span></div>
      <button class="btn btn-primary btn-sm" onclick="showPage('book',{pkg:${pkg.package_id}})">Book This Package</button>
    </div>
  `).join('');
}
function trackByPhone(){
  const ph = document.getElementById('hero-phone').value.trim();
  if(!ph){ flash('Please enter your phone number.','danger'); return; }
  // Store temp to read on bookings page
  sessionStorage.setItem('tempTrackPhone', ph);
  window.location.href = 'bookings.html';
}

// ═══════════════════════════════════════════════════════════════
//  TESTS PAGE
// ═══════════════════════════════════════════════════════════════
let selectedCat = '';
function renderTests(){
  const tests = getTests(), packages = getPackages();
  const cats = [...new Set(tests.map(t=>t.category))].sort();
  const search = (document.getElementById('test-search')||{}).value||'';

  const cb = document.getElementById('cat-btns');
  if(cb) cb.innerHTML=
    `<button class="btn btn-sm ${!selectedCat?'btn-teal':'btn-outline'}" onclick="selectedCat='';renderTests()">All</button>`+
    cats.map(c=>`<button class="btn btn-sm ${selectedCat===c?'btn-teal':'btn-outline'}" onclick="selectedCat='${c}';renderTests()">${c}</button>`).join('');

  const tp = document.getElementById('tests-packages');
  const showPkgs = !selectedCat && !search;
  if(tp) tp.innerHTML = showPkgs?`
    <h2 style="font-size:1.4rem;margin-bottom:1.1rem">📦 Wellness Health Packages</h2>
    <div class="grid4">${packages.map(pkg=>`
      <div class="card">
        <div class="card-badge ${pkg.tier==='Premium'?'b-premium':'b-mass'}">${pkg.tier} Package</div>
        <h3 style="font-size:1.1rem;margin-bottom:.5rem">${pkg.package_name}</h3>
        <p style="color:var(--muted);font-size:.83rem;margin-bottom:1rem;flex:1">${pkg.description}</p>
        <div class="card-price" style="font-size:1.35rem">₹${pkg.price}</div>
        <button class="btn btn-teal btn-sm" style="width:100%" onclick="showPage('book',{pkg:${pkg.package_id}})">Book Package</button>
      </div>
    `).join('')}</div>
  `:'';

  let filtered = tests;
  if(selectedCat) filtered = filtered.filter(t=>t.category===selectedCat);
  if(search) filtered = filtered.filter(t=>t.test_name.toLowerCase().includes(search.toLowerCase())||t.category.toLowerCase().includes(search.toLowerCase()));
  
  const tt = document.getElementById('tests-table');
  if(tt) tt.innerHTML = filtered.map(t=>`
    <tr>
      <td><strong>${t.test_name}</strong></td>
      <td><span class="badge b-scheduled">${t.category}</span></td>
      <td>🩸 ${t.sample_type}</td>
      <td>⏱️ ${t.report_time_hrs} hrs</td>
      <td><strong style="color:var(--primary)">₹${t.price}</strong></td>
      <td><button class="btn btn-primary btn-sm" onclick="showPage('book',{test:${t.test_id}})">Book</button></td>
    </tr>
  `).join('');
}
window.renderTests = renderTests;

// ═══════════════════════════════════════════════════════════════
//  BOOK PAGE
// ═══════════════════════════════════════════════════════════════
function initBookFromURL(){
  const params = new URLSearchParams(window.location.search);
  const extra = {};
  if(params.get('pkg')) extra.pkg = parseInt(params.get('pkg'));
  if(params.get('test')) extra.test = parseInt(params.get('test'));
  initBook(extra);
}

function initBook(extra){
  extra = extra||{};
  const bd = document.getElementById('b-date');
  if(bd) bd.value = new Date().toISOString().split('T')[0];
  
  const pkgs = getPackages();
  const bp = document.getElementById('b-package');
  if(bp) bp.innerHTML=
    '<option value="">-- None (Choose Individual Tests Below) --</option>'+
    pkgs.map(p=>`<option value="${p.package_id}" data-price="${p.price}" ${extra.pkg==p.package_id?'selected':''}>${p.package_name} — ₹${p.price}</option>`).join('');
  
  const btg = document.getElementById('book-tests-grid');
  if(btg) btg.innerHTML=getTests().map(t=>`
    <label class="test-check">
      <div><strong>${t.test_name}</strong><div style="font-size:.76rem;color:var(--muted)">${t.category} | ${t.sample_type}</div></div>
      <div style="display:flex;align-items:center;gap:.5rem">
        <span style="font-weight:700;color:var(--primary)">₹${t.price}</span>
        <input type="checkbox" name="test_ids" value="${t.test_id}" data-price="${t.price}" ${extra.test==t.test_id?'checked':''} onchange="calcTotal()">
      </div>
    </label>
  `).join('');
  calcTotal();
  updateSlots();
}
window.initBook = initBook;

function updateSlots(){
  const dateEl = document.getElementById('b-date');
  if(!dateEl) return;
  const date = dateEl.value;
  const bookings = getBookings().filter(b=>b.booking_date === date && b.status !== 'Cancelled');
  const bookedSlots = bookings.map(b=>b.slot_time);
  
  const allSlots = ['08:00','09:00','10:00','11:00','14:00','16:00','18:00'];
  const slotSel = document.getElementById('b-slot');
  if(slotSel){
    slotSel.innerHTML = allSlots.map(s=>{
      const num = parseInt(s);
      const timeLabel = (num<12 ? s+' AM' : (num===12 ? '12:00 PM' : (num-12<10?'0'+(num-12):num-12)+':00 PM'));
      if(bookedSlots.includes(s)){
        return `<option value="${s}" disabled>${timeLabel} (Booked)</option>`;
      } else {
        return `<option value="${s}">${timeLabel}</option>`;
      }
    }).join('');
  }
}
window.updateSlots = updateSlots;

function calcTotal(){
  const checks = document.querySelectorAll('input[name=test_ids]:checked');
  let total = 0;
  const pkgSel = document.getElementById('b-package');
  let pkgTestIds = [];
  if(pkgSel && pkgSel.value){
    const pkgPrice = parseFloat(pkgSel.options[pkgSel.selectedIndex].dataset.price||0);
    total += pkgPrice;
    const pkg = getPackages().find(p=>p.package_id==pkgSel.value);
    if(pkg) pkgTestIds = pkg.test_ids || [];
  }
  checks.forEach(c => {
    if(!pkgTestIds.includes(parseInt(c.value))){
      total += parseFloat(c.dataset.price||0);
    }
  });
  const typeEl = document.getElementById('b-type');
  const tierEl = document.getElementById('b-tier');
  if(typeEl && tierEl) {
    const type = typeEl.value;
    const tier = tierEl.value;
    if(type==='Home Collection' && tier!=='Premium') total+=150;
    document.getElementById('total-display').innerText='₹'+total.toFixed(2);
    document.getElementById('total-note').innerText = (type==='Home Collection'&&tier!=='Premium')?'Includes ₹150 Home Sample Pickup Fee':'Standard processing included.';
  }
}
window.calcTotal = calcTotal;

function submitBooking(){
  const name  = document.getElementById('b-name').value.trim();
  const phone = document.getElementById('b-phone').value.trim();
  const email = document.getElementById('b-email').value.trim();
  const dob   = document.getElementById('b-dob').value;
  const gender= document.getElementById('b-gender').value;
  const tier  = document.getElementById('b-tier').value;
  const addr  = document.getElementById('b-address').value.trim();
  const type  = document.getElementById('b-type').value;
  const date  = document.getElementById('b-date').value;
  const slot  = document.getElementById('b-slot').value;
  const pay   = document.getElementById('b-pay').value;

  if(!name||!phone||!dob){ flash('Please fill in required patient fields (Name, Phone, DOB).','danger'); return; }
  if(phone.length<10||!/^\d+$/.test(phone)){ flash('Please enter a valid 10-digit phone number.','danger'); return; }

  const checks = [...document.querySelectorAll('input[name=test_ids]:checked')];
  const pkgSel = document.getElementById('b-package');
  if(!checks.length && !pkgSel.value){ flash('Please select at least one test or a package.','danger'); return; }

  let patients = getPatients();
  let patient = patients.find(p=>p.phone===phone);
  let patientId;
  if(patient){
    patientId = patient.patient_id;
    patient.email = email||patient.email;
    patient.membership_tier = tier;
    lsSet('patients', patients);
  } else {
    patientId = nextPatientId();
    patients.push({patient_id:patientId,full_name:name,dob,gender,phone,email,address:addr,membership_tier:tier});
    lsSet('patients', patients);
  }

  let testIds = checks.map(c=>parseInt(c.value));
  let total = 0;
  let pkgTestIds = [];
  if(pkgSel.value){
    const pkg = getPackages().find(p=>p.package_id==pkgSel.value);
    if(pkg) {
      pkg.test_ids.forEach(id=>{if(!testIds.includes(id))testIds.push(id)});
      pkgTestIds = pkg.test_ids;
      total += parseFloat(pkg.price);
    }
  }

  const extraTests = getTests().filter(t => checks.map(c=>parseInt(c.value)).includes(t.test_id) && !pkgTestIds.includes(t.test_id));
  total += extraTests.reduce((s,t)=>s+parseFloat(t.price),0);
  if(type==='Home Collection' && tier!=='Premium') total+=150;

  const bookingId = nextBookingId();
  const bookings  = getBookings();
  bookings.push({booking_id:bookingId,patient_id:patientId,booking_type:type,booking_date:date,slot_time:slot,status:'Scheduled',total_amount:total,test_ids:testIds,payment_status:'Paid',payment_mode:pay});
  lsSet('bookings', bookings);

  sessionStorage.setItem('tempTrackPhone', phone);
  flash(`🎉 Booking #${bookingId} confirmed!`, 'success');
  setTimeout(() => window.location.href = 'bookings.html', 1500);
}
window.submitBooking = submitBooking;

// ═══════════════════════════════════════════════════════════════
//  MY BOOKINGS
// ═══════════════════════════════════════════════════════════════
function lookupBookings(){
  const lp = document.getElementById('lookup-phone');
  if(!lp) return;
  let phone = lp.value.trim();
  const tempPhone = sessionStorage.getItem('tempTrackPhone');
  if(!phone && tempPhone) {
    phone = tempPhone;
    lp.value = phone;
    sessionStorage.removeItem('tempTrackPhone');
  }

  const session = ls('session');
  if(session && session.type === 'patient'){
    const pt = getPatients().find(p=>p.patient_id === session.id);
    if(pt) phone = pt.phone;
    lp.value = phone;
  }
  if(!phone){ document.getElementById('patient-info').innerHTML=''; document.getElementById('bookings-results').innerHTML=emptyState(); return; }
  const patients = getPatients();
  const patient  = patients.find(p=>p.phone===phone);
  if(!patient){
    document.getElementById('patient-info').innerHTML='';
    document.getElementById('bookings-results').innerHTML=`<div style="text-align:center;padding:3.5rem;background:#fff;border-radius:var(--r);border:1px solid var(--border)"><p style="font-size:1.1rem;color:var(--muted)">No records found for <strong>${phone}</strong>.</p><button class="btn btn-primary" style="margin-top:1.25rem" onclick="showPage('book')">Book a New Test Now</button></div>`;
    return;
  }
  document.getElementById('patient-info').innerHTML=`
    <div style="background:var(--primary-light);border:1px solid var(--focus);border-radius:var(--r);padding:1.2rem 1.5rem;margin-bottom:2rem;display:flex;align-items:center;justify-content:space-between">
      <div><h3 style="font-size:1.2rem;color:var(--primary-dark)">👤 Patient: ${patient.full_name}</h3>
      <div style="font-size:.88rem;color:var(--muted)">Phone: ${patient.phone} | Email: ${patient.email||'N/A'}</div></div>
      <span class="badge ${patient.membership_tier==='Premium'?'b-ready':'b-scheduled'}" style="font-size:.88rem;padding:.4rem 1rem">${patient.membership_tier} Membership</span>
    </div>`;
  const bookings = getBookings().filter(b=>b.patient_id===patient.patient_id).sort((a,b)=>b.booking_id-a.booking_id);
  document.getElementById('bookings-results').innerHTML=`
    <h2 style="font-size:1.3rem;margin-bottom:1.1rem">📋 Booking Records (${bookings.length})</h2>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Booking ID</th><th>Type</th><th>Date &amp; Slot</th><th>Tests Booked</th><th>Amount</th><th>Payment</th><th>Status</th><th>Report</th></tr></thead>
        <tbody>${bookings.map(b=>`
          <tr>
            <td><strong style="color:var(--primary)">#${b.booking_id}</strong></td>
            <td><span class="badge ${b.booking_type==='Home Collection'?'b-ready':'b-scheduled'}">${b.booking_type}</span></td>
            <td><div style="font-weight:600">${b.booking_date}</div><div style="font-size:.78rem;color:var(--muted)">🕒 ${b.slot_time}</div></td>
            <td><div style="max-width:220px;font-size:.86rem">${testNames(b.test_ids||[])}</div></td>
            <td><strong>₹${b.total_amount}</strong></td>
            <td><span class="badge ${b.payment_status==='Paid'?'b-paid':'b-pending'}">${b.payment_status||'Pending'}</span></td>
            <td>${statusBadge(b.status)}</td>
            <td>${b.status==='Report Ready'?`<button class="btn btn-teal btn-sm" onclick="showPage('report',${b.booking_id})">📄 View</button>`:'<span style="font-size:.8rem;color:var(--muted);font-style:italic">In Progress</span>'}</td>
          </tr>`).join('')}
        </tbody>
      </table>
    </div>`;
}
window.lookupBookings = lookupBookings;

function statusBadge(s){
  const map = {'Scheduled':'b-scheduled 📅','Sample Collected':'b-collected 🧪','Report Ready':'b-ready ✅','Cancelled':'b-cancelled ❌'};
  const [cls,icon] = (map[s]||'b-scheduled 📅').split(' ');
  return `<span class="badge ${cls}">${icon} ${s}</span>`;
}
function emptyState(){
  return `<div style="text-align:center;padding:4rem 2rem;background:#fff;border-radius:var(--r);border:1px solid var(--border)"><div style="font-size:3rem;margin-bottom:1rem">🔍</div><h3 style="font-size:1.3rem;margin-bottom:.5rem">Track Your Lab Results</h3><p style="color:var(--muted);max-width:480px;margin:0 auto">Enter your 10-digit mobile number above to view all diagnostic appointments and download your verified lab reports.</p></div>`;
}

// ═══════════════════════════════════════════════════════════════
//  ADMIN PAGE
// ═══════════════════════════════════════════════════════════════
function renderAdmin(){
  const bookings  = getBookings();
  const patients  = getPatients();
  const staff     = getStaff();
  const statusF   = (document.getElementById('admin-status-filter')||{}).value||'';
  const typeF     = (document.getElementById('admin-type-filter')||{}).value||'';

  const scheduled  = bookings.filter(b=>b.status==='Scheduled').length;
  const processing = bookings.filter(b=>b.status==='Sample Collected').length;
  const ready      = bookings.filter(b=>b.status==='Report Ready').length;
  const revenue    = bookings.filter(b=>b.status!=='Cancelled').reduce((s,b)=>s+parseFloat(b.total_amount||0),0);
  
  const as = document.getElementById('admin-stats');
  if(as) as.innerHTML=`
    <div class="stat-card"><div class="stat-card-label">Scheduled</div><div class="stat-card-num" style="color:var(--primary)">${scheduled}</div></div>
    <div class="stat-card"><div class="stat-card-label">In Processing</div><div class="stat-card-num" style="color:var(--warning)">${processing}</div></div>
    <div class="stat-card"><div class="stat-card-label">Reports Ready</div><div class="stat-card-num" style="color:var(--success)">${ready}</div></div>
    <div class="stat-card"><div class="stat-card-label">Total Revenue</div><div class="stat-card-num" style="color:var(--text)">₹${revenue.toLocaleString()}</div></div>
  `;

  let filtered = bookings.slice().reverse();
  if(statusF) filtered = filtered.filter(b=>b.status===statusF);
  if(typeF)   filtered = filtered.filter(b=>b.booking_type===typeF);
  filtered = filtered.slice(0,50);

  const atw = document.getElementById('admin-table-wrap');
  if(atw) atw.innerHTML=`
    <table>
      <thead><tr><th>ID</th><th>Patient</th><th>Type / Slot</th><th>Tests</th><th>Update Status</th><th>Payment</th></tr></thead>
      <tbody>${filtered.map(b=>{
        const pt = patients.find(p=>p.patient_id===b.patient_id)||{full_name:'Unknown',phone:''};
        return `<tr>
          <td><strong style="color:var(--primary)">#${b.booking_id}</strong></td>
          <td><strong>${pt.full_name}</strong><div style="font-size:.77rem;color:var(--muted)">📞 ${pt.phone}</div></td>
          <td><span class="badge ${b.booking_type==='Home Collection'?'b-ready':'b-scheduled'}">${b.booking_type}</span><div style="font-size:.77rem;color:var(--muted);margin-top:.2rem">${b.slot_time}</div></td>
          <td><div style="max-width:170px;font-size:.82rem">${testNames(b.test_ids||[])}</div></td>
          <td>
            <select onchange="updateBookingStatus(${b.booking_id},this.value)" style="padding:.3rem .5rem;font-size:.8rem;width:auto">
              ${['Scheduled','Sample Collected','Report Ready','Cancelled'].map(s=>`<option ${b.status===s?'selected':''}>${s}</option>`).join('')}
            </select>
          </td>
          <td>
            <button class="btn btn-sm ${b.payment_status==='Paid'?'btn-teal':'btn-outline'}" onclick="togglePayment(${b.booking_id})">
              ${b.payment_status||'Pending'}
            </button>
          </td>
        </tr>`;
      }).join('')}</tbody>
    </table>`;

  const workload = staff.map(s=>({
    name:s.full_name, role:s.role,
    count:bookings.filter(b=>(b.staff_id||0)===s.staff_id).length
  }));
  const sw = document.getElementById('staff-workload');
  if(sw) sw.innerHTML=workload.map(w=>`
    <div style="display:flex;justify-content:space-between;align-items:center;padding:.7rem 0;border-bottom:1px solid var(--border)">
      <div><strong style="font-size:.93rem">${w.name}</strong><div style="font-size:.76rem;color:var(--muted)">${w.role}</div></div>
      <span class="badge b-scheduled">${w.count} Assigned</span>
    </div>`).join('');
}
window.renderAdmin = renderAdmin;

function updateBookingStatus(id, status){
  const bookings = getBookings();
  const b = bookings.find(b=>b.booking_id===id);
  if(b){ b.status=status; lsSet('bookings',bookings); }
  flash(`Booking #${id} updated to "${status}".`, 'success');
  renderAdmin();
}
window.updateBookingStatus = updateBookingStatus;

function togglePayment(id){
  const bookings = getBookings();
  const b = bookings.find(b=>b.booking_id===id);
  if(b){ b.payment_status = b.payment_status==='Paid'?'Pending':'Paid'; lsSet('bookings',bookings); }
  renderAdmin();
}
window.togglePayment = togglePayment;

function resetFilters(){
  document.getElementById('admin-status-filter').value='';
  document.getElementById('admin-type-filter').value='';
  renderAdmin();
}
window.resetFilters = resetFilters;

// ═══════════════════════════════════════════════════════════════
//  REPORT PAGE
// ═══════════════════════════════════════════════════════════════
function renderReport(bookingId){
  const bookings = getBookings();
  const b = bookings.find(bk=>bk.booking_id===bookingId);
  if(!b){ flash('Booking not found.','danger'); setTimeout(()=>showPage('bookings'),1500); return; }
  const pt = getPatients().find(p=>p.patient_id===b.patient_id)||{full_name:'Unknown'};
  const tests = getTestsByIds(b.test_ids||[]);
  const results = ['Normal','Normal','Normal','Abnormal','Normal','Normal','Normal','Abnormal','Normal','Normal'];
  const rc = document.getElementById('report-content');
  if(rc) rc.innerHTML=`
    <div class="report-hdr">
      <div>
        <div style="font-family:var(--font-h);font-size:1.9rem;font-weight:800;color:var(--primary)">+ MediCheck Diagnostics</div>
        <div style="font-size:.83rem;color:var(--muted)">NABL Accredited &amp; ISO 9001:2015 Certified Reference Laboratory<br>Helpline: +91 1800-123-4567 | Email: reports@medicheck.in</div>
      </div>
      <div style="text-align:right">
        <span class="badge b-ready" style="font-size:.88rem">OFFICIAL TEST REPORT</span>
        <div style="font-size:.83rem;color:var(--muted);margin-top:.5rem">Report Ref: <strong>#MC-${b.booking_id}-2026</strong></div>
      </div>
    </div>
    <div class="report-meta">
      <div>
        <div style="font-size:.79rem;color:var(--muted);font-weight:700;text-transform:uppercase">Patient Info</div>
        <div style="font-size:1.1rem;font-weight:700">${pt.full_name}</div>
        <div style="font-size:.88rem;color:var(--muted)">DOB: ${pt.dob||'N/A'} | Gender: ${pt.gender||'N/A'} | Phone: ${pt.phone||''}</div>
      </div>
      <div style="text-align:right">
        <div style="font-size:.79rem;color:var(--muted);font-weight:700;text-transform:uppercase">Booking Info</div>
        <div style="font-size:.93rem;font-weight:600">Booking Date: ${b.booking_date}</div>
        <div style="font-size:.83rem;color:var(--muted)">Report Generated: ${new Date().toISOString().split('T')[0]}</div>
      </div>
    </div>
    <h3 style="font-size:1.2rem;margin-bottom:1rem;border-bottom:1px solid var(--border);padding-bottom:.5rem">Diagnostic Test Results Summary</h3>
    <div class="table-wrap" style="margin-bottom:2.5rem">
      <table>
        <thead><tr><th>Test Investigation</th><th>Category</th><th>Sample Type</th><th>Observed Result</th><th>Status</th></tr></thead>
        <tbody>${tests.map((t,i)=>{
          const rs = results[i%results.length];
          return `<tr>
            <td><strong>${t.test_name}</strong></td>
            <td>${t.category}</td>
            <td>${t.sample_type}</td>
            <td>${rs==='Normal'?'<span style="color:var(--success);font-weight:700">Within Normal Limits</span>':'<span style="color:var(--danger);font-weight:700">Attention Required</span>'}</td>
            <td><span class="badge ${rs==='Normal'?'b-ready':'b-cancelled'}">${rs}</span></td>
          </tr>`;
        }).join('')}</tbody>
      </table>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:flex-end;border-top:1px dashed var(--border);padding-top:2rem">
      <div style="font-size:.83rem;color:var(--muted)">*** End of Medical Laboratory Report ***<br>This report is electronically authenticated by qualified pathologists.</div>
      <div style="text-align:center">
        <div style="font-family:serif;font-size:1.4rem;color:var(--primary-dark);font-style:italic">Dr. R. K. Patil (MD Path)</div>
        <div style="font-size:.79rem;color:var(--muted);font-weight:700">Chief Consultant Pathologist</div>
      </div>
    </div>`;
}

// ═══════════════════════════════════════════════════════════════
//  CONTACT
// ═══════════════════════════════════════════════════════════════
function submitContact(){
  const name = document.getElementById('c-name').value.trim();
  const email= document.getElementById('c-email').value.trim();
  const msg  = document.getElementById('c-msg').value.trim();
  if(!name||!email||!msg){ flash('Please fill in all required fields.','danger'); return; }
  ['c-name','c-email','c-phone','c-msg'].forEach(id=>document.getElementById(id).value='');
  flash(`Thank you ${name}! Your query has been received. Our team will get back to you within 2 hours.`, 'success');
}
window.submitContact = submitContact;

// ═══════════════════════════════════════════════════════════════
//  AUTHENTICATION POPUP
// ═══════════════════════════════════════════════════════════════
let authLocked = false;
function openAuth(mode='login', locked=true){
  authLocked = locked;
  switchAuth(mode);
  const overlay = document.getElementById('auth-overlay');
  if(overlay) {
    overlay.classList.add('open');
    overlay.classList.toggle('locked', locked);
  }
  document.body.classList.toggle('auth-locked', locked);
}
window.openAuth = openAuth;

function closeAuth(){
  if(authLocked) return;
  const overlay = document.getElementById('auth-overlay');
  if(overlay) {
    overlay.classList.remove('open');
    overlay.classList.remove('locked');
  }
  document.body.classList.remove('auth-locked');
}
window.closeAuth = closeAuth;

function switchAuth(mode){
  ['login','register','staff'].forEach(x=>{
    const p=document.getElementById('auth-'+x); if(p) p.classList.toggle('active',x===mode);
  });
  const tl=document.getElementById('tab-login'), tr=document.getElementById('tab-register');
  if(tl) tl.classList.toggle('active',mode==='login');
  if(tr) tr.classList.toggle('active',mode==='register');
  const tabs=document.querySelector('.auth-tabs');
  if(tabs) tabs.style.display=mode==='staff'?'none':'grid';
  const sw=document.getElementById('staff-switch');
  if(sw){
    sw.textContent=mode==='staff'?'← Back to Patient Login':'Are you a staff member? Staff Login →';
    sw.onclick=()=>switchAuth(mode==='staff'?'login':'staff');
  }
}
window.switchAuth = switchAuth;

function updateAuthNav(){
  const nav=document.getElementById('auth-nav');
  const session=ls('session');
  const adminNav = document.getElementById('nav-admin');
  if(adminNav){
    adminNav.style.display = (session && session.type === 'staff') ? 'block' : 'none';
  }
  if(!nav) return;
  if(session){
    nav.textContent='Logout';
    nav.onclick=logout;
  }else{
    nav.textContent='Login';
    nav.onclick=()=>openAuth('login', false);
  }
}

function patientRegister(){
  const name=document.getElementById('reg-name').value.trim();
  const phone=document.getElementById('reg-phone').value.trim();
  const password=document.getElementById('reg-password').value;
  if(!name||!phone||!password){ alert('Please fill all required fields.'); return; }
  if(!/^\d{10}$/.test(phone)){ alert('Please enter a valid 10-digit phone number.'); return; }
  if(password.length<4){ alert('Password must contain at least 4 characters.'); return; }
  let patients=getPatients();
  let patient=patients.find(p=>p.phone===phone);
  if(patient && patient.password){ alert('An account with this phone number already exists. Please login.'); switchAuth('login'); return; }
  if(patient){ patient.full_name=name; patient.password=password; }
  else{ patient={patient_id:nextPatientId(),full_name:name,dob:'',gender:'',phone,email:'',address:'',membership_tier:'Mass',password}; patients.push(patient); }
  lsSet('patients',patients);
  lsSet('session',{type:'patient',id:patient.patient_id,name:patient.full_name});
  authLocked=false; closeAuth(); updateAuthNav();
  flash('Account created successfully. Welcome, '+patient.full_name+'!','success');
  if(document.body.id === 'page-bookings') window.location.reload();
}
window.patientRegister = patientRegister;

function patientLogin(){
  const phone=document.getElementById('login-phone').value.trim();
  const password=document.getElementById('login-password').value;
  if(!phone||!password){ alert('Please enter phone number and password.'); return; }
  const patient=getPatients().find(p=>p.phone===phone);
  if(!patient){ alert('No patient account found. Please register first.'); return; }
  if(!patient.password){ alert('Demo account. Please register with this number to set a password.'); switchAuth('register'); document.getElementById('reg-phone').value=phone; return; }
  if(patient.password!==password){ alert('Incorrect password.'); return; }
  lsSet('session',{type:'patient',id:patient.patient_id,name:patient.full_name});
  authLocked=false; closeAuth(); updateAuthNav();
  flash('Welcome back, '+patient.full_name+'!','success');
  if(document.body.id === 'page-bookings') window.location.reload();
}
window.patientLogin = patientLogin;

function staffLogin(){
  const id=parseInt(document.getElementById('staff-id').value);
  const password=document.getElementById('staff-password').value;
  const staff=getStaff().find(s=>s.staff_id===id);
  if(!staff){ alert('Invalid Staff ID.'); return; }
  if(password!=='medicheck123'){ alert('Incorrect staff password.'); return; }
  lsSet('session',{type:'staff',id:staff.staff_id,name:staff.full_name,role:staff.role});
  authLocked=false; closeAuth(); updateAuthNav(); 
  flash('Staff login successful — '+staff.full_name+' ('+staff.role+').','success');
  setTimeout(()=>showPage('admin'), 500);
}
window.staffLogin = staffLogin;

function logout(){
  localStorage.removeItem('mc_session');
  updateAuthNav();
  if(document.body.id === 'page-admin' || document.body.id === 'page-bookings') showPage('home');
  else flash('You have been logged out.','success');
}
window.logout = logout;

document.addEventListener('keydown',e=>{ if(e.key==='Escape') closeAuth(); });
