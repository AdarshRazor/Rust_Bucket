# **Process Requirement Document (PRD): Automated Personalized Cold Email Outreach System**

**1. Project Overview**

*   **Project Name:** AI-Powered Personalized Email Automation Engine
*   **Problem:** Manually sending customized emails to a large list of HR contacts is time-consuming and inefficient. Free automation tools often include undesirable watermarks, which appear unprofessional to recruiters.
*   **Goal:** To build a Python-based application that automatically sends personalized cold emails, with a resume attached, to a list of up to 600 HR contacts. The system will leverage Large Language Models (LLMs) via LangChain for personalization and standard Python libraries for email dispatch, ensuring no external watermarks.

**2. Core Features**

*   **F1: Bulk Data Ingestion:** The system must read a list of contacts from a structured file (e.g., CSV). This file will contain essential data for personalization, such as `FirstName`, `LastName`, `Company`, `JobTitle`, `EmailAddress`, and a `PersonalizationHook` (e.g., a recent company achievement or a relevant job opening).
*   **F2: Dynamic Email Personalization:** For each contact, the system will use LangChain to generate a unique, human-like opening line or paragraph. This logic will take the `PersonalizationHook` and other data points from the input file to create relevant content.
*   **F3: Resume Attachment:** The system must attach a specified resume file (e.g., a PDF) to every email it sends.
*   **F4: Secure & Reliable Email Sending:** The application will use a standard SMTP (Simple Mail Transfer Protocol) provider (like Gmail or Outlook) to send emails. Credentials will be handled securely and not hardcoded into the script.
*   **F5: Rate Limiting & Throttling:** To avoid being flagged as spam and having the email account blocked, the system must include a delay between sending emails (e.g., one email every 60-90 seconds).
*   **F6: Logging and Error Handling:** The application will log its progress, recording which emails were sent successfully and which failed. This allows for tracking and resuming the process if it's interrupted.

**3. Technical Stack**

*   **Programming Language:** Python 3.9+
*   **Core Libraries:**
    *   **LangChain:** To orchestrate the interaction with the Language Model (LLM).
    *   **LLM Provider:** An API from a service like OpenAI (GPT-3.5/GPT-4), Anthropic, or Google. An API key will be required.
    *   **Pandas:** For reading and processing the HR contact list from a CSV file.
    *   **SMTPLIB & Email:** Standard Python libraries for connecting to an email server and constructing the emails with attachments.
    *   **Python-Dotenv:** To manage sensitive information like email passwords and API keys securely using a `.env` file.
*   **Prototyping (Optional but Recommended):**
    *   **LangFlow:** A graphical user interface (GUI) for LangChain. Excellent for visually designing and testing the personalization logic before writing the final Python script.
*   **Advanced Orchestration (Optional):**
    *   **LangGraph:** Could be used for more complex flows, such as handling different email templates based on HR seniority or automatically trying a different prompt if the first one fails. For this project's core goal, a simple Python loop is sufficient, but LangGraph offers a path for future expansion.

**4. Project Phases & Steps**

**Phase 1: Setup and Preparation (The Foundation)**
1.  **Data Preparation:** Create a CSV file with the 600 HR contacts. Columns: `FirstName`, `LastName`, `Company`, `EmailAddress`, `PersonalizationHook`.
2.  **Email Account Setup:** For the sending email address (e.g., a Gmail account), generate an "App Password". This is more secure than using your main password.
3.  **LLM API Key:** Obtain an API key from your chosen LLM provider (e.g., OpenAI).
4.  **Environment Setup:** Set up a Python virtual environment and install the required libraries. Create a `.env` file to securely store your App Password and LLM API Key.
5.  **Base Content:** Write a generic version of your cold email template and finalize your resume PDF.

**Phase 2: Personalization Logic (The Brain)**
1.  **Design in LangFlow:** Use LangFlow to visually build the personalization chain.
    *   Input: `Company`, `FirstName`, `PersonalizationHook`.
    *   Prompt Template: Create a template like: "You are a helpful assistant. Write a single, professional, and friendly opening sentence for a cold email to {FirstName} who works at {Company}. The email's goal is to seek a job opportunity. Mention this interesting fact about their company: {PersonalizationHook}."
    *   LLM Node: Connect the prompt to your chosen LLM.
2.  **Test & Refine:** Test the flow with a few examples from your CSV to ensure the output is high quality.
3.  **Export:** Export the working LangFlow design as Python code. This will serve as the core logic for your script.

**Phase 3: Application Scripting (The Body)**
1.  **Main Script:** Create a `main.py` file.
2.  **Integrate LangChain Logic:** Copy the exported code from LangFlow into a function in your script.
3.  **Build Data Loader:** Write a function using Pandas to read the CSV file into a list of dictionaries.
4.  **Build Email Sender:** Write a function that takes recipient details, a subject line, body text, and a file path for an attachment. This function will use `smtplib` to connect, authenticate, and send the email.
5.  **Create Main Loop:** Write the main execution block that iterates through each contact from the CSV, calls the LangChain function to generate personalized content, constructs the full email body, and then calls the email sender function.
6.  **Implement Safeguards:** Add `time.sleep()` inside the loop for rate limiting and implement `try...except` blocks for robust error handling and logging.

