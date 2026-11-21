import os

content = open('MediCheck.html', encoding='utf-8').read()

old1 = """        <div>
          <span class="badge b-scheduled">${w.count} Assigned</span>
          <button class="btn btn-outline btn-sm" style="margin-left:.5rem;padding:.2rem .5rem;font-size:.75rem" onclick="removeStaff(${w.id})">Remove</button>
        </div>"""
new1 = """        <div>
          <span class="badge b-scheduled">${w.count} Assigned</span>
          ${w.id !== session.id ? `<button class="btn btn-outline btn-sm" style="margin-left:.5rem;padding:.2rem .5rem;font-size:.75rem" onclick="removeStaff(${w.id})">Remove</button>` : ''}
        </div>"""

old2 = """function removeStaff(id) {
  const session = ls('session');
  if(!session || session.role !== 'Admin') return;
  let staff = getStaff();"""
new2 = """function removeStaff(id) {
  const session = ls('session');
  if(!session || session.role !== 'Admin') return;
  if(id === session.id) { flash('You cannot remove yourself.', 'danger'); return; }
  let staff = getStaff();"""

if old1 in content and old2 in content:
    content = content.replace(old1, new1).replace(old2, new2)
    open('MediCheck.html', 'w', encoding='utf-8').write(content)
    print('Replaced')
else:
    print('Not found')
