import os
from dotenv import load_dotenv
import pandas as pd
from outreach import send_bulk_emails

# --- P2.2: Load secrets from the .env file ---
load_dotenv(dotenv_path=".env.local")

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
APP_PASSWORD = os.getenv("APP_PASSWORD")

# --- P2.3: Load contacts.csv into a DataFrame ---
contacts_path = "emails/contacts.csv"
df = pd.read_csv(contacts_path)

# Ensure 'Comments' column exists
if "Comments" not in df.columns:
    df["Comments"] = ""

print()
print("-------------------------------------------")
print("Welcome to Mail Automation Pro Ultra Max 🔥")
print("-------------------------------------------")
print()

# --- Get salutation from FirstName column ---
def get_smart_salutation(row) -> str:
    """
    Returns the first name from the row, or 'Team' if the first name is missing/empty.
    """
    first_name = str(row.get("FirstName", "")).strip()
    return first_name if first_name else "Team"

# Example usage:
if __name__ == "__main__":
    send_bulk_emails()