**Phase 4: Testing and Execution (The Launch)**
1.  **Dry Run:** Test the entire script with a small batch of 2-3 of your own email addresses to verify formatting, personalization, and attachment delivery.
2.  **Live Execution:** Once testing is successful, run the script on the full list of 600 contacts. Monitor the console output for logs.
3.  **Review:** After the script completes, check the log file for any failed sends and address them manually if necessary.

***

### **Project TODO List: AI-Powered Email Automation**

#### **Phase 1: Setup & Preparation**
This phase is about gathering all your assets and setting up the technical foundation for the project.

| Task ID | Task Description | Status | Priority | Dependency |
| :--- | :--- | :--- | :--- | :--- |
| **P1.1** | Create the master HR contact list in a CSV file with all required columns. | Not Started | High | - |
| **P1.2** | Write the base template for the cold email. | Not Started | High | - |
| **P1.3** | Finalize the resume and save it as a PDF file (e.g., `resume.pdf`). | Not Started | High | - |
| **P1.4** | For your sending email (e.g., Gmail), generate a secure "App Password". | Not Started | High | - |
| **P1.5** | Sign up for an LLM provider (e.g., OpenAI) and get an API key. | Not Started | High | - |
| **P1.6** | Set up a local Python virtual environment for the project. | Not Started | High | - |
| **P1.7** | Install necessary libraries: `langchain`, `openai`, `pandas`, `python-dotenv`. | Not Started | Medium | P1.6 |
| **P1.8** | Create a `.env` file and store the App Password and API Key in it. | Not Started | High | P1.4, P1.5 |

---

#### **Phase 2: Personalization Logic**
This phase focuses on designing and testing the "brain" of the operation—the AI-powered content generation.

| Task ID | Task Description | Status | Priority | Dependency |
| :--- | :--- | :--- | :--- | :--- |
| **P2.1** | Install and launch LangFlow. | Not Started | Medium | P1.6 |
| **P2.2** | Design the Prompt Template for email personalization within LangFlow. | Not Started | High | P1.2 |
| **P2.3** | Connect the prompt to an LLM node in LangFlow using your API key. | Not Started | High | P1.5, P2.2 |
| **P2.4** | Test the LangFlow chain with sample data from your CSV to verify output quality. | Not Started | High | P1.1, P2.3 |
| **P2.5** | Export the final, working LangFlow chain as Python code. | Not Started | Medium | P2.4 |

---

#### **Phase 3: Application Scripting**
In this phase, you will write the Python script that brings all the components together to perform the automation.

| Task ID | Task Description | Status | Priority | Dependency |
| :--- | :--- | :--- | :--- | :--- |
| **P3.1** | Create the main project script file (e.g., `send_emails.py`). | Not Started | High | - |
| **P3.2** | Write a function to load secrets (keys, passwords) from the `.env` file. | Not Started | High | P1.8 |
| **P3.3** | Write a function to read and parse the HR contacts CSV using Pandas. | Not Started | Medium | P1.1 |
| **P3.4** | Integrate the exported LangFlow code into a personalization function. | Not Started | High | P2.5 |
| **P3.5** | Write the core `send_email` function using `smtplib` to handle connection, auth, and sending with attachments. | Not Started | High | P1.3, P3.2 |
| **P3.6** | Create the main loop to iterate through contacts from the CSV. | Not Started | High | P3.3 |
| **P3.7** | Inside the loop, call the personalization and email sending functions. | Not Started | High | P3.4, P3.5, P3.6 |
| **P3.8** | Implement rate limiting in the loop using `time.sleep(SECONDS)`. | Not Started | High | P3.7 |
| **P3.9** | Add logging to a file (`log.txt`) for successes and failures. | Not Started | Medium | P3.7 |

---

#### **Phase 4: Testing & Execution**
The final phase involves testing your application thoroughly before running it on your full contact list.

| Task ID | Task Description | Status | Priority | Dependency |
| :--- | :--- | :--- | :--- | :--- |
| **P4.1** | Create a smaller test CSV with 2-3 of your own email addresses. | Not Started | High | P1.1 |
| **P4.2** | Run the script with the test CSV to perform a full end-to-end test. | Not Started | High | P3.9, P4.1 |
| **P4.3** | Verify you received the emails, the personalization is correct, and the resume is attached. | Not Started | High | P4.2 |
| **P4.4** | **(FINAL STEP)** Point the script to the full 600-contact CSV and execute. | Not Started | High | P4.3 |
| **P4.5** | Monitor the execution logs. After completion, review the log file for any errors. | Not Started | Medium | P4.4 |