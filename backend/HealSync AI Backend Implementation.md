# HealSync AI - Backend Implementation Plan

This document outlines the step-by-step plan for implementing the backend of the HealSync AI platform using FastAPI, SQLModel, and PostgreSQL, based on the existing project template.

## 1. Project Setup

The project is based on the "Full Stack FastAPI Template". The backend is located in the `/backend` directory. Ensure all dependencies are installed using `uv sync`.

## 2. Database Models and Schemas

The first step is to ensure the SQLModel classes in `backend/app/models.py` accurately represent the database schema defined in `HealSync AI Overview.md`. These models are the foundation for the database tables, API validation, and response structures.

**Action:**
1.  **Verify/Update SQLModel Classes:** Review `backend/app/models.py` and ensure it contains SQLModel classes for all necessary tables. The current implementation uses integer primary keys, which should be maintained for consistency.

    **Key Models to Verify:**
    - `Hospital`, `Patient`, `Disease`, `MedicineGroup`, `Medicine`
    - `Doctor`, `Nurse`, `DoctorAttendance`
    - `Laboratory`, `LabEquipment`, `LabKit`
    - `Bed`, `Inventory`, `InventoryTransaction`
    - `Supplier`, `SupplierMedicine` (many-to-many)
    - `DiseaseMedicine` (many-to-many), `DiseaseTest` (many-to-many)
    - `PatientTest`
    - `Forecast`, `Alert`, `Recommendation`
    - `DailyPatientStats`, `DailyInventoryUsage`, `DailyBedStats`, `DailyDoctorStats`

2.  **Create Pydantic Schemas:** For each core model, define corresponding Pydantic schemas for API interaction. These should be placed in a new file, `backend/app/schemas.py`, or organized into a `schemas` module.

    - **`_Base` Schema:** Contains common fields.
    - **`_Create` Schema:** Inherits from `_Base` for creation payloads.
    - **`_Update` Schema:** Inherits from `_Base` for update payloads.
    - **`_Public` Schema:** Inherits from `_Base` for public-facing API responses (read operations).

    *Example for `Hospital`:*
    ```python
    # In backend/app/schemas.py
    from app.models import Hospital

    class HospitalPublic(Hospital):
        pass

    class HospitalCreate(Hospital):
        pass

    class HospitalUpdate(SQLModel):
        # Fields that can be updated
        total_beds: int | None = None
    ```

## 3. Database Migrations

Once the SQLModel classes are finalized, create the corresponding SQL migration file for Flyway. Flyway runs SQL files from the `/backend/db/migrations` directory to manage the database schema.

**Action:**
1. Create a new SQL file in `backend/db/migrations/` named `V2__create_healsync_tables.sql` (or a subsequent version number).
2. Write the `CREATE TABLE` SQL statements corresponding to the SQLModel classes in `backend/app/models.py`. Include primary keys, foreign keys, constraints, and indexes.
3. Flyway will automatically apply this migration the next time the backend service starts. The `prestart.sh` script handles this on container startup.

## 4. API Endpoint Development

Create API routers for each core module in `backend/app/api/endpoints/`. Each router will contain the CRUD operations and business logic for its domain.

**Action:** Implement the following API routers and endpoints, using the Pydantic schemas for request bodies and response models.

### a. Hospitals (`hospitals.py`)
- `POST /hospitals/`: Create a hospital.
- `GET /hospitals/`: Get a list of all hospitals with pagination.
- `GET /hospitals/{hospital_id}`: Get details for a single hospital.
- `PUT /hospitals/{hospital_id}`: Update a hospital.
- `GET /hospitals/{hospital_id}/health-score`: (Future) Get the calculated health score.

### b. Patients (`patients.py`)
- `POST /patients/`: Register a new patient. This endpoint will trigger updates to other tables (inventory, beds, etc.) as part of its business logic.
- `GET /patients/`: Get a list of patients.
- `GET /patients/{patient_id}`: Get patient details.

