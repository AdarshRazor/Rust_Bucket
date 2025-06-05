# Comprehensive Guide: Phase 3 - Automated Communication (Email/DM Prep)

## 1. Introduction

Welcome to Phase 3. Now that you have processed your CV and extracted structured information from job postings (Phase 2), the next step is to leverage this data to prepare personalized communications. This phase focuses on using LangChain to draft:

1.  **Emails:** Tailored emails for applying to jobs or contacting HR personnel.
2.  **Direct Messages (DMs):** Sequences of shorter, conversational messages suitable for platforms like LinkedIn (to be sent manually, as requested, avoiding a bot-like feel).

Personalization is key here. Generic messages are ineffective. We will explore how to use LangChain, potentially with Retrieval-Augmented Generation (RAG), to reference specific job requirements and relevant parts of your CV, creating compelling and context-aware drafts.

## 2. The Power of Retrieval-Augmented Generation (RAG)

Simply feeding the entire CV and job description into an LLM prompt for drafting might work for short texts, but it has limitations:

*   **Context Window:** Long CVs or detailed job descriptions might exceed the LLM's context limit.
*   **Relevance:** The LLM might get lost in irrelevant details.
*   **Hallucination:** Without specific grounding, the LLM might invent details.

RAG addresses these issues. It involves:

1.  **Indexing:** Storing your CV (and potentially other relevant documents like cover letter templates or personal notes) in a searchable format, usually a **Vector Store**.
2.  **Retrieval:** When drafting communication for a specific job, first search the Vector Store for the *most relevant* parts of your CV based on the job description's requirements.
3.  **Generation:** Provide the LLM with the job description, the *retrieved relevant CV snippets*, and a prompt instructing it to draft the email/DM. The LLM now has focused, relevant context.

## 3. Setting up RAG for Your CV

To implement RAG, we need to process your CV documents (loaded in Phase 1, potentially split in Phase 2) into embeddings and store them in a vector store.

**Steps:**

1.  **Choose an Embedding Model:** Converts text chunks into numerical vectors. Options include models from OpenAI (`OpenAIEmbeddings`), Hugging Face (`HuggingFaceEmbeddings`), or others.
2.  **Choose a Vector Store:** Stores the embeddings and allows efficient similarity searches. Options:
    *   `FAISS`: Fast, in-memory library (good for smaller datasets, requires `pip install faiss-cpu`).
    *   `Chroma`: Open-source, can persist to disk (requires `pip install chromadb`).
    *   Others like Pinecone, Weaviate (often cloud-based).
3.  **Embed and Store:** Process your CV chunks through the embedding model and add them to the vector store.

**Code Snippet (Creating a CV Vector Store with FAISS):**

```python
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings # Or HuggingFaceEmbeddings, etc.
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader # Assuming CV is PDF

# --- Setup ---
load_dotenv()
# Ensure OPENAI_API_KEY is set for OpenAIEmbeddings
# Ensure you have run: pip install langchain-openai faiss-cpu pypdf python-dotenv

# --- Configuration ---
CV_FILE_PATH = "/path/to/your/cv.pdf" # Replace with your CV path
VECTOR_STORE_PATH = "/home/ubuntu/cv_vector_store_faiss" # Directory to save the FAISS index
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

# --- Load and Split CV (Adapt from Phase 1 & 2) ---
def load_and_split_cv(file_path):
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        if not documents:
            print("CV loading failed or document is empty.")
            return None
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        cv_chunks = text_splitter.split_documents(documents)
        print(f"Loaded and split CV into {len(cv_chunks)} chunks.")
        return cv_chunks
    except Exception as e:
        print(f"Error loading/splitting CV: {e}")
        return None

# --- Create or Load Vector Store ---
def get_cv_vector_store(cv_chunks):
    """Creates a FAISS vector store from CV chunks."""
    if not cv_chunks:
        print("No CV chunks to process.")
        return None
    try:
        # Initialize embedding model
        # Make sure the model matches your LLM provider or use a general one
        embeddings = OpenAIEmbeddings()
        
        # Create FAISS index from documents
        print("Creating FAISS index from CV chunks...")
        vector_store = FAISS.from_documents(cv_chunks, embeddings)
        print("FAISS index created successfully.")
        
        # Optional: Save the index for later use
        # vector_store.save_local(VECTOR_STORE_PATH)
        # print(f"FAISS index saved to {VECTOR_STORE_PATH}")
        
        return vector_store
        
    except Exception as e:
        print(f"Error creating vector store: {e}")
        return None

# --- Main Execution ---
if __name__ == "__main__":
    cv_document_chunks = load_and_split_cv(CV_FILE_PATH)
    if cv_document_chunks:
        cv_vectorstore = get_cv_vector_store(cv_document_chunks)
        
        if cv_vectorstore:
            print("CV Vector Store is ready.")
            # Example: Test similarity search
            # query = "experience with Python and machine learning"
            # relevant_docs = cv_vectorstore.similarity_search(query, k=3) # Get top 3 relevant chunks
            # print(f"\n--- Relevant CV Chunks for '{query}' ---")
            # for doc in relevant_docs:
            #     print(f"- {doc.page_content[:150]}...")
            # print("--- End Relevant Chunks ---\n")
        else:
            print("Failed to create CV Vector Store.")
    else:
        print("Failed to load and split CV.")

# To load a saved index later:
# embeddings = OpenAIEmbeddings()
# loaded_vector_store = FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True) # Be cautious with allow_dangerous_deserialization

```

