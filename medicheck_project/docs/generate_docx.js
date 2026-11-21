const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType,
  ImageRun, LevelFormat, PageBreak, VerticalAlign
} = require("docx");

const PINE = "1F4D42";
const MARIGOLD = "D99A34";
const INK = "14231F";
const TABLE_W = 9026; // A4 minus 1in margins, in DXA

const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const thinBorder = { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" };
const cellBorders = { top: thinBorder, bottom: thinBorder, left: thinBorder, right: thinBorder };

function h1(text) {
  return new Paragraph({ text, heading: HeadingLevel.HEADING_1, spacing: { before: 300, after: 150 } });
}
function h2(text) {
  return new Paragraph({ text, heading: HeadingLevel.HEADING_2, spacing: { before: 250, after: 120 } });
}
function body(text, opts = {}) {
  return new Paragraph({ children: [new TextRun({ text, ...opts })], spacing: { after: 120 } });
}
function bullet(text) {
  return new Paragraph({ text, numbering: { reference: "bullet-list", level: 0 }, spacing: { after: 60 } });
}
function labelValue(label, value) {
  return new Paragraph({
    children: [
      new TextRun({ text: label + ": ", bold: true, color: PINE }),
      new TextRun({ text: value }),
    ],
    spacing: { after: 100 },
  });
}

function headerCell(text, width) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, color: "auto", fill: PINE },
    verticalAlign: VerticalAlign.CENTER,
    borders: cellBorders,
    children: [new Paragraph({ children: [new TextRun({ text, bold: true, color: "FFFFFF", size: 20 })] })],
  });
}
function dataCell(text, width) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    verticalAlign: VerticalAlign.CENTER,
    borders: cellBorders,
    children: [new Paragraph({ children: [new TextRun({ text: String(text), size: 20 })] })],
  });
}
function makeTable(headers, widths, rows) {
  return new Table({
    width: { size: TABLE_W, type: WidthType.DXA },
    columnWidths: widths,
    rows: [
      new TableRow({ tableHeader: true, children: headers.map((h, i) => headerCell(h, widths[i])) }),
      ...rows.map(r => new TableRow({ children: r.map((c, i) => dataCell(c, widths[i])) })),
    ],
  });
}

function image(path, width, height) {
  const data = fs.readFileSync(path);
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 200 },
    children: [new ImageRun({ data, type: "png", transformation: { width, height } })],
  });
}

// ---------------------------------------------------------------
// Content
// ---------------------------------------------------------------

const entities = [
  ["Patients", "patient_id (PK), full_name, dob, gender, phone (unique), email (unique), address, membership_tier, registered_on"],
  ["Staff", "staff_id (PK), full_name, role, phone, email"],
  ["Tests", "test_id (PK), test_name, category, sample_type, price, report_time_hrs"],
  ["Packages", "package_id (PK), package_name, description, price, tier"],
  ["Package_Tests (bridge)", "package_id (FK), test_id (FK)"],
  ["Bookings", "booking_id (PK), patient_id (FK), booking_type, booking_date, slot_time, status, assigned_staff (FK), total_amount"],
  ["Booking_Tests (bridge)", "booking_id (FK), test_id (FK)"],
  ["Reports", "report_id (PK), booking_id (FK), test_id (FK), result_status, report_date"],
  ["Payments", "payment_id (PK), booking_id (FK), amount, payment_mode, payment_status, payment_date"],
];

const relationships = [
  ["1", "Patients", "1 : M  makes", "Bookings"],
  ["2", "Staff", "1 : M  assigned to", "Bookings"],
  ["3", "Bookings", "1 : M  includes", "Booking_Tests"],
  ["4", "Tests", "1 : M  appears in", "Booking_Tests"],
  ["5", "Packages", "1 : M  bundles", "Package_Tests"],
  ["6", "Tests", "1 : M  included in", "Package_Tests"],
  ["7", "Bookings", "1 : M  generates", "Reports"],
  ["8", "Tests", "1 : M  result for", "Reports"],
  ["9", "Bookings", "1 : M  paid via", "Payments"],
];

