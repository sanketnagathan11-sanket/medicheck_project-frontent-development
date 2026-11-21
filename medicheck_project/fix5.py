import os

content = open('MediCheck.html', encoding='utf-8').read()

old = """        </div>
      </div>
    </div>
  </div>

  <!-- 🧪 TESTS PAGE 🧪 -->"""

new = """        </div>
      </div>
      
      <!-- New Login Section on Home Page -->
      <div class="split-login-section" style="margin-top: 5rem; display: flex; flex-wrap: wrap; background: #fff; border: 1px solid var(--border); border-radius: 20px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,.05);">
        <div style="flex: 1; min-width: 320px; padding: 3rem; display: flex; flex-direction: column; justify-content: center;">
          <h2 class="section-title" style="text-align:left; margin-bottom: 0.5rem; font-size:1.6rem">Patient Portal Login</h2>
          <p class="section-sub" style="text-align:left; margin-bottom: 2rem; max-width: 100%;">Log in to view your diagnostic reports, track active bookings, and manage your health.</p>
          <div class="fg" style="margin-bottom:1.2rem;"><label>Phone Number</label><input id="page-login-phone" type="tel" maxlength="10" placeholder="Enter registered 10-digit number"></div>
          <div class="fg" style="margin-bottom:1.5rem;"><label>Password</label><input id="page-login-password" type="password" placeholder="Enter password"></div>
          <button class="btn btn-primary" style="width:100%" onclick="pagePatientLogin()">Login to My Account</button>
        </div>
        <div style="flex: 1; min-width: 320px; background: url('login_banner.jpg') center/cover no-repeat; min-height: 400px;"></div>
      </div>

    </div>
  </div>

  <!-- 🧪 TESTS PAGE 🧪 -->"""

if old in content:
    content = content.replace(old, new)
    open('MediCheck.html', 'w', encoding='utf-8').write(content)
    print('Success HTML injection')
else:
    print('Failed HTML injection')
