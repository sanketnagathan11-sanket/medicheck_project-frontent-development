"""
MediCheck -- Diagnostic Lab & Home Sample Collection Booking System
Field Project-I (24CsDscU3002)

Flask Application Engine
"""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import date, datetime
import db

app = Flask(__name__)
app.secret_key = "medicheck-super-secret-key-2026"


@app.route("/")
def home():
    stats_list = db.query("""
        SELECT (SELECT COUNT(*) FROM patients) AS patient_count,
               (SELECT COUNT(*) FROM tests)    AS test_count,
               (SELECT COUNT(*) FROM bookings) AS booking_count,
               (SELECT COUNT(*) FROM reports WHERE result_status != 'Pending') AS report_count
    """)
    stats = stats_list[0] if stats_list else {"patient_count": 0, "test_count": 0, "booking_count": 0, "report_count": 0}
    
    featured_packages = db.query("SELECT * FROM packages ORDER BY price LIMIT 3")
    featured_tests = db.query("SELECT * FROM tests WHERE category IN ('Blood & Sugar', 'Cardiac', 'Full Body Checkup') LIMIT 4")
    
    return render_template("index.html", stats=stats, packages=featured_packages, tests=featured_tests)


@app.route("/tests")
def tests():
    category = request.args.get("category", "").strip()
    search = request.args.get("q", "").strip()
    
    query_str = "SELECT * FROM tests WHERE 1=1"
    params = []
    
    if category:
        query_str += " AND category = %s"
        params.append(category)
    if search:
        query_str += " AND (test_name LIKE %s OR category LIKE %s)"
        params.extend([f"%{search}%", f"%{search}%"])
        
    query_str += " ORDER BY category, test_name"
    rows = db.query(query_str, tuple(params) if params else None)
    
    categories = db.query("SELECT DISTINCT category FROM tests ORDER BY category")
    packages = db.query("SELECT * FROM packages ORDER BY price")
    
    # Enrich packages with test counts
    for pkg in (packages or []):
        pkg_tests = db.query("""
            SELECT t.test_name FROM package_tests pt 
            JOIN tests t ON pt.test_id = t.test_id 
            WHERE pt.package_id = %s
        """, (pkg["package_id"],))
        pkg["tests_included"] = [t["test_name"] for t in (pkg_tests or [])]
        
    return render_template(
        "tests.html",
        tests=rows,
        categories=categories,
        packages=packages,
        selected_category=category,
        search_query=search
    )


