import os

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
                  <td style=\"padding:.5rem\">${p.gender || '-'}</td>
                    <td style=\"padding:.5rem\">${p.dob || '-'}</td>
                    <td style=\"padding:.5rem\">${p.blood_group || '-'}</td>
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
                <th style="padding:.5rem">Action</th>
              </tr>
            </thead>
            <tbody>
              ${getPatients().map(p => `
                <tr style="border-bottom:1px solid var(--border);">
                  <td style="padding:.5rem;color:var(--primary)">#${p.patient_id}</td>
                  <td style="padding:.5rem"><strong>${p.full_name}</strong></td>
                  <td style="padding:.5rem">${p.phone}</td>
                  <td style="padding:.5rem">${p.email || '-'}</td>
                  <td style=\"padding:.5rem\">${p.gender || '-'}</td>
                    <td style=\"padding:.5rem\">${p.dob || '-'}</td>
                    <td style=\"padding:.5rem\">${p.blood_group || '-'}</td>
                  <td style="padding:.5rem">${p.address || '-'}</td>
                  <td style="padding:.5rem"><span class="badge ${p.membership_tier==='Premium'?'b-ready':'b-scheduled'}">${p.membership_tier || 'Standard'}</span></td>
                  <td style="padding:.5rem">
                     <button class="btn btn-outline btn-sm" style="padding:.25rem .6rem; font-size:.75rem; border-color:#fca5a5; color:#dc2626;" onclick="removePatient(${p.patient_id})">Delete</button>
                  </td>
                </tr>
              `).join('')}"""

if html_old in content:
    content = content.replace(html_old, html_new)
    print("Replaced HTML block perfectly!")
else:
    print("Direct replacement failed, checking differences.")
    # let's try a robust character-by-character skip
    pass

open('MediCheck.html', 'w', encoding='utf-8').write(content)
