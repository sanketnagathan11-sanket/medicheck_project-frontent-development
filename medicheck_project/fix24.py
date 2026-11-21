import os, re

content = open('MediCheck.html', encoding='utf-8').read()

# 1. Replace #page-profile HTML
page_profile_old = r'<div id="page-profile" class="page">.*?</div>\s*</div>\s*</div>'
page_profile_new = """<div id="page-profile" class="page">
    <div class="wrap" style="padding-top:2.5rem; max-width:1100px;">
      
      <div style="display:flex; gap:2rem; flex-wrap:wrap; align-items:flex-start;">
        
        <!-- Profile Left Card -->
        <div style="flex:1; min-width:300px; max-width:350px; background:#fff; border-radius:16px; box-shadow:0 12px 32px rgba(0,0,0,.05); padding:2.5rem 2rem; text-align:center; border:1px solid var(--border);">
          <div style="width:110px; height:110px; border-radius:50%; background:var(--primary-light); color:var(--primary-dark); display:flex; align-items:center; justify-content:center; font-size:3rem; font-weight:700; margin:0 auto 1.5rem; box-shadow:0 4px 12px rgba(0,102,255,0.15);">
            <span id="prof-initial">A</span>
          </div>
          <h2 id="prof-display-name" style="font-size:1.6rem; margin-bottom:.5rem; color:var(--text);">Name</h2>
          <div style="margin-bottom:2rem;"><span id="prof-tier-badge" class="badge" style="background:#e0f2fe; color:#0369a1; padding:.4rem 1rem; border-radius:20px;">Premium</span></div>
          
          <button class="btn btn-primary" style="width:100%; margin-bottom:2.5rem; border-radius:8px; padding:.8rem; font-size:1rem;" onclick="showPage('book')">Book New Appointment</button>
          
          <!-- Editable Fields -->
          <div style="text-align:left; display:flex; flex-direction:column; gap:1.25rem;">
             <div style="background:#f8fafc; padding:1rem 1.25rem; border-radius:10px; border:1px solid #e2e8f0;">
               <label style="font-size:.75rem; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:.3rem; display:block;">Full Name</label>
               <input type="text" id="prof-name" style="width:100%; background:transparent; border:none; font-weight:600; font-size:.95rem; color:var(--text); outline:none;">
             </div>
             <div style="background:#f8fafc; padding:1rem 1.25rem; border-radius:10px; border:1px solid #e2e8f0;">
               <label style="font-size:.75rem; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:.3rem; display:block;">Phone Number (Locked)</label>
               <input type="text" id="prof-phone" disabled style="width:100%; background:transparent; border:none; font-weight:600; font-size:.95rem; color:var(--muted); outline:none;">
             </div>
             <div style="background:#f8fafc; padding:1rem 1.25rem; border-radius:10px; border:1px solid #e2e8f0;">
               <label style="font-size:.75rem; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:.3rem; display:block;">Change Password</label>
               <input type="password" id="prof-password" placeholder="Leave blank to keep..." style="width:100%; background:transparent; border:none; font-weight:600; font-size:.95rem; color:var(--text); outline:none;">
             </div>
          </div>
          
          <button class="btn btn-teal" style="width:100%; margin-top:2rem; border-radius:8px; padding:.8rem;" onclick="updateProfile()">Save Profile Details</button>
        </div>
        
        <!-- Right Content Area -->
        <div style="flex:2; min-width:500px;">
          <!-- Stats Row -->
          <div style="display:flex; gap:1.5rem; margin-bottom:2rem; flex-wrap:wrap;">
            <div style="flex:1; min-width:140px; background:#fff; padding:1.5rem; border-radius:16px; box-shadow:0 8px 24px rgba(0,0,0,.04); border:1px solid var(--border); display:flex; justify-content:space-between; align-items:center;">
               <div>
                 <div id="prof-stat-total" style="font-size:2.8rem; color:var(--primary); font-weight:700; line-height:1; margin-bottom:.5rem;">0</div>
                 <div style="color:var(--muted); font-size:.9rem; font-weight:600;">All Bookings</div>
               </div>
               <div style="font-size:2.5rem; opacity:0.1; color:var(--primary);">📊</div>
            </div>
            <div style="flex:1; min-width:140px; background:#fff; padding:1.5rem; border-radius:16px; box-shadow:0 8px 24px rgba(0,0,0,.04); border:1px solid var(--border); display:flex; justify-content:space-between; align-items:center;">
               <div>
                 <div id="prof-stat-done" style="font-size:2.8rem; color:#8b5cf6; font-weight:700; line-height:1; margin-bottom:.5rem;">0</div>
                 <div style="color:var(--muted); font-size:.9rem; font-weight:600;">Completed</div>
               </div>
               <div style="font-size:2.5rem; opacity:0.1; color:#8b5cf6;">📈</div>
            </div>
            <div style="flex:1; min-width:140px; background:#fff; padding:1.5rem; border-radius:16px; box-shadow:0 8px 24px rgba(0,0,0,.04); border:1px solid var(--border); display:flex; justify-content:space-between; align-items:center;">
               <div>
                 <div id="prof-stat-cancel" style="font-size:2.8rem; color:#f97316; font-weight:700; line-height:1; margin-bottom:.5rem;">0</div>
                 <div style="color:var(--muted); font-size:.9rem; font-weight:600;">Cancelled</div>
               </div>
               <div style="font-size:2.5rem; opacity:0.1; color:#f97316;">📉</div>
            </div>
          </div>
          
          <!-- Appointments List -->
          <div style="background:#fff; border-radius:16px; box-shadow:0 12px 32px rgba(0,0,0,.04); border:1px solid var(--border); overflow:hidden;">
            <div style="display:flex; border-bottom:1px solid var(--border);">
              <div style="padding:1.25rem 2rem; font-weight:600; color:var(--text); border-bottom:2px solid var(--primary);">Appointments</div>
            </div>
            <div id="prof-recent-bookings" style="padding:0 2rem;">
               <!-- Dynamic content injected here -->
            </div>
          </div>
          
        </div>
      </div>
    </div>
  </div>"""

