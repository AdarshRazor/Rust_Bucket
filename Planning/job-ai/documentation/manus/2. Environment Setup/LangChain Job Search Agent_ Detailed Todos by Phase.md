# LangChain Job Search Agent: Detailed Todos by Phase

This document provides a checklist of tasks for you to follow as you build your LangChain Job Search Agent, based on the comprehensive guides provided.

## Phase 0: Setup & Foundation

*   [ ] **Install Python:** Ensure you have Python 3.8+ installed. Verify with `python3 --version`.
*   [ ] **Create Project Directory:** Make a dedicated folder for this project (e.g., `mkdir langchain-job-agent && cd langchain-job-agent`).
*   [ ] **Create Virtual Environment:** Set up isolation with `python3 -m venv venv`.
*   [ ] **Activate Virtual Environment:** Use `source venv/bin/activate` (Linux/macOS) or `.\venv\Scripts\activate` (Windows).
*   [ ] **Install Core Libraries:** Run `pip install langchain python-dotenv`.
*   [ ] **Install LLM Integration:** Choose your LLM provider and install the corresponding library (e.g., `pip install langchain-openai` for OpenAI, `pip install langchain-huggingface` for Hugging Face Hub).
*   [ ] **Install Document Loaders:** Install necessary loaders (e.g., `pip install pypdf` for PDFs, `pip install beautifulsoup4` for web pages).
*   [ ] **Install Vector Store & Embeddings:** Install FAISS (`pip install faiss-cpu`) and the embedding integration matching your LLM (already covered if using `langchain-openai`, may need `langchain-huggingface` or others).
*   [ ] **Obtain API Keys:** Get keys for your chosen LLM provider (and LangSmith, if using).
*   [ ] **Create `.env` File:** Create a `.env` file in your project root.
*   [ ] **Add API Keys to `.env`:** Add keys like `OPENAI_API_KEY="your_key"`.
*   [ ] **Add `.env` to `.gitignore`:** If using Git, ensure `.env` is listed in your `.gitignore` file.
*   [ ] **(Optional) Setup LangSmith:** Install `pip install langsmith`, get API key, and add LangSmith variables to `.env` (`LANGCHAIN_TRACING_V2`, `LANGCHAIN_ENDPOINT`, `LANGCHAIN_API_KEY`, `LANGCHAIN_PROJECT`).
*   [ ] **Review Guides:** Read `introduction_to_langchain.md`, `environment_setup_guide.md`, `framework_blueprint.md`, and `architecture_diagram.md`.

## Phase 1: Data Gathering

*   [ ] **Locate Your CV:** Identify the path to your CV file (PDF or DOCX).
*   [ ] **Update CV Path in Script:** Modify the `CV_FILE_PATH` variable in your data gathering script (e.g., based on `phase1_data_gathering_guide.md` code).
*   [ ] **Run CV Loading Script:** Execute the script to test loading your CV into LangChain `Document` objects.
*   [ ] **Choose Job Data Strategy:** Decide on your method (Manual Collection + Text Files/CSV is recommended). **Avoid direct LinkedIn scraping.**
*   [ ] **Collect Initial Job Data:** Manually gather details for 2-3 relevant job postings.
*   [ ] **Save Job Data:** Store the collected data in your chosen format (e.g., create a `saved_jobs` directory and save descriptions as `.txt` files).
*   [ ] **Update Job Data Path in Script:** Modify the `JOBS_DIRECTORY` (or equivalent) variable in your script.
*   [ ] **Run Job Loading Script:** Execute the script to test loading job data into LangChain `Document` objects.
*   [ ] **Review Loaded Data:** Briefly check the `page_content` of the loaded CV and job `Document` objects to ensure they look correct.

## Phase 2: Data Processing & Summarization

*   [ ] **Implement Text Splitting:** Add the `RecursiveCharacterTextSplitter` code (from `phase2_data_processing_guide.md`) to your script if needed (especially for long CVs or job descriptions).
*   [ ] **Define Pydantic Model:** Create the `JobDetails` Pydantic class to define the structure for extracted information.
*   [ ] **Set Up Extraction Chain:**
    *   Initialize your chosen LLM (`ChatOpenAI`, etc.).
    *   Initialize the `PydanticOutputParser` with your `JobDetails` model.
    *   Create the `ChatPromptTemplate` for extraction, including format instructions.
    *   Combine into the `extraction_chain` using LCEL (`|`).
