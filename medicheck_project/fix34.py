import re

c = open('MediCheck.html', encoding='utf-8').read()

start_fn = c.find("function renderPatients()")
end_fn = c.find("function addStaff()", start_fn)

block = c[start_fn:end_fn]

# Find the <tbody>...</tbody>
tbody_match = re.search(r'<tbody>(.*?)</tbody>', block, re.DOTALL)
if tbody_match:
    old_tbody = tbody_match.group(1)
    new_tbody = """
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
                    <button class="btn btn-outline btn-sm" style="padding:.25rem .6rem; font-size:.75rem; border-color:#fca5a5; color:#dc2626;" onclick="removePatient(${p.patient_id})">Delete</button>
                  </td>
                </tr>
              `).join('')}
            """
    block = block.replace(old_tbody, new_tbody)
    c = c[:start_fn] + block + c[end_fn:]
    open('MediCheck.html', 'w', encoding='utf-8').write(c)
    print("Replaced successfully!")
else:
    print("Could not find tbody")