### c. Inventory (`inventory.py`)
- `GET /inventory/`: Get district-wide inventory with filters (e.g., by medicine).
- `GET /hospitals/{hospital_id}/inventory`: Get inventory for a specific hospital.
- `POST /inventory/transactions`: Record an inventory transaction (issue, receive, transfer).

### d. Staff (`doctors.py`, `nurses.py`)
- `POST /doctors/`: Add a new doctor.
- `GET /doctors/`: Get a list of doctors.
- `POST /doctors/attendance`: Record doctor attendance.

### e. Disease Intelligence (`diseases.py`)
- `GET /diseases/`: Get a list of diseases.
- `GET /diseases/{disease_id}`: Get disease details.

### f. AI & Analytics (`ai.py`)
- `GET /forecasts/`: Get stored forecasts.
- `GET /alerts/`: Get active alerts.
- `GET /recommendations/`: Get AI-generated recommendations.
- `POST /ai/ask`: Endpoint to interact with the Gemini AI Assistant.

## 5. CRUD Utilities and Business Logic

Implement the CRUD utility functions in `backend/app/crud.py`. These functions will interact directly with the database session to create, read, update, and delete records.

**Action:**
- Create a generic `CRUDBase` class for common operations.
- Create specific CRUD classes for each model (e.g., `CRUDHospital`, `CRUDPatient`).
- **Implement Event-Driven Logic:** Within the API endpoints (or a dedicated service layer), key actions should trigger a cascade of updates and AI tasks. Use FastAPI's `BackgroundTasks` to run these processes without blocking the API response.
    - **Example Event (Patient Registration):**
        - Decrement `Inventory` for prescribed medicines.
        - Update `Bed` status if a bed is allocated.
        - Trigger a background task to re-run the `Medicine Stock Forecast` for the affected items.
        - Trigger a background task to invoke the `AlertEngine` to check for new shortages.

## 6. AI/ML Model Integration

This is an advanced step. Create a new `backend/app/services` directory to house the logic for AI/ML features. These services should be designed to be called from background tasks triggered by events.

**Action:**
1. **Forecasting:**
   - **Service:** `backend/app/services/forecasting.py`
   - **Logic:** The forecasting service provides functions to generate predictions for key operational metrics. It's designed to be triggered via `BackgroundTasks` after relevant events occur, ensuring forecasts are kept up-to-date.
   - **Implementation Details:**
     - The service currently uses a **simulation pipeline** that mimics a real ML model, making it easy to integrate a pre-trained model like Prophet later.
     - **Pipeline Steps:**
       1.  **Fetch Historical Data:** Queries historical data from aggregated tables (`DailyInventoryUsage`, `DailyBedStats`) or transactional tables (`PatientTest`, `Patient`).
       2.  **Prepare Data:** If no data is found, it generates a random dataset for simulation. Otherwise, it formats the data into a `pandas` DataFrame with `ds` (datestamp) and `y` (value) columns, as required by Prophet.
       3.  **Simulate Prediction:** Calculates a 7-day projected demand based on the historical average. It also simulates a `confidence` score based on the standard deviation of past data (higher variance leads to lower confidence).
       4.  **Save Forecast:** Uses an "upsert" logic to update an existing forecast for the same target and date or create a new one in the `Forecasts` table.
     - **Implemented Forecasts:**
       - `generate_demand_forecast` (for medicines)
       - `generate_bed_occupancy_forecast`
       - `generate_kit_demand_forecast` (for lab tests)
       - `generate_disease_outbreak_forecast`

