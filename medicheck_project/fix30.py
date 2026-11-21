import os, re

content = open('MediCheck.html', encoding='utf-8').read()

html_old = """              <tr style="border-bottom:2px solid var(--border);text-align:left;">
                <th style="padding:.5rem">ID</th>
                <th style="padding:.5rem">Name</th>
                <th style="padding:.5rem">Phone</th>
                <th style="padding:.5rem">Email</th>
                <th style="padding:.5rem">Gender</th>
                  <th style="padding:.5rem">DOB</th>
                  <th style="padding:.5rem">Blood</th>
                <th style="padding:.5rem">Address</th>
                <th style="padding:.5rem">Tier</th>
              </tr>
            </thead>
            <tbody>
              ${getPatients().map(p => `
                <tr style="border-bottom:1px solid var(--border);">
                  <td style="padding:.5rem;color:var(--primary)">#${p.patient_id}</td>
                  <td style="padding:.5rem"><strong>${p.full_name}</strong></td>
                  <td style="padding:.5rem">${p.phone}</td>
                  <td style="padding:.5rem">${p.email || '-'}</td>
                  <td style="padding:.5rem">${p.gender || '-'}</td>
                    <td style="padding:.5rem">${p.dob || '-'}</td>
                    <td style="padding:.5rem">${p.blood_group || '-'}</td>
                  <td style="padding:.5rem">${p.address || '-'}</td>
                  <td style="padding:.5rem"><span class="badge ${p.membership_tier==='Premium'?'b-ready':'b-scheduled'}">${p.membership_tier || 'Standard'}</span></td>
                </tr>
              `).join('')}"""

html_new = """              <tr style="border-bottom:2px solid var(--border);text-align:left;">
                <th style="padding:.5rem">ID</th>
                <th style="padding:.5rem">Name</th>
                <th style="padding:.5rem">Phone</th>
                <th style="padding:.5rem">Email</th>
                <th style="padding:.5rem">Gender</th>
                  <th style="padding:.5rem">DOB</th>
                  <th style="padding:.5rem">Blood</th>
                <th style="padding:.5rem">Address</th>
                <th style="padding:.5rem">Tier</th>
                <th style="padding:.5rem;text-align:center;">Action</th>
              </tr>
            </thead>
            <tbody>
              ${getPatients().map(p => `
                <tr style="border-bottom:1px solid var(--border);">
                  <td style="padding:.5rem;color:var(--primary)">#${p.patient_id}</td>
                  <td style="padding:.5rem"><strong>${p.full_name}</strong></td>
                  <td style="padding:.5rem">${p.phone}</td>
                  <td style="padding:.5rem">${p.email || '-'}</td>
                  <td style="padding:.5rem">${p.gender || '-'}</td>
                    <td style="padding:.5rem">${p.dob || '-'}</td>
                    <td style="padding:.5rem">${p.blood_group || '-'}</td>
                  <td style="padding:.5rem">${p.address || '-'}</td>
                  <td style="padding:.5rem"><span class="badge ${p.membership_tier==='Premium'?'b-ready':'b-scheduled'}">${p.membership_tier || 'Standard'}</span></td>
                  <td style="padding:.5rem;text-align:center;">
                    <button class="btn btn-outline btn-sm" style="padding:.25rem .6rem; font-size:.75rem; border-color:#fca5a5; color:#dc2626;" onclick="removePatient(${p.patient_id})">Remove</button>
                  </td>
                </tr>
              `).join('')}"""

def fix_spaces(t):
    return re.sub(r'\s+', '', t).replace('\\"', '"')

content_stripped = fix_spaces(content)
html_old_stripped = fix_spaces(html_old)

if html_old_stripped in content_stripped:
    # Use re to replace the block
    pattern = re.compile(
        r'<tr[^>]*>\s*<th[^>]*>ID</th>.*?<td[^>]*><span[^>]*>\$\{p\.membership_tier \|\| \'Standard\'\}</span></td>\s*</tr>\s*`\)\.join\(\'\'\)\}',
        re.DOTALL
    )
    
    match = pattern.search(content)
    if match:
        content = content[:match.start()] + html_new + content[match.end():]
        print("Replaced HTML generation")
    else:
        print("Regex match failed")
else:
    print("Could not find stripped HTML")


# Add removePatient function
remove_js = """
  function removePatient(id) {
    const session = ls('session');
    if(!session || session.role !== 'Admin') return;
    if(!confirm('Are you sure you want to remove this patient from the database? This cannot be undone.')) return;
    let patients = getPatients();
    patients = patients.filter(p => p.patient_id !== id);
    lsSet('patients', patients);
    flash('Patient removed successfully!', 'success');
    renderPatients();
  }
"""

if "function removePatient(" not in content:
    idx = content.find("function renderPatients()")
    if idx != -1:
        content = content[:idx] + remove_js + "\n" + content[idx:]
        print("Injected removePatient function")
    else:
        print("Failed to find renderPatients to inject before")

open('MediCheck.html', 'w', encoding='utf-8').write(content)
print("Done!")
