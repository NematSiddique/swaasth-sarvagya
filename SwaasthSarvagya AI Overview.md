# SwaasthSarvagya AI

## AI-Driven Health Center & Supply Chain Management Platform

### Hackathon

**Hack2Skill - Build with AI: Code for Communities**

**Track 3 - Smart Health**

# 1\. Problem Statement

Primary Health Centres (PHCs) and Community Health Centres (CHCs) often operate with fragmented and manually maintained data. Medicine inventory, doctor attendance, patient registrations, bed occupancy, laboratory availability, and equipment status are usually tracked independently, resulting in:

- Medicine stock-outs
- Overcrowded health centres
- Under-utilized neighbouring hospitals
- Lack of real-time district visibility
- Delayed interventions
- Inefficient resource allocation

District administrators are forced to react after problems occur instead of preventing them.

# 2\. Vision

Develop an AI-powered District Health Intelligence Platform that continuously monitors healthcare operations across all PHCs and CHCs and proactively recommends interventions before shortages or operational failures occur.

The platform serves as a centralized command center for district healthcare administrators while remaining simple enough for hospital staff to use daily.

# 3\. Objectives

- Digitize operational health center data
- Forecast medicine demand and shortages
- Predict patient footfall and bed occupancy
- Monitor doctor attendance and staffing
- Detect disease outbreaks early
- Recommend inter-hospital resource redistribution
- Provide multilingual AI assistance
- Generate explainable recommendations instead of raw dashboards

# 4\. System Architecture

Patients  
Doctors  
Nurses  
Inventory  
Laboratories  
Beds  
Equipment  
Attendance  
Weather  
Government Datasets  
<br/>│  
▼  
<br/>PostgreSQL  
(Single Source of Truth)  
<br/>│  
▼  
<br/>Analytics & AI Layer  
<br/>• Forecasting  
• Classification  
• Optimization  
• Alert Engine  
<br/>│  
▼  
<br/>Recommendations Database  
<br/>│  
▼  
<br/>Gemini AI Assistant  
<br/>│  
▼  
<br/>Dashboard  
Mobile App  
Voice Assistant  
District Command Center

# 5\. Core Modules

## Module 1: Patient Registration

Stores complete patient encounter information.

### Data Captured

- Patient ID
- Hospital
- Registration Time
- Age
- Gender
- Disease
- Severity
- Assigned Doctor
- Bed Requirement
- Laboratory Tests
- Medicines Prescribed
- Discharge Status

### AI Capabilities

- Disease classification
- Admission prediction
- Patient summary generation
- Resource requirement estimation

## Module 2: Hospital Management

Tracks operational health of every PHC/CHC.

### Static Information

- Hospital ID
- Type
- Location
- Departments
- Capacity

### Live Information

- Available beds
- Occupied beds
- Doctor availability
- Patient count
- Medicine inventory
- Laboratory status

### Historical Information

- Daily OPD
- Daily admissions
- Medicine consumption
- Bed occupancy trends
- Disease statistics

## Module 3: Medicine Inventory

Maintains district-wide medicine availability.

### Stores

- Medicine
- Generic Name
- Brand Name
- Quantity
- Expiry Date
- Supplier
- Reorder Threshold
- Hospital

Supports medicine substitutions through generic mapping.

Example:

Generic:

- Paracetamol

Brands:

- Dolo
- Crocin
- Calpol

## Module 4: Doctor & Nurse Management

Tracks workforce availability.

Stores

- Specialization
- Shift
- Assigned Hospital
- Attendance
- Leave Status
- Consultation Count

AI predicts staffing shortages before they occur.

## Module 5: Disease Intelligence

Stores healthcare knowledge.

For every disease:

- Required medicines
- Required laboratory tests
- Specialist required
- Seasonal trends
- Weather correlation
- Demographic risk
- Historical prevalence

Example

Dengue

Requires:

- Paracetamol
- ORS
- CBC
- Platelet Count

Season:

- Monsoon

## Module 6: Laboratory Management

Tracks

Equipment

- X-Ray
- CBC Analyzer
- ECG
- Ultrasound

Consumables

- Test Kits
- Reagents
- Chemicals

AI predicts both kit shortages and equipment failures.

## Module 7: Bed Management

Tracks

- Total Beds
- Occupied Beds
- Available Beds
- ICU Beds
- Isolation Beds

Forecasts future occupancy.

## Module 8: Supplier Management

Stores

- Supplier
- Medicines Supplied
- Delivery Time
- Reliability
- Active Orders

Supports procurement recommendations.

# 6\. Event Driven Workflow

Every patient registration updates multiple components.

