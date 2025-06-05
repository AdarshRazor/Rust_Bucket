# Comprehensive Guide: Phase 4 - Orchestration and Planning

## 1. Introduction

Welcome to the final implementation phase, Phase 4: Orchestration and Planning. In the previous phases, we built individual components for gathering data (Phase 1), processing and summarizing it (Phase 2), and drafting communications (Phase 3). Now, we need to connect these pieces into a coherent workflow and manage the overall process.

Orchestration involves defining how the agent moves from one step to the next. Should it process jobs one by one? Should it gather all data first, then process, then draft? LangChain offers tools like **Chains** and **Agents** to manage these workflows.

Planning, in the context of your request, involves organizing the outputs (like drafted emails, summaries) and potentially scheduling or suggesting next steps for the user (e.g., "Review these 5 email drafts for jobs X, Y, Z," or "Schedule time to manually send DMs").

## 2. Orchestration Options in LangChain

There are several ways to orchestrate the workflow, ranging from simple sequential execution to more complex, LLM-driven decision-making.

**Option 1: Simple Sequential Scripting (Manual Orchestration)**

*   **Concept:** Write a single Python script that calls the functions/chains developed in previous phases in a fixed order.
*   **Example Flow:**
    1.  Load CV.
    2.  Load job data (e.g., from saved files or web pages one by one).
    3.  For each job:
        a.  Split job description text.
        b.  Extract job details (using the extraction chain).
        c.  Summarize job description (using the summarization chain).
        d.  Draft email (using the RAG email chain).
        e.  Draft DM hook (using the RAG DM chain).
    4.  Collect all results (extracted info, summaries, drafts).
    5.  Present results to the user (e.g., print to console, save to files).
*   **Pros:** Simple to implement and understand, full control over the flow.
*   **Cons:** Not very flexible; doesn't use LangChain's advanced orchestration features; requires manual modification to change the flow.
*   **LangChain Use:** Primarily uses the individual chains built in Phases 2 & 3.

**Option 2: LangChain Sequential Chains**

*   **Concept:** Use LangChain's `SequentialChain` or `SimpleSequentialChain` to link multiple chains together, where the output of one chain becomes the input for the next.
*   **Example:** A chain that takes a job description URL, loads the content, extracts details, and then summarizes the extracted details.
*   **Pros:** Encapsulates a linear workflow within LangChain.
*   **Cons:** Only suitable for strictly linear processes; managing complex inputs/outputs between chains can be tricky.
*   **LangChain Use:** `SequentialChain`, individual component chains.

**Option 3: LangChain Agents (LLM-Driven Orchestration)**

*   **Concept:** Use an LLM as a reasoning engine to decide which actions (Tools) to take and in what order to achieve a goal. You define a set of available tools (e.g., `load_cv_tool`, `find_jobs_tool`, `extract_details_tool`, `draft_email_tool`) and give the agent an objective.
*   **Tools:** These are functions that the agent can call. You would wrap the core logic from Phases 1-3 into tools.
*   **Example Flow:**
    1.  User gives objective: "Find Python developer jobs in London, summarize them, and draft application emails using my CV."
    2.  Agent decides to use `find_jobs_tool` with query "Python developer London".
    3.  Tool returns a list of job URLs/data.
    4.  Agent iterates through jobs:
        a.  Decides to use `extract_details_tool` on job data.
        b.  Decides to use `draft_email_tool` with extracted details and CV context (implicitly using RAG via the tool).
    5.  Agent compiles results and presents them.
*   **Pros:** Highly flexible, can adapt to different situations, can handle errors or unexpected inputs more dynamically.
*   **Cons:** More complex to set up and debug; agent behavior can sometimes be unpredictable; potentially higher LLM usage costs.
*   **LangChain Use:** `AgentExecutor`, `Tools`, LLMs, potentially `Memory`.

**Recommendation for Beginners:** Start with **Option 1 (Simple Sequential Scripting)**. It allows you to ensure each component works correctly and gives you a clear understanding of the end-to-end process. Once that's working, you can explore wrapping the functionality into **Tools** and experimenting with **Option 3 (LangChain Agents)** for more advanced capabilities.

## 3. Implementing Simple Sequential Orchestration

