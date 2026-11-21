c = open('MediCheck.html', encoding='utf-8').read()
print('admin page html:', 'id="page-admin"' in c)
print('renderAdmin function:', 'function renderAdmin(' in c)