const tableDefs = [
  ["1. patients", [
    ["patient_id", "SERIAL", "Primary key"],
    ["full_name", "VARCHAR(100)", "NOT NULL"],
    ["dob", "DATE", "NOT NULL"],
    ["gender", "VARCHAR(10)", "CHECK IN (Male, Female, Other)"],
    ["phone", "VARCHAR(15)", "NOT NULL, UNIQUE"],
    ["email", "VARCHAR(100)", "UNIQUE"],
    ["address", "TEXT", "Nullable"],
    ["membership_tier", "VARCHAR(10)", "CHECK IN (Mass, Premium), default Mass"],
    ["registered_on", "DATE", "default CURRENT_DATE"],
  ]],
  ["2. staff", [
    ["staff_id", "SERIAL", "Primary key"],
    ["full_name", "VARCHAR(100)", "NOT NULL"],
    ["role", "VARCHAR(20)", "CHECK IN (Technician, Receptionist, Courier, Admin)"],
    ["phone", "VARCHAR(15)", "NOT NULL"],
    ["email", "VARCHAR(100)", "UNIQUE"],
  ]],
  ["3. tests", [
    ["test_id", "SERIAL", "Primary key"],
    ["test_name", "VARCHAR(100)", "NOT NULL"],
    ["category", "VARCHAR(50)", "NOT NULL"],
    ["sample_type", "VARCHAR(30)", "NOT NULL"],
    ["price", "DECIMAL(8,2)", "CHECK price >= 0"],
    ["report_time_hrs", "INT", "default 24"],
  ]],
  ["4. packages", [
    ["package_id", "SERIAL", "Primary key"],
    ["package_name", "VARCHAR(100)", "NOT NULL"],
    ["description", "TEXT", "Nullable"],
    ["price", "DECIMAL(8,2)", "CHECK price >= 0"],
    ["tier", "VARCHAR(10)", "CHECK IN (Mass, Premium)"],
  ]],
  ["5. package_tests (bridge)", [
    ["package_id", "INT", "FK -> packages, part of composite PK"],
    ["test_id", "INT", "FK -> tests, part of composite PK"],
  ]],
  ["6. bookings", [
    ["booking_id", "SERIAL", "Primary key"],
    ["patient_id", "INT", "FK -> patients, NOT NULL"],
    ["booking_type", "VARCHAR(20)", "CHECK IN (Walk-in, Home Collection)"],
    ["booking_date", "DATE", "default CURRENT_DATE"],
    ["slot_time", "TIME", "NOT NULL"],
    ["status", "VARCHAR(20)", "CHECK IN (Scheduled, Sample Collected, Report Ready, Cancelled)"],
    ["assigned_staff", "INT", "FK -> staff, nullable"],
    ["total_amount", "DECIMAL(8,2)", "default 0"],
  ]],
  ["7. booking_tests (bridge)", [
    ["booking_id", "INT", "FK -> bookings, part of composite PK"],
    ["test_id", "INT", "FK -> tests, part of composite PK"],
  ]],
  ["8. reports", [
    ["report_id", "SERIAL", "Primary key"],
    ["booking_id", "INT", "FK -> bookings, NOT NULL"],
    ["test_id", "INT", "FK -> tests, NOT NULL"],
    ["result_status", "VARCHAR(15)", "CHECK IN (Normal, Abnormal, Pending)"],
    ["report_date", "DATE", "Nullable until ready"],
  ]],
  ["9. payments", [
    ["payment_id", "SERIAL", "Primary key"],
    ["booking_id", "INT", "FK -> bookings, NOT NULL"],
    ["amount", "DECIMAL(8,2)", "NOT NULL"],
    ["payment_mode", "VARCHAR(20)", "CHECK IN (Cash, UPI, Card, Online)"],
    ["payment_status", "VARCHAR(15)", "CHECK IN (Pending, Paid, Refunded)"],
  ]],
];

