import os

content = open('MediCheck.html', encoding='utf-8').read()

# 1. Add ID to phone lookup container
page_bookings_old = """      <div class="wrap" style="padding-top:2.5rem">
        <div class="section-head">
          <div>
            <h1 class="section-title">Patient Portal &amp; Bookings Lookup</h1>
            <p class="section-sub">Search your bookings by phone number to check live report status.</p>
          </div>
        </div>
        <div style="background:#fff;border:1px solid var(--border);border-radius:var(--r);padding:1.5rem;margin-bottom:2.5rem;max-width:620px;box-shadow:0 1px 3px rgba(0,0,0,.05)">
          <div style="display:flex;gap:.75rem">
            <input id="lookup-phone" type="tel" placeholder="Enter 10-digit registered phone number" style="flex:1">
            <button class="btn btn-primary" onclick="lookupBookings()">Find My Bookings</button>
          </div>
        </div>
        <div id="patient-info"></div>"""
page_bookings_new = """      <div class="wrap" style="padding-top:2.5rem">
        <div class="section-head">
          <div>
            <h1 class="section-title">Patient Portal &amp; Bookings</h1>
            <p class="section-sub">View your bookings and track live report status.</p>
          </div>
        </div>
        <div id="lookup-phone-container" style="background:#fff;border:1px solid var(--border);border-radius:var(--r);padding:1.5rem;margin-bottom:2.5rem;max-width:620px;box-shadow:0 1px 3px rgba(0,0,0,.05);display:none;">
          <div style="display:flex;gap:.75rem">
            <input id="lookup-phone" type="tel" placeholder="Enter 10-digit registered phone number" style="flex:1">
            <button class="btn btn-primary" onclick="lookupBookings()">Find My Bookings</button>
          </div>
        </div>
        <div id="patient-info"></div>"""
if page_bookings_old in content:
    content = content.replace(page_bookings_old, page_bookings_new)

# 2. Modify showPage
show_page_old = """  if(name==='admin') renderAdmin();
  if(name==='profile') renderProfile();
  if(name==='report' && extra) renderReport(extra);
}"""
show_page_new = """  if(name==='admin') renderAdmin();
  if(name==='profile') renderProfile();
  if(name==='report' && extra) renderReport(extra);
  if(name==='bookings') lookupBookings();
}"""
if show_page_old in content:
    content = content.replace(show_page_old, show_page_new)


# 3. Update lookupBookings logic slightly to correctly hide the search bar if not needed
# Wait, lookup-phone-container is now display:none by default. Let's make it display only if NOT patient.
lookup_old = """function lookupBookings(){
  let phone = document.getElementById('lookup-phone').value.trim();
  const session = ls('session');
  if(session && session.type === 'patient'){
    const pt = getPatients().find(p=>p.patient_id === session.id);
    if(pt) phone = pt.phone;
  }
  if(!phone){ document.getElementById('patient-info').innerHTML=''; document.getElementById('bookings-results').innerHTML=emptyState(); return; }"""
lookup_new = """function lookupBookings(){
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
  if(!phone){ document.getElementById('patient-info').innerHTML=''; document.getElementById('bookings-results').innerHTML=emptyState(); return; }"""
if lookup_old in content:
    content = content.replace(lookup_old, lookup_new)

open('MediCheck.html', 'w', encoding='utf-8').write(content)
print('Fix9 applied')
