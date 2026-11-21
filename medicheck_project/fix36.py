import re

c = open('MediCheck.html', encoding='utf-8').read()

old_block = """  if(!nav) return;
  if(session){
    nav.textContent='Logout';
    nav.onclick=logout;
  }else{
    nav.textContent='Login';
    nav.onclick=()=>openAuth('login', false);
  }"""

# Normalize spaces to find it
old_block_pattern = r"if\(!nav\)\s*return;\s*if\(session\)\{\s*nav\.textContent='Logout';\s*nav\.onclick=logout;\s*\}else\{\s*nav\.textContent='Login';\s*nav\.onclick=\(\)=>openAuth\('login',\s*false\);\s*\}"

new_block = """  if(!nav) return;
  if(session){
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

c = re.sub(old_block_pattern, new_block, c)
print("Replaced!")

open('MediCheck.html', 'w', encoding='utf-8').write(c)
