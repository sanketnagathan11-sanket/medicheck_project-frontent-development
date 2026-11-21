import re

c = open('MediCheck.html', encoding='utf-8').read()

start_marker = '<div id="page-profile" class="page">'
end_marker = '<!-- PATIENT DB PAGE -->'

start_idx = c.find(start_marker)
end_idx = c.find(end_marker, start_idx)

new_profile_html = """<div id="page-profile" class="page">
    <div class="wrap" style="padding-top:1.5rem; max-width:1150px;">
      
      <!-- Professional Profile Banner (Top) -->
      <div style="background:linear-gradient(135deg, var(--primary) 0%, #0369a1 100%); border-radius:16px 16px 0 0; height:180px; position:relative; margin-bottom: 5rem;">
        <!-- Abstract subtle shapes in background -->
        <svg style="position:absolute; width:100%; height:100%; opacity:0.1; top:0; left:0; border-radius:16px 16px 0 0;" preserveAspectRatio="none"><path d="M0,0 L100,100 L0,100 Z" fill="#fff" /></svg>
        
        <!-- Profile Avatar Overlapping -->
        <div style="position:absolute; bottom:-45px; left:3rem; display:flex; align-items:flex-end; gap:1.5rem;">
          <div style="width:140px; height:140px; border-radius:50%; background:#fff; padding:6px; box-shadow:0 8px 24px rgba(0,0,0,0.15); display:inline-block;">
            <div style="width:100%; height:100%; border-radius:50%; background:var(--primary-light); color:var(--primary-dark); display:flex; align-items:center; justify-content:center; font-size:4rem; font-weight:800; border:2px solid #e0f2fe;">
              <span id="prof-initial">A</span>
            </div>
          </div>
          <div style="padding-bottom:12px;">
            <h2 id="prof-display-name" style="font-size:2.4rem; font-weight:800; color:#334155; margin:0; line-height:1; text-shadow:0 2px 10px rgba(0,0,0,0.1);">Name</h2>
            <div style="margin-top:.8rem;">
              <span id="prof-tier-badge" class="badge" style="background:var(--primary); color:#fff; padding:.4rem 1.2rem; border-radius:20px; font-weight:700; box-shadow:0 4px 10px rgba(2,132,199,0.3);">Premium Member</span>
            </div>
          </div>
        </div>
        
        <!-- Top Right Action -->
        <div style="position:absolute; top:2rem; right:2rem;">
          <button class="btn btn-outline-white" style="border-radius:8px; padding:.7rem 1.2rem; font-weight:700; border-color:rgba(255,255,255,0.4); background:rgba(255,255,255,0.1); backdrop-filter:blur(4px); box-shadow:0 4px 12px rgba(0,0,0,0.1);" onclick="showPage('book')">
            <span style="font-size:1.1rem; margin-right:.4rem;">+</span> Book Appointment
          </button>
        </div>
      </div>

      <div style="display:flex; gap:2.5rem; flex-wrap:wrap; align-items:flex-start;">
        
        <!-- Left Column: Personal Information -->
        <div style="flex:1; min-width:320px; max-width:450px;">
          <div style="background:#fff; border-radius:16px; box-shadow:0 12px 32px rgba(0,0,0,.05); padding:2rem; border:1px solid var(--border);">
            <h3 style="font-size:1.2rem; margin-bottom:1.5rem; color:#334155; border-bottom:1px solid var(--border); padding-bottom:.8rem; display:flex; align-items:center; justify-content:space-between;">
              Personal Details
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--muted);"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
            </h3>
            
            <!-- Editable Fields -->
            <div style="text-align:left; display:flex; flex-direction:column; gap:1.2rem; background:#fff; padding:0; border-radius:12px;">
              
              <div>
                <label style="font-size:.75rem; font-weight:700; color:var(--primary); text-transform:uppercase; letter-spacing:1px; margin-bottom:.4rem; display:block;">Full Name</label>
                <input type="text" id="prof-name" style="width:100%; border:none; border-bottom:2px solid #e2e8f0; padding:.5rem 0; font-weight:600; font-size:1rem; color:var(--text); outline:none; transition:border-color 0.2s; background:transparent;" onfocus="this.style.borderColor='var(--primary)'" onblur="this.style.borderColor='#e2e8f0'">
              </div>

              <div>
                <label style="font-size:.75rem; font-weight:700; color:var(--primary); text-transform:uppercase; letter-spacing:1px; margin-bottom:.4rem; display:block;">Email Address</label>
                <input type="email" id="prof-email" style="width:100%; border:none; border-bottom:2px solid #e2e8f0; padding:.5rem 0; font-weight:600; font-size:1rem; color:var(--text); outline:none; transition:border-color 0.2s; background:transparent;" onfocus="this.style.borderColor='var(--primary)'" onblur="this.style.borderColor='#e2e8f0'">
              </div>

              <div style="display:flex; gap:1.5rem;">
                <div style="flex:1;">
                  <label style="font-size:.75rem; font-weight:700; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:.4rem; display:flex; align-items:center; gap:.3rem;">Phone <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg></label>
                  <input type="text" id="prof-phone" disabled style="width:100%; border:none; border-bottom:1px dashed #cbd5e1; padding:.5rem 0; font-weight:600; font-size:.95rem; color:var(--muted); outline:none; background:transparent;">
                </div>
                <div style="flex:1;">
                  <label style="font-size:.75rem; font-weight:700; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:.4rem; display:flex; align-items:center; gap:.3rem;">DOB <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg></label>
                  <input type="text" id="prof-dob" disabled style="width:100%; border:none; border-bottom:1px dashed #cbd5e1; padding:.5rem 0; font-weight:600; font-size:.95rem; color:var(--muted); outline:none; background:transparent;">
                </div>
              </div>

              <div style="display:flex; gap:1.5rem;">
                <div style="flex:1;">
                  <label style="font-size:.75rem; font-weight:700; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:.4rem; display:flex; align-items:center; gap:.3rem;">Gender <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg></label>
                  <input type="text" id="prof-gender" disabled style="width:100%; border:none; border-bottom:1px dashed #cbd5e1; padding:.5rem 0; font-weight:600; font-size:.95rem; color:var(--muted); outline:none; background:transparent;">
                </div>
                <div style="flex:1;">
                  <label style="font-size:.75rem; font-weight:700; color:var(--muted); text-transform:uppercase; letter-spacing:1px; margin-bottom:.4rem; display:flex; align-items:center; gap:.3rem;">Blood <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg></label>
                  <input type="text" id="prof-blood" disabled style="width:100%; border:none; border-bottom:1px dashed #cbd5e1; padding:.5rem 0; font-weight:600; font-size:.95rem; color:var(--muted); outline:none; background:transparent;">
                </div>
              </div>

              <div>
                <label style="font-size:.75rem; font-weight:700; color:var(--primary); text-transform:uppercase; letter-spacing:1px; margin-bottom:.4rem; display:block;">Home Address</label>
                <input type="text" id="prof-address" style="width:100%; border:none; border-bottom:2px solid #e2e8f0; padding:.5rem 0; font-weight:600; font-size:1rem; color:var(--text); outline:none; transition:border-color 0.2s; background:transparent;" onfocus="this.style.borderColor='var(--primary)'" onblur="this.style.borderColor='#e2e8f0'">
              </div>

              <div>
                <label style="font-size:.75rem; font-weight:700; color:var(--primary); text-transform:uppercase; letter-spacing:1px; margin-bottom:.4rem; display:block;">Change Password</label>
                <input type="password" id="prof-password" placeholder="Leave blank to keep..." style="width:100%; border:none; border-bottom:2px solid #e2e8f0; padding:.5rem 0; font-weight:600; font-size:1rem; color:var(--text); outline:none; transition:border-color 0.2s; background:transparent;" onfocus="this.style.borderColor='var(--primary)'" onblur="this.style.borderColor='#e2e8f0'">
              </div>
            </div>
            
            <button class="btn btn-teal" style="width:100%; margin-top:2.5rem; border-radius:8px; padding:1rem; font-weight:700; font-size:1rem; box-shadow:0 6px 16px rgba(20,184,166,0.3);" onclick="updateProfile()">Save Profile Changes</button>
          </div>
        </div>
        
        <!-- Right Column: Dashboard Stats & Recent History -->
        <div style="flex:2; min-width:500px;">
          
          <!-- Stats Row -->
          <div style="display:flex; gap:1.5rem; margin-bottom:2rem; flex-wrap:wrap;">
            <div style="flex:1; min-width:140px; background:#fff; padding:1.5rem; border-radius:16px; box-shadow:0 8px 24px rgba(0,0,0,.04); border:1px solid var(--border); display:flex; justify-content:space-between; align-items:center;">
               <div>
                 <div id="prof-stat-total" style="font-size:2.8rem; color:var(--primary); font-weight:800; line-height:1; margin-bottom:.5rem;">0</div>
                 <div style="color:var(--muted); font-size:.9rem; font-weight:600; text-transform:uppercase; letter-spacing:1px;">All Bookings</div>
               </div>
               <div style="font-size:2.5rem; opacity:0.1; color:var(--primary);">
                 <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
               </div>
            </div>
            <div style="flex:1; min-width:140px; background:#fff; padding:1.5rem; border-radius:16px; box-shadow:0 8px 24px rgba(0,0,0,.04); border:1px solid var(--border); display:flex; justify-content:space-between; align-items:center;">
               <div>
                 <div id="prof-stat-done" style="font-size:2.8rem; color:#8b5cf6; font-weight:800; line-height:1; margin-bottom:.5rem;">0</div>
                 <div style="color:var(--muted); font-size:.9rem; font-weight:600; text-transform:uppercase; letter-spacing:1px;">Completed</div>
               </div>
               <div style="font-size:2.5rem; opacity:0.1; color:#8b5cf6;">
                 <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
               </div>
            </div>
            <div style="flex:1; min-width:140px; background:#fff; padding:1.5rem; border-radius:16px; box-shadow:0 8px 24px rgba(0,0,0,.04); border:1px solid var(--border); display:flex; justify-content:space-between; align-items:center;">
               <div>
                 <div id="prof-stat-cancel" style="font-size:2.8rem; color:#f97316; font-weight:800; line-height:1; margin-bottom:.5rem;">0</div>
                 <div style="color:var(--muted); font-size:.9rem; font-weight:600; text-transform:uppercase; letter-spacing:1px;">Cancelled</div>
               </div>
               <div style="font-size:2.5rem; opacity:0.1; color:#f97316;">
                 <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>
               </div>
            </div>
          </div>
          
          <!-- Appointments List -->
          <div style="background:#fff; border-radius:16px; box-shadow:0 12px 32px rgba(0,0,0,.04); border:1px solid var(--border); overflow:hidden;">
            <div style="display:flex; border-bottom:1px solid var(--border);">
              <div style="padding:1.25rem 2rem; font-weight:700; font-size:1.1rem; color:var(--text); border-bottom:2px solid var(--primary);">Recent Appointments</div>
            </div>
            <div style="overflow-x:auto;">
              <table style="width:100%; border-collapse:collapse; text-align:left; font-size:.9rem; white-space:nowrap;">
                <thead>
                  <tr style="border-bottom:2px solid var(--border); color:var(--muted); background:#f8fafc;">
                    <th style="padding:1rem 2rem; font-weight:600;">ID</th>
                    <th style="padding:1rem 2rem; font-weight:600;">Type</th>
                    <th style="padding:1rem 2rem; font-weight:600;">Date & Time</th>
                    <th style="padding:1rem 2rem; font-weight:600;">Status</th>
                  </tr>
                </thead>
                <tbody id="prof-recent-table">
                  <tr><td colspan="4" style="padding:2rem; text-align:center; color:var(--muted);">Loading...</td></tr>
                </tbody>
              </table>
            </div>
          </div>
          
        </div>
      </div>
    </div>
  
    """

if start_idx != -1 and end_idx != -1:
    c = c[:start_idx] + new_profile_html + c[end_idx:]
    open('MediCheck.html', 'w', encoding='utf-8').write(c)
    print("Replaced Profile Dashboard HTML completely!")
else:
    print("Markers not found.")