Patient Registration  
<br/>↓  
<br/>Patient Table  
<br/>↓  
<br/>Medicine Inventory  
<br/>↓  
<br/>Bed Occupancy  
<br/>↓  
<br/>Disease Statistics  
<br/>↓  
<br/>Doctor Workload  
<br/>↓  
<br/>Forecast Engine  
<br/>↓  
<br/>Alert Engine  
<br/>↓  
<br/>Recommendations  
<br/>↓  
<br/>Gemini Summary

No manual reporting is required.

# 7\. AI Features

## 7.1 Medicine Stock Forecast

Predicts future medicine consumption.

Inputs

- Historical usage
- Disease trends
- Weather
- Season
- Festivals
- Population

Output

- Expected demand
- Stock depletion date
- Reorder quantity

Model

- Prophet
- XGBoost

## 7.2 Patient Footfall Forecast

Predicts OPD demand.

Inputs

- Historical registrations
- Disease prevalence
- Weather
- Holidays

Output

Expected patient count for future days.

Model

- Prophet

## 7.3 Bed Occupancy Forecast

Predicts

- Admissions
- Discharges
- Occupancy

Model

- Prophet

## 7.4 Doctor Shortage Prediction

Predicts staffing shortages using

- Attendance history
- Leave records
- Expected patient load

Model

- LightGBM

## 7.5 Disease Outbreak Detection

Detects unusual increases in diseases.

Inputs

- Patient registrations
- Locations
- Historical trends

Models

- DBSCAN
- CUSUM

Output

Potential outbreak alerts.

## 7.6 Equipment Failure Prediction

Predicts equipment maintenance requirements.

Inputs

- Usage frequency
- Maintenance history
- Machine age

Model

- Random Forest

## 7.7 Smart Redistribution

Suggests transferring medicines between hospitals.

Inputs

- Current inventory
- Demand forecast
- Distance
- Transport cost

Algorithm

- Google OR-Tools

## 7.8 Hospital Health Score

Scores each hospital using

- Inventory
- Beds
- Attendance
- Laboratory readiness
- Patient load

Output

Hospital Readiness Score (0-100)

## 7.9 Gemini AI Assistant

Supports natural language queries.

Examples

- Which hospitals require intervention today?
- Which medicines will run out this week?
- Why is PHC-12 marked critical?
- Show hospitals affected by dengue.

Gemini converts structured analytics into actionable recommendations.

# 8\. Alert Engine

Alerts are generated from model predictions and predefined thresholds.

## Medicine Alerts

- Stock below threshold
- Predicted stock-out within 3 days
- Expiring medicines

## Hospital Alerts

- Bed occupancy >90%
- Doctor shortage
- Laboratory unavailable

## Disease Alerts

- Outbreak detected
- Rapid case increase

## Equipment Alerts

- Machine failure risk
- Maintenance overdue

## Administrative Alerts

- Underperforming health centre
- Referral required
- Resource redistribution recommendation

# 9\. Recommendation Engine

Instead of only identifying problems, the platform recommends solutions.

Example

Problem

Paracetamol shortage at PHC-12

Recommendation

Transfer 300 tablets from PHC-8.

Reason

- Predicted stock-out in 2 days
- PHC-8 has 14-day surplus
- Distance 9 km

# 10\. Data Sources

Government

- data.gov.in
- HMIS
- National Health Mission
- Census
- NFHS
- IMD Weather Data

Generated

- Patient registrations
- Inventory events
- Attendance records
- Disease simulations

External APIs

- Google Maps Platform
- IMD Weather
- Gemini API

# 11\. Technology Stack

## Frontend

- React
- Next.js
- Tailwind CSS

## Backend

- FastAPI

## Database

- PostgreSQL

## AI

- Gemini API
- Prophet
- XGBoost
- LightGBM
- Random Forest
- DBSCAN
- Google OR-Tools

## Deployment

- Docker
- Cloud Run

# 12\. Why PostgreSQL?

PostgreSQL acts as the single source of truth.

Advantages

- ACID transactions
- Reliable inventory updates
- Easy analytics
- Time-series support
- JSON support
- Simple deployment
- Faster hackathon development

Future versions may introduce Neo4j as a knowledge graph for explainable reasoning and complex relationship traversal.

# 13\. End-to-End Workflow Example

- Patient registers with dengue.
- Registration is stored in PostgreSQL.
- Bed occupancy increases.
- Medicine inventory decreases.
- Disease statistics are updated.
- Forecasting service predicts medicine demand.
- Alert engine detects a possible stock-out.
- Optimization engine identifies a nearby hospital with surplus inventory.
- Gemini generates a human-readable recommendation.
- District administrator receives the alert and recommendation through the dashboard.

# 14\. Future Enhancements

- Neo4j knowledge graph
- Digital twin of district healthcare
- Drone medicine delivery planning
- Ambulance routing optimization
- Citizen mobile application
- Offline-first synchronization
- IoT-enabled inventory monitoring
- Predictive procurement planning
- Explainable AI dashboards
- State-wide interoperability through ABDM standards

