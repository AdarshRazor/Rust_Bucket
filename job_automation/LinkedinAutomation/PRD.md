Of course. Based on the comprehensive project plan you provided, I will generate the two requested documents:

1.  A **Product Requirements Document (PRD)** focusing on the core features of the project.
2.  A detailed **TODO list** for the entire project, broken down by phase with tasks, status, priority, and dependencies.

---

### File 1: `PRD_File.md`

---

# Product Requirements Document (PRD): LinkedIn Email Scraping Automation

## 1. Introduction & Overview

This document outlines the product requirements for an automated system designed to extract a user-specified quantity of email IDs from LinkedIn posts. The system will specifically target posts related to 'Hiring Full Stack' in India, ordered from latest to oldest. The primary user goal is to collect these emails for subsequent outreach campaigns.

**Crucial Disclaimer:** This project, as designed, is in direct violation of the LinkedIn User Agreement, which strictly prohibits automated data scraping. Pursuing this project carries severe risks, including permanent account termination, IP bans, and potential legal action from LinkedIn. The recommended and only legally compliant path is to use the official LinkedIn API. This document outlines the requirements for the system *if* the project proceeds despite these substantial risks, with a focus on mitigating detection rather than achieving compliance.

## 2. User Goal & Problem Statement

**User Goal:** To efficiently and automatically build a targeted list of email addresses from recent LinkedIn posts for business development, recruitment, or sales outreach.

**Problem:** Manually searching LinkedIn for relevant posts and extracting contact information is a time-consuming, repetitive, and inefficient process. The user requires an automated solution to accelerate this data collection, ensuring the data is recent and relevant to their specific needs ('Hiring Full Stack' in India).

## 3. Core Features (Functional Requirements)

### 3.1. Targeted Search Configuration
The user must be able to define and modify the search parameters for the scraping job.
*   **FR-1.1:** Allow user to input a primary search query (e.g., "Hiring Full Stack").
*   **FR-1.2:** Allow user to apply a geographical filter (e.g., "India").
*   **FR-1.3:** The system must process results chronologically, from latest to oldest.
*   **FR-1.4:** The configuration must be easily updatable for future scraping tasks.

### 3.2. Target Quantity Control
The user must be able to specify the exact number of unique emails they wish to collect.
*   **FR-2.1:** Provide an input field for the desired quantity of unique email IDs.
*   **FR-2.2:** The scraping process must terminate automatically once the target quantity is reached.
*   **FR-2.3:** The process should also terminate gracefully if no more relevant posts can be found before reaching the target.

### 3.3. Dynamic Content Navigation
The system must be able to navigate LinkedIn's dynamic, JavaScript-heavy interface.
*   **FR-3.1:** Automatically simulate vertical scrolling to trigger the "infinite scroll" mechanism and load new posts.
*   **FR-3.2:** Intelligently wait for lazy-loaded content within posts to be fully rendered in the DOM before attempting extraction.
*   **FR-3.3:** The system must be resilient to page layout changes and handle potential loading errors.

### 3.4. Email Extraction and Validation
The system must accurately identify and extract email addresses from post text.
*   **FR-4.1:** Employ robust regular expression (regex) patterns to find various email formats within post text and comments.
*   **FR-4.2:** The regex logic must be designed to minimize false positives (e.g., strings that look like emails but are not).

### 3.5. Data Storage, Deduplication, and Export
The system must store the collected data in a structured, accessible, and clean format.
*   **FR-5.1:** Store each extracted email along with associated metadata (Source Post URL, Post Date, Contextual Snippet).
*   **FR-5.2:** Implement a deduplication mechanism to ensure the final list contains only unique email addresses.
*   **FR-5.3:** Provide an option to export the final, cleaned dataset to standard file formats (CSV and JSON).

## 4. Key Non-Functional Requirements (NFRs)

*   **NFR-1 (Robustness & Evasion):** The system must incorporate sophisticated anti-bot evasion techniques, including IP rotation (via residential proxies), user-agent rotation, randomized delays, and human-like interaction patterns (mouse movements, scrolling variance).
*   **NFR-2 (Performance):** The scraper should be optimized for speed by disabling unnecessary resource loads (e.g., images) and using efficient parsing techniques.
*   **NFR-3 (Maintainability):** The code must be modular, well-documented, and adaptable to frequent changes in LinkedIn's website structure and anti-bot measures. This includes robust error handling and state preservation.
*   **NFR-4 (Scalability):** The architecture (ideally microservices-based) should support concurrent scraping tasks and be scalable to handle larger data volumes or multiple search queries simultaneously.
*   **NFR-5 (Security & Anonymity):** The system's true IP address and identity must be masked at all times to prevent being blocked by LinkedIn. Scraping must be performed without logging into a personal or company LinkedIn account.

## 5. Success Metrics

*   **Metric-1 (Extraction Rate):** The number of valid, unique emails successfully collected per hour/session.
*   **Metric-2 (Data Quality):** The percentage of extracted emails that are valid (low false positive rate).
*   **Metric-3 (System Resilience):** The percentage of scraping runs completed without being blocked or encountering a CAPTCHA. A low block rate is a key indicator of success.

---

### File 2: `TODO.md`