Let's outline a Python script structure based on Option 1, assuming you have saved the core logic from previous phases into functions or reusable chain objects.

```python
import os
import json
from dotenv import load_dotenv

# --- Import functions/chains from previous phases --- 
# (These would be in separate .py files or defined earlier in this script)
# from phase1_loader import load_cv, load_jobs_from_directory # Example imports
# from phase2_processor import split_documents, extract_job_info, summarize_document # Example imports
# from phase3_drafting import get_cv_vector_store, rag_email_chain_refined, rag_dm_hook_chain # Example imports

# --- Placeholder functions (replace with actual imports/definitions) ---
def load_cv(path): 
    print(f"[Placeholder] Loading CV from {path}")
    # Returns list of Document objects or None
    from langchain_core.documents import Document
    if os.path.exists(path):
        return [Document(page_content="Sample CV content: Python, LangChain expert.", metadata={"source": path})]
    return None

def load_jobs_from_directory(path):
    print(f"[Placeholder] Loading jobs from {path}")
    # Returns list of Document objects or None
    from langchain_core.documents import Document
    # Simulate loading two job files
    job_docs = [
        Document(page_content="Job 1: Software Engineer at TechCorp. Requires Python.", metadata={"source": os.path.join(path, "job1.txt")}),
        Document(page_content="Job 2: Data Analyst at DataInc. Requires SQL and Python.", metadata={"source": os.path.join(path, "job2.txt")})
    ]
    return job_docs

def split_documents(docs): 
    print(f"[Placeholder] Splitting {len(docs)} documents")
    # Returns list of chunked Document objects
    return docs # Assume no splitting needed for placeholder

def extract_job_info(text): 
    print(f"[Placeholder] Extracting info from text: {text[:50]}...")
    # Returns a dictionary (or Pydantic object) with extracted details
    # Simulate extraction based on content
    details = {
        'job_title': 'Software Engineer' if 'Software Engineer' in text else 'Data Analyst',
        'company_name': 'TechCorp' if 'TechCorp' in text else 'DataInc',
        'required_skills': ['Python'] + (['SQL'] if 'SQL' in text else []),
        'contact_email': None,
        'salary_info': None,
        'summary_points': ['Responsibility 1', 'Responsibility 2']
    }
    return type('JobDetails', (object,), details)() # Simple object simulation

def summarize_document(doc): 
    print(f"[Placeholder] Summarizing doc: {doc.metadata['source']}")
    # Returns summary string
    return f"Summary for {doc.metadata['source']}: Focuses on {doc.page_content.split('Requires ')[-1]}"

def get_cv_vector_store(cv_chunks): 
    print(f"[Placeholder] Getting CV vector store from {len(cv_chunks)} chunks")
    # Returns a retriever object or None
    # Simulate a simple retriever
    class MockRetriever:
        def invoke(self, query):
            return [type('Document', (object,), {'page_content': 'Relevant CV snippet about Python.'})()]
    if cv_chunks: return MockRetriever()
    return None

def rag_email_chain_refined(job_info_dict, retriever): 
    print(f"[Placeholder] Drafting email for: {job_info_dict['job_title']}")
    # Returns email draft string
    cv_context = retriever.invoke("query")[0].page_content
    return f"Subject: Application for {job_info_dict['job_title']}\n\nDear Hiring Manager,\n\nBased on my experience in {cv_context}, I am applying...\n\nSincerely,\n[Your Name]"

def rag_dm_hook_chain(job_info_dict, retriever): 
    print(f"[Placeholder] Drafting DM for: {job_info_dict['job_title']}")
    # Returns DM draft string
    cv_context = retriever.invoke("query")[0].page_content
    return f"Hi [Target Name], saw the {job_info_dict['job_title']} role. My background in {cv_context} seems relevant."

# --- Configuration ---
load_dotenv()
CV_FILE_PATH = "/path/to/your/cv.pdf" # Replace!
JOBS_DIRECTORY = "/path/to/your/saved/jobs/" # Replace!
OUTPUT_FILE = "/home/ubuntu/job_agent_results.json"

# --- Main Orchestration Script ---
def run_job_agent():
    print("--- Starting Job Agent Workflow ---")
    
    # 1. Load CV
    cv_docs = load_cv(CV_FILE_PATH)
    if not cv_docs:
        print("Error: Could not load CV. Exiting.")
        return
    cv_chunks = split_documents(cv_docs) # Split if needed
    
    # 2. Setup CV Retriever (RAG)
    retriever = get_cv_vector_store(cv_chunks)
    if not retriever:
        print("Error: Could not create CV vector store. Proceeding without RAG for drafting.")
        # Handle case where retriever is None in drafting functions if necessary

    # 3. Load Job Postings
    job_docs = load_jobs_from_directory(JOBS_DIRECTORY)
    if not job_docs:
        print("No job documents found or loaded. Exiting.")
        return
        
    # 4. Process Each Job
    results = []
    for job_doc in job_docs:
        print(f"\n--- Processing Job: {job_doc.metadata.get('source', 'Unknown')} ---")
        job_text = job_doc.page_content
        source_id = job_doc.metadata.get('source', f'doc_{id(job_doc)}')
        
        # a. Extract Info
        extracted_info_obj = extract_job_info(job_text)
        if not extracted_info_obj:
            print(f"Skipping job {source_id} due to extraction error.")
            continue
        # Convert Pydantic/object to dict for easier saving
        extracted_info = vars(extracted_info_obj) if hasattr(extracted_info_obj, '__dict__') else extracted_info_obj 
            
        # b. Summarize
        summary = summarize_document(job_doc)
        
        # c. Draft Email (using RAG if retriever available)
        email_draft = "Not generated (Retriever unavailable)"
        if retriever:
            email_draft = rag_email_chain_refined(extracted_info, retriever)
            
        # d. Draft DM Hook (using RAG if retriever available)
        dm_hook_draft = "Not generated (Retriever unavailable)"
        if retriever:
            dm_hook_draft = rag_dm_hook_chain(extracted_info, retriever)
            
        # e. Store results for this job
        results.append({
            "source": source_id,
            "extracted_details": extracted_info,
            "summary": summary,
            "draft_email": email_draft,
            "draft_dm_hook": dm_hook_draft
        })
        
    # 5. Save Results
    print(f"\n--- Workflow Complete. Saving {len(results)} results to {OUTPUT_FILE} ---")
    try:
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(results, f, indent=4)
        print("Results saved successfully.")
    except Exception as e:
        print(f"Error saving results to JSON: {e}")
        # Optionally print results to console as fallback
        # print(json.dumps(results, indent=4))

# --- Run the Agent ---
if __name__ == "__main__":
    # Create dummy files/dirs if they don't exist for placeholder execution
    if not os.path.exists(os.path.dirname(CV_FILE_PATH)): os.makedirs(os.path.dirname(CV_FILE_PATH), exist_ok=True)
    if not os.path.exists(CV_FILE_PATH): open(CV_FILE_PATH, 'a').close()
    if not os.path.exists(JOBS_DIRECTORY): os.makedirs(JOBS_DIRECTORY, exist_ok=True)
    if not os.path.exists(os.path.join(JOBS_DIRECTORY, "job1.txt")): open(os.path.join(JOBS_DIRECTORY, "job1.txt"), 'a').close()
    if not os.path.exists(os.path.join(JOBS_DIRECTORY, "job2.txt")): open(os.path.join(JOBS_DIRECTORY, "job2.txt"), 'a').close()
        
    run_job_agent()

```

