# Comprehensive Guide: Phase 2 - Data Processing and Summarization

## 1. Introduction

Having gathered your CV and job posting data in Phase 1, we now move to Phase 2: Processing and Summarization. The goal here is to transform the raw text data into structured, actionable information. This involves breaking down large texts, extracting key details (like required skills, company information, contact emails), and generating concise summaries of job descriptions.

This phase heavily utilizes LangChain's core strengths: interacting with Large Language Models (LLMs) through prompts, handling text efficiently, and structuring the output. We will cover Text Splitting, Information Extraction, and Summarization techniques using LangChain components.

## 2. Text Splitting (Handling Large Documents)

LLMs have limitations on the amount of text they can process at once (context window). Your CV or detailed job descriptions might exceed this limit. Therefore, the first step is often to split large documents into smaller, manageable chunks.

**Why Split Text?**

*   **Context Window Limits:** To fit text within the LLM's processing capacity.
*   **Performance:** Processing smaller chunks can sometimes be faster or more cost-effective.
*   **Relevance:** Allows focusing on specific parts of a document (e.g., for targeted extraction or embedding).

**LangChain Text Splitters:**

LangChain provides various text splitters. A common and often effective one is the `RecursiveCharacterTextSplitter`.

*   `RecursiveCharacterTextSplitter`: Tries to split text based on a list of characters (e.g., `\n\n`, `\n`, ` `, ``) recursively, aiming to keep related pieces of text (like paragraphs) together as much as possible. It allows specifying `chunk_size` (maximum characters per chunk) and `chunk_overlap` (number of characters to overlap between chunks, helping maintain context).

**Code Snippet (Splitting Loaded Documents):**

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
# Assuming 'cv_documents' and 'job_documents' are lists of Document objects
# loaded in Phase 1 (e.g., using PyPDFLoader, WebBaseLoader, DirectoryLoader)

# --- Configuration ---
# Adjust these values based on the LLM's context window and your needs
CHUNK_SIZE = 1000 # Max characters per chunk
CHUNK_OVERLAP = 150 # Characters to overlap between chunks

# --- Initialize Splitter ---
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    length_function=len, # Function to measure chunk size (usually len)
)

# --- Split the Documents ---
def split_documents(documents):
    """Splits a list of LangChain Documents into smaller chunks."""
    if not documents:
        print("No documents provided to split.")
        return []
    try:
        split_docs = text_splitter.split_documents(documents)
        print(f"Split {len(documents)} document(s) into {len(split_docs)} chunks.")
        return split_docs
    except Exception as e:
        print(f"An error occurred during text splitting: {e}")
        return []

# --- Example Usage (assuming documents are loaded) ---
# cv_chunks = split_documents(cv_documents) 
# job_chunks = split_documents(job_documents) # Split one job doc at a time or all together

# print(f"Example CV chunk 0 content snippet: {cv_chunks[0].page_content[:200]}...")
# print(f"Example CV chunk 0 metadata: {cv_chunks[0].metadata}")

