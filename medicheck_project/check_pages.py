c=open('MediCheck.html', encoding='utf-8').read()
print('page-admin exists:', 'id="page-admin"' in c)
print('page-patients exists:', 'id="page-patients"' in c)
print('page-contact exists:', 'id="page-contact"' in c)