const websitePages = [
  ["Home (/)", "Landing page introducing MediCheck, showing live counts of patients/tests/bookings, and explaining the Mass vs Premium tiers."],
  ["Tests & Packages (/tests)", "Lists all tests with category filter chips, and bundled packages with pricing."],
  ["Book a Test (/book)", "Booking form: patient details, tier, booking type, slot time, and a checklist of tests. Writes to patients, bookings, booking_tests, and payments on submit."],
  ["My Bookings (/my-bookings)", "Patient looks up booking history and live status using their phone number."],
  ["Staff Dashboard (/admin)", "Shows today's bookings with an inline status-update control, plus a staff workload summary for the month."],
  ["Contact (/contact)", "Static lab information and about section."],
];

const doQuery = [
  "Run schema.sql, then seed_data.sql, on your own PostgreSQL instance and screenshot the actual table output before submission.",
  "Do a quick 15-minute real check (call or visit 1-2 local labs, or check their sites) so the 'existing system' section reflects genuine, if small-scale, field research.",
  "Be ready to explain every table and every query in your viva -- examiners often ask you to modify a query live.",
  "Personalise the branding, colours, or lab name if you want the project to feel distinctly yours.",
];
const avoidList = [
  "Don't submit without running the project once yourself end-to-end -- a screenshot of an error looks worse than a late submission.",
  "Don't memorise queries without understanding joins vs. nested subqueries vs. aggregates -- that's exactly what gets probed in viva.",
  "Don't skip drawing/exporting the ER diagram separately just because schema.sql exists -- it is graded on its own.",
  "Don't claim field-visit research you didn't do -- be ready to describe it if asked.",
];

const introText = "Most diagnostic laboratories serving Indian neighbourhoods still operate on a walk-in, first-come-first-served basis, with results communicated by phone call or a printed slip collected in person. As diagnostic testing volumes grow -- driven by rising lifestyle-disease screening (diabetes, thyroid, cardiac risk) and greater post-pandemic health awareness -- this manual model creates avoidable waiting time, scheduling conflicts, and leaves no digital record for patients who test regularly. MediCheck is a database-backed booking and management system for a diagnostic lab. It lets patients browse tests and packages, book a slot online -- either a standard walk-in slot or a Premium home sample collection -- track booking status, and (in a full deployment) download reports digitally. It also gives lab staff a dashboard to manage the day's bookings, assign technicians, and track workload.";

const objectives = [
  "Design a normalized relational database (PostgreSQL, 3NF) that stores patients, staff, tests, packages, bookings, reports, and payments without redundancy.",
  "Let patients browse tests/packages and book an appointment online, choosing a Mass walk-in slot or a Premium home-collection slot.",
  "Let patients check booking status and history using their registered phone number.",
  "Give lab staff a dashboard to view the day's bookings, assign staff, and update booking status.",
  "Write functional queries (joins, nested subqueries, aggregate functions) that support real decisions -- revenue tracking, staff workload, patient retention.",
  "Visualize booking and revenue data using Pandas and Matplotlib (line, bar, and pie charts).",
];

const existingSystemText = "Most neighbourhood diagnostic labs use a manual, walk-in-register model. A patient visits the counter, states which test(s) they need, and is added to a handwritten or spreadsheet register. Sample collection happens first-come-first-served. Reports are collected in person 24-48 hours later or read out over a phone call. A few larger chains offer an online enquiry form, but it typically just emails the lab, and a staff member calls back manually to confirm a slot -- there is no real-time booking.";

const drawbacks = [
  "No visibility into current queue length or expected wait time before arriving at the lab.",
  "No self-service way to check whether a report is ready.",
  "Manual registers make it hard to compute accurate monthly revenue or staff workload.",
  "No structured way to price and offer a differentiated service such as home collection.",
  "Risk of transcription errors when handwritten details are later typed up for billing.",
  "No history tied to a patient across visits, making it hard to spot patients who are overdue for a repeat test.",
];