**Explanation:**

*   We load and split the CV as before.
*   `OpenAIEmbeddings` is initialized (requires API key).
*   `FAISS.from_documents(cv_chunks, embeddings)` takes the text chunks and the embedding model, computes embeddings for each chunk, and builds the FAISS index.
*   The `vector_store` object can now perform similarity searches.
*   The commented-out `save_local` and `load_local` show how to persist the index so you don't have to rebuild it every time.

## 4. Drafting Personalized Emails

Now, let's combine the job details (extracted in Phase 2) and the CV vector store (created above) to draft emails.

**Steps:**

1.  **Retrieve Relevant CV Snippets:** Use the key requirements or summary from the extracted job details as a query for the CV vector store.
2.  **Construct Prompt:** Create a prompt that includes:
    *   Instructions to draft a professional email.
    *   The extracted job details (title, company, key requirements).
    *   The *retrieved relevant CV snippets*.
    *   Placeholders for sender/recipient info (if available).
3.  **Use LLM Chain:** Run the prompt through an LLM chain.

**Code Snippet (Email Drafting Chain with RAG):**

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# --- Setup ---
load_dotenv()
# Ensure API keys are set
# Assuming cv_vectorstore is created and available (as shown in the previous snippet)
# You also need the extracted job details (e.g., the 'job_info' Pydantic object from Phase 2)

# --- Initialize LLM and Retriever ---
llm = ChatOpenAI(model="gpt-4o", temperature=0.5) # Use a capable model for drafting

# Assuming cv_vectorstore is loaded or created
# cv_vectorstore = FAISS.load_local(VECTOR_STORE_PATH, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
# Create a retriever from the vector store
# search_kwargs={'k': 3} retrieves the top 3 most relevant CV chunks
retriever = cv_vectorstore.as_retriever(search_kwargs={'k': 3})

# --- Define Prompt Template ---
email_prompt_template = """
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

[Draft the email body here, incorporating the CV context and job details naturally.]

Sincerely,
[Your Name]
[Your Contact Information - e.g., Phone, LinkedIn Profile URL]
"""

email_prompt = ChatPromptTemplate.from_template(email_prompt_template)

# --- Build the RAG Chain for Email Drafting ---
def format_docs(docs):
    """Helper function to format retrieved documents for the prompt."""
    return "\n\n".join(doc.page_content for doc in docs)

rag_email_chain = (
    # Context includes job details and the retrieval query (e.g., job summary)
    {"cv_context": retriever | format_docs, "job_title": RunnablePassthrough(), "company_name": RunnablePassthrough(), "job_summary": RunnablePassthrough(), "contact_email": RunnablePassthrough()} 
    | email_prompt
    | llm
    | StrOutputParser()
)

# --- Example Usage (using sample job info and assuming retriever is ready) ---
if __name__ == "__main__" and 'cv_vectorstore' in locals() and cv_vectorstore:
    # Example extracted job info (replace with actual data from Phase 2)
    sample_extracted_info = {
        'job_title': 'AI Research Scientist',
        'company_name': 'Future AI Labs',
        'job_summary': 'Seeking PhD holder with experience in NLP and PyTorch to develop novel algorithms. Strong publication record preferred.',
        'contact_email': 'recruiting@futureailabs.example.com'
    }

    print("\n--- Drafting Email --- ")
    # The retriever will use the 'job_summary' (or other relevant fields) to find CV chunks
    # We pass the job details dictionary directly to invoke
    # Note: The keys in the dictionary passed to invoke must match the keys expected by the RunnablePassthrough components in the chain setup.
    # We need to ensure the retriever gets its query implicitly or explicitly. Let's refine the chain slightly.

    # Refined Chain Setup for clarity on retriever input:
    rag_email_chain_refined = (
        {
            "cv_context": (lambda x: x["job_summary"]) | retriever | format_docs, # Query retriever with job summary
            "job_title": (lambda x: x["job_title"]),
            "company_name": (lambda x: x["company_name"]),
            "job_summary": (lambda x: x["job_summary"]),
            "contact_email": (lambda x: x["contact_email"])
        }
        | email_prompt
        | llm
        | StrOutputParser()
    )

    email_draft = rag_email_chain_refined.invoke(sample_extracted_info)
    
    print(email_draft)
    print("--- Email Draft Complete ---")
else:
     if 'cv_vectorstore' not in locals() or not cv_vectorstore:
         print("CV Vector Store not available. Cannot draft email.")

