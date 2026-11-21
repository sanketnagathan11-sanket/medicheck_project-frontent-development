// ═══════════════════════════════════════════════════════════════
//  DATA STORE — persisted to localStorage
// ═══════════════════════════════════════════════════════════════
const DEFAULT_TESTS = [
  {test_id:1,test_name:'Complete Blood Count (CBC)',category:'Blood & Sugar',sample_type:'Blood',price:350,report_time_hrs:6},
  {test_id:2,test_name:'Fasting Blood Sugar',category:'Blood & Sugar',sample_type:'Blood',price:150,report_time_hrs:4},
  {test_id:3,test_name:'HbA1c',category:'Blood & Sugar',sample_type:'Blood',price:500,report_time_hrs:12},
  {test_id:4,test_name:'Lipid Profile',category:'Cardiac',sample_type:'Blood',price:600,report_time_hrs:12},
  {test_id:5,test_name:'ECG',category:'Cardiac',sample_type:'N/A',price:400,report_time_hrs:2},
  {test_id:6,test_name:'Troponin-I',category:'Cardiac',sample_type:'Blood',price:900,report_time_hrs:6},
  {test_id:7,test_name:'Thyroid Profile (T3 T4 TSH)',category:'Thyroid',sample_type:'Blood',price:700,report_time_hrs:24},
  {test_id:8,test_name:'Liver Function Test (LFT)',category:'Liver & Kidney',sample_type:'Blood',price:650,report_time_hrs:12},
  {test_id:9,test_name:'Kidney Function Test (KFT)',category:'Liver & Kidney',sample_type:'Blood',price:650,report_time_hrs:12},
  {test_id:10,test_name:'Urine Routine',category:'Liver & Kidney',sample_type:'Urine',price:200,report_time_hrs:6},
  {test_id:11,test_name:'Chest X-Ray',category:'Imaging',sample_type:'N/A',price:500,report_time_hrs:4},
  {test_id:12,test_name:'Abdominal Ultrasound',category:'Imaging',sample_type:'N/A',price:1200,report_time_hrs:8},
  {test_id:13,test_name:'Vitamin D',category:'Full Body Checkup',sample_type:'Blood',price:1400,report_time_hrs:24},
  {test_id:14,test_name:'Vitamin B12',category:'Full Body Checkup',sample_type:'Blood',price:900,report_time_hrs:24},
  {test_id:15,test_name:'COVID-19 RT-PCR',category:'Full Body Checkup',sample_type:'Swab',price:700,report_time_hrs:24}
];
const DEFAULT_PACKAGES = [
  {package_id:1,package_name:'Basic Health Checkup',description:'CBC + Sugar + Urine Routine',price:550,tier:'Mass',test_ids:[1,2,10]},
  {package_id:2,package_name:'Diabetes Care Package',description:'Sugar + HbA1c + KFT',price:1100,tier:'Mass',test_ids:[2,3,9]},
  {package_id:3,package_name:'Executive Full Body Checkup',description:'15-parameter premium panel',price:3999,tier:'Premium',test_ids:[1,3,4,7,8,9,13,14]},
  {package_id:4,package_name:'Cardiac Risk Package',description:'Lipid + ECG + Troponin-I',price:1800,tier:'Premium',test_ids:[4,5,6]}
];
const DEFAULT_STAFF = [
  {staff_id:1,full_name:'Diya Deshmukh',role:'Technician'},
  {staff_id:2,full_name:'Karan Reddy',role:'Technician'},
  {staff_id:3,full_name:'Rohan Shah',role:'Technician'},
  {staff_id:4,full_name:'Pranav Verma',role:'Receptionist'},
  {staff_id:5,full_name:'Aditi Verma',role:'Courier'},
  {staff_id:6,full_name:'Ritu Patil',role:'Admin'}
];
const SEED_PATIENTS = [
  {patient_id:1,full_name:'Nikhil Patil',dob:'1956-12-09',gender:'Male',phone:'9339670711',email:'nikhil.patil1@example.com',membership_tier:'Premium'},
  {patient_id:2,full_name:'Anjali Gokhale',dob:'1989-02-19',gender:'Female',phone:'9134126396',email:'anjali.gokhale2@example.com',membership_tier:'Premium'},
  {patient_id:3,full_name:'Isha Reddy',dob:'1993-01-18',gender:'Male',phone:'9868820204',email:'isha.reddy3@example.com',membership_tier:'Mass'},
  {patient_id:4,full_name:'Neha Deshmukh',dob:'1983-10-09',gender:'Male',phone:'9914763202',email:'neha.deshmukh4@example.com',membership_tier:'Mass'},
  {patient_id:5,full_name:'Neha Kumar',dob:'1972-03-07',gender:'Female',phone:'9209747451',email:'neha.kumar5@example.com',membership_tier:'Premium'},
];
const SEED_BOOKINGS = [
  {booking_id:1,patient_id:1,booking_type:'Walk-in',booking_date:'2026-01-03',slot_time:'11:00',status:'Report Ready',total_amount:1500,test_ids:[4,14],payment_status:'Paid',payment_mode:'Online'},
  {booking_id:2,patient_id:2,booking_type:'Walk-in',booking_date:'2026-01-10',slot_time:'14:00',status:'Report Ready',total_amount:2350,test_ids:[11,12,8],payment_status:'Paid',payment_mode:'UPI'},
  {booking_id:3,patient_id:3,booking_type:'Walk-in',booking_date:'2026-01-02',slot_time:'08:00',status:'Report Ready',total_amount:1500,test_ids:[3,1,9],payment_status:'Paid',payment_mode:'Online'},
  {booking_id:4,patient_id:4,booking_type:'Home Collection',booking_date:'2026-01-08',slot_time:'17:00',status:'Sample Collected',total_amount:700,test_ids:[7],payment_status:'Pending',payment_mode:'Cash'},
  {booking_id:5,patient_id:5,booking_type:'Walk-in',booking_date:'2026-01-07',slot_time:'18:00',status:'Scheduled',total_amount:1200,test_ids:[7,3],payment_status:'Paid',payment_mode:'Card'},
];

function ls(key){ return JSON.parse(localStorage.getItem('mc_'+key)||'null') }
function lsSet(key,val){ localStorage.setItem('mc_'+key, JSON.stringify(val)) }

function initData(){
  if(!ls('patients')){ lsSet('patients', SEED_PATIENTS) }
  if(!ls('bookings')){ lsSet('bookings', SEED_BOOKINGS) }
  if(!ls('tests')){ lsSet('tests', DEFAULT_TESTS) }
  if(!ls('packages')){ lsSet('packages', DEFAULT_PACKAGES) }
  if(!ls('staff')){ lsSet('staff', DEFAULT_STAFF) }
}
initData();

function getTests(){ return ls('tests')||[] }
function getPackages(){ return ls('packages')||[] }
function getPatients(){ return ls('patients')||[] }
function getBookings(){ return ls('bookings')||[] }
function getStaff(){ return ls('staff')||[] }

let nextPatientId = () => Math.max(0,...getPatients().map(p=>p.patient_id))+1;
let nextBookingId = () => Math.max(0,...getBookings().map(b=>b.booking_id))+1;

function getTestsByIds(ids){ return getTests().filter(t=>ids.includes(t.test_id)) }
function testNames(ids){ return getTestsByIds(ids).map(t=>t.test_name).join(', ') }