```

**Explanation:**

*   We initialize `RecursiveCharacterTextSplitter` with desired `chunk_size` and `chunk_overlap`.
*   The `split_documents` function takes the list of `Document` objects (from Phase 1 loaders) and uses the splitter's `split_documents` method.
*   The result (`split_docs`) is a new list of `Document` objects, where each object represents a smaller chunk of the original text. The metadata (like the source file) is preserved and often includes information about the chunk's position.

## 3. Information Extraction

Now that we have manageable text chunks (or if the original documents were small enough), we can use LLMs to extract specific pieces of information. For the job search agent, we want details like:

*   Required skills and qualifications
*   Company name
*   Job title
*   Contact information (HR email, hiring manager name - if present)
*   Location
*   Salary range (if mentioned)

**Using LLMs and Prompts for Extraction:**

The core idea is to provide the text (or a chunk) to an LLM along with a carefully crafted prompt instructing it to find and return the desired information, preferably in a structured format.

**LangChain Components:**

*   **LLM/Chat Model:** The brain doing the extraction (e.g., `ChatOpenAI`, `ChatHuggingFace`).
*   **Prompt Template:** To structure the request to the LLM.
*   **Output Parsers (Optional but Recommended):** To convert the LLM's text response into a more usable format like JSON or a Python object. `PydanticOutputParser` or `JsonOutputParser` are useful here.

**Code Snippet (Extracting Job Details using a Chain):**

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI # Or use other models like ChatHuggingFace
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser # Simple string output
# For structured output (better!): Pydantic or JSON parsers
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser
from typing import List, Optional

# --- Setup (Ensure environment variables and imports are correct) ---
load_dotenv()
# Make sure OPENAI_API_KEY is set in your .env file or environment
# Ensure you have run: pip install langchain-openai python-dotenv

# --- Define Desired Output Structure (using Pydantic) ---
class JobDetails(BaseModel):
    """Structured representation of extracted job details."""
    job_title: Optional[str] = Field(description="The title of the job position")
    company_name: Optional[str] = Field(description="The name of the hiring company")
    location: Optional[str] = Field(description="The location(s) of the job")
    required_skills: List[str] = Field(description="A list of key skills, tools, or qualifications mentioned")
    contact_email: Optional[str] = Field(description="Any contact email address found in the text")
    salary_info: Optional[str] = Field(description="Any salary or compensation details mentioned")
    summary_points: List[str] = Field(description="3-5 bullet points summarizing the core responsibilities or requirements")

# --- Initialize LLM and Parser ---
# Select your LLM (ensure API key is available)
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0) # Use temperature=0 for deterministic extraction

# Set up the parser
output_parser = PydanticOutputParser(pydantic_object=JobDetails)

# --- Create the Prompt Template ---
prompt_template = """
Analyze the following job description text and extract the requested information.

{format_instructions}

Job Description Text:
```
{job_description_text}
```

Extracted Information:
"""

prompt = ChatPromptTemplate.from_template(
    prompt_template,
    partial_variables={"format_instructions": output_parser.get_format_instructions()}
)

# --- Build the Extraction Chain ---
extraction_chain = prompt | llm | output_parser

# --- Example Usage (using a sample job description text) ---
# Replace with actual text from your loaded job documents/chunks
sample_job_text = """
Software Engineer - AI Team
TechCorp Inc. - London, UK
We are seeking a talented Software Engineer to join our growing AI team. 
Responsibilities include developing machine learning models and deploying them to production. 
Requires 3+ years of Python experience, familiarity with TensorFlow or PyTorch, and a BS in Computer Science. 
Experience with cloud platforms (AWS/GCP) is a plus. Competitive salary (£60,000 - £80,000) and benefits. 
Please apply via our website or contact hr@techcorp.example.com.
"""

def extract_job_info(text):
    """Runs the extraction chain on the given text."""
    try:
        extracted_data = extraction_chain.invoke({"job_description_text": text})
        return extracted_data
    except Exception as e:
        print(f"Error during extraction: {e}")
        # Consider adding retry logic or fallback (e.g., StrOutputParser)
        return None

# --- Execute Extraction ---
if __name__ == "__main__":
    job_info = extract_job_info(sample_job_text)

    if job_info:
        print("--- Extracted Job Information ---")
        print(f"Title: {job_info.job_title}")
        print(f"Company: {job_info.company_name}")
        print(f"Location: {job_info.location}")
        print(f"Contact Email: {job_info.contact_email}")
        print(f"Salary: {job_info.salary_info}")
        print("Skills:")
        for skill in job_info.required_skills:
            print(f"  - {skill}")
        print("Summary Points:")
        for point in job_info.summary_points:
            print(f"  - {point}")
    else:
        print("Could not extract information.")

```

**Explanation:**

*   **Pydantic Model (`JobDetails`):** Defines the structure we want the LLM to return. Field descriptions help the LLM understand what to extract.
*   **Output Parser (`PydanticOutputParser`):** Takes the Pydantic model and generates formatting instructions for the LLM. It also parses the LLM's string output back into a `JobDetails` Python object.
*   **LLM (`ChatOpenAI`):** The language model instance.
*   **Prompt Template:** Includes placeholders for the `format_instructions` (from the parser) and the `job_description_text`. The instructions guide the LLM to output JSON matching the Pydantic model.
*   **Chain (`extraction_chain`):** Uses the LangChain Expression Language (LCEL) pipe (`|`) operator to link the prompt, LLM, and parser together.
*   **`.invoke()`:** Executes the chain with the input text.
*   **Error Handling:** Basic error handling is included. In a real application, you might want more robust handling (e.g., retries, logging, fallbacks).

## 4. Summarization

Job descriptions can be lengthy. Creating concise summaries helps you quickly grasp the essence of a role.

**LangChain Summarization Chains:**

LangChain offers built-in chains specifically for summarization, designed to handle documents that might exceed the context window.

*   **`load_summarize_chain`:** A convenient function to create summarization chains.
*   **Chain Types:**
    *   `stuff`: Simplest method. Stuffs all text chunks into a single prompt. Fails if the total text exceeds the context window.
    *   `map_reduce`: Processes each chunk individually (map step) to get summaries, then combines these summaries (reduce step) into a final summary. Good for large documents.
    *   `refine`: Processes the first chunk, then iteratively refines the summary by processing subsequent chunks one by one. Can be good for detail but potentially slower.

**Code Snippet (Summarizing Job Documents using `map_reduce`):**

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document # For creating example docs if needed

# --- Setup ---
load_dotenv()
# Ensure OPENAI_API_KEY is set
# Ensure you have run: pip install langchain-openai python-dotenv

