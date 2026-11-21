import os

content = open('MediCheck.html', encoding='utf-8').read()

admin_db_old = """    let customerHTML = `<h2 style="font-size:1.3rem;margin:2rem 0 1rem 0">Customer / Patient Database</h2>
      <div style="background:#fff;border:1px solid var(--border);border-radius:var(--r);padding:1.25rem;box-shadow:0 1px 3px rgba(0,0,0,.05);overflow-x:auto;">
        <table style="width:100%; border-collapse:collapse; font-size:.9rem;">
          <thead>
            <tr style="border-bottom:2px solid var(--border);text-align:left;">
              <th style="padding:.5rem">ID</th>
              <th style="padding:.5rem">Name</th>
              <th style="padding:.5rem">Phone</th>
            </tr>
          </thead>
          <tbody>
            ${getPatients().map(p => `
              <tr style="border-bottom:1px solid var(--border);">
                <td style="padding:.5rem;color:var(--primary)">#${p.patient_id}</td>
                <td style="padding:.5rem"><strong>${p.full_name}</strong></td>
                <td style="padding:.5rem">${p.phone}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>`;"""

admin_db_new = """    let customerHTML = `<h2 style="font-size:1.3rem;margin:2rem 0 1rem 0">Customer / Patient Database</h2>
      <div style="background:#fff;border:1px solid var(--border);border-radius:var(--r);padding:1.25rem;box-shadow:0 1px 3px rgba(0,0,0,.05);overflow-x:auto;">
        <table style="width:100%; border-collapse:collapse; font-size:.9rem;">
          <thead>
            <tr style="border-bottom:2px solid var(--border);text-align:left;">
              <th style="padding:.5rem">ID</th>
              <th style="padding:.5rem">Name</th>
              <th style="padding:.5rem">Phone</th>
              <th style="padding:.5rem">Email</th>
              <th style="padding:.5rem">Gender / DOB</th>
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
                <td style="padding:.5rem">${p.gender || '-'} (${p.dob || '-'})</td>
                <td style="padding:.5rem">${p.address || '-'}</td>
                <td style="padding:.5rem"><span class="badge ${p.membership_tier==='Premium'?'b-ready':'b-scheduled'}">${p.membership_tier || 'Standard'}</span></td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      </div>`;"""

if admin_db_old in content:
    content = content.replace(admin_db_old, admin_db_new)
    print("Admin DB Expanded")
else:
    print("Failed Admin DB Expand")

open('MediCheck.html', 'w', encoding='utf-8').write(content)
