import re

c = open('MediCheck.html', encoding='utf-8').read()

if 'id="prof-recent-table"' in c:
    c = c.replace('id="prof-recent-table"', 'id="prof-recent-bookings"')
    open('MediCheck.html', 'w', encoding='utf-8').write(c)
    print("Replaced prof-recent-table with prof-recent-bookings!")
else:
    print("Not found")

