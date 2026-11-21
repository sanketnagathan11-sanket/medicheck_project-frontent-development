csv_data = """Month,Category,Tier,Bookings,Revenue
2026-01,Blood & Sugar,Mass,10,3850
2026-01,Cardiac,Mass,3,1600
2026-01,Full Body Checkup,Mass,3,3000
2026-01,Imaging,Mass,5,3900
2026-01,Liver & Kidney,Mass,6,3900
2026-01,Thyroid,Mass,3,2100
2026-02,Blood & Sugar,Mass,1,350
2026-02,Cardiac,Mass,5,2600
2026-02,Full Body Checkup,Mass,1,900
2026-02,Imaging,Mass,1,500
2026-02,Imaging,Premium,1,1200
2026-02,Liver & Kidney,Mass,4,1700
2026-03,Blood & Sugar,Premium,1,150
2026-03,Cardiac,Mass,4,2000
2026-03,Full Body Checkup,Mass,3,3700
2026-03,Full Body Checkup,Premium,5,5300
2026-03,Imaging,Premium,1,500
2026-03,Liver & Kidney,Premium,2,850
2026-03,Thyroid,Mass,3,2100
2026-03,Thyroid,Premium,1,700
2026-04,Blood & Sugar,Mass,1,500
2026-04,Blood & Sugar,Premium,1,150
2026-04,Cardiac,Mass,3,2200
2026-04,Cardiac,Premium,5,2700
2026-04,Full Body Checkup,Mass,3,3000
2026-04,Full Body Checkup,Premium,1,900
2026-04,Imaging,Mass,1,1200
2026-04,Imaging,Premium,2,1700
2026-04,Liver & Kidney,Mass,5,3250
2026-04,Thyroid,Premium,1,700
2026-05,Blood & Sugar,Mass,7,2150
2026-05,Blood & Sugar,Premium,3,450
2026-05,Cardiac,Mass,1,600
2026-05,Cardiac,Premium,2,1000
2026-05,Full Body Checkup,Mass,1,700
2026-05,Imaging,Mass,1,500
2026-05,Liver & Kidney,Mass,2,850
2026-05,Liver & Kidney,Premium,3,1500
2026-06,Blood & Sugar,Mass,2,650
2026-06,Cardiac,Mass,4,2300
2026-06,Cardiac,Premium,1,400
2026-06,Full Body Checkup,Mass,4,3900
2026-06,Imaging,Mass,3,2900
2026-06,Liver & Kidney,Mass,4,2150
2026-06,Thyroid,Mass,1,700
2026-07,Blood & Sugar,Mass,4,1150
2026-07,Cardiac,Mass,5,3400
2026-07,Cardiac,Premium,1,900
2026-07,Full Body Checkup,Mass,1,700
2026-07,Full Body Checkup,Premium,2,1600
2026-07,Imaging,Mass,3,1500
2026-07,Liver & Kidney,Mass,6,2550
2026-07,Thyroid,Mass,1,700"""

import re
import random
import json

tests = {
    'Blood & Sugar': [1, 2, 3],
    'Cardiac': [4, 5, 6],
    'Thyroid': [7],
    'Liver & Kidney': [8, 9, 10],
    'Imaging': [11, 12],
    'Full Body Checkup': [13, 14, 15]
}

first_names = ["Arjun", "Rohan", "Priya", "Anjali", "Diya", "Kabir", "Neha", "Vihaan", "Aditi", "Rahul", "Vikram", "Isha", "Riya", "Karan", "Aarav"]
last_names = ["Sharma", "Verma", "Patil", "Deshmukh", "Reddy", "Singh", "Shah", "Mehta", "Iyer", "Rao", "Nair", "Pillai", "Das"]

patients = []
bookings = []

p_id = 1
b_id = 1

for line in csv_data.split('\n')[1:]:
    if not line.strip(): continue
    month, cat, tier, count, rev = line.split(',')
    count = int(count)
    rev = float(rev)
    
    rev_per_booking = round(rev / count, 2)
    
    for _ in range(count):
        # Generate patient
        fname = random.choice(first_names) + " " + random.choice(last_names)
        phone = "98" + "".join([str(random.randint(0,9)) for _ in range(8)])
        gender = random.choice(["Male", "Female"])
        mem_tier = "Premium" if tier == "Premium" else "Standard"
        patients.append({
            "patient_id": p_id,
            "full_name": fname,
            "phone": phone,
            "dob": f"{random.randint(1960, 2005)}-01-01",
            "gender": gender,
            "email": "",
            "address": "Local City",
            "membership_tier": mem_tier,
            "password": "pass"
        })
        
        # Generate booking
        booking_type = "Home Collection" if tier == "Premium" else "Walk-in"
        test_id_choice = random.choice(tests[cat])
        
        day = random.randint(1, 28)
        b_date = f"{month}-{day:02d}"
        
        status_choice = random.choice(["Report Ready", "Sample Collected", "Scheduled"])
        
        bookings.append({
            "booking_id": b_id,
            "patient_id": p_id,
            "booking_type": booking_type,
            "booking_date": b_date,
            "slot_time": f"{random.randint(9, 17):02d}:00",
            "status": status_choice,
            "total_amount": rev_per_booking,
            "test_ids": [test_id_choice],
            "payment_status": "Paid",
            "payment_mode": "Online",
            "staff_id": random.randint(1, 3)
        })
        
        p_id += 1
        b_id += 1

# Generate JS strings
patients_js = "const SEED_PATIENTS = [\n" + ",\n".join(["    " + json.dumps(p) for p in patients]) + "\n  ];"
bookings_js = "const SEED_BOOKINGS = [\n" + ",\n".join(["    " + json.dumps(b) for b in bookings]) + "\n  ];"

c = open('MediCheck.html', encoding='utf-8').read()

# Replace SEED_PATIENTS
c = re.sub(r'const SEED_PATIENTS = \[.*?\];', patients_js, c, flags=re.DOTALL)
c = re.sub(r'const SEED_BOOKINGS = \[.*?\];', bookings_js, c, flags=re.DOTALL)

# Inject localStorage clear to wipe old data on next load
clear_script = "localStorage.removeItem('mc_patients'); localStorage.removeItem('mc_bookings'); initData();\n  function ls(key){"
c = c.replace("function ls(key){", clear_script)

open('MediCheck.html', 'w', encoding='utf-8').write(c)
print("Updated successfully.")
