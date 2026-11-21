-- =========================================================
-- MediCheck: Diagnostic Lab & Home Sample Collection System
-- PostgreSQL Schema (3NF)
-- Field Project-I (24CsDscU3002)
-- =========================================================

DROP TABLE IF EXISTS payments, reports, booking_tests, bookings,
    package_tests, packages, tests, staff, patients CASCADE;

-- 1. PATIENTS ------------------------------------------------
CREATE TABLE patients (
    patient_id      SERIAL PRIMARY KEY,
    full_name       VARCHAR(100) NOT NULL,
    dob             DATE NOT NULL,
    gender          VARCHAR(10)  CHECK (gender IN ('Male','Female','Other')),
    phone           VARCHAR(15)  NOT NULL UNIQUE,
    email           VARCHAR(100) UNIQUE,
    address         TEXT,
    membership_tier VARCHAR(10)  NOT NULL DEFAULT 'Mass'
                     CHECK (membership_tier IN ('Mass','Premium')),
    registered_on   DATE NOT NULL DEFAULT CURRENT_DATE
);

-- 2. STAFF ----------------------------------------------------
CREATE TABLE staff (
    staff_id    SERIAL PRIMARY KEY,
    full_name   VARCHAR(100) NOT NULL,
    role        VARCHAR(20)  NOT NULL
                 CHECK (role IN ('Technician','Receptionist','Courier','Admin')),
    phone       VARCHAR(15)  NOT NULL,
    email       VARCHAR(100) UNIQUE
);

-- 3. TESTS ------------------------------------------------------
CREATE TABLE tests (
    test_id         SERIAL PRIMARY KEY,
    test_name       VARCHAR(100) NOT NULL,
    category        VARCHAR(50)  NOT NULL,
    sample_type     VARCHAR(30)  NOT NULL,
    price           DECIMAL(8,2) NOT NULL CHECK (price >= 0),
    report_time_hrs INT NOT NULL DEFAULT 24
);

-- 4. PACKAGES (bundles of tests, e.g. "Full Body Checkup") -----
CREATE TABLE packages (
    package_id   SERIAL PRIMARY KEY,
    package_name VARCHAR(100) NOT NULL,
    description  TEXT,
    price        DECIMAL(8,2) NOT NULL CHECK (price >= 0),
    tier         VARCHAR(10)  NOT NULL DEFAULT 'Mass'
                  CHECK (tier IN ('Mass','Premium'))
);

-- 5. PACKAGE_TESTS (bridge table: packages <-> tests, M:M) -----
CREATE TABLE package_tests (
    package_id INT NOT NULL REFERENCES packages(package_id) ON DELETE CASCADE,
    test_id    INT NOT NULL REFERENCES tests(test_id)    ON DELETE CASCADE,
    PRIMARY KEY (package_id, test_id)
);

-- 6. BOOKINGS ----------------------------------------------------
CREATE TABLE bookings (
    booking_id     SERIAL PRIMARY KEY,
    patient_id     INT NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    booking_type   VARCHAR(20) NOT NULL
                    CHECK (booking_type IN ('Walk-in','Home Collection')),
    booking_date   DATE NOT NULL DEFAULT CURRENT_DATE,
    slot_time      TIME NOT NULL,
    status         VARCHAR(20) NOT NULL DEFAULT 'Scheduled'
                    CHECK (status IN ('Scheduled','Sample Collected','Report Ready','Cancelled')),
    assigned_staff INT REFERENCES staff(staff_id),
    total_amount   DECIMAL(8,2) NOT NULL DEFAULT 0
);

-- 7. BOOKING_TESTS (bridge table: bookings <-> tests, M:M) ------
CREATE TABLE booking_tests (
    booking_id INT NOT NULL REFERENCES bookings(booking_id) ON DELETE CASCADE,
    test_id    INT NOT NULL REFERENCES tests(test_id),
    PRIMARY KEY (booking_id, test_id)
);

-- 8. REPORTS -------------------------------------------------------
CREATE TABLE reports (
    report_id     SERIAL PRIMARY KEY,
    booking_id    INT NOT NULL REFERENCES bookings(booking_id) ON DELETE CASCADE,
    test_id       INT NOT NULL REFERENCES tests(test_id),
    result_status VARCHAR(15) CHECK (result_status IN ('Normal','Abnormal','Pending')),
    report_date   DATE,
    UNIQUE (booking_id, test_id)
);

-- 9. PAYMENTS --------------------------------------------------------
CREATE TABLE payments (
    payment_id     SERIAL PRIMARY KEY,
    booking_id     INT NOT NULL REFERENCES bookings(booking_id) ON DELETE CASCADE,
    amount         DECIMAL(8,2) NOT NULL,
    payment_mode   VARCHAR(20) CHECK (payment_mode IN ('Cash','UPI','Card','Online')),
    payment_status VARCHAR(15) NOT NULL DEFAULT 'Pending'
                    CHECK (payment_status IN ('Pending','Paid','Refunded')),
    payment_date   DATE
);

-- Helpful indexes for the query workload in queries.sql
CREATE INDEX idx_bookings_patient ON bookings(patient_id);
CREATE INDEX idx_bookings_date    ON bookings(booking_date);
CREATE INDEX idx_payments_status  ON payments(payment_status);