const scopeIn = [
  "Online browsing of tests and bundled packages.",
  "Slot booking for both Walk-in and Home Collection.",
  "Phone-number based booking lookup and status tracking for patients.",
  "A staff dashboard for status updates and monthly workload view.",
  "A normalized PostgreSQL schema with referential integrity.",
  "Functional queries for reporting (joins, nested queries, aggregates).",
  "CSV-based visualization of booking and revenue trends.",
];
const scopeOut = [
  "Live payment gateway integration (payments are recorded, not processed).",
  "SMS / email notifications.",
  "Staff authentication / role-based login (a real deployment would add this).",
  "Integration with actual lab diagnostic instruments.",
];

const endUsers = [
  "Patient -- Mass tier: browses tests, books a walk-in slot, checks status.",
  "Patient -- Premium tier: same, plus home sample collection.",
  "Receptionist: manages walk-in bookings at the counter.",
  "Lab Technician: views assigned bookings, updates sample-collection status.",
  "Courier: views assigned home-collection bookings.",
  "Admin / Lab Manager: views today's bookings, staff workload, and revenue reports.",
];
const inputData = [
  "Patient details: name, DOB, gender, phone, email, address, tier.",
  "Test/package selection for a booking.",
  "Booking type, preferred date, and slot time.",
  "Payment amount and mode.",
  "Staff updates to booking status and report results.",
];
const outputData = [
  "Booking confirmation with a booking ID.",
  "List of selected tests and total amount for a booking.",
  "Booking status and history for a patient (via phone lookup).",
  "Staff dashboard: today's bookings, assigned staff, live status.",
  "Reports: revenue by category, staff workload, top tests, pending payments, monthly revenue trend.",
];

const functionalReqIntro = "The system supports the following functional requirements, each backed by a SQL query in queries.sql (full text and results in that file / your own screenshot after running it):";
const functionalReqs = [
  "View all bookings with patient and payment details -- JOIN (Q1).",
  "View the tests included in one specific booking -- multi-table JOIN (Q2).",
  "Identify frequent/returning patients for loyalty outreach -- GROUP BY + HAVING (Q3).",
  "Track revenue earned per test category -- JOIN + SUM (Q4).",
  "Identify lapsed Premium patients to re-engage -- NESTED QUERY with NOT IN (Q5).",
  "Identify the most popular tests to guide staffing/inventory -- COUNT + LIMIT (Q6).",
  "Monitor average report turnaround time by category -- JOIN + AVG (Q7).",
  "Monitor staff workload for the current month -- JOIN + date filter (Q8).",
  "Identify patients with a pending payment -- NESTED QUERY with IN (Q9).",
  "Track the monthly revenue trend over time -- GROUP BY month (Q10).",
];

// ---------------------------------------------------------------
// Build document
// ---------------------------------------------------------------

const children = [];

// Title block
children.push(
  new Paragraph({ text: "", spacing: { before: 600 } }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text: "MediCheck", bold: true, size: 56, color: PINE })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 100 },
    children: [new TextRun({ text: "Diagnostic Lab & Home Sample Collection Booking System", size: 28, color: MARIGOLD })],
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 500 },
    children: [new TextRun({ text: "Field Project-I Documentation  |  24CsDscU3002", size: 22, italics: true })],
  }),
);

children.push(h1("1. Introduction and Objectives"));
children.push(h2("Introduction"));
children.push(body(introText));
children.push(h2("Objectives"));
objectives.forEach(o => children.push(bullet(o)));

children.push(h2("Study of Existing System"));
children.push(body(existingSystemText));
children.push(h2("Drawbacks of Existing System"));
drawbacks.forEach(d => children.push(bullet(d)));
children.push(h2("Scope of the Proposed System"));
children.push(body("In scope:", { bold: true }));
scopeIn.forEach(s => children.push(bullet(s)));
children.push(body("Out of scope for this project phase:", { bold: true }));
scopeOut.forEach(s => children.push(bullet(s)));

