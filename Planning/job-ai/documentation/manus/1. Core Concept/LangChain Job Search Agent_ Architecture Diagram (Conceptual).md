# LangChain Job Search Agent: Architecture Diagram (Conceptual)

This document provides a conceptual architecture diagram, described textually, for the LangChain-based job search agent. It illustrates the flow of data and the interaction between different components.

```mermaid
flowchart TD
    subgraph User_Input
        A[User_CV_pdf_docx] --> B(Load_CV)
        C[Job_Search_Criteria_e.g._keywords_location] --> D(Configure_Scraper_Search)
    end

    subgraph Phase_1_Data_Gathering
        D --> E{Web_Scraper_Job_Board_API}
        E -- Job_Postings_Data --> F(Store_Raw_Data)
        B -- CV_Text --> F
    end

    subgraph Phase_2_Data_Processing_Summarization
        F -- Raw_Job_Data_CV_Text --> G(LangChain_Text_Splitter)
        G -- Chunks --> H(LangChain_Information_Extraction_Chain)
        H -- LLM_Prompt --> I[Extracted_Info_Emails_Skills_Company]
        G -- Chunks --> J(LangChain_Summarization_Chain)
        J -- LLM_Prompt --> K[Job_Summaries]
        I --> L(Store_Processed_Data)
        K --> L
    end

    subgraph Phase_3_Communication_Preparation
        L -- Processed_Job_Info_CV_Text --> M(LangChain_RAG_Setup)
        M -- Embeddings_Vector_Store --> N
        N -- Relevant_CV_Snippets_Job_Info --> O(LangChain_Email_Drafting_Chain)
        O -- LLM_Prompt --> P[Draft_Emails]
        N -- Relevant_CV_Snippets_Job_Info --> Q(LangChain_DM_Sequence_Chain)
        Q -- LLM_Prompt --> R[Draft_DMs_Sequence]
        P --> S(Store_Draft_Communications)
        R --> S
    end

    subgraph Phase_4_Orchestration_Output
        T(LangChain_Agent_Main_Chain) -- Controls --> E
        T -- Controls --> H
        T -- Controls --> J
        T -- Controls --> O
        T -- Controls --> Q
        L -- Data --> U(Output_Module)
        S -- Drafts --> U
        U -- Formatted_Output --> V[User_Interface_Report_File]
    end

    style User_Input fill:#f9f,stroke:#333,stroke-width:2px
    style Phase_1_Data_Gathering fill:#ccf,stroke:#333,stroke-width:2px
    style Phase_2_Data_Processing_Summarization fill:#cfc,stroke:#333,stroke-width:2px
    style Phase_3_Communication_Preparation fill:#ffc,stroke:#333,stroke-width:2px
    style Phase_4_Orchestration_Output fill:#fcc,stroke:#333,stroke-width:2px
```

**Explanation of Components:**

1.  **User Input:**
    *   `User CV`: The user provides their Curriculum Vitae.
    *   `Job Search Criteria`: User specifies what kind of jobs to look for.
    *   `Load CV`: Uses LangChain `Document Loaders` to read the CV content.
    *   `Configure Scraper/Search`: Sets up the data gathering parameters.

2.  **Phase 1: Data Gathering:**
    *   `Web Scraper / Job Board API`: The module responsible for fetching job postings. *Note: Direct LinkedIn scraping is problematic; alternatives are preferred.*
    *   `Store Raw Data`: A temporary storage (e.g., files, database) for collected job details and CV text.

3.  **Phase 2: Data Processing & Summarization:**
    *   `Text Splitter`: Breaks down large documents (CV, job descriptions) into manageable chunks.
    *   `Information Extraction Chain`: Uses an LLM with specific prompts to pull out structured data (emails, skills, names) from job descriptions.
    *   `Summarization Chain`: Uses an LLM to create concise summaries of job postings.
    *   `Store Processed Data`: Stores the cleaned, extracted, and summarized information.

4.  **Phase 3: Communication Preparation:**
    *   `RAG Setup`: (Retrieval-Augmented Generation) Sets up embeddings and a vector store for the CV text to allow semantic searching for relevant skills/experience based on job requirements.
    *   `Email Drafting Chain`: Uses the LLM, job info, and relevant CV parts (retrieved via RAG) to draft personalized emails.
    *   `DM Sequence Chain`: Similar to email drafting, but generates a sequence of shorter, conversational DMs, referencing the job and CV.
    *   `Store Draft Communications`: Saves the generated email and DM drafts.

5.  **Phase 4: Orchestration & Output:**
    *   `Agent/Main Chain`: The central LangChain component (either an `Agent` or a master `Chain`) that coordinates the workflow, triggering different phases and modules.
    *   `Output Module`: Collects the processed data and drafted communications.
    *   `User Interface / Report File`: Presents the results (job lists, summaries, drafts, plans) to the user, potentially through a simple UI or structured files.

This diagram provides a visual guide to how the different parts of the agent connect and interact, using LangChain components to handle the core LLM-related tasks.
