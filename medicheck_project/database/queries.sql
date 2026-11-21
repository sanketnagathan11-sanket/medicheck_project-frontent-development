-- =========================================================
-- MediCheck: Functional Requirement Queries
-- Assignment 3 (24CsDscU3002) — Joins, Nested Queries, Aggregates
-- Run schema.sql then seed_data.sql before these.
-- =========================================================

-- Q1 [JOIN] All bookings with patient name, type, and amount
SELECT b.booking_id, p.full_name, b.booking_type, b.booking_date,
       b.status, b.total_amount
FROM bookings b
JOIN patients p ON b.patient_id = p.patient_id
ORDER BY b.booking_date DESC;

-- Q2 [JOIN, multi-table] All tests included in a specific booking
SELECT b.booking_id, t.test_name, t.category, t.price
FROM booking_tests bt
JOIN bookings b ON bt.booking_id = b.booking_id
JOIN tests t    ON bt.test_id    = t.test_id
WHERE b.booking_id = 1;

-- Q3 [AGGREGATE + HAVING] Patients who booked more than 2 times
SELECT p.full_name, COUNT(b.booking_id) AS total_bookings
FROM patients p
JOIN bookings b ON p.patient_id = b.patient_id
GROUP BY p.full_name
HAVING COUNT(b.booking_id) > 2
ORDER BY total_bookings DESC;

-- Q4 [JOIN + AGGREGATE] Revenue earned per test category (paid only)
SELECT t.category, SUM(pay.amount) AS revenue
FROM payments pay
JOIN bookings b       ON pay.booking_id = b.booking_id
JOIN booking_tests bt ON b.booking_id   = bt.booking_id
JOIN tests t          ON bt.test_id    = t.test_id
WHERE pay.payment_status = 'Paid'
GROUP BY t.category
ORDER BY revenue DESC;

-- Q5 [NESTED QUERY] Premium patients with no booking in the last 90 days
--    (candidates for a "we miss you" re-engagement campaign)
SELECT full_name, phone
FROM patients
WHERE membership_tier = 'Premium'
  AND patient_id NOT IN (
        SELECT patient_id FROM bookings
        WHERE booking_date >= CURRENT_DATE - INTERVAL '90 days'
  );

-- Q6 [AGGREGATE + LIMIT] Top 5 most-booked tests overall
SELECT t.test_name, COUNT(*) AS times_booked
FROM booking_tests bt
JOIN tests t ON bt.test_id = t.test_id
GROUP BY t.test_name
ORDER BY times_booked DESC
LIMIT 5;

-- Q7 [JOIN + AGGREGATE] Average turnaround (days) from booking to report, by category
SELECT t.category,
       ROUND(AVG(r.report_date - b.booking_date), 1) AS avg_days_to_report
FROM reports r
JOIN bookings b ON r.booking_id = b.booking_id
JOIN tests t    ON r.test_id    = t.test_id
WHERE r.report_date IS NOT NULL
GROUP BY t.category
ORDER BY avg_days_to_report;

-- Q8 [JOIN + AGGREGATE + date filter] Staff workload this calendar month
SELECT s.full_name, s.role, COUNT(b.booking_id) AS bookings_this_month
FROM staff s
JOIN bookings b ON s.staff_id = b.assigned_staff
WHERE date_trunc('month', b.booking_date) = date_trunc('month', CURRENT_DATE)
GROUP BY s.full_name, s.role
ORDER BY bookings_this_month DESC;

-- Q9 [NESTED QUERY] Patients with a pending payment right now
SELECT DISTINCT p.full_name, p.phone
FROM patients p
WHERE p.patient_id IN (
        SELECT b.patient_id
        FROM bookings b
        JOIN payments pay ON b.booking_id = pay.booking_id
        WHERE pay.payment_status = 'Pending'
);

-- Q10 [AGGREGATE, time series] Monthly revenue trend (paid bookings only)
SELECT to_char(payment_date, 'YYYY-MM') AS month, SUM(amount) AS revenue
FROM payments
WHERE payment_status = 'Paid'
GROUP BY month
ORDER BY month;