2. **Alerting:**
   - **Service:** `backend/app/services/alerting.py`
   - **Logic:** The `AlertEngine` is a rule-based service that scans the system's state to identify current and future problems. It is designed to be run as a `BackgroundTask` after any significant state change (e.g., inventory update, new forecast). A helper function prevents the creation of duplicate, unresolved alerts.
   - **Implemented Alert Checks:**
     - **`check_inventory_alerts`:**
       - **Low Stock (Static):** Triggers `low_inventory` or `low_kit_inventory` alert if stock is below a static reorder level.
       - **Expiring Stock:** Triggers `expiring_inventory` alert for medicines expiring within 30 days.
       - **Low Stock (Forecasted):** Triggers `forecasted_shortage` or `forecasted_kit_shortage` alert if current stock is less than the predicted demand for the next 7 days. This is a key proactive alert.
     - **`check_bed_occupancy_alerts`:**
       - **High Occupancy (Current):** Triggers `high_bed_occupancy` alert if the current occupancy ratio exceeds a critical threshold (e.g., 90%).
       - **High Occupancy (Forecasted):** Triggers `forecasted_high_occupancy` alert if the forecasted occupancy exceeds a warning threshold (e.g., 85%).
     - **`check_disease_outbreak_alerts`:**
       - **Anomaly-Based:** Triggers a `disease_spike` alert if the number of new cases for a specific disease today is significantly higher (e.g., >2.5x) than the recent daily average.
     - **`check_staffing_and_infra_alerts`:**
       - **Staffing:** Triggers `doctor_shortage` alert if a doctor is marked as absent.
       - **Infrastructure:** Triggers `lab_unavailable` or `maintenance_overdue` alerts for laboratory and equipment issues.

3. **Recommendations:**
   - **Service:** `backend/app/services/recommendation.py` (to be created)
   - **Logic:** While an alert identifies a problem, a recommendation proposes a concrete, actionable solution. This service will be triggered by the creation of new, high-priority alerts.
   - **Planned Implementation for Medicine Shortage:**
     1.  **Trigger:** A `forecasted_shortage` alert is created for Medicine X at Hospital A.
     2.  **Process:** The `RecommendationEngine` is invoked with the alert details.
     3.  **Identify Surplus:** The engine queries the `Inventory` and `Forecast` tables for all other hospitals to find potential sources. A hospital is a valid source if its `(current_stock - forecasted_demand)` shows a significant surplus.
     4.  **Optimize Transfer:** From the list of valid sources, an optimization algorithm (e.g., using geographic distance from hospital coordinates) is used to find the *best* source (e.g., nearest hospital with sufficient surplus).
     5.  **Formulate Recommendation:** A structured recommendation is created.
         - **Action:** "Transfer 500 units of Medicine X from Hospital B to Hospital A."
         - **Reason:** "A stock-out is predicted at Hospital A in 2 days. Hospital B has a 20-day surplus and is the nearest viable source."
     6.  **Save:** The new recommendation is saved to the `Recommendations` table, linked to the original alert.

4. **Gemini Assistant:**
   - In the `/ai/ask` endpoint, create a prompt for the Gemini API.
   - The prompt should include context from the database (e.g., active alerts, recommendations) and the user's question.
   - *Example Prompt:* "Given the following critical alerts: [alerts], answer the user's question: 'Which hospitals require intervention today?'"
   - Return the processed response from Gemini.

## 7. Background Tasks & Aggregations

The system will use two types of background processing: immediate tasks for real-time intelligence and periodic tasks for historical aggregation and model retraining.

**Action:**
- **Immediate Event-Driven Tasks:** Use FastAPI's built-in `BackgroundTasks` to run forecasting and alerting services immediately after an API request is processed. This ensures the system state is always as up-to-date as possible.
- **Periodic Aggregate Tasks:** For performance on historical dashboards and for providing feature data for model *retraining*, daily statistics should be pre-calculated. Set up a dedicated task runner (like ARQ or Celery) for these heavier, periodic jobs.
    - Create a daily task that populates:
    - `daily_patient_stats`
    - `daily_inventory_usage`
    - `daily_bed_stats`
    - `daily_doctor_stats`
- This daily task will query the transactional tables for the previous day's data and save the aggregates, which can then be used to retrain the forecasting models periodically.

## 8. Testing

Write unit and integration tests for all new functionality in the `/backend/tests` directory.

**Action:**
- Write tests for all CRUD operations.
- Write tests for API endpoints, mocking external services like the Gemini API.
- Ensure business logic, like the event-driven updates from patient registration, is fully tested.

By following this plan, the backend for HealSync AI can be systematically developed, ensuring all requirements from the overview document are met.