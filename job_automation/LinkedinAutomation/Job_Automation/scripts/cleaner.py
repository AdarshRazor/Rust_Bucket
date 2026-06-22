"""
Phase 2 of the pipeline: reads extracted_emails.csv, calls Gemma via NVIDIA NIM
with the Prompt.md system prompt, and writes cleaned contacts to emails/contacts.csv.
"""
import os
import io
from pathlib import Path

import requests
import pandas as pd
from dotenv import load_dotenv

from logger import get_logger

log = get_logger(__name__)

_BASE_DIR = Path(__file__).parent.parent
for _candidate in [_BASE_DIR / ".env.local", _BASE_DIR / ".env"]:
    if _candidate.exists():
        load_dotenv(dotenv_path=_candidate)
        log.debug("Loaded env from: %s", _candidate)
        break

EXTRACTED_EMAILS_PATH = _BASE_DIR / "output" / "extracted_emails.csv"
CONTACTS_PATH = _BASE_DIR / "emails" / "contacts.csv"
PROMPT_PATH = _BASE_DIR / "docs" / "Prompt.md"

NVIDIA_API_URL = os.getenv(
    "NVIDIA_API_URL",
    "https://29b8ec64-9d5f-4770-bde8-b6067de8cb73.invocation.api.nvcf.nvidia.com/v1/chat/completions",
)
NVIDIA_MODEL = "google/gemma-4-26B-A4B-it"


def _load_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def _call_gemma(raw_emails: list[str], system_prompt: str) -> str:
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("NVIDIA_API_KEY not set in .env.local")

    raw_content = "\n".join(raw_emails)
    payload = {
        "model": NVIDIA_MODEL,
        "messages": [
            {"role": "user", "content": system_prompt + "\n\n" + raw_content}
        ],
        "max_tokens": 4096,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    log.debug("Calling Gemma with %d emails", len(raw_emails))
    response = requests.post(NVIDIA_API_URL, headers=headers, json=payload, timeout=90)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def _parse_csv_response(text: str) -> pd.DataFrame:
    """Extract the CSV table from the LLM response text."""
    lines = text.strip().splitlines()
    csv_lines = []
    in_csv = False

    for line in lines:
        clean = line.strip()
        if clean.startswith("```"):
            continue
        if "EmailAddress" in clean and "FirstName" in clean:
            in_csv = True
        if in_csv and clean:
            csv_lines.append(clean)

    if not csv_lines:
        log.warning("No CSV block found in LLM response")
        return pd.DataFrame(columns=["EmailAddress", "FirstName", "Comments"])

    try:
        df = pd.read_csv(io.StringIO("\n".join(csv_lines)))
        # Normalise column names in case of minor variations
        df.columns = [c.strip() for c in df.columns]
        if "EmailAddress" not in df.columns:
            log.warning("EmailAddress column missing from parsed response")
            return pd.DataFrame(columns=["EmailAddress", "FirstName", "Comments"])
        if "Comments" not in df.columns:
            df["Comments"] = ""
        if "FirstName" not in df.columns:
            df["FirstName"] = "Team"
        return df[["EmailAddress", "FirstName", "Comments"]]
    except Exception as e:
        log.error("CSV parse error: %s", e)
        return pd.DataFrame(columns=["EmailAddress", "FirstName", "Comments"])


def clean_and_prepare_contacts(
    extracted_path: str = str(EXTRACTED_EMAILS_PATH),
    contacts_path: str = str(CONTACTS_PATH),
    batch_size: int = 50,
) -> str:
    """
    Process extracted_emails.csv → emails/contacts.csv using Gemma.
    Returns the path to contacts.csv.
    """
    log.info("=== clean_and_prepare_contacts START ===")

    extracted_file = Path(extracted_path)
    if not extracted_file.exists():
        log.error("Extracted emails file not found: %s", extracted_path)
        return ""

    df_raw = pd.read_csv(extracted_path)
    all_emails: list[str] = df_raw["email"].dropna().astype(str).unique().tolist()
    log.info("Loaded %d unique extracted emails", len(all_emails))

    contacts_file = Path(contacts_path)
    if contacts_file.exists():
        df_existing = pd.read_csv(contacts_path)
        existing_set = set(df_existing["EmailAddress"].dropna().str.lower())
        log.info("Found %d existing contacts — will skip duplicates", len(existing_set))
    else:
        df_existing = pd.DataFrame(columns=["EmailAddress", "FirstName", "Comments"])
        existing_set = set()

    new_emails = [e for e in all_emails if e.lower() not in existing_set]
    log.info("%d new emails to process through LLM", len(new_emails))

    if not new_emails:
        log.info("Nothing new to process — contacts.csv is already up to date")
        return contacts_path

    prompt = _load_prompt()
    batches_results: list[pd.DataFrame] = []
    total_batches = (len(new_emails) + batch_size - 1) // batch_size

    for i in range(0, len(new_emails), batch_size):
        batch = new_emails[i : i + batch_size]
        batch_num = i // batch_size + 1
        log.info("Processing batch %d/%d (%d emails)", batch_num, total_batches, len(batch))
        try:
            response_text = _call_gemma(batch, prompt)
            df_batch = _parse_csv_response(response_text)
            if not df_batch.empty:
                batches_results.append(df_batch)
                log.info("Batch %d yielded %d contacts", batch_num, len(df_batch))
            else:
                log.warning("Batch %d produced no usable output", batch_num)
        except Exception as e:
            log.error("Batch %d failed: %s", batch_num, e)

    if not batches_results:
        log.error("LLM produced no usable contacts — contacts.csv unchanged")
        return contacts_path if contacts_file.exists() else ""

    df_new = pd.concat(batches_results, ignore_index=True)
    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    df_combined = df_combined.drop_duplicates(subset=["EmailAddress"])
    df_combined["Comments"] = df_combined["Comments"].fillna("")

    contacts_file.parent.mkdir(exist_ok=True)
    df_combined.to_csv(contacts_path, index=False)
    log.info("Saved %d total contacts to %s (added %d new)",
             len(df_combined), contacts_path, len(df_new))

    log.info("=== clean_and_prepare_contacts END ===")
    return contacts_path


if __name__ == "__main__":
    clean_and_prepare_contacts()
