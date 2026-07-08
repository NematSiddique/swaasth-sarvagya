# SwaasthSarvagya AI

## AI-Driven Health Center & Supply Chain Management Platform

This file provides a high-level overview of the SwaasthSarvagya AI project. For more detailed information, please refer to the `GEMINI.md` files in the `backend` and `frontend` directories.

## Vision

Develop an AI-powered District Health Intelligence Platform that continuously monitors healthcare operations across all PHCs and CHCs and proactively recommends interventions before shortages or operational failures occur.

The platform serves as a centralized command center for district healthcare administrators while remaining simple enough for hospital staff to use daily.

## Objectives

- Digitize operational health center data
- Forecast medicine demand and shortages
- Predict patient footfall and bed occupancy
- Monitor doctor attendance and staffing
- Detect disease outbreaks early
- Recommend inter-hospital resource redistribution
- Provide multilingual AI assistance
- Generate explainable recommendations instead of raw dashboards

## System Architecture

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