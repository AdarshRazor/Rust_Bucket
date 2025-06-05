# LangChain Job Search Agent: Consolidated Code Snippets

"""
This file contains consolidated Python code snippets from the comprehensive guide 
for building the LangChain Job Search Agent. Refer to the individual phase guides 
for detailed explanations and context.

Remember to:
1. Install all necessary libraries (`pip install ...`).
2. Set up your `.env` file with API keys.
3. Replace placeholder file paths (like "/path/to/your/cv.pdf") with actual paths.
4. Import necessary functions/classes if you split code into multiple files.
"""

import os
import json
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List, Optional

# --- Common Setup ---
load_dotenv() # Load API keys from .env file

# --- Snippets from Phase 1: Data Gathering ---

from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, DirectoryLoader, TextLoader

def load_cv_pdf(file_path):
    """Loads a PDF CV."""
    print(f"Attempting to load CV from: {file_path}")
    if not os.path.exists(file_path):
        print(f"Error: CV file not found at {file_path}")
        return None
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        print(f"Successfully loaded {len(documents)} page(s) from {file_path}")
        return documents
    except Exception as e:
        print(f"An error occurred while loading CV PDF {file_path}: {e}")
        return None

def load_web_page_content(url):
    """Loads content from a single URL."""
    print(f"Attempting to load web page: {url}")
    try:
        loader = WebBaseLoader(url)
        documents = loader.load()
        print(f"Successfully loaded content from {url}")
        return documents
    except Exception as e:
        print(f"An error occurred while loading {url}: {e}")
        return None

def load_jobs_from_text_directory(directory_path):
    """Loads all .txt files from a specified directory."""
    print(f"Attempting to load job files from: {directory_path}")
    if not os.path.isdir(directory_path):
        print(f"Error: Directory not found at {directory_path}")
        return None
    try:
        loader = DirectoryLoader(directory_path, glob="**/*.txt", loader_cls=TextLoader, show_progress=True)
        documents = loader.load()
        print(f"Successfully loaded {len(documents)} job files from {directory_path}")
        return documents
    except Exception as e:
        print(f"An error occurred while loading from {directory_path}: {e}")
        return None

# --- Snippets from Phase 2: Data Processing ---

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI # Assuming OpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.chains.summarize import load_summarize_chain

# Text Splitter Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    length_function=len,
)

def split_langchain_documents(documents):
    """Splits a list of LangChain Documents."""
    if not documents: return []
    print(f"Splitting {len(documents)} documents...")
    try:
        split_docs = text_splitter.split_documents(documents)
        print(f"Split into {len(split_docs)} chunks.")
        return split_docs
    except Exception as e:
        print(f"An error occurred during text splitting: {e}")
        return []

# Pydantic Model for Extraction
class JobDetails(BaseModel):
    job_title: Optional[str] = Field(description="The title of the job position")
    company_name: Optional[str] = Field(description="The name of the hiring company")
    location: Optional[str] = Field(description="The location(s) of the job")
    required_skills: List[str] = Field(description="A list of key skills, tools, or qualifications mentioned")
    contact_email: Optional[str] = Field(description="Any contact email address found in the text")
    salary_info: Optional[str] = Field(description="Any salary or compensation details mentioned")
    summary_points: List[str] = Field(description="3-5 bullet points summarizing the core responsibilities or requirements")

# Extraction Chain Setup
llm_extract = ChatOpenAI(model="gpt-3.5-turbo", temperature=0) # Or your preferred LLM
extraction_output_parser = PydanticOutputParser(pydantic_object=JobDetails)
extraction_prompt_template = """
Analyze the following job description text and extract the requested information.
{format_instructions}
Job Description Text:
```
{job_description_text}
```
Extracted Information:
"""
extraction_prompt = ChatPromptTemplate.from_template(
    extraction_prompt_template,
    partial_variables={"format_instructions": extraction_output_parser.get_format_instructions()}
)
extraction_chain = extraction_prompt | llm_extract | extraction_output_parser

def run_extraction(text):
    """Runs the extraction chain on the given text."""
    print(f"Running extraction on text: {text[:60]}...")
    try:
        extracted_data = extraction_chain.invoke({"job_description_text": text})
        return extracted_data
    except Exception as e:
        print(f"Error during extraction: {e}")
        return None

