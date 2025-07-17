from playwright.sync_api import sync_playwright
import time, re, random
import pandas as pd
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path=".env.local")

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15',
    # Add more if needed
]

LINKEDIN_EMAIL = os.environ.get("LINKEDIN_ID")
LINKEDIN_PASSWORD = os.environ.get("LINKEDIN_PASS")

if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
    raise ValueError("Please set the LINKEDIN_ID and LINKEDIN_PASS environment variables.")

def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)

def save_to_csv(emails, filename="linkedin_emails.csv"):
    df = pd.DataFrame(emails, columns=["Email"])
    df.to_csv(filename, index=False)
    print(f"Saved {len(emails)} emails to {filename}")

def scrape_linkedin_post(post_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent=random.choice(USER_AGENTS))
        page = context.new_page()

        # Login
        page.goto("https://www.linkedin.com/login")
        page.fill("input#username", str(LINKEDIN_EMAIL))
        page.fill("input#password", str(LINKEDIN_PASSWORD))
        page.click("button[type=submit]")
        page.wait_for_load_state("networkidle")
        page.screenshot(path="after_login.png")

        # Go to the specific post
        page.goto(post_url)
        page.wait_for_load_state("networkidle")
        time.sleep(3)
        page.screenshot(path="post_loaded.png")

        # Try to extract post content and author
        try:
            # These selectors may need adjustment based on LinkedIn's current DOM
            post_text = page.locator("div.feed-shared-update-v2__description, div.update-components-text").inner_text()
        except Exception as e:
            post_text = ""
            print(f"Could not extract post text: {e}")

        try:
            author = page.locator("span.feed-shared-actor__name").inner_text()
        except Exception as e:
            author = ""
            print(f"Could not extract author: {e}")

        emails = extract_emails(post_text)

        browser.close()

        print("Post text:", post_text)
        print("Author:", author)
        print("Emails found:", emails)

        return {
            "url": post_url,
            "author": author,
            "text": post_text,
            "emails": emails
        }

if __name__ == "__main__":
    post_url = "https://www.linkedin.com/search/results/content/?keywords=hiring%20full%20stack&origin=FACETED_SEARCH"  # your target post
    result = scrape_linkedin_post(post_url)
    if result["emails"]:
        save_to_csv(result["emails"])
    else:
        print("No emails found in the post.")