# 15\. Expected Impact

- Reduced medicine stock-outs
- Better utilization of district resources
- Lower patient waiting times
- Early disease outbreak detection
- Improved hospital preparedness
- Data-driven administrative decisions
- Increased healthcare accessibility in underserved regions
- Higher operational efficiency across PHCs and CHCs

The platform transforms reactive healthcare administration into proactive, AI-assisted district health management by combining real-time operational data, predictive analytics, optimization algorithms, and multilingual generative AI into a single intelligent ecosystem.

**16\. PostgreSQL Database Schema**

**Database Overview**

PostgreSQL serves as the **single source of truth** for all operational healthcare data.

The database is normalized to minimize redundancy while supporting analytical queries for forecasting and AI models.

District  
│  
├── Hospitals  
│ │  
│ ├── Doctors  
│ ├── Nurses  
│ ├── Beds  
│ ├── Laboratories  
│ ├── Inventory  
│ └── Patients  
│  
├── Suppliers  
│  
├── Medicines  
│  
├── Diseases  
│  
└── AI Predictions

**Entity Relationship Overview**

District  
│  
▼  
Hospitals  
│  
├────────────┐  
▼ ▼  
Doctors Patients  
│ │  
│ ▼  
│ Diseases  
│ │  
▼ ▼  
Attendance Prescriptions  
│  
▼  
Medicines  
│  
▼  
Inventory  
│  
▼  
Suppliers

**hospitals**

Stores static information about every PHC/CHC.

| **Column** | **Type**                          |
| ---------- | --------------------------------- |
| id         | UUID                              |
| name       | TEXT                              |
| district   | TEXT                              |
| type       | ENUM(PHC, CHC, District Hospital) |
| latitude   | DOUBLE                            |
| longitude  | DOUBLE                            |
| total_beds | INT                               |
| created_at | TIMESTAMP                         |

**patients**

Stores every registration.

| **Column**       | **Type**  |
| ---------------- | --------- |
| id               | UUID      |
| hospital_id      | FK        |
| doctor_id        | FK        |
| disease_id       | FK        |
| age              | INT       |
| gender           | TEXT      |
| severity         | ENUM      |
| bed_required     | BOOLEAN   |
| bed_allocated    | BOOLEAN   |
| admission_status | ENUM      |
| registered_at    | TIMESTAMP |
| discharged_at    | TIMESTAMP |

**diseases**

Master disease table.

| **Column**   | **Type** |
| ------------ | -------- |
| id           | UUID     |
| disease_name | TEXT     |
| category     | TEXT     |
| seasonal     | BOOLEAN  |
| description  | TEXT     |

**medicine_groups**

Generic medicine categories.

Example

Painkiller  
<br/>Antibiotic  
<br/>Antacid  
<br/>Antiviral  
<br/>Vaccine

| **Column** | **Type** |
| ---------- | -------- |
| id         | UUID     |
| group_name | TEXT     |

**medicines**

Medicine master.

| **Column**   | **Type** |
| ------------ | -------- |
| id           | UUID     |
| group_id     | FK       |
| generic_name | TEXT     |
| brand_name   | TEXT     |
| dosage       | TEXT     |

Example

Generic  
<br/>Paracetamol  
<br/>↓  
<br/>Brands  
<br/>Crocin  
<br/>Dolo  
<br/>Calpol

**disease_medicines**

Many-to-many mapping.

Dengue  
<br/>↓  
<br/>Paracetamol  
<br/>↓  
<br/>ORS

| **Column**  | **Type** |
| ----------- | -------- |
| disease_id  | FK       |
| medicine_id | FK       |
| priority    | INT      |

**laboratories**

Each hospital's laboratory.

| **Column**  | **Type** |
| ----------- | -------- |
| id          | UUID     |
| hospital_id | FK       |
| name        | TEXT     |

**lab_equipment**

| **Column**     | **Type** |
| -------------- | -------- |
| id             | UUID     |
| laboratory_id  | FK       |
| equipment_name | TEXT     |
| status         | ENUM     |
| last_service   | DATE     |
| expected_life  | INT      |

**lab_kits**

| **Column**    | **Type** |
| ------------- | -------- |
| id            | UUID     |
| laboratory_id | FK       |
| test_name     | TEXT     |
| stock         | INT      |
| threshold     | INT      |

**doctors**

| **Column**     | **Type** |
| -------------- | -------- |
| id             | UUID     |
| hospital_id    | FK       |
| name           | TEXT     |
| specialization | TEXT     |
| shift          | TEXT     |

**doctor_attendance**

Historical attendance.

| **Column** | **Type** |
| ---------- | -------- |
| doctor_id  | FK       |
| date       | DATE     |
| status     | BOOLEAN  |