# Summarization Chain Setup
llm_summarize = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)
summarization_text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)

def run_summarization(doc):
    """Summarizes a single LangChain Document using map_reduce."""
    source = doc.metadata.get("source", "N/A")
    print(f"Running summarization for: {source}")
    try:
        chunks = summarization_text_splitter.split_documents([doc])
        summary_chain = load_summarize_chain(llm_summarize, chain_type="map_reduce")
        summary_result = summary_chain.invoke(chunks)
        return summary_result.get("output_text", "Summary could not be generated.")
    except Exception as e:
        print(f"Error summarizing document {source}: {e}")
        return "Error during summarization."

# --- Snippets from Phase 3: Communication Prep (RAG) ---

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# RAG Setup: CV Vector Store
def create_cv_vector_store(cv_chunks):
    """Creates a FAISS vector store from CV chunks."""
    if not cv_chunks:
        print("No CV chunks provided for vector store creation.")
        return None
    print(f"Creating vector store from {len(cv_chunks)} CV chunks...")
    try:
        embeddings = OpenAIEmbeddings() # Or your preferred embeddings
        vector_store = FAISS.from_documents(cv_chunks, embeddings)
        print("FAISS vector store created successfully.")
        # Optional: Save the index
        # vector_store.save_local("cv_vector_store_faiss")
        return vector_store
    except Exception as e:
        print(f"Error creating vector store: {e}")
        return None

