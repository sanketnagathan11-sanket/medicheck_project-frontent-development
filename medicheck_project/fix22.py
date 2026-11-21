import os

content = open('MediCheck.html', encoding='utf-8').read()

# 1. Remove "Authorized Admin Access Only."
auth_txt_old = '<p class="section-sub" style="text-align:left; margin-bottom: 2rem;">Authorized Admin Access Only.</p>'
if auth_txt_old in content:
    content = content.replace(auth_txt_old, '')
    print("Removed Admin text")
else:
    print("Failed to find Admin text")

# 2. Update renderPatients columns
col_old = """              <tr style="border-bottom:2px solid var(--border);text-align:left;">
                <th style="padding:.5rem">ID</th>
                <th style="padding:.5rem">Name</th>
                <th style="padding:.5rem">Phone</th>
                <th style="padding:.5rem">Email</th>
                <th style="padding:.5rem">Gender/DOB/Blood</th>
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
                  <td style="padding:.5rem">${p.gender || '-'} (${p.dob || '-'}) [${p.blood_group || '-'}]</td>
                  <td style="padding:.5rem">${p.address || '-'}</td>
                  <td style="padding:.5rem"><span class="badge ${p.membership_tier==='Premium'?'b-ready':'b-scheduled'}">${p.membership_tier || 'Standard'}</span></td>
                </tr>"""

col_new = """              <tr style="border-bottom:2px solid var(--border);text-align:left;">
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
                </tr>"""

if col_old in content:
    content = content.replace(col_old, col_new)
    print("Updated columns")
else:
    print("Failed to find columns pattern")
    
open('MediCheck.html', 'w', encoding='utf-8').write(content)
