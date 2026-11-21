import os

content = open("MediCheck.html", encoding="utf-8").read()

old_funcs = """  function updateBookingStaff(bookingId, staffId) {
    const bookings = getBookings();
    const b = bookings.find(b=>b.booking_id===bookingId);
    if (b) {
      b.staff_id = staffId ? parseInt(staffId) : null;
      lsSet('bookings', bookings);
    }
    flash(`Assigned technician to booking #${bookingId}`, 'success');
    renderAdmin();
  }
  
  function updateStaffRole(staffId, newRole) {
    const staff = getStaff();
    const s = staff.find(st=>st.staff_id===staffId);
    if (s) {
      s.role = newRole;
      lsSet('staff', staff);
    }
    flash(`Updated role for ${s.full_name} to ${newRole}`, 'success');
    renderAdmin();
  }
  
  function togglePayment(id){
    const bookings = getBookings();
    const b = bookings.find(b=>b.booking_id===id);
    if(b){ b.payment_status = b.payment_status==='Paid'?'Pending':'Paid'; lsSet('bookings',bookings); }
    renderAdmin();
  }"""

new_funcs = """  function updateBookingStaff(bookingId, staffId) {
    const session = ls('session');
    if(!session || session.role !== 'Admin') { flash('Access denied', 'danger'); return; }
    const bookings = getBookings();
    const b = bookings.find(b=>b.booking_id===bookingId);
    if (b) {
      b.staff_id = staffId ? parseInt(staffId) : null;
      lsSet('bookings', bookings);
    }
    flash(`Assigned technician to booking #${bookingId}`, 'success');
    renderAdmin();
  }
  
  function updateStaffRole(staffId, newRole) {
    const session = ls('session');
    if(!session || session.role !== 'Admin') { flash('Access denied', 'danger'); return; }
    const staff = getStaff();
    const s = staff.find(st=>st.staff_id===staffId);
    if (s) {
      s.role = newRole;
      lsSet('staff', staff);
    }
    flash(`Updated role for ${s.full_name} to ${newRole}`, 'success');
    renderAdmin();
  }
  
  function togglePayment(id){
    const session = ls('session');
    if(!session || (session.role !== 'Admin' && session.role !== 'Receptionist')) { flash('Only Admin or Receptionist can modify payment status', 'danger'); return; }
    const bookings = getBookings();
    const b = bookings.find(b=>b.booking_id===id);
    if(b){ b.payment_status = b.payment_status==='Paid'?'Pending':'Paid'; lsSet('bookings',bookings); }
    renderAdmin();
  }"""

if old_funcs in content:
    content = content.replace(old_funcs, new_funcs)
    open("MediCheck.html", "w", encoding="utf-8").write(content)
    print("Success replacing funcs")
else:
    print("Could not find old_funcs")
