import {
  Activity,
  AlertTriangle,
  Bed,
  Bot,
  Boxes,
  HeartPulse,
  Hospital,
  Pill,
  ShieldCheck,
  Stethoscope,
  TestTube2,
  Truck,
  Users,
} from "lucide-react"

export const metrics = [
  {
    title: "Patients today",
    value: "1,248",
    change: "+12% vs yesterday",
    icon: HeartPulse,
  },
  {
    title: "Beds at risk",
    value: "18",
    change: "4 centres above 90%",
    icon: Bed,
  },
  {
    title: "Stock risks",
    value: "7 SKUs",
    change: "2 predicted stock-outs",
    icon: Pill,
  },
  {
    title: "Readiness",
    value: "86/100",
    change: "District average",
    icon: ShieldCheck,
  },
]

export const alerts = [
  {
    title: "Paracetamol shortage at PHC-12",
    detail: "Predicted stock-out in 2 days. Transfer 300 tablets from PHC-8.",
    severity: "High",
    type: "Medicine",
  },
  {
    title: "Doctor shortage at CHC-4",
    detail:
      "Evening shift coverage drops below threshold against forecast load.",
    severity: "Medium",
    type: "Staffing",
  },
  {
    title: "Dengue spike in eastern corridor",
    detail:
      "Case registrations are 2.4x above seasonal baseline across 3 PHCs.",
    severity: "High",
    type: "Disease",
  },
  {
    title: "CBC analyzer maintenance due",
    detail: "District Hospital lab has high utilization and overdue servicing.",
    severity: "Medium",
    type: "Equipment",
  },
]

export const hospitals = [
  {
    name: "PHC-12",
    type: "PHC",
    status: "Critical",
    occupancy: 92,
    readiness: 71,
    patients: 186,
    doctors: "3/5",
  },
  {
    name: "CHC-4",
    type: "CHC",
    status: "Watch",
    occupancy: 81,
    readiness: 84,
    patients: 312,
    doctors: "8/11",
  },
  {
    name: "District Hospital",
    type: "District",
    status: "Stable",
    occupancy: 63,
    readiness: 94,
    patients: 514,
    doctors: "24/26",
  },
  {
    name: "PHC-8",
    type: "PHC",
    status: "Surplus",
    occupancy: 48,
    readiness: 91,
    patients: 94,
    doctors: "4/4",
  },
]

export const inventory = [
  {
    item: "Paracetamol 500mg",
    group: "Painkiller",
    stock: 420,
    daysLeft: 2,
    risk: "High",
    hospital: "PHC-12",
  },
  {
    item: "ORS sachets",
    group: "Rehydration",
    stock: 1240,
    daysLeft: 14,
    risk: "Low",
    hospital: "PHC-8",
  },
  {
    item: "Insulin",
    group: "Diabetes",
    stock: 84,
    daysLeft: 4,
    risk: "High",
    hospital: "CHC-4",
  },
  {
    item: "CBC kits",
    group: "Diagnostics",
    stock: 32,
    daysLeft: 6,
    risk: "Medium",
    hospital: "District Hospital",
  },
]

export const recommendations = [
  {
    action: "Transfer 300 Paracetamol tablets",
    from: "PHC-8",
    to: "PHC-12",
    reason: "PHC-12 will stock out in 2 days while PHC-8 has 14-day surplus.",
    icon: Truck,
  },
  {
    action: "Add one general physician to CHC-4 evening shift",
    from: "District Hospital roster",
    to: "CHC-4",
    reason: "Expected OPD load exceeds safe consultation capacity by 22%.",
    icon: Stethoscope,
  },
  {
    action: "Pre-position dengue diagnostics",
    from: "District lab",
    to: "Eastern PHC cluster",
    reason: "Detected spike requires CBC and platelet test readiness.",
    icon: TestTube2,
  },
]

export const modules = [
  {
    label: "Patients",
    value: "Registrations, severity and admissions",
    icon: Users,
  },
  {
    label: "Hospitals",
    value: "Beds, doctors, labs and readiness",
    icon: Hospital,
  },
  {
    label: "Inventory",
    value: "Stock, expiry, suppliers and transfers",
    icon: Boxes,
  },
  {
    label: "Forecasting",
    value: "Footfall, stock-outs and occupancy",
    icon: Activity,
  },
  {
    label: "Alerts",
    value: "Threshold and prediction-based risks",
    icon: AlertTriangle,
  },
  {
    label: "AI assistant",
    value: "Plain-language explanations and actions",
    icon: Bot,
  },
]
