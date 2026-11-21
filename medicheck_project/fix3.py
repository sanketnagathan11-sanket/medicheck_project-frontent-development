import os

content = open("MediCheck.html", encoding="utf-8").read()

old = """    if (isAdmin) {
      document.getElementById('staff-workload').innerHTML=workload.map(w=>`
        <div style="display:flex;justify-content:space-between;align-items:center;padding:.7rem 0;border-bottom:1px solid var(--border)">
          <div><strong style="font-size:.93rem">${w.name}</strong>
            <div style="font-size:.76rem;color:var(--muted);margin-top:.2rem;">
              <select onchange="updateStaffRole(${w.id}, this.value)" style="padding:.1rem; font-size:.75rem;">
                ${['Technician', 'Receptionist', 'Courier', 'Admin'].map(r => `<option ${w.role===r?'selected':''}>${r}</option>`).join('')}
              </select>
            </div>
          </div>
          <div>
            <span class="badge b-scheduled">${w.count} Assigned</span>
            <button class="btn btn-outline btn-sm" style="margin-left:.5rem;padding:.2rem .5rem;font-size:.75rem" onclick="removeStaff(${w.id})">Remove</button>
          </div>
        </div>`).join('') + `
        <div style="margin-top:1.5rem;display:flex;gap:.5rem;border-top:1px solid var(--border);padding-top:1rem">
          <input id="new-staff-name" placeholder="New Staff Name..." style="flex:1;padding:.4rem .6rem;font-size:.85rem;border:1px solid var(--border);border-radius:4px">
          <button class="btn btn-teal btn-sm" onclick="addStaff()">+ Add Staff</button>
        </div>`;
    } else {
      document.getElementById('staff-workload').innerHTML=`<div style="padding:1rem;color:var(--muted);font-size:.9rem;text-align:center">You do not have administrative privileges to view or manage staff.</div>`;
    }"""

new = """    if (isAdmin) {
      document.getElementById('staff-workload').innerHTML=workload.map(w=>`
        <div style="display:flex;justify-content:space-between;align-items:center;padding:.7rem 0;border-bottom:1px solid var(--border)">
          <div><strong style="font-size:.93rem">${w.name}</strong>
            <div style="font-size:.76rem;color:var(--muted);margin-top:.2rem;">
              <select onchange="updateStaffRole(${w.id}, this.value)" style="padding:.1rem; font-size:.75rem;">
                ${['Technician', 'Receptionist', 'Courier', 'Admin'].map(r => `<option ${w.role===r?'selected':''}>${r}</option>`).join('')}
              </select>
            </div>
          </div>
          <div>
            <span class="badge b-scheduled">${w.count} Assigned</span>
            <button class="btn btn-outline btn-sm" style="margin-left:.5rem;padding:.2rem .5rem;font-size:.75rem" onclick="removeStaff(${w.id})">Remove</button>
          </div>
        </div>`).join('') + `
        <div style="margin-top:1.5rem;display:flex;gap:.5rem;border-top:1px solid var(--border);padding-top:1rem">
          <input id="new-staff-name" placeholder="New Staff Name..." style="flex:1;padding:.4rem .6rem;font-size:.85rem;border:1px solid var(--border);border-radius:4px">
          <button class="btn btn-teal btn-sm" onclick="addStaff()">+ Add Staff</button>
        </div>`;
    } else {
      const myStaff = workload.find(w => w.id === session.id);
      if (myStaff) {
        document.getElementById('staff-workload').innerHTML=`
          <div style="padding:.7rem 0;">
            <div><strong style="font-size:1.1rem;color:var(--primary-dark)">${myStaff.name}</strong></div>
            <div style="font-size:.9rem;color:var(--muted);margin-top:.4rem;">Role: ${myStaff.role}</div>
            <div style="margin-top:.8rem;"><span class="badge b-scheduled">${myStaff.count} Assigned Bookings</span></div>
          </div>
        `;
      }
    }"""

if old in content:
    content = content.replace(old, new)
    open("MediCheck.html", "w", encoding="utf-8").write(content)
    print("Replaced")
else:
    print("Not found")