children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("2. Requirement Gathering, ER Diagram, Normalized Database Design"));
children.push(h2("End Users of the System"));
endUsers.forEach(e => children.push(bullet(e)));
children.push(h2("Input Data to the System"));
inputData.forEach(e => children.push(bullet(e)));
children.push(h2("Output Information from the System"));
outputData.forEach(e => children.push(bullet(e)));

children.push(h2("Entities and Attributes"));
children.push(makeTable(
  ["Entity", "Attributes"], [2400, 6626],
  entities
));

children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h2("Entity Relationship Diagram"));
children.push(image("/home/claude/medicheck/diagrams/er_diagram.png", 560, 330));
children.push(body("(Editable source also provided as er_diagram.mmd / er_diagram.dot -- open in mermaid.live or a Graphviz viewer if you want to restyle it, or redraw in draw.io / Lucidchart if your department prefers a specific tool.)", { italics: true, size: 18 }));

children.push(h2("Normalized Database Design -- Table Relationships"));
children.push(makeTable(
  ["#", "Table 1", "Relationship", "Table 2"], [700, 2600, 3200, 2526],
  relationships
));

children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h2("Table Definitions (9 tables, 3NF)"));
children.push(body("Package_Tests and Booking_Tests are bridge (junction) tables. They exist because a package can contain many tests and a test can appear in many packages (and likewise for bookings) -- a direct many-to-many relationship can't be stored in a single table without repeating groups, so it's split into two 1:M relationships through a bridge table. This is the normalization step examiners most often ask students to justify.", { italics: true }));
tableDefs.forEach(([name, fields]) => {
  children.push(new Paragraph({ text: name, heading: HeadingLevel.HEADING_3, spacing: { before: 200, after: 80 } }));
  children.push(makeTable(["Field name", "Data type", "Description / Constraint"], [2200, 1800, 5026], fields));
});

children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("3. Functional Requirements"));
children.push(body(functionalReqIntro));
functionalReqs.forEach(f => children.push(bullet(f)));

children.push(h1("4. Website"));
children.push(body("Built with Flask (Python) + PostgreSQL (via psycopg2), server-rendered with Jinja2 templates. Minimum of 5 pages required -- 6 provided:"));
children.push(makeTable(["Page", "Purpose"], [2600, 6426], websitePages));
children.push(body("Insert your own screenshots here after running the app locally (python3 app.py, then visit http://localhost:5000).", { italics: true, color: MARIGOLD }));

children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("5. Data Visualization"));
children.push(body("bookings_data.csv summarizes bookings by Month, Category, and Tier, with columns: Month, Category, Tier, Bookings, Revenue. It was generated from the same underlying data used to seed the database, so the charts below are consistent with what queries.sql would return."));
children.push(h2("Line Chart -- Monthly Revenue Trend"));
children.push(image("/home/claude/medicheck/visualization/charts_line_revenue_trend.png", 480, 300));
children.push(h2("Bar Chart -- Bookings by Test Category"));
children.push(image("/home/claude/medicheck/visualization/charts_bar_category_bookings.png", 480, 300));
children.push(h2("Pie Chart -- Mass vs Premium Booking Share"));
children.push(image("/home/claude/medicheck/visualization/charts_pie_tier_share.png", 400, 400));

children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1("Guide's Notes -- Do / Avoid"));
children.push(h2("Do"));
doQuery.forEach(d => children.push(bullet(d)));
children.push(h2("Avoid"));
avoidList.forEach(a => children.push(bullet(a)));

const doc = new Document({
  numbering: {
    config: [{
      reference: "bullet-list",
      levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 450, hanging: 260 } } } }],
    }],
  },
  styles: {
    default: {
      document: { run: { font: "Calibri", size: 22 } },
      heading1: { run: { color: PINE, size: 32, bold: true }, paragraph: { spacing: { before: 300, after: 150 } } },
      heading2: { run: { color: MARIGOLD, size: 26, bold: true } },
      heading3: { run: { color: INK, size: 23, bold: true } },
    },
  },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("MediCheck_Project_Documentation.docx", buf);
  console.log("Written: MediCheck_Project_Documentation.docx");
});