# --- Initialize LLM ---
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2) # Slightly creative temp for summary

# --- Load or Prepare Documents to Summarize ---
# Assuming 'job_documents' is a list of Document objects from Phase 1
# Or create sample documents for testing:
job_doc_1_text = """
Senior Data Scientist at Innovate Solutions Inc. (Remote)
We are looking for an experienced Data Scientist to lead projects in predictive analytics and machine learning. 
Key responsibilities involve designing experiments, building models using Python (scikit-learn, XGBoost), and communicating findings to stakeholders. 
Must have 5+ years of experience, a Master's or PhD in a quantitative field, and strong SQL skills. 
Familiarity with big data technologies (Spark) and cloud platforms (Azure) is essential. 
Excellent communication skills required. Join our dynamic team and make an impact!
"""
job_doc_2_text = """
Junior Web Developer - Frontend Focus
Creative Web Ltd. - Austin, TX
Join our team as a Junior Web Developer! You'll work closely with designers to implement user interfaces using HTML, CSS, and JavaScript (React preferred). 
Responsibilities include writing clean code, participating in code reviews, and debugging frontend issues. 
Requires a Bachelor's degree in CS or related field, or equivalent experience/portfolio. 
Strong understanding of web fundamentals and Git is necessary. 
Opportunity to learn and grow. Send resume to careers@creativeweb.example.com.
"""

# Create Document objects if testing directly
job_documents_to_summarize = [
    Document(page_content=job_doc_1_text, metadata={"source": "job1.txt"}),
    Document(page_content=job_doc_2_text, metadata={"source": "job2.txt"})
]

# --- Split Documents if Necessary (especially for long descriptions) ---
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
# Process each document individually for summarization
all_summaries = {}

# --- Create and Run Summarization Chain ---
def summarize_document(doc):
    """Summarizes a single LangChain Document using map_reduce."""
    try:
        # Split the single document into chunks
        chunks = text_splitter.split_documents([doc]) # Pass as a list
        
        # Load the summarization chain (map_reduce is good for potentially large docs)
        # You can customize the map and combine prompts if needed
        summary_chain = load_summarize_chain(llm, chain_type="map_reduce")
        
        # Run the chain on the chunks
        summary = summary_chain.invoke(chunks)
        
        # The result is usually a dictionary, often {'output_text': 'summary...'}
        return summary.get('output_text', 'Summary could not be generated.')
        
    except Exception as e:
        print(f"Error summarizing document {doc.metadata.get('source', 'N/A')}: {e}")
        return "Error during summarization."

# --- Execute Summarization for each job document ---
if __name__ == "__main__":
    print("--- Generating Job Summaries ---")
    for job_doc in job_documents_to_summarize:
        source = job_doc.metadata.get('source', f'doc_{id(job_doc)}') # Get a unique ID
        print(f"Summarizing: {source}")
        summary_text = summarize_document(job_doc)
        all_summaries[source] = summary_text
        print(f"Summary for {source}:\n{summary_text}\n---")

    # 'all_summaries' dictionary now holds summaries keyed by source
    print("Summarization complete.")

```

**Explanation:**

*   We prepare the documents (either loaded from Phase 1 or created as examples).
*   A `TextSplitter` is defined in case individual job descriptions are long.
*   The `summarize_document` function takes a *single* `Document` object.
*   It first splits that document into chunks.
*   `load_summarize_chain(llm, chain_type="map_reduce")` creates the summarization chain.
    *   The `map_reduce` type first runs a prompt on each chunk (map) and then runs a different prompt to combine the individual summaries (reduce).
*   `summary_chain.invoke(chunks)` executes the process.
*   The code iterates through each job document, generates its summary, and stores it.

## 5. Storing Processed Data

After extraction and summarization, you need to store this valuable, structured information. Options include:

*   **Python Objects/Dictionaries:** Keep the Pydantic objects or dictionaries in memory if the script is short-lived.
*   **JSON Files:** Serialize the extracted `JobDetails` objects and summaries into a JSON file for persistence.
*   **CSV Files:** Flatten the data and save it to a CSV.
*   **Databases:** For larger scale or more complex querying, use a database (SQLite for simplicity, or others).

**Recommendation:** Start with saving to JSON files. It maps well to the structured data we've extracted.

## 6. Summary and Next Steps

In Phase 2, you learned how to process raw text data using LangChain. You can now split large documents, extract structured information like skills and contact details using LLMs and Pydantic models, and generate concise summaries of job descriptions using summarization chains.

The next step, **Phase 3: Automated Communication (Email/DM Prep)**, will leverage the structured data (extracted job details, summaries) and your processed CV data to generate personalized email drafts and Direct Message (DM) sequences tailored to specific job opportunities.