@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        address = request.form.get("address", "").strip()
        dob = request.form.get("dob", str(date.today()))
        gender = request.form.get("gender", "Other")
        tier = request.form.get("tier", "Mass")
        booking_type = request.form.get("booking_type", "Walk-in")
        slot_time = request.form.get("slot_time", "09:00")
        booking_date = request.form.get("booking_date", str(date.today()))
        test_ids = request.form.getlist("test_ids")
        package_id = request.form.get("package_id", "")

        if not test_ids and not package_id:
            flash("Please select at least one test or a package.", "danger")
            return redirect(url_for("book"))

        # 1. Find or create patient
        existing = db.query("SELECT patient_id FROM patients WHERE phone = %s", (phone,))
        if existing:
            patient_id = existing[0]["patient_id"]
            # Update address/tier if updated
            db.query("""
                UPDATE patients 
                SET full_name = %s, email = %s, address = %s, membership_tier = %s 
                WHERE patient_id = %s
            """, (full_name, email, address, tier, patient_id), fetch=False, commit=True)
        else:
            row = db.query("""
                INSERT INTO patients (full_name, dob, gender, phone, email, address, membership_tier)
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING patient_id
            """, (full_name, dob, gender, phone, email, address, tier), commit=True)
            patient_id = row[0]["patient_id"] if row else 1

        # 2. Gather selected test IDs (including package tests if selected)
        final_test_ids = list(set([int(tid) for tid in test_ids if tid.isdigit()]))
        
        if package_id and package_id.isdigit():
            pkg_tests = db.query("SELECT test_id FROM package_tests WHERE package_id = %s", (int(package_id),))
            for pt in (pkg_tests or []):
                if pt["test_id"] not in final_test_ids:
                    final_test_ids.append(pt["test_id"])

        if not final_test_ids:
            flash("No valid tests selected.", "danger")
            return redirect(url_for("book"))

        # 3. Calculate price
        placeholders = ",".join(["%s"] * len(final_test_ids))
        priced = db.query(f"SELECT test_id, price FROM tests WHERE test_id IN ({placeholders})", tuple(final_test_ids))
        
        total = sum(float(t["price"]) for t in (priced or []))
        if package_id and package_id.isdigit():
            pkg_row = db.query("SELECT price FROM packages WHERE package_id = %s", (int(package_id),))
            if pkg_row:
                total = min(total, float(pkg_row[0]["price"]))

        # Add home collection fee for non-premium members if home collection chosen
        if booking_type == "Home Collection" and tier != "Premium":
            total += 150.0  # nominal home sample pickup charge

        # 4. Create booking record
        booking_row = db.query("""
            INSERT INTO bookings (patient_id, booking_type, booking_date, slot_time, status, total_amount)
            VALUES (%s, %s, %s, %s, 'Scheduled', %s) RETURNING booking_id
        """, (patient_id, booking_type, booking_date, slot_time, total), commit=True)
        
        booking_id = booking_row[0]["booking_id"] if booking_row else 1

        # 5. Link tests to booking
        for t in (priced or []):
            db.query("INSERT INTO booking_tests (booking_id, test_id) VALUES (%s, %s)",
                     (booking_id, t["test_id"]), fetch=False, commit=True)

        # 6. Record payment status
        payment_mode = request.form.get("payment_mode", "UPI")
        db.query("""
            INSERT INTO payments (booking_id, amount, payment_mode, payment_status, payment_date)
            VALUES (%s, %s, %s, 'Paid', %s)
        """, (booking_id, total, payment_mode, booking_date), fetch=False, commit=True)

        flash(f"🎉 Booking #{booking_id} successfully confirmed! Use your phone number ({phone}) to track progress.", "success")
        return redirect(url_for("my_bookings", phone=phone))

    test_rows = db.query("SELECT * FROM tests ORDER BY category, test_name")
    package_rows = db.query("SELECT * FROM packages ORDER BY price")
    selected_test = request.args.get("test_id", "")
    selected_pkg = request.args.get("package_id", "")
    
    return render_template("book.html", tests=test_rows, packages=package_rows, selected_test=selected_test, selected_pkg=selected_pkg)


@app.route("/my-bookings")
def my_bookings():
    phone = request.args.get("phone", "").strip()
    booking_id_search = request.args.get("booking_id", "").strip()
    bookings = []
    patient_info = None

    if phone or booking_id_search:
        sql = """
            SELECT b.booking_id, b.booking_type, b.booking_date, b.slot_time,
                   b.status, b.total_amount, p.full_name, p.phone, p.email, p.membership_tier,
                   pay.payment_status, pay.payment_mode,
                   (SELECT string_agg(t.test_name, ', ')
                      FROM booking_tests bt JOIN tests t ON bt.test_id = t.test_id
                     WHERE bt.booking_id = b.booking_id) AS test_list
            FROM bookings b
            JOIN patients p ON b.patient_id = p.patient_id
            LEFT JOIN payments pay ON b.booking_id = pay.booking_id
        """
        params = []
        if booking_id_search and booking_id_search.isdigit():
            sql += " WHERE b.booking_id = %s ORDER BY b.booking_date DESC"
            params.append(int(booking_id_search))
        else:
            sql += " WHERE p.phone = %s ORDER BY b.booking_date DESC"
            params.append(phone)

        bookings = db.query(sql, tuple(params))
        
        if bookings:
            patient_info = {
                "full_name": bookings[0]["full_name"],
                "phone": bookings[0]["phone"],
                "email": bookings[0]["email"],
                "membership_tier": bookings[0]["membership_tier"]
            }

    return render_template("my_bookings.html", bookings=bookings, phone=phone, booking_id=booking_id_search, patient=patient_info)