**beds**

Tracks live occupancy.

| **Column**  | **Type** |
| ----------- | -------- |
| id          | UUID     |
| hospital_id | FK       |
| bed_type    | TEXT     |
| occupied    | BOOLEAN  |
| patient_id  | FK       |

**inventory**

Current inventory.

| **Column**    | **Type**  |
| ------------- | --------- |
| hospital_id   | FK        |
| medicine_id   | FK        |
| quantity      | INT       |
| expiry_date   | DATE      |
| reorder_level | INT       |
| updated_at    | TIMESTAMP |

**inventory_transactions**

Every inventory movement.

| **Column**       | **Type**                   |
| ---------------- | -------------------------- |
| id               | UUID                       |
| hospital_id      | FK                         |
| medicine_id      | FK                         |
| quantity         | INT                        |
| transaction_type | ISSUE / RECEIVE / TRANSFER |
| timestamp        | TIMESTAMP                  |

This table is extremely useful because forecasting models should learn from **consumption history**, not just current stock.

**suppliers**

| **Column**    | **Type** |
| ------------- | -------- |
| id            | UUID     |
| supplier_name | TEXT     |
| delivery_days | INT      |
| contact       | TEXT     |

**supplier_medicines**

Many-to-many mapping.

Supplier  
<br/>↓  
<br/>Medicines

**patient_tests**

| **Column** | **Type**                      |
| ---------- | ----------------------------- |
| patient_id | FK                            |
| test_id    | FK                            |
| status     | Ordered / Running / Completed |

**disease_tests**

Disease  
<br/>↓  
<br/>Required Test

Example

Dengue  
<br/>↓  
<br/>CBC  
<br/>Platelet Count

**forecasts**

Stores outputs from AI models.

| **Column**      | **Type**  |
| --------------- | --------- |
| id              | UUID      |
| hospital_id     | FK        |
| forecast_type   | TEXT      |
| target          | TEXT      |
| predicted_value | FLOAT     |
| confidence      | FLOAT     |
| generated_at    | TIMESTAMP |

Examples

- Bed Occupancy
- Medicine Demand
- Patient Footfall

**alerts**

Generated automatically.

| **Column**  | **Type**  |
| ----------- | --------- |
| id          | UUID      |
| hospital_id | FK        |
| alert_type  | TEXT      |
| severity    | TEXT      |
| message     | TEXT      |
| resolved    | BOOLEAN   |
| created_at  | TIMESTAMP |

Examples

Medicine Shortage  
<br/>Doctor Shortage  
<br/>Equipment Failure  
<br/>Disease Spike  
<br/>High Occupancy

**recommendations**

Stores AI-generated actions.

| **Column**     | **Type** |
| -------------- | -------- |
| id             | UUID     |
| alert_id       | FK       |
| recommendation | TEXT     |
| priority       | INT      |
| accepted       | BOOLEAN  |

Example

Transfer  
<br/>250 ORS  
<br/>PHC-4  
<br/>↓  
<br/>PHC-8

**Time-Series Tables**

Rather than recalculating history from transactional tables, create daily aggregates.

**daily_patient_stats**

Hospital  
<br/>Date  
<br/>Total Patients  
<br/>Disease Counts  
<br/>Admissions  
<br/>Discharges

**daily_inventory_usage**

Hospital  
<br/>Medicine  
<br/>Used Today  
<br/>Remaining  
<br/>Forecast

**daily_bed_stats**

Hospital  
<br/>Occupied  
<br/>Available  
<br/>Admissions  
<br/>Discharges

**daily_doctor_stats**

Doctor  
<br/>Patients Seen  
<br/>Attendance  
<br/>Hours Worked

These aggregate tables make dashboards and forecasting dramatically faster.

**Why this schema works well for AI**

The schema separates **transactional data** from **analytical data**:

- **Transactional tables** (patients, inventory, doctor_attendance, beds) capture real-time operations.
- **Mapping tables** (disease_medicines, disease_tests, supplier_medicines) model healthcare relationships in a normalized way.
- **Aggregate tables** (daily_patient_stats, daily_inventory_usage, etc.) provide efficient historical features for forecasting models.
- **AI output tables** (forecasts, alerts, recommendations) persist predictions and decisions so they can be audited, explained, and displayed without recomputing every request.

**One recommendation**

I would **avoid Firebase** for this project unless the hackathon explicitly requires it. Since almost every feature revolves around structured relational data, forecasting, and SQL analytics, **PostgreSQL** is a much stronger fit. If you need real-time dashboard updates, use **FastAPI + WebSockets** or **Server-Sent Events (SSE)** on top of PostgreSQL. That gives you transactional integrity, simpler architecture, and a database that's much closer to what a production health management system would use.