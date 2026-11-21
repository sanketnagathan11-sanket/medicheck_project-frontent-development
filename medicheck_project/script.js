
// ═══════════════════════════════════════════════════════════════
//  DATA STORE — persisted to localStorage
// ═══════════════════════════════════════════════════════════════
const DEFAULT_TESTS = [
  {test_id:1,test_name:'Complete Blood Count (CBC)',category:'Blood & Sugar',sample_type:'Blood',price:350,report_time_hrs:6},
  {test_id:2,test_name:'Fasting Blood Sugar',category:'Blood & Sugar',sample_type:'Blood',price:150,report_time_hrs:4},
  {test_id:3,test_name:'HbA1c',category:'Blood & Sugar',sample_type:'Blood',price:500,report_time_hrs:12},
  {test_id:4,test_name:'Lipid Profile',category:'Cardiac',sample_type:'Blood',price:600,report_time_hrs:12},
  {test_id:5,test_name:'ECG',category:'Cardiac',sample_type:'N/A',price:400,report_time_hrs:2},
  {test_id:6,test_name:'Troponin-I',category:'Cardiac',sample_type:'Blood',price:900,report_time_hrs:6},
  {test_id:7,test_name:'Thyroid Profile (T3 T4 TSH)',category:'Thyroid',sample_type:'Blood',price:700,report_time_hrs:24},
  {test_id:8,test_name:'Liver Function Test (LFT)',category:'Liver & Kidney',sample_type:'Blood',price:650,report_time_hrs:12},
  {test_id:9,test_name:'Kidney Function Test (KFT)',category:'Liver & Kidney',sample_type:'Blood',price:650,report_time_hrs:12},
  {test_id:10,test_name:'Urine Routine',category:'Liver & Kidney',sample_type:'Urine',price:200,report_time_hrs:6},
  {test_id:11,test_name:'Chest X-Ray',category:'Imaging',sample_type:'N/A',price:500,report_time_hrs:4},
  {test_id:12,test_name:'Abdominal Ultrasound',category:'Imaging',sample_type:'N/A',price:1200,report_time_hrs:8},
  {test_id:13,test_name:'Vitamin D',category:'Full Body Checkup',sample_type:'Blood',price:1400,report_time_hrs:24},
  {test_id:14,test_name:'Vitamin B12',category:'Full Body Checkup',sample_type:'Blood',price:900,report_time_hrs:24},
  {test_id:15,test_name:'COVID-19 RT-PCR',category:'Full Body Checkup',sample_type:'Swab',price:700,report_time_hrs:24}
];
const DEFAULT_PACKAGES = [
  {package_id:1,package_name:'Basic Health Checkup',description:'CBC + Sugar + Urine Routine',price:550,tier:'Mass',test_ids:[1,2,10]},
  {package_id:2,package_name:'Diabetes Care Package',description:'Sugar + HbA1c + KFT',price:1100,tier:'Mass',test_ids:[2,3,9]},
  {package_id:3,package_name:'Executive Full Body Checkup',description:'15-parameter premium panel',price:3999,tier:'Premium',test_ids:[1,3,4,7,8,9,13,14]},
  {package_id:4,package_name:'Cardiac Risk Package',description:'Lipid + ECG + Troponin-I',price:1800,tier:'Premium',test_ids:[4,5,6]}
];
const DEFAULT_STAFF = [
  {staff_id:1,full_name:'Diya Deshmukh',role:'Technician'},
  {staff_id:2,full_name:'Karan Reddy',role:'Technician'},
  {staff_id:3,full_name:'Rohan Shah',role:'Technician'},
  {staff_id:4,full_name:'Pranav Verma',role:'Receptionist'},
  {staff_id:5,full_name:'Aditi Verma',role:'Courier'},
  {staff_id:6,full_name:'Ritu Patil',role:'Admin'}
];
const SEED_PATIENTS = [
  {patient_id:1,full_name:'Nikhil Patil',dob:'1956-12-09',gender:'Male',phone:'9339670711',email:'nikhil.patil1@example.com',membership_tier:'Premium'},
  {patient_id:2,full_name:'Anjali Gokhale',dob:'1989-02-19',gender:'Female',phone:'9134126396',email:'anjali.gokhale2@example.com',membership_tier:'Premium'},
  {patient_id:3,full_name:'Isha Reddy',dob:'1993-01-18',gender:'Male',phone:'9868820204',email:'isha.reddy3@example.com',membership_tier:'Mass'},
  {patient_id:4,full_name:'Neha Deshmukh',dob:'1983-10-09',gender:'Male',phone:'9914763202',email:'neha.deshmukh4@example.com',membership_tier:'Mass'},
  {patient_id:5,full_name:'Neha Kumar',dob:'1972-03-07',gender:'Female',phone:'9209747451',email:'neha.kumar5@example.com',membership_tier:'Premium'},
];
const SEED_BOOKINGS = [
  {booking_id:1,patient_id:1,booking_type:'Walk-in',booking_date:'2026-01-03',slot_time:'11:00',status:'Report Ready',total_amount:1500,test_ids:[4,14],payment_status:'Paid',payment_mode:'Online'},
  {booking_id:2,patient_id:2,booking_type:'Walk-in',booking_date:'2026-01-10',slot_time:'14:00',status:'Report Ready',total_amount:2350,test_ids:[11,12,8],payment_status:'Paid',payment_mode:'UPI'},
  {booking_id:3,patient_id:3,booking_type:'Walk-in',booking_date:'2026-01-02',slot_time:'08:00',status:'Report Ready',total_amount:1500,test_ids:[3,1,9],payment_status:'Paid',payment_mode:'Online'},
  {booking_id:4,patient_id:4,booking_type:'Home Collection',booking_date:'2026-01-08',slot_time:'17:00',status:'Sample Collected',total_amount:700,test_ids:[7],payment_status:'Pending',payment_mode:'Cash'},
  {booking_id:5,patient_id:5,booking_type:'Walk-in',booking_date:'2026-01-07',slot_time:'18:00',status:'Scheduled',total_amount:1200,test_ids:[7,3],payment_status:'Paid',payment_mode:'Card'},
];

