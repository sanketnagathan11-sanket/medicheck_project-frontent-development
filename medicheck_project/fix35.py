import re

c = open('MediCheck.html', encoding='utf-8').read()

# 1. Update updateAuthNav function
old_update = """    if(session){
      nav.textContent='Logout';
      nav.onclick=logout;
    }else{
      nav.textContent='Login';
      nav.onclick=()=>openAuth('login', false);
    }"""
    
new_update = """    if(session){
      nav.textContent='Logout';
      nav.onclick=logout;
    }else{
      nav.textContent='Login';
      nav.onclick=() => {
        showPage('home');
        setTimeout(() => {
          const loginSec = document.querySelector('.split-login-section');
          if(loginSec) loginSec.scrollIntoView({behavior: 'smooth'});
          else openAuth('login', false);
        }, 50);
      };
    }"""

if old_update in c:
    c = c.replace(old_update, new_update)
    print("Replaced updateAuthNav!")
else:
    print("Failed to replace updateAuthNav.")

# 2. Update HTML nav button just in case
old_nav_html = """<a id="auth-nav" class="nav-btn btn" onclick="openAuth()" style="cursor:pointer">Login</a>"""
new_nav_html = """<a id="auth-nav" class="nav-btn btn" onclick="showPage('home'); setTimeout(()=>{document.querySelector('.split-login-section').scrollIntoView({behavior:'smooth'})},50);" style="cursor:pointer">Login</a>"""

if old_nav_html in c:
    c = c.replace(old_nav_html, new_nav_html)
    print("Replaced nav HTML!")
else:
    print("Failed to replace nav HTML.")

open('MediCheck.html', 'w', encoding='utf-8').write(c)