**Explanation:**

*   **Imports:** Bring in the necessary functions/chains (replace placeholders with actual imports).
*   **Configuration:** Set file paths.
*   **`run_job_agent()`:** The main orchestration function.
    *   Loads CV and sets up the RAG retriever.
    *   Loads job documents.
    *   Iterates through each job document.
    *   Calls the extraction, summarization, and drafting functions/chains for each job.
    *   Collects all results in a list of dictionaries.
    *   Saves the final results to a JSON file.
*   **Placeholders:** The script uses placeholder functions to be runnable. You **must** replace these with your actual implemented functions/chains from the previous phases.
*   **Error Handling:** Basic checks are included (e.g., if CV loading fails, if retriever fails).

## 4. Planning and Presenting Outputs

The script above saves the results to a JSON file. This file acts as your primary output, containing the structured information and drafts for each processed job.

**How to Use the Output:**

1.  **Review the JSON:** Open `job_agent_results.json` to see the details for each job.
2.  **Prioritize:** Based on the summaries and extracted details, decide which jobs are most promising.
3.  **Refine Drafts:** Copy the `draft_email` and `draft_dm_hook` content, paste them into your email client or LinkedIn, and **edit them carefully** before sending. Add personalization, check tone, and correct any errors.
4.  **Manual Sending:** Send the finalized emails and DMs manually.

