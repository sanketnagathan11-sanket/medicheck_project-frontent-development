import os

content = open('MediCheck.html', encoding='utf-8').read()

pl_old = """    if(patient.password!==password){ alert('Incorrect password.'); return; }
    lsSet('session',{type:'patient',id:patient.patient_id,name:patient.full_name});
    authLocked=false; closeAuth(); updateAuthNav(); showPage('home');
    flash('Welcome back, '+patient.full_name+'!','success');"""
pl_new = """    if(patient.password!==password){ alert('Incorrect password.'); return; }
    lsSet('session',{type:'patient',id:patient.patient_id,name:patient.full_name});
    authLocked=false; closeAuth(); updateAuthNav(); showPage('bookings');
    flash('Welcome back, '+patient.full_name+'!','success');"""

if pl_old in content:
    content = content.replace(pl_old, pl_new)
    print("Replaced pl")
else:
    print("Failed pl")
    
open('MediCheck.html', 'w', encoding='utf-8').write(content)