*   [ ] **Test Extraction Chain:** Run the `extraction_chain.invoke()` method with sample job text (or text from your loaded job documents) and print the results. Debug the prompt or model if needed.
*   [ ] **Set Up Summarization Chain:**
    *   Initialize the LLM (can be the same or different from extraction).
    *   Use `load_summarize_chain` (e.g., with `chain_type="map_reduce"`).
*   [ ] **Test Summarization Chain:** Run the `summarize_document` function (from the guide) on your loaded job `Document` objects. Print the summaries. Adjust `chain_type` or prompts if needed.
*   [ ] **Decide on Storage:** Choose how to store processed results (e.g., Python dictionaries in memory, JSON file).

## Phase 3: Communication Preparation (RAG)

*   [ ] **Implement CV Loading & Splitting:** Ensure the code to load and split your CV into chunks is ready (can reuse from Phase 1/2).
*   [ ] **Set Up RAG Components:**
    *   Initialize the `OpenAIEmbeddings` (or other) model.
    *   Create the `FAISS` vector store using `FAISS.from_documents(cv_chunks, embeddings)`.
    *   (Optional) Implement `save_local` / `load_local` for the vector store to avoid rebuilding.
    *   Create the `retriever` using `cv_vectorstore.as_retriever()`.
*   [ ] **Test Retriever:** Perform a `similarity_search` or invoke the retriever with a sample query related to your skills to ensure it returns relevant CV chunks.
*   [ ] **Set Up Email Drafting Chain:**
    *   Define the `email_prompt` template.
    *   Build the `rag_email_chain` using LCEL, ensuring the retriever is correctly queried (e.g., using the job summary) and its output is formatted (`format_docs`).
*   [ ] **Test Email Drafting Chain:** Invoke the chain with sample extracted job details (from Phase 2). Review the generated draft.
*   [ ] **Set Up DM Hook Drafting Chain:**
    *   Define the `dm_hook_prompt` template.
    *   Build the `rag_dm_hook_chain` similarly to the email chain.
*   [ ] **Test DM Hook Drafting Chain:** Invoke the chain with sample job details and target info. Review the generated draft.
*   [ ] **Refine Prompts:** Adjust the email and DM prompts if the drafts are not satisfactory (e.g., tone, length, detail level).

## Phase 4: Orchestration & Planning

*   [ ] **Choose Orchestration Method:** Decide between Simple Sequential Script (recommended) or Agent.
*   [ ] **Structure Main Script:** Create a main Python script (`main.py` or similar).
*   [ ] **Import/Define Functions:** Bring in all the necessary functions and chain objects from the previous phases (or define them within the main script).
*   [ ] **Implement Sequential Flow (if using Method 1):**
    *   Add code to load CV and set up retriever.
    *   Add code to load job documents.
    *   Create a loop to iterate through job documents.
    *   Inside the loop, call extraction, summarization, and drafting functions/chains.
    *   Store the results for each job in a list.
*   [ ] **Implement Output Saving:** Add code to save the collected results to a JSON file (`json.dump`).
*   [ ] **Add Configuration:** Place file paths and other settings at the top of the script or in a separate config file.
*   [ ] **Add Basic Error Handling:** Include `try...except` blocks around major steps (file loading, API calls).
*   [ ] **Run End-to-End:** Execute the main script to process your sample job data from start to finish.
*   [ ] **Review Output File:** Check the generated JSON file (`job_agent_results.json`) for completeness and correctness.
*   [ ] **Plan User Workflow:** Understand how you will use the output JSON (review, prioritize, refine drafts, send manually).
*   [ ] **(Optional) Explore Agents:** If comfortable, try wrapping functions into `Tools` and setting up a basic `AgentExecutor`.

## Post-Development

*   [ ] **Review Challenges & Best Practices:** Read `challenges_best_practices.md`.
*   [ ] **Consider Alternatives:** Read `alternatives.md`.
*   [ ] **Refine and Iterate:** Improve prompts, add error handling, or enhance features based on testing.
*   [ ] **Organize Code:** Ensure your code is well-commented and organized into logical files/functions.