@app.route("/report/<int:booking_id>")
def view_report(booking_id):
    booking = db.query("""
        SELECT b.booking_id, b.booking_date, b.status, p.full_name, p.dob, p.gender, p.phone, p.email
        FROM bookings b
        JOIN patients p ON b.patient_id = p.patient_id
        WHERE b.booking_id = %s
    """, (booking_id,))

    if not booking:
        flash("Booking report not found.", "warning")
        return redirect(url_for("my_bookings"))

    reports = db.query("""
        SELECT t.test_name, t.category, t.sample_type,
               COALESCE(r.result_status, 'Normal') as result_status,
               COALESCE(r.report_date, b.booking_date) as report_date
        FROM booking_tests bt
        JOIN tests t ON bt.test_id = t.test_id
        JOIN bookings b ON bt.booking_id = b.booking_id
        LEFT JOIN reports r ON (r.booking_id = bt.booking_id AND r.test_id = bt.test_id)
        WHERE bt.booking_id = %s
    """, (booking_id,))

    return render_template("report.html", booking=booking[0], reports=reports)


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        action = request.form.get("action", "update_status")
        booking_id = request.form.get("booking_id")
        
        if action == "update_status" and booking_id:
            new_status = request.form.get("status")
            assigned_staff = request.form.get("assigned_staff")
            
            if assigned_staff and assigned_staff.isdigit():
                db.query("UPDATE bookings SET status = %s, assigned_staff = %s WHERE booking_id = %s",
                         (new_status, int(assigned_staff), booking_id), fetch=False, commit=True)
            else:
                db.query("UPDATE bookings SET status = %s WHERE booking_id = %s",
                         (new_status, booking_id), fetch=False, commit=True)
                
            flash(f"Status for Booking #{booking_id} updated to '{new_status}'.", "success")

        elif action == "update_payment" and booking_id:
            pay_status = request.form.get("payment_status", "Paid")
            db.query("UPDATE payments SET payment_status = %s WHERE booking_id = %s",
                     (pay_status, booking_id), fetch=False, commit=True)
            flash(f"Payment status for Booking #{booking_id} set to '{pay_status}'.", "success")

        return redirect(url_for("admin"))

    status_filter = request.args.get("status", "")
    type_filter = request.args.get("type", "")

    sql = """
        SELECT b.booking_id, p.full_name, p.phone, b.booking_type, b.booking_date, b.slot_time,
               b.status, b.total_amount, s.full_name AS staff_name, s.staff_id,
               pay.payment_status,
               (SELECT string_agg(t.test_name, ', ')
                  FROM booking_tests bt JOIN tests t ON bt.test_id = t.test_id
                 WHERE bt.booking_id = b.booking_id) AS test_list
        FROM bookings b
        JOIN patients p ON b.patient_id = p.patient_id
        LEFT JOIN staff s ON b.assigned_staff = s.staff_id
        LEFT JOIN payments pay ON b.booking_id = pay.booking_id
        WHERE 1=1
    """
    params = []

    if status_filter:
        sql += " AND b.status = %s"
        params.append(status_filter)
    if type_filter:
        sql += " AND b.booking_type = %s"
        params.append(type_filter)

    sql += " ORDER BY b.booking_id DESC LIMIT 50"

    todays_bookings = db.query(sql, tuple(params) if params else None)
    
    staff_list = db.query("SELECT * FROM staff ORDER BY role, full_name")

    workload = db.query("""
        SELECT s.full_name, s.role, COUNT(b.booking_id) AS bookings_assigned
        FROM staff s
        LEFT JOIN bookings b ON s.staff_id = b.assigned_staff
        GROUP BY s.staff_id, s.full_name, s.role 
        ORDER BY bookings_assigned DESC
    """)

    admin_stats = db.query("""
        SELECT 
            (SELECT COUNT(*) FROM bookings WHERE status = 'Scheduled') as pending_count,
            (SELECT COUNT(*) FROM bookings WHERE status = 'Sample Collected') as processing_count,
            (SELECT COUNT(*) FROM bookings WHERE status = 'Report Ready') as ready_count,
            (SELECT SUM(total_amount) FROM bookings WHERE status != 'Cancelled') as total_revenue
    """)[0]

    return render_template(
        "admin.html",
        bookings=todays_bookings,
        staff=staff_list,
        workload=workload,
        stats=admin_stats,
        selected_status=status_filter,
        selected_type=type_filter
    )


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        flash(f"Thank you {name}! Your query has been received. Our team will get back to you within 2 hours.", "success")
        return redirect(url_for("contact"))
    return render_template("contact.html")


if __name__ == "__main__":
    print("Starting MediCheck Flask Web App on http://localhost:5000")
    app.run(debug=True, port=5000)
