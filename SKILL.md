---
name: healsync-ai-project
description: Provides context and implementation guidance for the HealSync AI project, an AI-driven health center and supply chain management platform.
---

# HealSync AI Project Skill

This skill contains the core context for the **HealSync AI** project. Use this skill when working on any feature, bug fix, or documentation related to this project.

## Project Vision

HealSync AI is an AI-powered District Health Intelligence Platform designed to monitor healthcare operations across Primary (PHCs) and Community (CHCs) Health Centres. It aims to proactively recommend interventions to prevent shortages and operational failures, moving from reactive to proactive health management.

## Core Objective

To build a centralized command center for district healthcare administrators that digitizes operational data and uses AI to provide explainable recommendations, not just raw dashboards.

## Technology Stack

- **Frontend**: React, Vite, TypeScript, TanStack Router, TanStack Query, Tailwind CSS, shadcn/ui.
- **Backend**: FastAPI, Python, SQLModel (ORM).
- **Database**: PostgreSQL (Single Source of Truth).
- **AI/ML**: Gemini API, Prophet, XGBoost, Google OR-Tools.
- **Deployment**: Docker, Docker Compose.

The project is based on the "Full Stack FastAPI Template".

## Key Modules & Features

1.  **Patient Registration**: Capturing patient encounter data.
2.  **Hospital Management**: Tracking live operational data for each hospital (beds, doctors, inventory).
3.  **Medicine Inventory**: District-wide medicine tracking with forecasting.
4.  **Staff Management**: Tracking doctor/nurse availability and predicting shortages.
5.  **Disease Intelligence**: A knowledge base for diseases, their requirements, and trends.
6.  **AI Features**:
    - **Forecasting**: Medicine demand, patient footfall, bed occupancy.
    - **Detection**: Disease outbreaks, equipment failure.
    - **Optimization**: Smart redistribution of resources between hospitals.
    - **Scoring**: A "Health Score" for each hospital.
    - **Gemini AI Assistant**: A natural language interface for querying the system's state.
7.  **Alert & Recommendation Engine**: Automatically generates alerts for problems and recommends concrete solutions.

## Development Workflow

- **Backend**:
  1.  Define/update data structures in `backend/app/models.py` using SQLModel.
  2.  Create a new SQL migration file in `backend/db/migrations/` for Flyway.
  3.  Implement API endpoints in `backend/app/api/endpoints/`.
  4.  Implement business logic in `backend/app/crud.py` and `backend/app/services/`.
  5.  Write tests in `backend/tests/`.
- **Frontend**:
  1.  After backend changes, regenerate the client SDK with `bash ./scripts/generate-client.sh`.
  2.  Develop pages/routes in `frontend/src/routes/`.
  3.  Use TanStack Query for data fetching and state management.
  4.  Use `shadcn/ui` components for the UI.

Refer to `HealSync AI Backend Implementation.md` and `HealSync AI Frontend Implementation.md` for detailed, step-by-step implementation plans.