# Helper for formatting retrieved docs
def format_docs_for_prompt(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# RAG Email Drafting Chain Setup
llm_draft = ChatOpenAI(model="gpt-4o", temperature=0.5) # Use a capable model
rag_email_prompt_template = """
Draft a professional and concise email applying for the position described below. 
Highlight how the candidate's experience (from the provided CV context) matches the key requirements. 
Keep the tone enthusiastic and professional. Address it generically if no specific contact name is available.

**Job Details:**
Title: {job_title}
Company: {company_name}
Key Requirements/Summary: {job_summary}
Contact Email (if known): {contact_email}

**Relevant Candidate CV Context:**
{cv_context}

**Email Draft:**
Subject: Application for {job_title} Position - [Your Name]

Dear [Hiring Manager or To Whom It May Concern],

[Draft the email body here...]

Sincerely,
[Your Name]
[Your Contact Information]
"""
rag_email_prompt = ChatPromptTemplate.from_template(rag_email_prompt_template)

def get_rag_email_chain(retriever):
    """Creates the RAG chain for email drafting."""
    return (
        {
            "cv_context": (lambda x: x["job_summary"]) | retriever | format_docs_for_prompt,
            "job_title": (lambda x: x["job_title"]),
            "company_name": (lambda x: x["company_name"]),
            "job_summary": (lambda x: x["job_summary"]),
            "contact_email": (lambda x: x.get("contact_email", "N/A"))
        }
        | rag_email_prompt
        | llm_draft
        | StrOutputParser()
    )

# RAG DM Hook Drafting Chain Setup (Similar structure, different prompt)
rag_dm_hook_prompt_template = """
Draft a short, professional, and engaging opening message (like for LinkedIn) to someone regarding the job opportunity below. 
Reference one specific point from the candidate's CV context that strongly aligns with the job. Avoid generic phrases. 
Keep it concise (2-3 sentences).

**Job Details:**
Title: {job_title}
Company: {company_name}
Key Requirements/Summary: {job_summary}

**Relevant Candidate CV Context:**
{cv_context}

**Target Person Info (Optional):**
Name: {target_name}
Role: {target_role}

**Draft Opening Message:**
"""
rag_dm_hook_prompt = ChatPromptTemplate.from_template(rag_dm_hook_prompt_template)

def get_rag_dm_hook_chain(retriever):
    """Creates the RAG chain for DM hook drafting."""
    return (
        {
            "cv_context": (lambda x: x["job_summary"]) | retriever | format_docs_for_prompt,
            "job_title": (lambda x: x["job_title"]),
            "company_name": (lambda x: x["company_name"]),
            "job_summary": (lambda x: x["job_summary"]),
            "target_name": (lambda x: x.get("target_name", "there")), 
            "target_role": (lambda x: x.get("target_role", ""))
        }
        | rag_dm_hook_prompt
        | llm_draft # Can use same or different LLM
        | StrOutputParser()
    )

# --- Snippets from Phase 4: Orchestration --- 

# Main Orchestration Function (Sequential Script)
def run_job_agent_main(cv_path, jobs_dir, output_json_path):
    """Main function to run the sequential job agent workflow."""
    print("--- Starting Job Agent Workflow --- ")
    
    # 1. Load CV and Create Retriever
    cv_docs = load_cv_pdf(cv_path)
    if not cv_docs: return
    cv_chunks = split_langchain_documents(cv_docs)
    cv_vectorstore = create_cv_vector_store(cv_chunks)
    retriever = None
    if cv_vectorstore:
        retriever = cv_vectorstore.as_retriever(search_kwargs={'k': 3})
        print("CV Retriever created.")
    else:
        print("Warning: Could not create CV vector store. Proceeding without RAG drafting.")

    # 2. Load Job Postings
    job_docs = load_jobs_from_text_directory(jobs_dir)
    if not job_docs:
        print("No job documents found. Exiting.")
        return
        
    # 3. Initialize Drafting Chains (if retriever exists)
    rag_email_chain = get_rag_email_chain(retriever) if retriever else None
    rag_dm_hook_chain = get_rag_dm_hook_chain(retriever) if retriever else None

    # 4. Process Each Job
    all_results = []
    for job_doc in job_docs:
        source_id = job_doc.metadata.get('source', f'doc_{id(job_doc)}')
        print(f"\n--- Processing Job: {source_id} ---")
        job_text = job_doc.page_content
        
        # a. Extract Info
        extracted_info_obj = run_extraction(job_text)
        if not extracted_info_obj:
            print(f"Skipping job {source_id} due to extraction error.")
            continue
        # Convert Pydantic obj to dict for chains/saving
        extracted_info_dict = extracted_info_obj.dict() 
            
        # b. Summarize
        summary = run_summarization(job_doc)
        
        # c. Draft Email
        email_draft = "Not generated (Retriever unavailable)"
        if rag_email_chain:
            try:
                email_draft = rag_email_chain.invoke(extracted_info_dict)
            except Exception as e:
                print(f"Error drafting email for {source_id}: {e}")
                email_draft = "Error during generation."
            
        # d. Draft DM Hook
        dm_hook_draft = "Not generated (Retriever unavailable)"
        if rag_dm_hook_chain:
            try:
                # Add dummy target info if needed by prompt, or adjust chain input
                dm_input = {**extracted_info_dict, "target_name": "Hiring Manager", "target_role": "Recruiter"}
                dm_hook_draft = rag_dm_hook_chain.invoke(dm_input)
            except Exception as e:
                print(f"Error drafting DM for {source_id}: {e}")
                dm_hook_draft = "Error during generation."
            
        # e. Store results
        all_results.append({
            "source": source_id,
            "extracted_details": extracted_info_dict,
            "summary": summary,
            "draft_email": email_draft,
            "draft_dm_hook": dm_hook_draft
        })
        
    # 5. Save Results
    print(f"\n--- Workflow Complete. Saving {len(all_results)} results to {output_json_path} ---")
    try:
        with open(output_json_path, 'w') as f:
            json.dump(all_results, f, indent=4)
        print("Results saved successfully.")
    except Exception as e:
        print(f"Error saving results to JSON: {e}")

# --- Example Execution --- 
if __name__ == "__main__":
    # Define actual paths here
    MY_CV_PATH = "/path/to/your/cv.pdf" # <<< REPLACE
    MY_JOBS_DIR = "/path/to/your/saved/jobs/" # <<< REPLACE
    MY_OUTPUT_PATH = "/home/ubuntu/job_agent_results.json"

    # Basic check if paths exist (replace with actual file/dir creation if needed for testing)
    if not os.path.exists(MY_CV_PATH):
        print(f"Error: CV Path not found: {MY_CV_PATH}")
    elif not os.path.isdir(MY_JOBS_DIR):
         print(f"Error: Jobs Directory not found: {MY_JOBS_DIR}")
    else:
        run_job_agent_main(MY_CV_PATH, MY_JOBS_DIR, MY_OUTPUT_PATH)


