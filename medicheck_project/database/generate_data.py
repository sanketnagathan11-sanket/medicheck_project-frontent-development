"""
Generates realistic sample data for MediCheck.
Produces TWO outputs from one consistent dataset:
  1. database/seed_data.sql        -> INSERT statements for PostgreSQL
  2. visualization/bookings_data.csv -> for the pandas/matplotlib assignment

Run: python3 generate_data.py
"""
import random
import csv
from datetime import date, timedelta

random.seed(42)  # reproducible output

# ---------- Reference data ----------
TESTS = [
    ("Complete Blood Count (CBC)", "Blood & Sugar", "Blood", 350, 6),
    ("Fasting Blood Sugar", "Blood & Sugar", "Blood", 150, 4),
    ("HbA1c", "Blood & Sugar", "Blood", 500, 12),
    ("Lipid Profile", "Cardiac", "Blood", 600, 12),
    ("ECG", "Cardiac", "N/A", 400, 2),
    ("Troponin-I", "Cardiac", "Blood", 900, 6),
    ("Thyroid Profile (T3 T4 TSH)", "Thyroid", "Blood", 700, 24),
    ("Liver Function Test (LFT)", "Liver & Kidney", "Blood", 650, 12),
    ("Kidney Function Test (KFT)", "Liver & Kidney", "Blood", 650, 12),
    ("Urine Routine", "Liver & Kidney", "Urine", 200, 6),
    ("Chest X-Ray", "Imaging", "N/A", 500, 4),
    ("Abdominal Ultrasound", "Imaging", "N/A", 1200, 8),
    ("Vitamin D", "Full Body Checkup", "Blood", 1400, 24),
    ("Vitamin B12", "Full Body Checkup", "Blood", 900, 24),
    ("COVID-19 RT-PCR", "Full Body Checkup", "Swab", 700, 24),
]

PACKAGES = [
    ("Basic Health Checkup", "CBC + Sugar + Urine Routine", 550, "Mass"),
    ("Diabetes Care Package", "Sugar + HbA1c + KFT", 1100, "Mass"),
    ("Executive Full Body Checkup", "15-parameter premium panel", 3999, "Premium"),
    ("Cardiac Risk Package", "Lipid + ECG + Troponin-I", 1800, "Premium"),
]

FIRST_NAMES = ["Aarav","Vivaan","Aditi","Diya","Rohan","Sneha","Karan","Isha",
    "Pranav","Meera","Sanjay","Pooja","Amit","Neha","Rahul","Kavya","Arjun",
    "Ritu","Manish","Priya","Nikhil","Anjali","Suresh","Divya","Rajesh"]
LAST_NAMES = ["Sharma","Patil","Kulkarni","Deshmukh","Joshi","Kumar","Shah",
    "Verma","Reddy","Iyer","Naik","Gokhale","Bhosale","Kadam","Pawar"]

ROLES = ["Technician","Technician","Technician","Receptionist","Courier","Admin"]

CATEGORIES = sorted(set(t[1] for t in TESTS))
MONTHS = ["2026-01","2026-02","2026-03","2026-04","2026-05","2026-06","2026-07"]

# ---------- Generate patients ----------
patients = []
for i in range(1, 31):
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    dob = date(random.randint(1955, 2006), random.randint(1, 12), random.randint(1, 28))
    gender = random.choice(["Male", "Female"])
    phone = f"9{random.randint(100000000, 999999999)}"
    email = name.lower().replace(" ", ".") + f"{i}@example.com"
    tier = "Premium" if random.random() < 0.3 else "Mass"
    reg_on = date(2026, 1, random.randint(1, 28))
    patients.append((i, name, dob, gender, phone, email, tier, reg_on))

# ---------- Generate staff ----------
staff = []
for i in range(1, 7):
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    role = ROLES[i - 1]
    phone = f"9{random.randint(100000000, 999999999)}"
    email = name.lower().replace(" ", ".") + f".staff{i}@medicheck.in"
    staff.append((i, name, role, phone, email))

# ---------- Generate bookings + booking_tests + reports + payments ----------
bookings, booking_tests, reports, payments = [], [], [], []
csv_rows = []  # for visualization CSV: month, category, tier, bookings, revenue

booking_id = 1
report_id = 1
payment_id = 1

# track (month, category, tier) -> [count, revenue] for the CSV
agg = {}

for month_str in MONTHS:
    y, m = map(int, month_str.split("-"))
    n_bookings_this_month = random.randint(8, 14)
    for _ in range(n_bookings_this_month):
        patient = random.choice(patients)
        pid, tier = patient[0], patient[6]
        booking_type = "Home Collection" if (tier == "Premium" and random.random() < 0.7) else \
                        random.choice(["Walk-in", "Walk-in", "Home Collection"])
        day = random.randint(1, 27)
        b_date = date(y, m, day)
        slot_hour = random.randint(8, 18)
        status = random.choices(
            ["Report Ready", "Sample Collected", "Scheduled", "Cancelled"],
            weights=[70, 15, 10, 5])[0]
        staff_id = random.choice(staff)[0]

        n_tests = random.randint(1, 3)
        chosen_tests = random.sample(range(1, len(TESTS) + 1), n_tests)
        total = 0
        for t_idx in chosen_tests:
            price = TESTS[t_idx - 1][3]
            total += price
            booking_tests.append((booking_id, t_idx))
            category = TESTS[t_idx - 1][1]
            key = (month_str, category, tier)
            if key not in agg:
                agg[key] = [0, 0]
            agg[key][0] += 1
            agg[key][1] += price

            if status in ("Report Ready",):
                result = random.choices(["Normal", "Abnormal"], weights=[80, 20])[0]
                report_date = b_date + timedelta(days=random.randint(1, 3))
                reports.append((report_id, booking_id, t_idx, result, report_date))
                report_id += 1

        bookings.append((booking_id, pid, booking_type, b_date, f"{slot_hour:02d}:00:00",
                          status, staff_id, total))

        if status != "Cancelled":
            pay_status = "Paid" if status in ("Report Ready", "Sample Collected") \
                         else random.choice(["Paid", "Pending"])
            pay_mode = random.choice(["UPI", "Card", "Cash", "Online"])
            pay_date = b_date if pay_status == "Paid" else None
            payments.append((payment_id, booking_id, total, pay_mode, pay_status, pay_date))
            payment_id += 1

        booking_id += 1

