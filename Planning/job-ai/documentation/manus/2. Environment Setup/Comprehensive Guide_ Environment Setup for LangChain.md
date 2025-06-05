# Comprehensive Guide: Environment Setup for LangChain, LangSmith, and LangGraph

## 1. Introduction

Before you can start building your LangChain job search agent, you need to set up a suitable development environment. This involves installing Python, managing dependencies using a virtual environment, installing the necessary LangChain libraries, and configuring access to Large Language Models (LLMs). Additionally, we will cover setting up LangSmith for debugging and LangGraph for orchestration.

This guide assumes you have some basic familiarity with using the command line or terminal on your operating system (Linux, macOS, or Windows).

## 2. Prerequisites

*   **Python:** LangChain is primarily a Python library. You need Python installed on your system. LangChain typically requires a recent version of Python (e.g., 3.8 or higher). You can check your Python version by opening a terminal and running:
    ```bash
    python --version
    # or
    python3 --version
    ```
    If you don't have Python or need a newer version, download it from the official Python website ([python.org](https://python.org/)) or use a version manager like `pyenv`.

*   **pip:** Python's package installer. It usually comes bundled with Python installations. You can check its version with:
    ```bash
    pip --version
    # or
    pip3 --version
    ```

## 3. Setting Up a Virtual Environment (Recommended)

It's highly recommended to use a virtual environment for each Python project. This isolates project dependencies, preventing conflicts between different projects that might require different versions of the same library.

1.  **Navigate to your project directory:** Open your terminal and navigate to the folder where you want to create your LangChain project.
    ```bash
    mkdir langchain-job-agent
    cd langchain-job-agent
    ```

2.  **Create a virtual environment:** Use Python's built-in `venv` module.
    ```bash
    python3 -m venv venv
    ```
    This command creates a directory named `venv` (you can choose another name) containing a copy of the Python interpreter and a place to install project-specific libraries.

3.  **Activate the virtual environment:**
    *   **On macOS and Linux:**
        ```bash
        source venv/bin/activate
        ```
    *   **On Windows (Command Prompt):**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **On Windows (PowerShell):**
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
        (You might need to adjust execution policy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`)

    Once activated, your terminal prompt should change to indicate you're inside the virtual environment (e.g., `(venv) your-user@your-machine:...$`). All packages installed now will be local to this environment.

4.  **Deactivate:** When you're done working, simply type `deactivate` in the terminal.

## 4. Installing LangChain Core Libraries

With your virtual environment activated, you can install the core LangChain package:

```bash
pip install langchain
```

This installs the main `langchain` library, which provides the fundamental abstractions and components.

## 5. Installing Specific Integrations

LangChain's power comes from its integrations. You'll need to install additional packages depending on the specific LLMs, document loaders, vector stores, or tools you plan to use.

*   **LLM Providers:**
    *   For OpenAI models (GPT-3.5, GPT-4): `pip install langchain-openai`
    *   For Google models (Gemini): `pip install langchain-google-genai`
    *   For Hugging Face Hub models (various open-source models): `pip install langchain-huggingface`
    *   For Anthropic models (Claude): `pip install langchain-anthropic`
*   **Document Loaders:**
    *   For PDF files: `pip install pypdf`
    *   For Web Pages: `pip install beautifulsoup4`
    *   For Microsoft Word (.docx): `pip install python-docx`
*   **Vector Stores:**
    *   For FAISS (local, efficient): `pip install faiss-cpu` (or `faiss-gpu` if you have CUDA)
    *   For ChromaDB (local, persistent): `pip install chromadb`
*   **Web Scraping/Browser Automation (for Phase 1):**
    *   Basic HTTP requests: `pip install requests`
    *   HTML Parsing: `pip install beautifulsoup4` (often installed with web loaders)
    *   Browser Automation (more robust but complex): `pip install playwright` and then `playwright install` to install browser binaries.
*   **LangGraph (for orchestration):**
    *   Install LangGraph: `pip install langgraph`
*   **Common Utilities:**
    *   Environment variable management: `pip install python-dotenv` (useful for API keys)

**Recommendation for this project:** Start by installing the core library and add others as needed. For the job search agent, you'll likely need:

```bash
pip install langchain langchain-openai langchain-huggingface pypdf beautifulsoup4 requests faiss-cpu python-dotenv langgraph
# Add others like playwright or chromadb later if required
```

## 6. Setting Up API Keys

Most commercial LLM providers (OpenAI, Google AI Studio, Anthropic) require API keys for authentication.

1.  **Obtain API Keys:** Sign up on the respective provider's website and generate API keys.
2.  **Secure Storage (Recommended):** Do **not** hardcode API keys directly in your script. Use environment variables.
    *   Create a file named `.env` in your project root directory (`langchain-job-agent/.env`).
    *   Add your keys to this file:
        ```
        OPENAI_API_KEY="your_openai_api_key_here"
        HUGGINGFACEHUB_API_TOKEN="your_huggingface_token_here"
        # Add other keys as needed
        ```
    *   **Important:** Add `.env` to your `.gitignore` file if you're using Git to prevent accidentally committing your keys.
3.  **Load Keys in Your Script:** Use the `python-dotenv` library at the beginning of your Python scripts:
    ```python
    import os
    from dotenv import load_dotenv

    load_dotenv() # Loads variables from .env into environment variables

    openai_api_key = os.getenv("OPENAI_API_KEY")
    huggingface_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    # LangChain often automatically picks up keys from environment variables
    # (e.g., os.environ["OPENAI_API_KEY"]), but loading them explicitly is good practice.
    ```

## 7. Optional: LangSmith Setup (Highly Recommended)

LangSmith helps you trace and debug your LangChain applications.

1.  **Sign Up:** Create an account at [smith.langchain.com](https://smith.langchain.com/).
2.  **Create API Key:** Generate an API key within your LangSmith account settings.
3.  **Install LangSmith Client:** `pip install langsmith`
4.  **Configure Environment Variables:** Add these to your `.env` file:
    ```
    LANGCHAIN_TRACING_V2="true"
    LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
    LANGCHAIN_API_KEY="your_langsmith_api_key_here"
    LANGCHAIN_PROJECT="Your-Project-Name" # Optional: name your project
    ```
5.  **Load Variables:** Ensure `load_dotenv()` is called in your script.

With these environment variables set, LangChain will automatically send traces to LangSmith, allowing you to visualize the execution of your chains and agents.

## 8. Optional: LangGraph Setup (For Advanced Orchestration)

LangGraph is a framework for building stateful, multi-actor applications with LLMs. It integrates seamlessly with LangChain but can also be used independently.

1.  **Install LangGraph:** Ensure you have installed LangGraph using:
    ```bash
    pip install langgraph
    ```
2.  **Explore LangGraph Tutorials:** Visit the [LangGraph Tutorials](https://langchain-ai.github.io/langgraph/tutorials/introduction/) for hands-on examples.
3.  **Set Up LangGraph in Your Project:** Follow the LangGraph documentation to integrate it into your LangChain workflows.

## 9. Summary

You should now have a working Python environment with LangChain, LangSmith, and LangGraph installed, ready for development. Remember to activate your virtual environment (`source venv/bin/activate` or equivalent) each time you work on the project. The next steps involve writing the actual code for your job search agent, starting with data gathering.
