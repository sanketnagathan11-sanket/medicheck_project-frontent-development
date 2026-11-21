import os

content = open('MediCheck.html', encoding='utf-8').read()

# 1. Update #flash-container CSS
css_old = """    #flash-container{padding:0 1.5rem;max-width:1200px;margin:0 auto}"""
css_new = """    #flash-container{position:fixed;top:1.5rem;right:1.5rem;z-index:10000;display:flex;flex-direction:column;gap:.5rem;pointer-events:none}
    #flash-container .flash{pointer-events:auto;margin:0;min-width:300px;box-shadow:0 10px 25px rgba(0,0,0,.1)}"""
if css_old in content:
    content = content.replace(css_old, css_new)

# 2. Update page-auth-register HTML
preg_old = """            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:1rem">
              <div class="fg" style="margin-bottom:0"><label>Phone *</label><input id="page-reg-phone" type="tel" maxlength="10" placeholder="10 digits"></div>
              <div class="fg" style="margin-bottom:0"><label>Email</label><input id="page-reg-email" type="email" placeholder="Optional"></div>
            </div>
            <div class="fg" style="margin-bottom:1rem"><label>Address *</label><input id="page-reg-address" placeholder="Residential address"></div>"""
preg_new = """            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:1rem">
              <div class="fg" style="margin-bottom:0"><label>Phone *</label><input id="page-reg-phone" type="tel" maxlength="10" placeholder="10 digits"></div>
              <div class="fg" style="margin-bottom:0"><label>Email</label><input id="page-reg-email" type="email" placeholder="Optional"></div>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:1rem">
              <div class="fg" style="margin-bottom:0"><label>Blood Group *</label><select id="page-reg-bloodgroup" style="width:100%;padding:.65rem;border:1px solid var(--border);border-radius:4px"><option value="">Select</option><option>A+</option><option>A-</option><option>B+</option><option>B-</option><option>O+</option><option>O-</option><option>AB+</option><option>AB-</option></select></div>
              <div class="fg" style="margin-bottom:0"><label>Address *</label><input id="page-reg-address" placeholder="Residential address"></div>
            </div>"""
if preg_old in content:
    content = content.replace(preg_old, preg_new)

# 3. Update auth-register HTML
areg_old = """      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px">
        <div class="fg"><label>Phone *</label><input id="reg-phone" type="tel" maxlength="10" placeholder="10 digits"></div>
        <div class="fg"><label>Email</label><input id="reg-email" type="email" placeholder="Optional"></div>
      </div>
      <div class="fg"><label>Address *</label><input id="reg-address" placeholder="Residential address"></div>"""
areg_new = """      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px">
        <div class="fg"><label>Phone *</label><input id="reg-phone" type="tel" maxlength="10" placeholder="10 digits"></div>
        <div class="fg"><label>Email</label><input id="reg-email" type="email" placeholder="Optional"></div>
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px">
        <div class="fg"><label>Blood Group *</label><select id="reg-bloodgroup"><option value="">Select</option><option>A+</option><option>A-</option><option>B+</option><option>B-</option><option>O+</option><option>O-</option><option>AB+</option><option>AB-</option></select></div>
        <div class="fg"><label>Address *</label><input id="reg-address" placeholder="Address"></div>
      </div>"""
if areg_old in content:
    content = content.replace(areg_old, areg_new)

# 4. Update pagePatientRegister
ppr_old = """  const email=document.getElementById('page-reg-email').value.trim();
  const address=document.getElementById('page-reg-address').value.trim();

  if(!name||!phone||!password||!dob||!gender||!address){ flash('Please fill in all required fields.', 'danger'); return; }"""
ppr_new = """  const email=document.getElementById('page-reg-email').value.trim();
  const address=document.getElementById('page-reg-address').value.trim();
  const bloodgroup=document.getElementById('page-reg-bloodgroup').value;

  if(!name||!phone||!password||!dob||!gender||!address||!bloodgroup){ flash('Please fill in all required fields.', 'danger'); return; }"""
if ppr_old in content:
    content = content.replace(ppr_old, ppr_new)
    
ppr2_old = """    dob:dob, gender:gender, email:email, address:address, membership_tier:'Standard'"""
ppr2_new = """    dob:dob, gender:gender, email:email, address:address, blood_group:bloodgroup, membership_tier:'Standard'"""
if ppr2_old in content:
    content = content.replace(ppr2_old, ppr2_new)

# 5. Update patientRegister
pr_old = """  const email=document.getElementById('reg-email').value.trim();
  const address=document.getElementById('reg-address').value.trim();

  if(!name||!phone||!password||!dob||!gender||!address){ flash('Please fill in all required fields.', 'danger'); return; }"""
pr_new = """  const email=document.getElementById('reg-email').value.trim();
  const address=document.getElementById('reg-address').value.trim();
  const bloodgroup=document.getElementById('reg-bloodgroup').value;

  if(!name||!phone||!password||!dob||!gender||!address||!bloodgroup){ flash('Please fill in all required fields.', 'danger'); return; }"""
if pr_old in content:
    content = content.replace(pr_old, pr_new)

if ppr2_old in content:
    content = content.replace(ppr2_old, ppr2_new)

# 6. Update submitBooking
sb_old = """    const pay   = document.getElementById('b-pay').value;
  
    if(!name||!phone||!dob){ flash('Please fill in required patient fields (Name, Phone, DOB).','danger'); return; }"""
sb_new = """    const pay   = document.getElementById('b-pay').value;
    const blood = document.getElementById('b-bloodgroup').value;
  
    if(!name||!phone||!dob||!blood){ flash('Please fill in required patient fields (Name, Phone, DOB, Blood Group).','danger'); return; }"""
if sb_old in content:
    content = content.replace(sb_old, sb_new)
    
sb2_old = """      patients.push({patient_id:patientId,full_name:name,dob,gender,phone,email,address:addr,membership_tier:tier});"""
sb2_new = """      patients.push({patient_id:patientId,full_name:name,dob,gender,phone,email,address:addr,blood_group:blood,membership_tier:tier});"""
if sb2_old in content:
    content = content.replace(sb2_old, sb2_new)

# 7. Add Blood Group to Admin Table
ad_old = """              <th style="padding:.5rem">Email</th>
              <th style="padding:.5rem">Gender / DOB</th>
              <th style="padding:.5rem">Address</th>"""
ad_new = """              <th style="padding:.5rem">Email</th>
              <th style="padding:.5rem">Gender/DOB/Blood</th>
              <th style="padding:.5rem">Address</th>"""
if ad_old in content:
    content = content.replace(ad_old, ad_new)
    
ad2_old = """                <td style="padding:.5rem">${p.gender || '-'} (${p.dob || '-'})</td>"""
ad2_new = """                <td style="padding:.5rem">${p.gender || '-'} (${p.dob || '-'}) [${p.blood_group || '-'}]</td>"""
if ad2_old in content:
    content = content.replace(ad2_old, ad2_new)

# 8. Update book a test page HTML label to say Blood Group *
b_old = """<div class="fg"><label>Blood Group</label><select id="b-bloodgroup"><option value="">Select</option>"""
b_new = """<div class="fg"><label>Blood Group *</label><select id="b-bloodgroup"><option value="">Select</option>"""
if b_old in content:
    content = content.replace(b_old, b_new)

open('MediCheck.html', 'w', encoding='utf-8').write(content)
print("Fix13 applied")
