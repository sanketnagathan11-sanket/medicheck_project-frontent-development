import os

content = open('MediCheck.html', encoding='utf-8').read()

css_old = """    @media(max-width:768px){
      .hdr{flex-direction:column;height:auto;padding:1rem 0;gap:.8rem}
      nav{flex-wrap:wrap;justify-content:center;gap:.75rem}
      .tests-grid{grid-template-columns:1fr}
    }"""
css_new = """    @media(max-width:768px){
      .hdr{flex-direction:column;height:auto;padding:1rem 0;gap:.8rem}
      nav{flex-wrap:wrap;justify-content:center;gap:.75rem}
      .tests-grid{grid-template-columns:1fr}
      .split-login-section { flex-direction: column; border-radius: 12px; }
      .split-login-section > div { min-width: 100%; padding: 1.5rem !important; }
      .login-banner-img { min-height: 250px !important; }
    }

    /* Test tube image animation */
    .login-banner-img {
      transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease;
      cursor: pointer;
    }
    .login-banner-img:hover {
      transform: scale(1.03) rotate(1deg);
      box-shadow: 0 10px 20px rgba(0,0,0,.15);
    }
    .login-banner-img:active {
      transform: scale(0.95) rotate(-2deg);
    }"""

html_old = """          <button class="btn btn-primary" style="width:100%" onclick="pagePatientLogin()">Login to My Account</button>
        </div>
        <div style="flex: 1; min-width: 320px; background: url('login_banner.jpg') center/cover no-repeat; min-height: 400px;"></div>
      </div>"""
html_new = """          <button class="btn btn-primary" style="width:100%" onclick="pagePatientLogin()">Login to My Account</button>
          
          <div style="margin-top:1.5rem; text-align:center; font-size:.9rem; color:var(--muted)">
            <p style="margin-bottom:.6rem;">New patient? <button style="background:none;border:none;color:var(--primary);cursor:pointer;font-weight:600" onclick="openAuth(); switchAuth('register')">Create an account</button></p>
            <p><button style="background:none;border:none;color:var(--muted);cursor:pointer;text-decoration:underline" onclick="openAuth(); switchAuth('staff')">Are you a staff member? Staff Login &rarr;</button></p>
          </div>

        </div>
        <div class="login-banner-img" style="flex: 1; min-width: 320px; background: url('login_banner.jpg') center/cover no-repeat; min-height: 400px;"></div>
      </div>"""

if css_old in content and html_old in content:
    content = content.replace(css_old, css_new).replace(html_old, html_new)
    open('MediCheck.html', 'w', encoding='utf-8').write(content)
    print('Replaced')
else:
    print('Failed')