function ls(key){ return JSON.parse(localStorage.getItem('mc_'+key)||'null') }
function lsSet(key,val){ localStorage.setItem('mc_'+key, JSON.stringify(val)) }

function initData(){
  if(!ls('patients')){ lsSet('patients', SEED_PATIENTS) }
  if(!ls('bookings')){ lsSet('bookings', SEED_BOOKINGS) }
  if(!ls('tests')){ lsSet('tests', DEFAULT_TESTS) }
  if(!ls('packages')){ lsSet('packages', DEFAULT_PACKAGES) }
  if(!ls('staff')){ lsSet('staff', DEFAULT_STAFF) }
}
initData();

function getTests(){ return ls('tests')||[] }
function getPackages(){ return ls('packages')||[] }
function getPatients(){ return ls('patients')||[] }
function getBookings(){ return ls('bookings')||[] }
function getStaff(){ return ls('staff')||[] }

let nextPatientId = () => Math.max(0,...getPatients().map(p=>p.patient_id))+1;
let nextBookingId = () => Math.max(0,...getBookings().map(b=>b.booking_id))+1;

function getTestsByIds(ids){ return getTests().filter(t=>ids.includes(t.test_id)) }
function testNames(ids){ return getTestsByIds(ids).map(t=>t.test_name).join(', ') }

// ═══════════════════════════════════════════════════════════════
//  NAVIGATION
// ═══════════════════════════════════════════════════════════════
let currentPage = 'home';
function showPage(name, extra){
  if (name === 'bookings') {
    const session = ls('session');
    if (!session || session.type !== 'patient') {
      showPage('home');
      setTimeout(() => {
        const loginSec = document.querySelector('.split-login-section');
        if(loginSec) loginSec.scrollIntoView({behavior: 'smooth'});
        else openAuth();
      }, 50);
      flash('Please login to view your bookings.', 'warning');
      return;
    }
  }

  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('nav a[id]').forEach(a=>a.classList.remove('active'));
  const pg = document.getElementById('page-'+name);
  if(pg) pg.classList.add('active');
  const navEl = document.getElementById('nav-'+name);
  if(navEl) navEl.classList.add('active');
  currentPage = name;
  window.scrollTo(0,0);
  if(name==='home') renderHome();
  if(name==='tests') renderTests();
  if(name==='book') initBook(extra);
  if(name==='admin') renderAdmin();
  if(name==='profile') renderProfile();
  if(name==='report' && extra) renderReport(extra);
  if(name==='bookings') lookupBookings();
  if(name==='profile') renderProfile();
  if(name==='patients') renderPatients();
}









