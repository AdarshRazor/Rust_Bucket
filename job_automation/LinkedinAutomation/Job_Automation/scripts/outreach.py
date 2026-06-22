import os
import smtplib
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from pathlib import Path

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

CONTACTS_PATH = _BASE_DIR / "emails" / "contacts.csv"
TEMPLATE_PATH = _BASE_DIR / "content" / "email_template.html"
RESUME_PATH = _BASE_DIR / "content" / "AdarshAnand__Full_Stack_AI_Engineer__Resume.pdf"


def _load_credentials() -> tuple[str, str]:
    email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("APP_PASSWORD")
    if not email or not password:
        raise ValueError("EMAIL_ADDRESS and APP_PASSWORD must be set in .env.local")
    return email, password


def _load_template() -> str:
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"Email template not found: {TEMPLATE_PATH}")
    return TEMPLATE_PATH.read_text(encoding="utf-8")


def send_email(recipient: str, salutation: str, sender: str, password: str) -> bool:
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = formataddr(("Adarsh Anand", sender))
        msg["To"] = recipient
        msg["Subject"] = "Adarsh Anand | Full Stack AI Engineer | Resume"

        body = _load_template().replace("{{name}}", salutation)
        msg.attach(MIMEText(body, "html"))

        if RESUME_PATH.exists():
            with open(RESUME_PATH, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f'attachment; filename="{RESUME_PATH.name}"',
            )
            msg.attach(part)
        else:
            log.warning("Resume not found at %s — sending without attachment", RESUME_PATH)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, recipient, msg.as_string())

        log.info("Sent to %s (salutation: %s)", recipient, salutation)
        return True

    except Exception as e:
        log.error("Failed to send to %s: %s", recipient, e)
        return False


def send_bulk_emails(contacts_path: str = str(CONTACTS_PATH), delay_seconds: int = 10) -> None:
    """
    Send emails to all contacts not yet marked 'Sent' in the Comments column.
    Updates the CSV in-place after each send.
    """
    log.info("=== send_bulk_emails START ===")
    sender, password = _load_credentials()

    contacts_file = Path(contacts_path)
    if not contacts_file.exists():
        log.error("Contacts file not found: %s", contacts_path)
        return

    df = pd.read_csv(contacts_path)
    if "Comments" not in df.columns:
        df["Comments"] = ""
    df["Comments"] = df["Comments"].astype(object)

    total = len(df)
    skipped = int((df["Comments"].astype(str).str.strip().str.lower() == "sent").sum())
    log.info("Contacts: %d total | %d already sent | %d to process", total, skipped, total - skipped)

    updated = False
    for idx, row in df.iterrows():
        if str(row.get("Comments", "")).strip().lower() == "sent":
            continue

        recipient = str(row["EmailAddress"]).strip()
        first_name = str(row.get("FirstName", "")).strip()
        salutation = first_name if first_name else "Team"

        log.info("Sending to %s ...", recipient)
        try:
            success = send_email(recipient, salutation, sender, password)
            df.at[idx, "Comments"] = "Sent" if success else "Failed"
        except Exception as e:
            log.error("Exception for %s: %s", recipient, e)
            df.at[idx, "Comments"] = "Failed"

        updated = True
        df.to_csv(contacts_path, index=False)

        log.info("Waiting %ds before next email...", delay_seconds)
        time.sleep(delay_seconds)

    if updated:
        log.info("Final contacts saved to %s", contacts_path)
    else:
        log.info("No emails were sent (all already marked Sent)")

    log.info("=== send_bulk_emails END ===")


if __name__ == "__main__":
    send_bulk_emails()
