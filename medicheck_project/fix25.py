import os, re

content = open('MediCheck.html', encoding='utf-8').read()

# We have a duplicate renderProfile() and possibly duplicate updateProfile()
# Let's clean up this mess.

# Find the start of the first renderProfile or updateProfile
start_idx = content.find("function renderProfile() {")
if start_idx == -1:
    print("Could not find renderProfile")

# We want to delete the whole block containing both.
# Let's just find the first "function renderProfile()" and the last "flash('Profile updated successfully!', 'success');\n      renderProfile();\n    }\n  }" or similar.
# Actually, let's just use regex to remove ALL renderProfile and updateProfile functions, and then append them nicely before flash().

# Remove any function renderProfile() {...} and function updateProfile() {...}
def remove_func(func_name, text):
    pattern = r"function\s+" + func_name + r"\s*\(\)\s*\{"
    match = re.search(pattern, text)
    while match:
        # manual brace matching to find end
        start = match.start()
        idx = text.find('{', start)
        stack = 1
        i = idx + 1
        while i < len(text) and stack > 0:
            if text[i] == '{': stack += 1
            elif text[i] == '}': stack -= 1
            i += 1
        text = text[:start] + text[i:]
        match = re.search(pattern, text)
    return text

content = remove_func('renderProfile', content)
content = remove_func('updateProfile', content)

# Now inject both correctly before function flash(msg, type='') {
inject_code = """
  function renderProfile() {
    const session = ls('session');
    if(!session || session.type !== 'patient') { showPage('home'); return; }
    const patient = getPatients().find(p => p.patient_id === session.id);
    if(patient) {
      document.getElementById('prof-name').value = patient.full_name;
      document.getElementById('prof-phone').value = patient.phone;
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
      renderProfile();
    }
  }
"""

content = content.replace("function flash(msg", inject_code + "\n  function flash(msg")

open('MediCheck.html', 'w', encoding='utf-8').write(content)
print("Cleaned up renderProfile and updateProfile")
