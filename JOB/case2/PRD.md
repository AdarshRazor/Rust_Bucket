### **Document 1: Product Requirements Document (PRD_File)**

---

## **Product Requirements Document: Agent Mira - AI-Powered Property Recommendation System**

**Version:** 1.0
**Status:** Draft
**Author:** AI Assistant
**Date:** October 26, 2023

### 1. Introduction & Problem Statement

Homebuyers are often overwhelmed by the sheer volume of property listings on the market. Sifting through hundreds of options that only partially match their needs is time-consuming, frustrating, and inefficient. They lack a tool that can intelligently prioritize listings based on a holistic view of their preferences, not just on simple filters like price or bedroom count.

**Agent Mira's AI-Powered Property Recommendation System** aims to solve this by providing a smart, personalized, and transparent home discovery experience. By leveraging user preferences and a sophisticated machine learning model, the system will deliver a curated list of top-matching properties, complete with clear, data-driven reasoning for each recommendation.

### 2. Product Goals & Objectives

*   **User Goal:** To quickly and confidently identify 2-3 highly relevant properties that match their budget, lifestyle, and feature requirements, saving them time and effort in their home search.
*   **Business Goal:** To increase user engagement and generate highly qualified leads for real estate agents by providing valuable, data-driven insights that build trust and demonstrate market expertise.
*   **Technical Goal:** To build a scalable and resilient MVP that successfully integrates a predictive ML model into a real-time user-facing application.

### 3. Target Audience

*   **Primary:** Prospective homebuyers who are actively searching for a property. They may be first-time buyers, families looking to upgrade, or investors. They are tech-savvy enough to use web applications but are not necessarily data science experts.
*   **Secondary:** Real estate agents (like Agent Mira) who can use this tool to quickly shortlist properties for their clients.

### 4. Core Features (MVP Scope)

#### **F1: User Preference Input Form**
*   **Description:** A clean, intuitive web form where users can input their home-buying criteria.
*   **User Story:** "As a homebuyer, I want to specify my budget, desired location, minimum number of bedrooms, and other key preferences so that the system can find properties that are right for me."
*   **Requirements:**
    *   **Budget:** A numerical input for the user's maximum budget (e.g., `$500,000`).
    *   **Location:** A text or dropdown input for preferred city/area (e.g., "New York, NY").
    *   **Minimum Bedrooms:** A numerical input for the minimum number of bedrooms required.
    *   **Commute Time:** A dropdown to select maximum acceptable commute time (e.g., `< 15 min`, `15-30 min`, `30-45 min`, `45+ min`).
    *   **School Rating:** A slider or input for minimum desired school rating (1-10).
    *   **Key Amenities:** Checkboxes for essential amenities (`Pool`, `Garage`, `Garden`).

#### **F2: AI-Powered Scoring & Recommendation Engine**
*   **Description:** The backend service that processes user preferences, scores all available properties, and identifies the top matches. This is the core logic of the application.
*   **User Story:** "As a user, I expect the system to use my preferences to intelligently score and rank properties, with a special focus on whether the property is a good value for the price."
*   **Requirements:**
    *   The system must ingest property data from our database (or the provided JSON files).
    *   It must use the `complex_price_model_v2.pkl` model to predict the price for each property based on its features.
    *   It must calculate a `total_match_score` for each property based on the weighted formula provided in the case study.
    *   The engine must return the top 3 properties sorted by `total_match_score`.
    *   For each property, the response must include a breakdown of the component scores to generate the reasoning.

#### **F3: Personalized Recommendation Display**
*   **Description:** A user-friendly interface that presents the top 3 recommended properties to the user.
*   **User Story:** "As a homebuyer, after I submit my preferences, I want to see a clear list of the best-matching properties, including an image, key details, and a simple explanation of *why* each one is a good match for me."
*   **Requirements:**
    *   Display up to 3 properties in a card-based layout.
    *   Each property card must show:
        *   Property Image (`image_url`)
        *   Title (`title`)
        *   Listing Price (`price`)
        *   Predicted Price (from the ML model)
        *   Location (`location`)
        *   Key specs (`bedrooms`, `bathrooms`, `size_sqft`)
    *   **Reasoning for Match:** Each card must feature a dedicated section that explains its match score. This should be generated dynamically. For example:
        *   "**Overall Match: 88/100**"
        *   "✅ **Excellent Price:** Our model predicts a value near the listing price, and it's within your budget."
        *   "✅ **Meets Bedroom Needs:** Has 3 bedrooms, meeting your minimum requirement."
        *   "⚠️ **Good Commute:** The commute time of 25 minutes is a reasonable match."

### 5. Data Requirements & Assumptions

The recommendation logic requires data points not present in the provided JSON files.
*   **Required Data:** `school_rating`, `commute_time`, `year_built`, and structured amenity flags (`has_pool`, `has_garage`, `has_garden`).
*   **MVP Assumption:** For this prototype, **this missing data will be mocked/simulated.** A helper script will merge the provided JSON files and augment them with realistic, randomly generated values for these fields.
*   **Future Work:** In a production environment, this data would be sourced from third-party APIs (e.g., Google Maps API for commute times, GreatSchools API for school ratings) or be a part of the core property database.

### 6. Out of Scope for MVP

*   User accounts, login, and saving searches/favorites.
*   Direct contact forms for real estate agents.
*   Map-based search and filtering.
*   Real-time updates on property availability.
*   Pagination for more than 3 results.

