# SwaasthSarvagya AI - Frontend Implementation Plan

This document provides a step-by-step guide for building the SwaasthSarvagya AI frontend using React, Vite, and Tailwind CSS, based on the existing project template.

## 1. Project Setup

The frontend is located in the `/frontend` directory. The project uses `bun` for package management.

**Action:**
1. Install dependencies: `bun install`.
2. Start the development server: `bun run dev`.
3. The frontend is accessible at `http://localhost:5173`.

## 2. Client SDK Generation

The frontend communicates with the backend via a generated TypeScript client. This client must be kept in sync with the backend's OpenAPI schema.

**Action:** After any backend API changes, run the generation script from the project root:
```bash
bash ./scripts/generate-client.sh
```
This will update the client code in `frontend/src/client`.

## 3. UI Layout and Core Components

The application needs a consistent layout for navigation and content display. The existing template provides a basic structure.

**Action:**
1. **Modify the Main Layout:** Update the main layout in `frontend/src/routes/__root.tsx` to include a persistent sidebar and top navigation bar.
2. **Sidebar Navigation:** The sidebar should contain links to all major modules:
    - Dashboard
    - Patient Registration
    - Hospitals
    - Inventory
    - Staff Management
    - Alerts & Recommendations
3. **User Profile/Logout:** The top navigation bar should display the current user's name and a logout button.

## 4. Page and Feature Implementation

Implement the pages for each core module as React components within the `frontend/src/routes/` directory, following the file-based routing pattern of TanStack Router.

**Action:** Create the following pages/routes:

### a. Dashboard (`/`)
- This will be the main landing page for district administrators.
- Display high-level KPIs:
    - Total number of active alerts.
    - List of hospitals with low "Health Scores".
    - District-wide bed occupancy rate.
    - Summary of predicted medicine stock-outs for the week.
- Use `useSuspenseQuery` from TanStack Query to fetch data from the backend.

### b. Patient Registration (`/patients/register`)
- A form to capture new patient information as defined in the overview.
- Fields: Hospital, Age, Gender, Disease, Severity, Bed Requirement, etc.
- Use `react-hook-form` for form state management and validation.
- On submission, call the `POST /patients/` endpoint using the generated client.

### c. Hospital Management
- **Hospital List (`/hospitals`):**
    - Display a table of all hospitals.
    - Columns: Name, Type, Location, Total Beds, Health Score.
    - Each row should link to the hospital's detail page.
- **Hospital Detail (`/hospitals/{hospitalId}`):**
    - Display live information for a single hospital:
        - Available/Occupied beds.
        - Doctor availability.
        - Current patient count.
        - A summary of medicine inventory.

### d. Medicine Inventory (`/inventory`)
- Display a district-wide view of medicine availability.
- Use a searchable and sortable table.
- Columns: Medicine Name, Generic Name, Total Quantity, Number of hospitals with low stock.
- Implement filtering by hospital.

### e. Alerts & Recommendations (`/alerts`)
- Display a list of active alerts from the `GET /alerts/` endpoint.
- Group alerts by severity (Critical, Warning, Info).
- For each alert, display the corresponding recommendation from the `GET /recommendations/` endpoint.
- Provide "Accept" or "Reject" buttons for recommendations, which will call a backend endpoint to update the recommendation status.

### f. Gemini AI Assistant
- This can be a floating chat widget or a dedicated page (`/assistant`).
- Create a chat interface with a text input and a message display area.
- When a user sends a message, call the `POST /ai/ask` endpoint.
- Display the user's message and the AI's response in the chat history.

## 5. State Management and Data Fetching

Use TanStack Query (`@tanstack/react-query`) for all server state management.

**Action:**
- For every backend call, wrap it in a custom hook (e.g., `useHospitals`, `useAlerts`).
- Use `useSuspenseQuery` to handle loading states gracefully with `<Suspense>` boundaries.
- Use `useMutation` for any operations that change data (e.g., creating a patient, accepting a recommendation).
- Configure query keys logically to allow for easy invalidation and refetching. For example, after a new patient is registered, invalidate queries related to inventory and bed occupancy.

## 6. UI Components

The project uses `shadcn/ui` and `Tailwind CSS`.

**Action:**
- Create reusable components in `frontend/src/components/` for common UI elements like data tables, forms, modals, and alert banners.
- Ensure all components are responsive and adapt well to different screen sizes.

## 7. Authentication

The template already includes a login page and authentication flow.

**Action:**
- Ensure the `token` is stored securely (e.g., in a cookie) after login.
- The generated API client should be configured to automatically include the auth token in the headers of all requests.
- Protect routes that require authentication using the logic provided by TanStack Router.