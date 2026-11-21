import os

content = open('MediCheck.html', encoding='utf-8').read()

initbook_old = """function initBook(extra){
  extra = extra||{};
  // Set today's date
  document.getElementById('b-date').value = new Date().toISOString().split('T')[0];"""

initbook_new = """function initBook(extra){
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
  }"""

if initbook_old in content:
    content = content.replace(initbook_old, initbook_new)
    print("InitBook patched")
else:
    print("InitBook patch failed")

open('MediCheck.html', 'w', encoding='utf-8').write(content)