---

### **Document 2: Project TODO List**

---

## **Project TODO List: Agent Mira MVP**

This plan breaks the project into logical phases. Tasks are designed to be completed in a sequential manner, respecting dependencies.

| Phase | Task ID | Task Description | Status | Priority | Dependency | Comments |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Phase 0: Project Setup & Planning** |
| | T0.1 | Set up Git repository and project structure (`/backend`, `/frontend`, `/docs`). | Completed | **High** | - | Added as `server`, `clent` and `docs` | 
| | T0.2 | Finalize the PRD and this TODO list. | Completed | **High** | - | Added in `root` folder as `PRD.md` |
| | T0.3 | Investigate `complex_price_model_v2.pkl`: confirm its input features and output format. | Completed | **High** | - | Added in `docs` folder |
| | T0.4 | Define the unified `Property` data schema, including mocked fields. | Completed | **High** | T0.3 |
| **Phase 1: Data Preparation & Backend API** |
| | T1.1 | Create a data-loading script to merge the three source JSON files by `id`. | Completed | **High** | T0.4 |
| | T1.2 | Augment the merged data with mocked fields (`school_rating`, `commute_time`, `year_built`, etc.). | Completed | **High** | T1.1 |
| | T1.3 | Set up a backend server using Flask or FastAPI. | Completed | **High** | T0.1 | Added as `server/main.py` |
| | T1.4 | Implement a service to load and cache the `complex_price_model_v2.pkl` on startup. | Completed | **High** | T1.3, T0.3 | Added as `server/model_service.py` |
| | T1.5 | Create a function/module for `predict_price` using the loaded model. | Completed | **High** | T1.4 | Added as `server/predict_price.py` |
| | T1.6 | Implement the full `calculate_total_score` function, including all component scores. | Completed | **High** | T1.5 | Added as `server/score.py` |
| | T1.7 | Create the main API endpoint (`POST /recommendations`) that accepts user preferences. | Completed | **High** | T1.6 | Added as `server/main.py` |
| | T1.8 | Implement the core logic within the endpoint: score all properties and return the top 3. | Completed | **High** | T1.7, T1.2 | Added as `server/main.py` |
| | T1.9 | Implement logic to generate the "reasoning" text for each recommended property. | Completed | **Medium** | T1.8 | Added as `server/reasoning.py` |
| | T1.10 | Add basic error handling and logging to the backend API. | Completed | **Medium** | T1.8 | Added as `server/main.py` |
| **Phase 2: Frontend Development** |
| | T2.1 | Set up a basic frontend project (e.g., using Vite + React/Vue). | Completed | **High** | T0.1 |
| | T2.2 | Build the "User Preference Input Form" component based on PRD requirements. | Completed | **High** | T2.1 | Added as `client/src/components/UserPreferenceForm.tsx` |
| | T2.3 | Build the "Recommendation Card" component to display a single property. | Completed | **High** | T2.1, T0.4 | Added as `client/src/components/RecommendationCard.tsx` |
| | T2.4 | Build the "Results Display" container to show the list of 3 recommendation cards. | Completed | **High** | T2.3 | Added as `client/src/components/ResultsDisplay.tsx` |
| | T2.5 | Implement state management for user inputs, loading state, and API responses. | Completed | **Medium** | T2.1 | Added as `client/src/app/page.tsx` |
| **Phase 3: Integration & Testing** |
| | T3.1 | Connect the frontend form submission to the backend `/recommendations` API endpoint. | Completed | **High** | T1.8, T2.2 | Implemented in `client/src/app/page.tsx` |
| | T3.2 | Render the API response dynamically in the "Results Display" on the frontend. | Completed | **High** | T3.1, T2.4 | Implemented in `client/src/app/page.tsx`, `client/src/components/ResultsDisplay.tsx` |
| | T3.3 | Implement frontend loading indicators and display of error messages from the API. | Completed | **Medium** | T3.2 | Implemented in `client/src/app/page.tsx` |
| | T3.4 | Perform end-to-end testing with various user inputs to validate results and reasoning. | Completed | **High** | T3.2 | Manual E2E testing possible via UI |
| | T3.5 | Write basic unit tests for the `calculate_total_score` function in the backend. | Completed | **Low** | T1.6 | Added as `server/tests/test_score.py` |
| **Phase 4: Deployment & Documentation** |
| | T4.1 | Containerize the backend application using a `Dockerfile`. | Completed | **Medium** | T1.8 | Added as `server/Dockerfile` |
| | T4.2 | Prepare deployment configuration (e.g., `docker-compose.yml`) for local execution. | Completed | **Medium** | T4.1, T2.1 | Added as `docker-compose.yml` |
| | T4.3 | Draft the Architecture & Design Document (for 1k and 20k users). | Completed | **High** | T1.10 | Added as `docs/architecture_design.md` |
| | T4.4 | Draft the Monitoring, Logging, and Error Handling strategy document. | Completed | **High** | T1.10 | Added as `docs/monitoring_logging_error_handling.md` |
| | T4.5 | Write the final `README.md` with detailed setup and run instructions. | Completed | **High** | T4.2 | Added as `README.md` |
| | T4.6 | Clean up code, add comments, and prepare the project for submission. | Completed | **Medium** | T4.5 | Code cleaned, comments added, project ready for submission |