**Further Planning Enhancements (Optional):**

*   **Scoring/Ranking:** Modify the script to add a simple scoring mechanism based on keyword matches between the job description and your CV (perhaps using the RAG retrieval scores) to help prioritize jobs.
*   **Status Tracking:** Add a field to the output JSON (e.g., `"status": "pending_review"`) and manually update it as you apply or contact people.
*   **Simple UI:** Use libraries like `Streamlit` or `Gradio` to build a basic web interface to display the results more interactively instead of just using a JSON file.

## 5. Exploring LangChain Agents (Advanced)

If you want to explore agent-based orchestration:

1.  **Define Tools:** Wrap your core functions (`load_cv`, `extract_job_info`, `summarize_document`, `rag_email_chain_refined`, etc.) into LangChain `Tool` objects. Each tool needs a name, description (crucial for the agent to know when to use it), and the function itself.
2.  **Initialize Agent:** Choose an agent type (e.g., `create_openai_functions_agent`) and provide it with an LLM and your list of tools.
3.  **Create AgentExecutor:** This runs the agent loop (think, act, observe).
4.  **Run with Objective:** Invoke the `AgentExecutor` with a high-level objective.

**Conceptual Code (Agent Setup):**

```python
# --- Conceptual Agent Setup (Requires more setup) ---
# from langchain.agents import Tool, create_openai_functions_agent, AgentExecutor
# from langchain_openai import ChatOpenAI
# from langchain import hub # To pull agent prompts

# # 1. Define Tools (Wrap your functions)
# tools = [
#     Tool(
#         name="JobInfoExtractor",
#         func=extract_job_info, # Assumes extract_job_info takes text and returns the object/dict
#         description="Extracts structured details (title, company, skills, email, summary) from job description text. Input is the raw job text."
#     ),
#     Tool(
#         name="JobSummarizer",
#         func=summarize_document, # Assumes summarize_document takes a Document object
#         description="Generates a concise summary of a job description Document object. Input is the Document object."
#     ),
#     Tool(
#         name="EmailDrafter",
#         func=lambda job_info_dict: rag_email_chain_refined(job_info_dict, retriever), # Need retriever in scope
#         description="Drafts a personalized application email using extracted job details and candidate CV context. Input is a dictionary of extracted job details."
#     ),
#     # Add tools for loading CV, loading jobs, etc.
# ]

# # 2. Initialize LLM and Agent Prompt
# llm = ChatOpenAI(model="gpt-4o", temperature=0)
# agent_prompt = hub.pull("hwchase17/openai-functions-agent") # Example prompt

# # 3. Create Agent
# agent = create_openai_functions_agent(llm, tools, agent_prompt)

# # 4. Create Agent Executor
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True) # verbose=True shows agent thinking

# # 5. Run Agent
# if __name__ == "__main__" and 'retriever' in locals() and retriever: # Ensure retriever is ready
#     objective = "Process the job found in '/path/to/your/saved/jobs/job1.txt', extract details, summarize it, and draft an application email using the CV."
#     try:
#         agent_result = agent_executor.invoke({"input": objective})
#         print("--- Agent Result ---")
#         print(agent_result.get('output'))
#     except Exception as e:
#         print(f"Agent execution failed: {e}")

```

This agent setup is more involved and requires careful tool definition and potentially prompt engineering.

## 6. Summary

Phase 4 focused on orchestrating the components built in earlier phases. We primarily detailed a simple sequential scripting approach, which is recommended for beginners, culminating in a JSON file containing processed job data and communication drafts. We also touched upon presenting these outputs and conceptually introduced the more advanced LangChain Agent approach.

With this phase, the core implementation of your job search agent guide is complete. The next steps involve writing supporting documents (Challenges, Alternatives), compiling resources (Mindmap, Todos), validating the content, and finally delivering the comprehensive guide.
