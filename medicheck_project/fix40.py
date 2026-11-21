import re

c = open('MediCheck.html', encoding='utf-8').read()

start_marker = '<div id="page-contact" class="page">'
end_marker = '<!-- '

start_idx = c.find(start_marker)

# We need to find the start of the next page (page-report)
end_idx = c.find('<div id="page-report"', start_idx)

# but wait, the marker might have comments before it, let's just find exactly where the `<!--` is before `page-report`.
if start_idx != -1 and end_idx != -1:
    # Walk backward from end_idx to include the comment
    actual_end_idx = c.rfind('<!--', start_idx, end_idx)
    if actual_end_idx == -1: actual_end_idx = end_idx
    
    new_contact_html = """<div id="page-contact" class="page">
    <div class="wrap" style="padding-top:2.5rem;max-width:1050px">
      <div style="text-align:center; margin-bottom:3rem">
        <h1 class="section-title">Get In Touch With MediCheck</h1>
        <p class="section-sub">Have questions about lab sample pick-ups, test reports, or corporate health checkups?</p>
      </div>
      
      <div class="contact-grid" style="display:grid; grid-template-columns:1fr 1fr; gap:3rem; align-items:start;">
        <!-- Left Side: Form -->
        <div>
          <div class="form-card" style="padding:2.5rem; background:#fff; border-radius:16px; box-shadow:0 12px 32px rgba(0,0,0,.05); border:1px solid var(--border);">
            <h3 style="font-size:1.4rem; margin-bottom:1.5rem; color:var(--primary-dark);">Send Us a Message</h3>
            
            <div class="fg" style="margin-bottom:1.2rem;">
              <label style="font-weight:700; color:var(--muted); font-size:.85rem; text-transform:uppercase; letter-spacing:1px;">Your Name *</label>
              <input id="c-name" placeholder="John Doe" style="padding:.75rem 1rem; border-radius:8px; border:1px solid var(--border); font-size:1rem; outline:none;" onfocus="this.style.borderColor='var(--primary)'" onblur="this.style.borderColor='var(--border)'">
            </div>
            
            <div class="fg" style="margin-bottom:1.2rem;">
              <label style="font-weight:700; color:var(--muted); font-size:.85rem; text-transform:uppercase; letter-spacing:1px;">Email Address *</label>
              <input id="c-email" type="email" placeholder="john@example.com" style="padding:.75rem 1rem; border-radius:8px; border:1px solid var(--border); font-size:1rem; outline:none;" onfocus="this.style.borderColor='var(--primary)'" onblur="this.style.borderColor='var(--border)'">
            </div>
            
            <div class="fg" style="margin-bottom:1.2rem;">
              <label style="font-weight:700; color:var(--muted); font-size:.85rem; text-transform:uppercase; letter-spacing:1px;">Phone Number</label>
              <input id="c-phone" type="tel" placeholder="10-digit mobile" style="padding:.75rem 1rem; border-radius:8px; border:1px solid var(--border); font-size:1rem; outline:none;" onfocus="this.style.borderColor='var(--primary)'" onblur="this.style.borderColor='var(--border)'">
            </div>
            
            <div class="fg" style="margin-bottom:2rem;">
              <label style="font-weight:700; color:var(--muted); font-size:.85rem; text-transform:uppercase; letter-spacing:1px;">How can we help you? *</label>
              <textarea id="c-msg" rows="5" placeholder="Ask about home collection, report status, or package details..." style="padding:.75rem 1rem; border-radius:8px; border:1px solid var(--border); font-size:1rem; font-family:inherit; outline:none; resize:vertical;" onfocus="this.style.borderColor='var(--primary)'" onblur="this.style.borderColor='var(--border)'"></textarea>
            </div>
            
            <button class="btn btn-primary" style="width:100%; padding:1rem; font-size:1.05rem; border-radius:8px; box-shadow:0 4px 12px rgba(2,132,199,.2);" onclick="submitContact()">Send Inquiry</button>
          </div>
        </div>
        
        <!-- Right Side: Info Cards -->
        <div style="display:flex; flex-direction:column; gap:1.5rem;">
          
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:16px; padding:2.5rem; box-shadow:0 4px 6px rgba(0,0,0,.02);">
            <h3 style="font-size:1.3rem; margin-bottom:1.5rem; color:var(--primary-dark); display:flex; align-items:center; gap:.5rem;">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
              Central Diagnostic Lab
            </h3>
            
            <div style="display:flex; align-items:flex-start; gap:1rem; margin-bottom:1.2rem;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-top:2px; flex-shrink:0;"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
              <p style="color:#475569; font-size:1rem; line-height:1.5; margin:0;">102 Health Avenue, Medical Hub Zone,<br>Sector 4, Pune, Maharashtra - 411001</p>
            </div>
            
            <div style="display:flex; align-items:flex-start; gap:1rem; margin-bottom:1.2rem;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-top:2px; flex-shrink:0;"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
              <p style="color:#475569; font-size:1rem; line-height:1.5; margin:0;"><strong>24/7 Helpline:</strong> +91 1800-123-4567<br><strong>WhatsApp:</strong> +91 98765-43210</p>
            </div>
            
            <div style="display:flex; align-items:flex-start; gap:1rem;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-top:2px; flex-shrink:0;"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
              <p style="color:#475569; font-size:1rem; line-height:1.5; margin:0;"><strong>Email:</strong> support@medicheck.in</p>
            </div>
          </div>
          
          <div style="background:linear-gradient(135deg, #14b8a6 0%, #0d9488 100%); border-radius:16px; padding:2.5rem; color:#fff; box-shadow:0 8px 24px rgba(20,184,166,.2);">
            <h4 style="font-size:1.2rem; margin-bottom:1.2rem; display:flex; align-items:center; gap:.5rem;">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
              Operating Hours
            </h4>
            
            <ul style="list-style:none; padding:0; margin:0; font-size:1rem; line-height:2.2; opacity:0.95;">
              <li style="display:flex; justify-content:space-between; border-bottom:1px solid rgba(255,255,255,0.2); padding-bottom:.5rem;">
                <strong>Lab Collection:</strong> <span>06:30 AM - 08:00 PM</span>
              </li>
              <li style="display:flex; justify-content:space-between; border-bottom:1px solid rgba(255,255,255,0.2); padding:.5rem 0;">
                <strong>Home Pickups:</strong> <span>07:00 AM - 05:00 PM</span>
              </li>
              <li style="display:flex; justify-content:space-between; padding-top:.5rem;">
                <strong>Report Access:</strong> <span>24 Hours Online</span>
              </li>
            </ul>
          </div>
          
        </div>
      </div>
    </div>
  </div>
  
  """
    
    c = c[:start_idx] + new_contact_html + c[actual_end_idx:]
    open('MediCheck.html', 'w', encoding='utf-8').write(c)
    print("Replaced Contact page successfully!")
else:
    print("Could not find start/end markers for contact page")
