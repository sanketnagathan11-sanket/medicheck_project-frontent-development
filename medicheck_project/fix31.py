import os

content = open('MediCheck.html', encoding='utf-8').read()

remove_js = """
  function removePatient(id) {
    const session = ls('session');
    if(!session || session.role !== 'Admin') return;
    if(!confirm('Are you sure you want to remove this patient from the database? This cannot be undone.')) return;
    let patients = getPatients();
    patients = patients.filter(p => p.patient_id !== id);
    lsSet('patients', patients);
    flash('Patient removed successfully!', 'success');
    renderPatients();
  }
"""

idx = content.find("function renderPatients() {")
if idx != -1:
    content = content[:idx] + remove_js + "\n  " + content[idx:]
    open('MediCheck.html', 'w', encoding='utf-8').write(content)
    print("Injected removePatient function!")
else:
    print("Not found")
