c = open('MediCheck.html', encoding='utf-8').read()
c = c.replace("background: url('login_banner.jpg') center/cover no-repeat;", "background: url('login_banner.jpg') no-repeat center center / cover;")
open('MediCheck.html', 'w', encoding='utf-8').write(c)