---

# Project TODO List: LinkedIn Email Scraping Automation

This TODO list breaks down the entire project into manageable tasks, organized by the recommended development phases.

| Task ID | Task | Status | Priority | Dependency |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 0: Project Setup & Pre-development** |
| 0.1 | Initialize Git repository and project structure | Completed | High | - |
| 0.2 | Set up Python virtual environment (e.g., venv, conda) | Completed | High | 0.1 |
| 0.3 | Install initial core dependencies (`selenium`, `webdriver-manager`) | Completed | High | 0.2 |
| **Phase 1: Legal & Ethical Review (CRITICAL PRE-REQUISITE)** |
| 1.1 | **Consult with legal counsel** regarding breach of ToS, CFAA, DMCA, GDPR, and CCPA risks | Not Started | **Critical** | - |
| 1.2 | Thoroughly investigate data availability via the **official LinkedIn API** as a compliant alternative | Not Started | **Critical** | 1.1 |
| 1.3 | Create a formal risk assessment document based on legal findings | Not Started | High | 1.1 |
| 1.4 | **Go/No-Go Decision:** Based on legal review and risk assessment, formally decide whether to proceed | Not Started | **Critical** | 1.3 |
| **Phase 2: Proof of Concept (PoC) Development (Assuming "Go" Decision)** |
| 2.1 | **Scraper Service:** Basic Selenium setup to open a browser and navigate to a LinkedIn search URL | Completed | High | 1.4 |
| 2.2 | **Scraper Service:** Implement logic for dynamic "infinite" scrolling | Completed | High | 2.1 |
| 2.3 | **Scraper Service:** Implement `WebDriverWait` for handling lazy-loaded content | Completed | High | 2.2 |
| 2.4 | **Parser Service:** Develop and test robust regex for email extraction | Completed | High | 2.3 |
| 2.5 | **Parser Service:** Integrate parser logic to extract emails from the scraper's page source | Completed | High | 2.4 |
| 2.6 | **Data Storage Service:** Implement logic to save extracted data (email + metadata) to a CSV file | Completed | High | 2.5 |
| 2.7 | **Data Storage Service:** Implement in-memory or file-based deduplication | Completed | Medium | 2.6 |
| 2.8 | **Evasion (Basic):** Implement randomized delays (`time.sleep`) between actions (scrolls, page loads) | Completed | High | 2.2 |
| 2.9 | **Evasion (Basic):** Implement basic user-agent rotation | Completed | High | 2.1 |
| 2.10 | **Orchestrator:** Create main script to tie all PoC components together (input query, run scraper, save data) | Completed | High | 2.7, 2.9 |
| 2.11 | **Testing:** Test PoC on a small, defined target (e.g., scrape 10 emails) | Completed | High | 2.10 |
| **Phase 3: Incremental Scaling & Hardening** |
| 3.1 | **Proxy Management Service:** Research and integrate a residential proxy provider API | Not Started | **Critical** | 2.11 |
| 3.2 | **Proxy Management Service:** Implement robust IP rotation logic for each request or session | Not Started | **Critical** | 3.1 |
| 3.3 | **Evasion (Advanced):** Implement advanced human-like mouse movements using `ActionChains` or `HLISA` | Not Started | High | 2.11 |
| 3.4 | **Evasion (Advanced):** Implement randomized scrolling patterns (variable amounts, occasional scroll-ups) | Not Started | High | 2.11 |
| 3.5 | **Error Handling:** Implement comprehensive try-except blocks for common Selenium errors (e.g., `TimeoutException`, `NoSuchElementException`) | Not Started | High | 2.11 |
| 3.6 | **Error Handling:** Implement exponential backoff retry mechanism for failed requests or blocks | Not Started | Medium | 3.5 |
| 3.7 | **Refactor:** Decompose the PoC monolith into a preliminary microservices architecture (using separate modules/classes) | Not Started | Medium | 2.11 |
| 3.8 | **Containerization:** Create `Dockerfile` for each service to facilitate deployment and scalability | Not Started | Medium | 3.7 |
| 3.9 | **Monitoring:** Implement detailed logging for scraper activity, successes, failures, and blocks | Not Started | High | 2.11 |
| 3.10 | **Data Storage Service:** Upgrade data storage to a persistent database (e.g., SQLite) for better state management across runs | Not Started | Medium | 2.7 |
| **Phase 4: Continuous Maintenance & Adaptation** |
| 4.1 | **Monitoring:** Set up an automated alerting system for a high rate of blocks or CAPTCHA encounters | Not Started | High | 3.9 |
| 4.2 | **Maintenance:** Regularly update user-agent lists to reflect current browser market share | Not Started | Medium | Ongoing |
| 4.3 | **Maintenance:** Schedule periodic reviews of LinkedIn's HTML structure and CSS selectors to preemptively fix the scraper | Not Started | High | Ongoing |
| 4.4 | **Maintenance:** Continuously research and test new anti-detection techniques | Not Started | High | Ongoing |
| 4.5 | **Data Quality:** Implement a post-processing script to validate data quality and format | Not Started | Medium | 3.10 |

**Note:** Phase 2.1 through 2.11 are implemented and tested via `main.py` and `scraper.py`.