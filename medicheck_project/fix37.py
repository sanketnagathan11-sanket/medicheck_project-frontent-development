import re

c = open('MediCheck.html', encoding='utf-8').read()

new_html = """            <!-- Editable Fields -->
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
            </div>"""

start_idx = c.find("<!-- Editable Fields -->")
if start_idx != -1:
    end_idx = c.find('<button class="btn btn-teal"', start_idx)
    if end_idx != -1:
        c = c[:start_idx] + new_html + "\n            " + c[end_idx:]
        open('MediCheck.html', 'w', encoding='utf-8').write(c)
        print("Replaced!")
    else:
        print("End not found")
else:
    print("Start not found")
