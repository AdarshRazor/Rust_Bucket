import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import pandas as pd
from email.utils import formataddr
import time

# Load environment variables
load_dotenv(dotenv_path=".env.local")

def load_email_credentials():
    """
    Load email credentials from .env file
    """
    email_address = os.getenv("EMAIL_ADDRESS")
    app_password = os.getenv("APP_PASSWORD")
    
    if not email_address or not app_password:
        raise ValueError("EMAIL_ADDRESS and APP_PASSWORD must be set in .env.local file")
    
    return email_address, app_password

def load_email_template():
    """
    Load the HTML email template and return it as a string
    """
    template_path = "content/email_template.html"
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Email template not found at {template_path}")

def send_email(recipient_email: str, salutation: str, sender_email: str, app_password: str) -> bool:
    """
    Send an email with resume attachment using SMTP
    
    Args:
        recipient_email: The email address to send to
        salutation: The personalized salutation (e.g., "Adarsh" or "Team")
        sender_email: The sender's email address
        app_password: The app password for authentication
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Create message container
        msg = MIMEMultipart('alternative')
        msg['From'] = formataddr(("Adarsh Anand", sender_email))
        msg['To'] = recipient_email
        msg['Subject'] = "Adarsh Anand | Full Stack Developer | Resume"
        
        # Load and personalize email template
        template = load_email_template()
        personalized_content = template.replace("{{name}}", salutation)
        
        # Attach HTML content
        html_part = MIMEText(personalized_content, 'html')
        msg.attach(html_part)
        
        # Attach resume PDF
        resume_path = "content/AdarshAnand_FullStack_Resume.pdf"
        if os.path.exists(resume_path):
            with open(resume_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename=AdarshAnand_FullStack_Resume.pdf'
            )
            msg.attach(part)
        else:
            print(f"Warning: Resume file not found at {resume_path}")
        
        # Send email using Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print(f"✅ Email sent successfully to {recipient_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email to {recipient_email}: {str(e)}")
        return False

def test_email_sending():
    """
    Test function to verify email sending works
    """
    try:
        # Load credentials
        sender_email, app_password = load_email_credentials()
        
        # Test with first contact from CSV
        contacts_path = "emails/contacts.csv"
        df = pd.read_csv(contacts_path)
        
        if len(df) > 0:
            first_row = df.iloc[0]
            recipient_email = first_row["EmailAddress"]
            salutation = first_row.get("FirstName", "Team")
            
            print(f"Testing email sending to: {recipient_email}")
            print(f"Using salutation: {salutation}")
            
            # Send test email
            success = send_email(recipient_email, salutation, sender_email, app_password)
            
            if success:
                print("🎉 Email test successful!")
            else:
                print("💥 Email test failed!")
        else:
            print("No contacts found in CSV file")
            
    except Exception as e:
        print(f"Error during email test: {str(e)}")

def send_bulk_emails(contacts_path="emails/contacts.csv"):
    """
    Iterate through the DataFrame, send emails to contacts not marked as 'Sent',
    and update the Comments column accordingly.
    Implements P2.8, P2.9, P2.10 from PRD.
    """
    sender_email, app_password = load_email_credentials()
    df = pd.read_csv(contacts_path)
    # Ensure Comments column is of type object (string)
    df["Comments"] = df["Comments"].astype("object")
    updated = False
    for idx, row in df.iterrows():
        # P2.7: Skip if already sent
        if str(row.get("Comments", "")).strip().lower() == "sent":
            print(f"Skipping {row['EmailAddress']} (already sent)")
            continue
        recipient_email = str(row["EmailAddress"])
        first_name = row.get("FirstName", "")
        # Use the value from FirstName if present, otherwise use empty string
        if isinstance(first_name, str):
            salutation = first_name.strip()
        elif pd.isna(first_name) == True:
            salutation = ""
        else:
            salutation = str(first_name).strip()
        print(f"Sending to {recipient_email} with salutation '{salutation}'...")
        try:
            success = send_email(recipient_email, salutation, sender_email, app_password)
            if success:
                df.at[idx, "Comments"] = "Sent"
            else:
                df.at[idx, "Comments"] = "Failed"
            updated = True
        except Exception as e:
            print(f"Exception for {recipient_email}: {e}")
            df.at[idx, "Comments"] = "Failed"
            updated = True
        # P2.9: Rate limiting
        print("Waiting 10 seconds before next email...")
        time.sleep(10)
    # P2.10: Save DataFrame
    if updated:
        df.to_csv(contacts_path, index=False)
        print(f"Updated contacts saved to {contacts_path}")
        print()
        print("Thanks for using - Mail Automation Pro Ultra Max 🔥")
        print()
    else:
        print("No updates made to contacts file.")
        print()
        print("Thanks for using - Mail Automation Pro Ultra Max 🔥")
        print()

if __name__ == "__main__":
    # Run email sending test
    test_email_sending()
