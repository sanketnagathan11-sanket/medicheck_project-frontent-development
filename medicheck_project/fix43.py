import re

c = open('MediCheck.html', encoding='utf-8').read()

# Replace the table headers to include Action if Admin
old_th = r"<thead><tr><th>ID</th><th>Patient</th><th>Type / Slot</th><th>Tests</th><th>Update Status</th><th>Assign\s*Staff</th><th>Payment</th></tr></thead>"
new_th = r"<thead><tr><th>ID</th><th>Patient</th><th>Type / Slot</th><th>Tests</th><th>Update Status</th><th>Assign Staff</th><th>Payment</th>${isAdmin ? '<th>Action</th>' : ''}</tr></thead>"
c = re.sub(old_th, new_th, c)

# Replace the row ending to include Delete button if Admin
old_row = r"""\s*<td>\s*<button class="btn btn-sm \$\{b\.payment_status==='Paid'\?'btn-teal':'btn-outline'\}"\s*onclick="togglePayment\(\$\{b\.booking_id\}\)">\s*\$\{b\.payment_status\|\|'Pending'\}\s*</button>\s*</td>\s*</tr>`;"""

new_row = """            <td>
              <button class="btn btn-sm ${b.payment_status==='Paid'?'btn-teal':'btn-outline'}" onclick="togglePayment(${b.booking_id})">
                ${b.payment_status||'Pending'}
              </button>
            </td>
            ${isAdmin ? `<td><button class="btn btn-sm btn-outline" style="border-color:red; color:red;" onclick="deleteBooking(${b.booking_id})">Delete</button></td>` : ''}
          </tr>`;"""

c = re.sub(old_row, new_row, c)

# Add the deleteBooking function
del_func = """function deleteBooking(id) {
    const session = ls('session');
    if (!session || session.role !== 'Admin') {
        alert('Access denied. Only Admins can delete records.');
        return;
    }
    if(confirm('Are you sure you want to permanently delete this booking?')) {
        let bookings = getBookings();
        bookings = bookings.filter(b => b.booking_id !== id);
        lsSet('bookings', bookings);
        renderAdmin();
    }
}
"""

if 'function deleteBooking' not in c:
    c = c.replace('function togglePayment', del_func + '\nfunction togglePayment')

open('MediCheck.html', 'w', encoding='utf-8').write(c)
print("Updated admin table with delete function!")
