c = open('MediCheck.html', encoding='utf-8').read()

s = c.find('function updateAuthNav()')
e = c.find('function switchPageAuth(type)')

good_code = """function updateAuthNav(){
  const nav=document.getElementById('auth-nav');
  const session=ls('session');
  
  const adminNav = document.getElementById('nav-admin');
  const bookingsNav = document.getElementById('nav-bookings');

  let isStaff = (session && session.type === 'staff');
  let isAdmin = false;
  if (isStaff) {
    let staff = getStaff().find(s => s.staff_id === session.id);
    if (staff && staff.role === 'Admin') isAdmin = true;
  }

  if(adminNav) adminNav.style.display = isStaff ? 'inline-block' : 'none';
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
  if(!/^\\d{10}$/.test(phone)){ alert('Please enter a valid 10-digit phone number.'); return; }
  if(password.length<4){ alert('Password must contain at least 4 characters.'); return; }

  let patients=getPatients();
  let patient=patients.find(p=>p.phone===phone);
  if(patient && patient.password){ alert('An account with this phone number already exists. Please login.'); switchAuth('login'); return; }
  if(patient){
    patient.full_name=name; patient.password=password;
  }else{
    patient={patient_id:nextPatientId(),full_name:name,dob:'',gender:'',phone,email:'',address:'',membership_tier:'Standard',password};
    patients.push(patient);
  }
  lsSet('patients',patients);
  lsSet('session',{type:'patient',id:patient.patient_id,name:patient.full_name});
  authLocked=false; closeAuth(); updateAuthNav(); showPage('bookings');
  flash('Account created successfully. Welcome, '+patient.full_name+'!','success');
}
"""

c = c[:s] + good_code + c[e:]
open('MediCheck.html', 'w', encoding='utf-8').write(c)
print("Restored updateAuthNav and patientRegister!")
