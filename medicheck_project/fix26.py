import os, re

content = open('MediCheck.html', encoding='utf-8').read()

old_workload_html = r"""document\.getElementById\('staff-workload'\)\.innerHTML=workload\.map\(w=>`\s*<div style="display:flex;justify-content:space-between;align-items:center;padding:\.7rem 0;border-bottom:1px\s*solid var\(--border\)">\s*<div><strong style="font-size:\.93rem">\$\{w\.name\}</strong>\s*<div style="font-size:\.76rem;color:var\(--muted\);margin-top:\.2rem;">\s*<select onchange="updateStaffRole\(\$\{w\.id\}, this\.value\)" style="padding:\.1rem; font-size:\.75rem;">\s*\$\{\['Technician', 'Receptionist', 'Courier', 'Admin'\]\.map\(r => `<option\s*\$\{w\.role===r\?'selected':''\}>\$\{r\}</option>`\)\.join\(''\)\}\s*</select>\s*</div>\s*</div>\s*<div>\s*<span class="badge b-scheduled">\$\{w\.count\} Assigned</span>\s*\$\{w\.id !== session\.id \? `<button class="btn btn-outline btn-sm" style="margin-left:\.5rem;padding:\.2rem\s*\.5rem;font-size:\.75rem" onclick="removeStaff\(\$\{w\.id\}\)">Remove</button>` : ''\}\s*</div>\s*</div>`\)\.join\(''\) \+ `\s*<div style="margin-top:1\.5rem;display:flex;gap:\.5rem;border-top:1px solid var\(--border\);padding-top:1rem">\s*<input id="new-staff-name" placeholder="New Staff Name\.\.\." style="flex:1;padding:\.4rem\s*\.6rem;font-size:\.85rem;border:1px solid var\(--border\);border-radius:4px">\s*<button class="btn btn-teal btn-sm" onclick="addStaff\(\)">\+ Add Staff</button>\s*</div>`;"""

new_workload_html = r"""document.getElementById('staff-workload').innerHTML=workload.map(w=>`
        <div style="display:flex; justify-content:space-between; align-items:center; gap:1rem; padding:1.25rem 0; border-bottom:1px solid var(--border)">
          <div style="flex:1; min-width:0; display:flex; flex-direction:column; gap:0.4rem;">
             <div style="font-size:1.05rem; font-weight:700; color:var(--text); white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" title="${w.name}">${w.name}</div>
             <select onchange="updateStaffRole(${w.id}, this.value)" style="padding:.3rem .5rem; font-size:.85rem; border:1px solid var(--border); border-radius:6px; background:#f8fafc; max-width:140px; cursor:pointer;">
               ${['Technician', 'Receptionist', 'Courier', 'Admin'].map(r => `<option ${w.role===r?'selected':''}>${r}</option>`).join('')}
             </select>
          </div>
          <div style="display:flex; flex-direction:column; align-items:flex-end; gap:.6rem;">
            <span class="badge b-scheduled" style="white-space:nowrap; font-size:.8rem; padding:.3rem .8rem;">${w.count} Assigned</span>
            ${w.id !== session.id ? `<button class="btn btn-outline btn-sm" style="padding:.3rem .8rem; font-size:.8rem; border-color:#cbd5e1; color:var(--text);" onclick="removeStaff(${w.id})">Remove</button>` : `<div style="height:28px;"></div>`}
          </div>
        </div>`).join('') + `
        <div style="margin-top:1.5rem;display:flex;flex-direction:column;gap:.75rem;border-top:1px solid var(--border);padding-top:1.5rem">
          <input id="new-staff-name" placeholder="Enter New Staff Name..." style="width:100%;padding:.7rem 1rem;font-size:.95rem;border:1px solid var(--border);border-radius:8px;outline:none;">
          <button class="btn btn-teal" style="width:100%;padding:.7rem;border-radius:8px;font-size:1rem;" onclick="addStaff()">+ Add Staff</button>
        </div>`;"""

# Need a careful replacement. I will use a more relaxed regex or simple find/replace on a stripped version.
# Let's extract the block.

import sys
start_idx = content.find("document.getElementById('staff-workload').innerHTML=workload.map(w=>`")
if start_idx == -1:
    print("Could not find start")
    sys.exit()

end_idx = content.find("</div>`;", start_idx) + len("</div>`;")

if end_idx < start_idx + 10:
    print("Could not find end")
    sys.exit()

new_content = content[:start_idx] + new_workload_html.replace('\\', '') + content[end_idx:]
open('MediCheck.html', 'w', encoding='utf-8').write(new_content)
print("Updated workload layout successfully!")