content = re.sub(page_profile_old, page_profile_new, content, flags=re.DOTALL)

# 2. Update renderProfile JS function
js_old = r"function renderProfile\(\) \{.*?document\.getElementById\('prof-password'\)\.value = '';\s*\}\s*\}"
js_new = """function renderProfile() {
    const session = ls('session');
    if(!session || session.type !== 'patient') { showPage('home'); return; }
    const patient = getPatients().find(p => p.patient_id === session.id);
    if(patient) {
      document.getElementById('prof-name').value = patient.full_name;
      document.getElementById('prof-phone').value = patient.phone;
      document.getElementById('prof-password').value = ''; 
      
      document.getElementById('prof-initial').innerText = patient.full_name.charAt(0).toUpperCase();
      document.getElementById('prof-display-name').innerText = patient.full_name;
      document.getElementById('prof-tier-badge').innerText = (patient.membership_tier || 'Standard') + ' Client';
      
      const pBookings = getBookings().filter(b=>b.patient_id===patient.patient_id).sort((a,b)=>b.booking_id-a.booking_id);
      
      const total = pBookings.length;
      const done = pBookings.filter(b=>b.status==='Report Ready').length;
      const cancelled = pBookings.filter(b=>b.status==='Cancelled').length;
      
      document.getElementById('prof-stat-total').innerText = total;
      document.getElementById('prof-stat-done').innerText = done;
      document.getElementById('prof-stat-cancel').innerText = cancelled;
      
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
      document.getElementById('prof-recent-bookings').innerHTML = html;
    }
  }"""

content = re.sub(js_old, js_new, content, flags=re.DOTALL)

# updateProfile function is untouched since it still reads the same inputs
# But we should update the display name and badge on save just in case
upd_old = r"flash\('Profile updated successfully!', 'success'\);"
upd_new = """flash('Profile updated successfully!', 'success');
      renderProfile();"""
content = re.sub(upd_old, upd_new, content)

open('MediCheck.html', 'w', encoding='utf-8').write(content)
print("Profile dashboard applied")
