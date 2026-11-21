import re
c = open('MediCheck.html', encoding='utf-8').read()

# We want to find the exact block for the patient table.
# It is within function renderPatients() 

start_fn = c.find("function renderPatients()")
if start_fn != -1:
    end_fn = c.find("function addStaff()", start_fn)
    block = c[start_fn:end_fn]
    
    # In this block, replace the headers:
    block = block.replace('<th style="padding:.5rem">Tier</th>', '<th style="padding:.5rem">Tier</th>\n                <th style="padding:.5rem;text-align:center;">Action</th>')
    
    # In this block, replace the row content:
    # </td>\n                  <td style="padding:.5rem"><span class="badge ${p.membership_tier==='Premium'?'b-ready':'b-scheduled'}">${p.membership_tier || 'Standard'}</span></td>
    
    row_end_old = """<td style="padding:.5rem"><span class="badge ${p.membership_tier==='Premium'?'b-ready':'b-scheduled'}">${p.membership_tier || 'Standard'}</span></td>
                </tr>"""
                
    row_end_new = """<td style="padding:.5rem"><span class="badge ${p.membership_tier==='Premium'?'b-ready':'b-scheduled'}">${p.membership_tier || 'Standard'}</span></td>
                  <td style="padding:.5rem;text-align:center;">
                    <button class="btn btn-outline btn-sm" style="padding:.25rem .6rem; font-size:.75rem; border-color:#fca5a5; color:#dc2626;" onclick="removePatient(${p.patient_id})">Delete</button>
                  </td>
                </tr>"""
                
    block = block.replace(row_end_old, row_end_new)
    
    c = c[:start_fn] + block + c[end_fn:]
    print("Replaced!")
else:
    print("Not found")

open('MediCheck.html', 'w', encoding='utf-8').write(c)