```

**Explanation:**

*   **Retriever:** `cv_vectorstore.as_retriever()` creates an object that can fetch relevant documents.
*   **Prompt:** The template explicitly asks the LLM to use the provided `cv_context` (which will be filled by the retriever) and `job_details`.
*   **RAG Chain (`rag_email_chain_refined`):**
    *   Uses a dictionary to structure the input for the chain.
    *   `(lambda x: x["job_summary"]) | retriever | format_docs`: This part defines how to get the `cv_context`. It takes the input dictionary (`x`), extracts the `job_summary`, passes it to the `retriever` to get relevant CV `docs`, and then formats these docs into a single string using `format_docs`.
    *   Other `lambda` functions simply pass through the corresponding values from the input dictionary to the prompt.
    *   The rest (`| email_prompt | llm | StrOutputParser()`) formats the prompt, sends it to the LLM, and gets the string output.
*   **`.invoke()`:** Runs the chain with the dictionary containing the extracted job details.

## 5. Preparing Conversational DMs (Sequence)

Your request specified generating DM *sequences* that feel less like a bot, intended for manual sending. This requires a slightly different approach.

**Strategy:**

1.  **Initial Hook:** Generate a short, personalized opening message referencing a specific aspect of the person's profile (if available) or the company/role.
2.  **Follow-up Prompts:** Generate potential follow-up messages based on anticipated responses or to elaborate on your interest/fit.
3.  **Focus on Relevance:** Use RAG similarly to emails, retrieving relevant CV snippets based on the job or the person's profile.

**Code Snippet (Generating an Initial DM Hook):**

```python
# --- (Setup: LLM, Retriever - similar to email) ---
# llm = ChatOpenAI(model="gpt-4o", temperature=0.6) # Slightly higher temp for conversational tone
# retriever = cv_vectorstore.as_retriever(search_kwargs={'k': 2}) # Maybe fewer chunks for brevity

# --- Define DM Prompt Template ---
dm_hook_prompt_template = """
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

dm_hook_prompt = ChatPromptTemplate.from_template(dm_hook_prompt_template)

# --- Build RAG Chain for DM Hook ---
# (Similar structure to the refined email chain, adjusting inputs/prompt)
rag_dm_hook_chain = (
    {
        "cv_context": (lambda x: x["job_summary"]) | retriever | format_docs,
        "job_title": (lambda x: x["job_title"]),
        "company_name": (lambda x: x["company_name"]),
        "job_summary": (lambda x: x["job_summary"]),
        "target_name": (lambda x: x.get("target_name", "there")), # Default if name unknown
        "target_role": (lambda x: x.get("target_role", ""))
    }
    | dm_hook_prompt
    | llm
    | StrOutputParser()
)

# --- Example Usage ---
if __name__ == "__main__" and 'cv_vectorstore' in locals() and cv_vectorstore:
    # Using same sample job info
    sample_dm_input = {
        'job_title': 'AI Research Scientist',
        'company_name': 'Future AI Labs',
        'job_summary': 'Seeking PhD holder with experience in NLP and PyTorch to develop novel algorithms. Strong publication record preferred.',
        'target_name': 'Dr. Evelyn Reed', # Example target
        'target_role': 'Head of AI Research'
    }

    print("\n--- Drafting DM Hook --- ")
    dm_hook_draft = rag_dm_hook_chain.invoke(sample_dm_input)
    print(dm_hook_draft)
    print("--- DM Hook Draft Complete ---")

    # --- Generating Potential Follow-ups (Conceptual) ---
    # You could create another chain that takes the initial hook + job info 
    # and suggests 2-3 potential follow-up questions or points based on the initial message.
    # E.g., Prompt: "Given the initial message '{dm_hook_draft}', suggest a brief follow-up question 
    #               related to the '{job_title}' role or the candidate's experience in {relevant_cv_skill}."
    print("\n(Conceptual: Generate follow-up prompts here...) ")

```

**Explanation:**

*   The process is similar to email drafting but uses a different prompt tailored for a short, engaging DM hook.
*   The prompt encourages referencing a *specific* alignment between the CV and the job.
*   Placeholders for target person information are included.
*   Generating follow-ups would involve creating additional chains/prompts that build upon the initial hook and context.

## 6. Review and Refinement

Crucially, the outputs of these chains are **drafts**. Always review and refine them before sending:

*   **Accuracy:** Check for any factual errors or misinterpretations by the LLM.
*   **Tone:** Adjust the tone to match your personal style and the context.
*   **Completeness:** Add any missing details or personalization.
*   **Grammar/Spelling:** Proofread carefully.

The goal is *AI-assisted* communication, not fully automated sending.

## 7. Summary and Next Steps

In Phase 3, you learned how to set up RAG using vector stores and embeddings to provide relevant CV context to your LLM. You built LangChain chains to draft personalized emails and initial DM hooks by combining job details with retrieved CV snippets. Remember the importance of reviewing these drafts.

The final phase, **Phase 4: Orchestration and Planning**, will focus on tying these different phases (data gathering, processing, drafting) together into a cohesive workflow, potentially using LangChain Agents or more complex chains, and managing the overall process.