// ═══════════════════════════════════════════════════════════════
//  FLASH MESSAGES
// ═══════════════════════════════════════════════════════════════

  function renderProfile() {
    const session = ls('session');
    if(!session || session.type !== 'patient') { showPage('home'); return; }
    const patient = getPatients().find(p => p.patient_id === session.id);
    if(patient) {
      document.getElementById('prof-name').value = patient.full_name;
      document.getElementById('prof-phone').value = patient.phone;
        document.getElementById('prof-email').value = patient.email || '';
        document.getElementById('prof-dob').value = patient.dob || '';
        document.getElementById('prof-gender').value = patient.gender || '';
        document.getElementById('prof-blood').value = patient.blood_group || '';
        document.getElementById('prof-address').value = patient.address || '';
        document.getElementById('prof-password').value = ''; 
      
      const initialEl = document.getElementById('prof-initial');
      if(initialEl) initialEl.innerText = patient.full_name.charAt(0).toUpperCase();
      const nameEl = document.getElementById('prof-display-name');
      if(nameEl) nameEl.innerText = patient.full_name;
      const tierEl = document.getElementById('prof-tier-badge');
      if(tierEl) tierEl.innerText = (patient.membership_tier || 'Standard') + ' Client';
      
      const pBookings = getBookings().filter(b=>b.patient_id===patient.patient_id).sort((a,b)=>b.booking_id-a.booking_id);
      
      const total = pBookings.length;
      const done = pBookings.filter(b=>b.status==='Report Ready').length;
      const cancelled = pBookings.filter(b=>b.status==='Cancelled').length;
      
      const tEl = document.getElementById('prof-stat-total');
      if(tEl) tEl.innerText = total;
      const dEl = document.getElementById('prof-stat-done');
      if(dEl) dEl.innerText = done;
      const cEl = document.getElementById('prof-stat-cancel');
      if(cEl) cEl.innerText = cancelled;
      
      let html = '';
      if(pBookings.length === 0){
         html = '<div style="padding:3rem 0;text-align:center;color:var(--muted)">No appointments found.</div>';
      } else {
         const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
         html = pBookings.map(b => {
            const d = new Date(b.booking_date);
            const m = months[d.getMonth()];
            const day = d.getDate();
            
            let badgeClass = 'b-scheduled';
            let statusText = 'Booked';
            if(b.status === 'Report Ready') { badgeClass = 'b-ready'; statusText = 'Done'; }
            if(b.status === 'Cancelled') { badgeClass = ''; statusText = 'Cancelled'; }
            if(b.status === 'Sample Collected') { badgeClass = 'b-ready'; statusText = 'Processing'; }
            
            return `
            <div style="display:flex; align-items:center; justify-content:space-between; padding:1.25rem 0; border-bottom:1px solid #f1f5f9;">
               <div style="display:flex; gap:1.5rem; align-items:center;">
                  <div style="text-align:center; min-width:40px;">
                     <div style="font-size:1.3rem; font-weight:700; color:var(--text); line-height:1;">${day}</div>
                     <div style="font-size:.8rem; color:var(--muted); text-transform:uppercase; margin-top:.1rem;">${m}</div>
                  </div>
                  <div>
                     <div style="font-weight:600; color:var(--text); font-size:1.05rem; max-width:200px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${b.booking_type} Visit</div>
                     <div style="font-size:.85rem; color:var(--muted); margin-top:.2rem;">${b.slot_time}</div>
                  </div>
               </div>
               <div style="display:flex; gap:2.5rem; align-items:center;">
                  <span class="badge ${badgeClass}" style="${statusText==='Cancelled'?'background:#ffedd5;color:#c2410c':''}">${statusText}</span>
                  <div style="text-align:right; min-width:70px;">
                     <div style="font-weight:700; color:var(--text); font-size:1.05rem;">,1${b.total_amount}</div>
                  </div>
               </div>
            </div>`;
         }).join('');
      }
      const rb = document.getElementById('prof-recent-bookings');
      if(rb) rb.innerHTML = html;
    }
  }

  function updateProfile() {
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
    }

  function flash(msg, type=''){
  const c = document.getElementById('flash-container');
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
  document.getElementById('home-stats').innerHTML=`
    <div class="stat-item"><div class="stat-num">${patients.length}+</div><div class="stat-label">Registered Patients</div></div>
    <div class="stat-item"><div class="stat-num">${tests.length}</div><div class="stat-label">Lab Tests Offered</div></div>
    <div class="stat-item"><div class="stat-num">${bookings.length}</div><div class="stat-label">Bookings Completed</div></div>
    <div class="stat-item"><div class="stat-num">NABL</div><div class="stat-label">Certified Accreditation</div></div>
  `;
  const pkgs = getPackages().slice(0,3);
  document.getElementById('home-packages').innerHTML=pkgs.map(pkg=>`
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
  document.getElementById('lookup-phone').value = ph;
  showPage('bookings');
  setTimeout(lookupBookings, 100);
}

// ═══════════════════════════════════════════════════════════════
//  TESTS PAGE
// ═══════════════════════════════════════════════════════════════
let selectedCat = '';
function renderTests(){
  const tests = getTests(), packages = getPackages();
  const cats = [...new Set(tests.map(t=>t.category))].sort();
  const search = (document.getElementById('test-search')||{}).value||'';

  // Category buttons
  document.getElementById('cat-btns').innerHTML=
    `<button class="btn btn-sm ${!selectedCat?'btn-teal':'btn-outline'}" onclick="selectedCat='';renderTests()">All</button>`+
    cats.map(c=>`<button class="btn btn-sm ${selectedCat===c?'btn-teal':'btn-outline'}" onclick="selectedCat='${c}';renderTests()">${c}</button>`).join('');

  // Packages grid (only when no filter)
  const showPkgs = !selectedCat && !search;
  document.getElementById('tests-packages').innerHTML = showPkgs?`
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

  // Tests table
  let filtered = tests;
  if(selectedCat) filtered = filtered.filter(t=>t.category===selectedCat);
  if(search) filtered = filtered.filter(t=>t.test_name.toLowerCase().includes(search.toLowerCase())||t.category.toLowerCase().includes(search.toLowerCase()));
  document.getElementById('tests-table').innerHTML = filtered.map(t=>`
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

// ═══════════════════════════════════════════════════════════════
//  BOOK PAGE
// ═══════════════════════════════════════════════════════════════
function initBook(extra){
  extra = extra||{};
  // Set today's date
  document.getElementById('b-date').value = new Date().toISOString().split('T')[0];
  
  // Pre-fill if logged in
  const session = ls('session');
  if(session && session.type === 'patient') {
    const pt = getPatients().find(p => p.patient_id === session.id);
    if(pt) {
      document.getElementById('b-name').value = pt.full_name || '';
      document.getElementById('b-phone').value = pt.phone || '';
      document.getElementById('b-email').value = pt.email || '';
      document.getElementById('b-dob').value = pt.dob || '';
      document.getElementById('b-gender').value = pt.gender || 'Male';
      document.getElementById('b-bloodgroup').value = pt.blood_group || '';
      document.getElementById('b-address').value = pt.address || '';
      
      // Lock identity fields for security
      document.getElementById('b-phone').disabled = true;
      document.getElementById('b-phone').style.background = '#f1f5f9';
    }
  } else {
    document.getElementById('b-name').value = '';
    document.getElementById('b-phone').value = '';
    document.getElementById('b-email').value = '';
    document.getElementById('b-dob').value = '';
    document.getElementById('b-gender').value = 'Male';
    document.getElementById('b-bloodgroup').value = '';
    document.getElementById('b-address').value = '';
    
    document.getElementById('b-phone').disabled = false;
    document.getElementById('b-phone').style.background = '#fff';
  }
  // Packages dropdown
  const pkgs = getPackages();
  document.getElementById('b-package').innerHTML=
    '<option value="">-- None (Choose Individual Tests Below) --</option>'+
    pkgs.map(p=>`<option value="${p.package_id}" data-price="${p.price}" ${extra.pkg==p.package_id?'selected':''}>${p.package_name} — ₹${p.price}</option>`).join('');
  // Tests checkboxes
  document.getElementById('book-tests-grid').innerHTML=getTests().map(t=>`
    <label class="test-check">
      <div><strong>${t.test_name}</strong><div style="font-size:.76rem;color:var(--muted)">${t.category} | ${t.sample_type}</div></div>
      <div style="display:flex;align-items:center;gap:.5rem">
        <span style="font-weight:700;color:var(--primary)">₹${t.price}</span>
        <input type="checkbox" name="test_ids" value="${t.test_id}" data-price="${t.price}" ${extra.test==t.test_id?'checked':''} onchange="calcTotal()">
      </div>
    </label>
  `).join('');
  calcTotal();
}

function calcTotal(){
  const checks = document.querySelectorAll('input[name=test_ids]:checked');
  let total = 0;
  checks.forEach(c=>total+=parseFloat(c.dataset.price||0));
  const pkgSel = document.getElementById('b-package');
  if(pkgSel && pkgSel.value){
    const pkgPrice = parseFloat(pkgSel.options[pkgSel.selectedIndex].dataset.price||0);
    if(pkgPrice>0) total = total>0?Math.min(total,pkgPrice):pkgPrice;
  }
  const type = document.getElementById('b-type').value;
  const tier = document.getElementById('b-tier').value;
  if(type==='Home Collection' && tier!=='Premium') total+=150;
  document.getElementById('total-display').innerText='₹'+total.toFixed(2);
  document.getElementById('total-note').innerText = (type==='Home Collection'&&tier!=='Premium')?'Includes ₹150 Home Sample Pickup Fee':'Standard processing included.';
}

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

  // Find or create patient
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

  // Gather test IDs
  let testIds = checks.map(c=>parseInt(c.value));
  if(pkgSel.value){
    const pkg = getPackages().find(p=>p.package_id==pkgSel.value);
    if(pkg) pkg.test_ids.forEach(id=>{if(!testIds.includes(id))testIds.push(id)});
  }

  // Price
  const priced = getTests().filter(t=>testIds.includes(t.test_id));
  let total = priced.reduce((s,t)=>s+parseFloat(t.price),0);
  if(pkgSel.value){
    const pkg = getPackages().find(p=>p.package_id==pkgSel.value);
    if(pkg) total = total>0?Math.min(total,parseFloat(pkg.price)):parseFloat(pkg.price);
  }
  if(type==='Home Collection' && tier!=='Premium') total+=150;

  const bookingId = nextBookingId();
  const bookings  = getBookings();
  bookings.push({booking_id:bookingId,patient_id:patientId,booking_type:type,booking_date:date,slot_time:slot,status:'Scheduled',total_amount:total,test_ids:testIds,payment_status:'Paid',payment_mode:pay});
  lsSet('bookings', bookings);

  flash(`🎉 Booking #${bookingId} confirmed! Use phone (${phone}) to track your booking.`, 'success');
  document.getElementById('lookup-phone').value = phone;
  showPage('bookings');
  setTimeout(lookupBookings, 100);
}

// ═══════════════════════════════════════════════════════════════
//  MY BOOKINGS
// ═══════════════════════════════════════════════════════════════
function lookupBookings(){
  let phone = document.getElementById('lookup-phone').value.trim();
  const session = ls('session');
  const container = document.getElementById('lookup-phone-container');
  if(session && session.type === 'patient'){
    const pt = getPatients().find(p=>p.patient_id === session.id);
    if(pt) phone = pt.phone;
    if(container) container.style.display = 'none';
  } else {
    if(container) container.style.display = 'block';
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
  const session   = ls('session') || {};
  const isAdmin   = session.role === 'Admin';

  // Stats
  const scheduled  = bookings.filter(b=>b.status==='Scheduled').length;
  const processing = bookings.filter(b=>b.status==='Sample Collected').length;
  const ready      = bookings.filter(b=>b.status==='Report Ready').length;
  const revenue    = bookings.filter(b=>b.status!=='Cancelled').reduce((s,b)=>s+parseFloat(b.total_amount||0),0);
  document.getElementById('admin-stats').innerHTML=`
    <div class="stat-card"><div class="stat-card-label">Scheduled</div><div class="stat-card-num" style="color:var(--primary)">${scheduled}</div></div>
    <div class="stat-card"><div class="stat-card-label">In Processing</div><div class="stat-card-num" style="color:var(--warning)">${processing}</div></div>
    <div class="stat-card"><div class="stat-card-label">Reports Ready</div><div class="stat-card-num" style="color:var(--success)">${ready}</div></div>
    <div class="stat-card"><div class="stat-card-label">Total Revenue</div><div class="stat-card-num" style="color:var(--text)">₹${revenue.toLocaleString()}</div></div>
  `;

  let filtered = bookings.slice().reverse();
  if(statusF) filtered = filtered.filter(b=>b.status===statusF);
  if(typeF)   filtered = filtered.filter(b=>b.booking_type===typeF);
  filtered = filtered.slice(0,50);

  document.getElementById('admin-table-wrap').innerHTML=`
    <table>
      <thead><tr><th>ID</th><th>Patient</th><th>Type / Slot</th><th>Tests</th><th>Update Status</th><th>Assign Staff</th><th>Payment</th></tr></thead>
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
            <select onchange="updateBookingStaff(${b.booking_id},this.value)" style="padding:.3rem .5rem;font-size:.8rem;width:auto">
              <option value="">Unassigned</option>
              ${staff.filter(s=>s.role==='Technician').map(s=>`<option value="${s.staff_id}" ${b.staff_id==s.staff_id?'selected':''}>${s.full_name}</option>`).join('')}
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

  // Staff workload
  const workload = staff.map(s=>({
    id:s.staff_id, name:s.full_name, role:s.role,
    count:bookings.filter(b=>(b.staff_id||0)===s.staff_id).length
  }));
  if (isAdmin) {
    document.getElementById('staff-workload').innerHTML=workload.map(w=>`
        <div style="display:flex; justify-content:space-between; align-items:center; gap:1rem; padding:1.25rem 0; border-bottom:1px solid var(--border)">
          <div style="flex:1; min-width:0; display:flex; flex-direction:column; gap:0.4rem;">
             <div style="font-size:1.05rem; font-weight:700; color:var(--text); white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" title="${w.name}">${w.name}</div>
             <select onchange="updateStaffRole(${w.id}, this.value)" style="padding:.3rem .5rem; font-size:.85rem; border:1px solid var(--border); border-radius:6px; background:#f8fafc; max-width:140px; cursor:pointer;">
               ${['Technician', 'Receptionist', 'Courier', 'Admin'].map(r => `<option ${w.role===r?'selected':''}>${r}</option>`).join('')}
             </select>
          </div>
          <div style="display:flex; flex-direction:column; align-items:flex-end; gap:.6rem;">
            <span class="badge b-scheduled" style="white-space:nowrap; font-size:.8rem; padding:.3rem .8rem;">${w.count} Assigned</span>
            ${w.id !== session.id ? `<button class="btn btn-outline btn-sm" style="padding:.3rem .8rem; font-size:.8rem; border-color:#cbd5e1; color:var(--text);" onclick="removeStaff(${w.id})">Remove</button>` : `<div style="height:28px;"></div>`}
          </div>
        </div>`).join('') + `
        <div style="margin-top:1.5rem;display:flex;flex-direction:column;gap:.75rem;border-top:1px solid var(--border);padding-top:1.5rem">
          <input id="new-staff-name" placeholder="Enter New Staff Name..." style="width:100%;padding:.7rem 1rem;font-size:.95rem;border:1px solid var(--border);border-radius:8px;outline:none;">
          <button class="btn btn-teal" style="width:100%;padding:.7rem;border-radius:8px;font-size:1rem;" onclick="addStaff()">+ Add Staff</button>
        </div>`;
  } else {
    const myStaff = workload.find(w => w.id === session.id);
    if (myStaff) {
      document.getElementById('staff-workload').innerHTML=`
        <div style="padding:.7rem 0;">
          <div><strong style="font-size:1.1rem;color:var(--primary-dark)">${myStaff.name}</strong></div>
          <div style="font-size:.9rem;color:var(--muted);margin-top:.4rem;">Role: ${myStaff.role}</div>
          <div style="margin-top:.8rem;"><span class="badge b-scheduled">${myStaff.count} Assigned Bookings</span></div>
        </div>
      `;
    }
  }
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
              <th style="padding:.5rem">Gender</th>
                <th style="padding:.5rem">DOB</th>
                <th style="padding:.5rem">Blood</th>
              <th style="padding:.5rem">Address</th>
              <th style="padding:.5rem">Tier</th>
                <th style="padding:.5rem;text-align:center;">Action</th>
            </tr>
          </thead>
          <tbody>
              ${getPatients().map(p => `
                <tr style="border-bottom:1px solid var(--border);">
                  <td style="padding:.5rem;color:var(--primary)">#${p.patient_id}</td>
                  <td style="padding:.5rem"><strong>${p.full_name}</strong></td>
                  <td style="padding:.5rem">${p.phone}</td>
                  <td style="padding:.5rem">${p.email || '-'}</td>
                  <td style="padding:.5rem">${p.gender || '-'}</td>
                  <td style="padding:.5rem">${p.dob || '-'}</td>
                  <td style="padding:.5rem">${p.blood_group || '-'}</td>
                  <td style="padding:.5rem">${p.address || '-'}</td>
                  <td style="padding:.5rem"><span class="badge ${p.membership_tier==='Premium'?'b-ready':'b-scheduled'}">${p.membership_tier || 'Standard'}</span></td>
                  <td style="padding:.5rem;text-align:center;">
                    <button class="btn btn-outline btn-sm" style="padding:.25rem .6rem; font-size:.75rem; border-color:#fca5a5; color:#dc2626;" onclick="removePatient(${p.patient_id})">Delete</button>
                  </td>
                </tr>
              `).join('')}
            </tbody>
        </table>
      </div>`;
      
  const container = document.getElementById('patients-table-container');
  if(container) container.innerHTML = customerHTML;
}

function addStaff() {
  const session = ls('session');
  if(!session || session.role !== 'Admin') return;
  const name = document.getElementById('new-staff-name').value.trim();
  if(!name) { flash('Please enter a staff name', 'danger'); return; }
  const staff = getStaff();
  const newId = Math.max(0, ...staff.map(s => s.staff_id)) + 1;
  staff.push({ staff_id: newId, full_name: name, role: 'Technician' });
  lsSet('staff', staff);
  flash('Staff member ' + name + ' added successfully.', 'success');
  renderAdmin();
}

function removeStaff(id) {
  const session = ls('session');
  if(!session || session.role !== 'Admin') return;
  if(id === session.id) { flash('You cannot remove yourself.', 'danger'); return; }
  let staff = getStaff();
  staff = staff.filter(s => s.staff_id !== id);
  lsSet('staff', staff);
  flash('Staff member removed.', 'success');
  renderAdmin();
}

function updateBookingStatus(id, status){
  const bookings = getBookings();
  const b = bookings.find(b=>b.booking_id===id);
  if(b){ b.status=status; lsSet('bookings',bookings); }
  flash(`Booking #${id} updated to "${status}".`, 'success');
  renderAdmin();
}

function updateBookingStaff(bookingId, staffId) {
  const bookings = getBookings();
  const b = bookings.find(b=>b.booking_id===bookingId);
  if (b) {
    b.staff_id = staffId ? parseInt(staffId) : null;
    lsSet('bookings', bookings);
  }
  flash(`Assigned technician to booking #${bookingId}`, 'success');
  renderAdmin();
}

function updateStaffRole(staffId, newRole) {
  const staff = getStaff();
  const s = staff.find(st=>st.staff_id===staffId);
  if (s) {
    s.role = newRole;
    lsSet('staff', staff);
  }
  flash(`Updated role for ${s.full_name} to ${newRole}`, 'success');
  renderAdmin();
}

function togglePayment(id){
  const bookings = getBookings();
  const b = bookings.find(b=>b.booking_id===id);
  if(b){ b.payment_status = b.payment_status==='Paid'?'Pending':'Paid'; lsSet('bookings',bookings); }
  renderAdmin();
}

function resetFilters(){
  document.getElementById('admin-status-filter').value='';
  document.getElementById('admin-type-filter').value='';
  renderAdmin();
}

// ═══════════════════════════════════════════════════════════════
//  REPORT PAGE
// ═══════════════════════════════════════════════════════════════
function renderReport(bookingId){
  const bookings = getBookings();
  const b = bookings.find(bk=>bk.booking_id===bookingId);
  if(!b){ flash('Booking not found.','danger'); showPage('bookings'); return; }
  const pt = getPatients().find(p=>p.patient_id===b.patient_id)||{full_name:'Unknown'};
  const tests = getTestsByIds(b.test_ids||[]);
  const results = ['Normal','Normal','Normal','Abnormal','Normal','Normal','Normal','Abnormal','Normal','Normal'];
  document.getElementById('report-content').innerHTML=`
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

// ═══════════════════════════════════════════════════════════════
//  INIT
// ═══════════════════════════════════════════════════════════════
renderHome();


let authLocked = false;

function openAuth(mode='login', locked=true){
  authLocked = locked;
  switchAuth(mode);
  const overlay = document.getElementById('auth-overlay');
  overlay.classList.add('open');
  overlay.classList.toggle('locked', locked);
  document.body.classList.toggle('auth-locked', locked);
}

function closeAuth(){
  if(authLocked) return;
  document.getElementById('auth-overlay').classList.remove('open');
  document.getElementById('auth-overlay').classList.remove('locked');
  document.body.classList.remove('auth-locked');
}
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
function updateAuthNav(){
  const nav=document.getElementById('auth-nav');
  const session=ls('session');
  
  const adminNav = document.getElementById('nav-admin');
  const profileNav = document.getElementById('nav-profile');
  const bookingsNav = document.getElementById('nav-bookings');
  const patientsNav = document.getElementById('nav-patients');

  let isStaff = (session && session.type === 'staff');
  let isAdmin = false;
  if (isStaff) {
    let staff = getStaff().find(s => s.staff_id === session.id);
    if (staff && staff.role === 'Admin') isAdmin = true;
  }

  if(adminNav) adminNav.style.display = isStaff ? 'inline-block' : 'none';
  if(patientsNav) patientsNav.style.display = isAdmin ? 'inline-block' : 'none';
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
    nav.onclick=() => {
      showPage('home');
      setTimeout(() => {
        const loginSec = document.querySelector('.split-login-section');
        if(loginSec) loginSec.scrollIntoView({behavior: 'smooth'});
        else openAuth('login', false);
      }, 50);
    };
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
  if(patient){
    patient.full_name=name; patient.password=password;
  }else{
    patient={patient_id:nextPatientId(),full_name:name,dob:'',gender:'',phone,email:'',address:'',membership_tier:'Mass',password};
    patients.push(patient);
  }
  lsSet('patients',patients);
  lsSet('session',{type:'patient',id:patient.patient_id,name:patient.full_name});
  authLocked=false; closeAuth(); updateAuthNav(); showPage('bookings');
  flash('Account created successfully. Welcome, '+patient.full_name+'!','success');
}
function switchPageAuth(type) {
  document.querySelectorAll('.page-auth-pane').forEach(p => p.classList.remove('active'));
  document.getElementById('page-auth-' + type).classList.add('active');
}

function pagePatientRegister() {
  const name=document.getElementById('page-reg-name').value.trim();
  const phone=document.getElementById('page-reg-phone').value.trim();
  const password=document.getElementById('page-reg-password').value;
  const dob=document.getElementById('page-reg-dob').value;
  const gender=document.getElementById('page-reg-gender').value;
  const email=document.getElementById('page-reg-email').value.trim();
  const address=document.getElementById('page-reg-address').value.trim();
  const bloodgroup=document.getElementById('page-reg-bloodgroup').value;

  if(!name||!phone||!password||!dob||!gender||!address||!bloodgroup){ flash('Please fill in all required fields.', 'danger'); return; }
  let patients=getPatients();
  if(patients.some(p=>p.phone===phone)){ flash('Phone number already registered. Please login.', 'danger'); switchPageAuth('login'); document.getElementById('page-login-phone').value=phone; return; }
  const newId=patients.length>0 ? Math.max(...patients.map(p=>p.patient_id))+1 : 1;
  
  const patient={
    patient_id:newId, full_name:name, phone:phone, password:password,
    dob:dob, gender:gender, email:email, address:address, blood_group:bloodgroup, membership_tier:'Standard'
  };
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

function pagePatientLogin(){
  const phone=document.getElementById('page-login-phone').value.trim();
  const password=document.getElementById('page-login-password').value;
  if(!phone||!password){ flash('Please enter phone number and password.', 'danger'); return; }
  const patient=getPatients().find(p=>p.phone===phone);
  if(!patient){ flash('No patient account found. Please register first.', 'danger'); return; }
  if(!patient.password){
    alert('This is a preloaded demo patient. Please use Register with this phone number once to create a password.');
    openAuth(); switchAuth('register'); document.getElementById('reg-phone').value=phone; return;
  }
  if(patient.password!==password){ flash('Incorrect password.', 'danger'); return; }
  lsSet('session',{type:'patient',id:patient.patient_id,name:patient.full_name});
  updateAuthNav(); showPage('bookings'); // Redirects to My Bookings directly!
  flash('Welcome back, '+patient.full_name+'!','success');
}

function patientLogin(){
  const phone=document.getElementById('login-phone').value.trim();
  const password=document.getElementById('login-password').value;
  if(!phone||!password){ alert('Please enter phone number and password.'); return; }
  const patient=getPatients().find(p=>p.phone===phone);
  if(!patient){ alert('No patient account found. Please register first.'); return; }
  if(!patient.password){
    alert('This is a preloaded demo patient. Please use Register with this phone number once to create a password.');
    switchAuth('register'); document.getElementById('reg-phone').value=phone; return;
  }
  if(patient.password!==password){ alert('Incorrect password.'); return; }
  lsSet('session',{type:'patient',id:patient.patient_id,name:patient.full_name});
  authLocked=false; closeAuth(); updateAuthNav(); showPage('bookings');
  flash('Welcome back, '+patient.full_name+'!','success');
}
function staffLogin(){
  const id=parseInt(document.getElementById('staff-id').value);
  const password=document.getElementById('staff-password').value;
  const staff=getStaff().find(s=>s.staff_id===id);
  if(!staff){ alert('Invalid Staff ID.'); return; }
  if(password!=='medicheck123'){ alert('Incorrect staff password.'); return; }
  lsSet('session',{type:'staff',id:staff.staff_id,name:staff.full_name,role:staff.role});
  authLocked=false; closeAuth(); updateAuthNav(); showPage('admin');
  flash('Staff login successful — '+staff.full_name+' ('+staff.role+').','success');
}
function logout(){
  localStorage.removeItem('mc_session');
  updateAuthNav(); showPage('home');
  flash('You have been logged out.','success');
}
document.addEventListener('keydown',e=>{ if(e.key==='Escape') closeAuth(); });
window.addEventListener('load',()=>{
  updateAuthNav();
  if(!ls('session')) setTimeout(()=>openAuth('login', false),250);
});

function downloadPDF() {
  const element = document.getElementById('report-content');
  const opt = {
    margin:       0.5,
    filename:     'MediCheck_Lab_Report.pdf',
    image:        { type: 'jpeg', quality: 0.98 },
    html2canvas:  { scale: 2 },
    jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
  };
  html2pdf().set(opt).from(element).save();
}


