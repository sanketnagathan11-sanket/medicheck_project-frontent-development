import os

content = open('MediCheck.html', encoding='utf-8').read()

pl_old = """  function patientLogin(){
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
    authLocked=false; closeAuth(); updateAuthNav(); showPage('home');
    flash('Welcome back, '+patient.full_name+'!','success');
  }"""

pl_new = """  function patientLogin(){
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
  }"""

if pl_old in content:
    content = content.replace(pl_old, pl_new)
    print("Patched patientLogin")
else:
    print("Failed patientLogin")

pr_old = """  lsSet('session',{type:'patient',id:patient.patient_id,name:patient.full_name});
  authLocked=false; closeAuth(); updateAuthNav();
  flash('Account created successfully. Welcome, '+patient.full_name+'!','success');
}"""
pr_new = """  lsSet('session',{type:'patient',id:patient.patient_id,name:patient.full_name});
  authLocked=false; closeAuth(); updateAuthNav(); showPage('bookings');
  flash('Account created successfully. Welcome, '+patient.full_name+'!','success');
}"""

if pr_old in content:
    content = content.replace(pr_old, pr_new)
    print("Patched patientRegister")
else:
    print("Failed patientRegister")

open('MediCheck.html', 'w', encoding='utf-8').write(content)
