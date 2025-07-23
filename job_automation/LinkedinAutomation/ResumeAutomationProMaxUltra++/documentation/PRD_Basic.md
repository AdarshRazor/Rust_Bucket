# **Process Requirement Document (PRD): Bulk Email Automation with Smart Tracking**

**1. Project Overview**

*   **Project Name:** Bulk Email Automation with Smart Tracking
*   **Problem:** Manually sending a standard recruiting email to a large list of HR contacts is repetitive and inefficient. It's difficult to track who has been contacted, especially if the process is interrupted.
*   **Goal:** To build a Python application that sends a single, standard email with a resume attached to a list of HR contacts from a CSV file. The application will smartly personalize the salutation (e.g., "Hi, [Name]" or "Hi, Team") and, after each successful send, update the source CSV file with a "Sent" status to maintain a clear record.

**2. Core Features**

*   **F1: CSV Data Handling (Read/Write):** The system must read a list of email addresses from a CSV file. Critically, after successfully sending an email, it must write back to that same CSV, adding a "Sent" status in a new `Comments` column for the corresponding email address.
*   **F2: Smart Salutation (AI Bonus):** Before sending, the system will analyze the recipient's email address.
    *   For personal emails (e.g., `anujbhatiya@company.com`), it will extract the first name ("Anuj").
    *   For generic emails (e.g., `hr@company.com`, `careers@...`), it will use the word "Team".
    This ensures a minor but effective level of personalization.
*   **F3: Resume Attachment:** The system must attach a specified resume file (PDF) to every email.
*   **F4: Standardized Content Delivery:** The system will use a single, pre-written email template for the body of all emails, inserting only the smart salutation.
*   **F5: Secure & Reliable Email Sending:** The application will use a standard SMTP provider (like Gmail or Outlook) to dispatch emails. Credentials will be managed securely via a `.env` file.
*   **F6: Resilient & Stateful Operation:** The script will check the `Comments` column before sending. If an email has already been marked as "Sent", it will be skipped. This allows the script to be stopped and restarted without sending duplicates.
*   **F7: Rate Limiting:** The system will include a mandatory delay between sending emails to avoid being flagged as spam by email providers.

**3. Technical Stack**

*   **Programming Language:** Python 3.9+
*   **Core Libraries:**
    *   **Pandas:** Essential for both reading the initial CSV and for updating and saving it with the "Sent" status.
    *   **LangChain & LLM Provider (e.g., OpenAI):** Used specifically for the "Smart Salutation" feature. An LLM is excellent at parsing varied email formats to extract a name or identify a generic address.
    *   **SMTPLIB & Email:** Standard Python libraries for constructing the email with attachments and sending via an SMTP server.
    *   **Python-Dotenv:** To securely manage sensitive credentials like your email App Password and LLM API Key.

**4. Project Phases & Steps**

**Phase 1: Setup and Preparation**
1.  **Data Preparation:** Create a CSV file named `contacts.csv` with a single header: `EmailAddress`. Populate it with the HR emails.
2.  **Environment Setup:** Create a Python virtual environment, install the required libraries, and create a `.env` file for your credentials (Email App Password, LLM API Key).
3.  **Content Creation:** Write your single, standard email body in a text file or as a string in your script. Finalize your resume PDF.

**Phase 2: Scripting & Core Logic**
1.  **Main Script:** Create a Python script (e.g., `run_outreach.py`).
2.  **Load Data:** Use Pandas to load `contacts.csv` into a DataFrame. Check if a `Comments` column exists; if not, create it.
3.  **Implement Smart Salutation:** Write a function that takes an email address, uses a LangChain prompt to an LLM to extract the first name or identify it as "Team", and returns the result.
4.  **Implement Email Sender:** Write a robust function using `smtplib` that sends an email with an attachment.
5.  **Create Main Loop:** Iterate through the rows of the Pandas DataFrame.
    *   **Check Status:** In the loop, first check if the `Comments` column for the current row is already "Sent". If so, print a "Skipping" message and continue to the next contact.
    *   **Process & Send:** If not sent, call the Smart Salutation function, construct the full email, and send it using the email sender function within a `try...except` block.
    *   **Update DataFrame:** If the email is sent successfully (in the `try` block), update the `Comments` column for that row in the DataFrame to "Sent". If it fails (in the `except` block), update it to "Failed".
    *   **Rate Limit:** Include a `time.sleep()` at the end of each loop iteration.