for (month_str, category, tier), (cnt, revenue) in sorted(agg.items()):
    csv_rows.append((month_str, category, tier, cnt, revenue))

# ---------- Write seed_data.sql ----------
def sql_str(v):
    if v is None:
        return "NULL"
    if isinstance(v, (int, float)):
        return str(v)
    return "'" + str(v).replace("'", "''") + "'"

with open("seed_data.sql", "w") as f:
    f.write("-- Auto-generated seed data for MediCheck (run after schema.sql)\n\n")

    f.write("INSERT INTO patients (patient_id, full_name, dob, gender, phone, email, membership_tier, registered_on) VALUES\n")
    f.write(",\n".join(
        f"({p[0]}, {sql_str(p[1])}, {sql_str(p[2])}, {sql_str(p[3])}, {sql_str(p[4])}, {sql_str(p[5])}, {sql_str(p[6])}, {sql_str(p[7])})"
        for p in patients) + ";\n\n")

    f.write("INSERT INTO staff (staff_id, full_name, role, phone, email) VALUES\n")
    f.write(",\n".join(
        f"({s[0]}, {sql_str(s[1])}, {sql_str(s[2])}, {sql_str(s[3])}, {sql_str(s[4])})"
        for s in staff) + ";\n\n")

    f.write("INSERT INTO tests (test_id, test_name, category, sample_type, price, report_time_hrs) VALUES\n")
    f.write(",\n".join(
        f"({i+1}, {sql_str(t[0])}, {sql_str(t[1])}, {sql_str(t[2])}, {t[3]}, {t[4]})"
        for i, t in enumerate(TESTS)) + ";\n\n")

    f.write("INSERT INTO packages (package_id, package_name, description, price, tier) VALUES\n")
    f.write(",\n".join(
        f"({i+1}, {sql_str(p[0])}, {sql_str(p[1])}, {p[2]}, {sql_str(p[3])})"
        for i, p in enumerate(PACKAGES)) + ";\n\n")

    f.write("INSERT INTO package_tests (package_id, test_id) VALUES\n")
    f.write(",\n".join(f"({pt[0]}, {pt[1]})" for pt in [
        (1,1),(1,2),(1,10),(2,2),(2,3),(2,9),(3,1),(3,3),(3,4),(3,7),(3,8),(3,9),(3,13),(3,14),
        (4,4),(4,5),(4,6)
    ]) + ";\n\n")

    f.write("INSERT INTO bookings (booking_id, patient_id, booking_type, booking_date, slot_time, status, assigned_staff, total_amount) VALUES\n")
    f.write(",\n".join(
        f"({b[0]}, {b[1]}, {sql_str(b[2])}, {sql_str(b[3])}, {sql_str(b[4])}, {sql_str(b[5])}, {b[6]}, {b[7]})"
        for b in bookings) + ";\n\n")

    f.write("INSERT INTO booking_tests (booking_id, test_id) VALUES\n")
    f.write(",\n".join(f"({bt[0]}, {bt[1]})" for bt in booking_tests) + ";\n\n")

    f.write("INSERT INTO reports (report_id, booking_id, test_id, result_status, report_date) VALUES\n")
    f.write(",\n".join(
        f"({r[0]}, {r[1]}, {r[2]}, {sql_str(r[3])}, {sql_str(r[4])})"
        for r in reports) + ";\n\n")

    f.write("INSERT INTO payments (payment_id, booking_id, amount, payment_mode, payment_status, payment_date) VALUES\n")
    f.write(",\n".join(
        f"({p[0]}, {p[1]}, {p[2]}, {sql_str(p[3])}, {sql_str(p[4])}, {sql_str(p[5])})"
        for p in payments) + ";\n\n")

    f.write("-- Keep SERIAL sequences in sync with the explicit IDs above\n")
    f.write("SELECT setval('patients_patient_id_seq', (SELECT MAX(patient_id) FROM patients));\n")
    f.write("SELECT setval('staff_staff_id_seq', (SELECT MAX(staff_id) FROM staff));\n")
    f.write("SELECT setval('tests_test_id_seq', (SELECT MAX(test_id) FROM tests));\n")
    f.write("SELECT setval('packages_package_id_seq', (SELECT MAX(package_id) FROM packages));\n")
    f.write("SELECT setval('bookings_booking_id_seq', (SELECT MAX(booking_id) FROM bookings));\n")
    f.write("SELECT setval('reports_report_id_seq', (SELECT MAX(report_id) FROM reports));\n")
    f.write("SELECT setval('payments_payment_id_seq', (SELECT MAX(payment_id) FROM payments));\n")

# ---------- Write visualization CSV ----------
with open("../visualization/bookings_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Month", "Category", "Tier", "Bookings", "Revenue"])
    for row in csv_rows:
        writer.writerow(row)

print(f"Generated: {len(patients)} patients, {len(staff)} staff, {len(TESTS)} tests, "
      f"{len(bookings)} bookings, {len(payments)} payments, {len(csv_rows)} CSV rows")