6.  **Save Progress:** After the loop completes, use `df.to_csv('contacts.csv', index=False)` to save the updated DataFrame back to the original file, preserving the tracking information.

**Phase 3: Testing and Execution**
1.  **Dry Run:** Test the entire script with a CSV containing 2-3 of your own email addresses.
2.  **Verification:** Confirm you received the emails. Check that the salutation is correct ("Hi, [Your Name]") and the resume is attached. Most importantly, open `contacts.csv` and verify that the `Comments` column is now filled with "Sent".
3.  **Live Run:** Once verified, run the script with the full list of 600 contacts. You can monitor the progress from the script's console output.

***

### **Project TODO List (Separated by Phase)**

#### **Phase 1: Setup & Preparation**

| Task ID | Task Description | Status | Priority | Dependency | Comments |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **P1.1** | Create `contacts.csv` with one column: `EmailAddress`. | ✅ Completed | High | - | Created in `/emails/contacts.csv` |
| **P1.2** | Write the standard email content and finalize the resume PDF. | ✅ Completed | High | - | Created in `/content/email_template.html` and `/content/AdarshAnand_FullStack_Resume.pdf` |
| **P1.3** | Generate a secure "App Password" for your sending email account. | ✅ Completed | High | - | Generated in `.env.local` - `APP_PASSWORD_NAME` and `APP_PASSWORD` |
| **P1.4** | Get an API key from an LLM provider (e.g., Gemini). | ✅ Completed | High | - | Generated in `.env.local` - `GEMINI_API_KEY` |
| **P1.5** | Set up a Python virtual environment and install `pandas`, `langchain`, `langsmith`, `google-genai`, `python-dotenv`. | ✅ Completed | High | - | Created in `requirements.txt` |
| **P1.6** | Create a `.env` file and store your App Password and API Key in it. | ✅ Completed | High | P1.3, P1.4 | Created in `.env.local` |

---

#### **Phase 2: Scripting & Core Logic**

| Task ID | Task Description | Status | Priority | Dependency | Comments |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **P2.1** | Create the main Python script file | ✅ Completed | High | P1.5 | Created `main.py` |
| **P2.2** | Write a function to load secrets from the `.env` file. | ✅ Completed | High | P1.6 |
| **P2.3** | Write a function using Pandas to load `contacts.csv` into a DataFrame. | ✅ Completed | High | P1.1 |
| **P2.4** | Implement the "Smart Salutation" function using LangChain and your LLM API key. | ✅ Completed | High | P1.4, P2.2 | Manually created the `FirstName` column in csv file and importing |
| **P2.5** | Implement the `send_email` function using `smtplib` for sending mail with attachments in `outreach.py` | ✅ Completed | High | P1.2, P2.2 | Created in `outreach.py` |
| **P2.6** | Build the main loop to iterate through the DataFrame. | ✅ Completed | Medium | P2.3 | 
| **P2.7** | Add logic inside the loop to check the `Comments` column and skip if "Sent". | ✅ Completed | High | P2.6 |
| **P2.8** | Add a `try...except` block for sending and updating the DataFrame with "Sent" or "Failed". | Not Started | High | P2.5, P2.7 |
| **P2.9** | Add `time.sleep()` in the loop for rate limiting for 10 seconds | Not Started | High | P2.8 |
| **P2.10** | Add the final line of code to save the updated DataFrame back to `contacts.csv`. | Not Started | High | P2.8 |

---

#### **Phase 3: Testing & Execution**

| Task ID | Task Description | Status | Priority | Dependency | Comments |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **P3.1** | Create a `test_contacts.csv` with 2-3 of your personal emails for a dry run. | Not Started | High | P1.1 |
| **P3.2** | Run the script on the test file to perform a full end-to-end test. | Not Started | High | P2.10, P3.1 |
| **P3.3** | Verify email receipt, salutation, attachment, and that the test CSV is updated with "Sent". | Not Started | High | P3.2 |
| **P3.4** | **(FINAL STEP)** Point the script to the real `contacts.csv` and execute. | Not Started | High | P3.3 |
| **P3.5** | Monitor the execution. After completion, check the final `contacts.csv` file for status. | Not Started | Medium | P3.4 |