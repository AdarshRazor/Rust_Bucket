import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import pandas as pd
from datetime import datetime
import random
from fake_useragent import UserAgent
import argparse
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import os
from dotenv import load_dotenv
from selenium.webdriver.common.keys import Keys

# --- Configuration ---
# LINKEDIN_SEARCH_URL = "https://www.linkedin.com/search/results/content/?keywords=Hiring%20Full%20Stack&origin=SWITCH_SEARCH_VERTICAL&location=India"

# --- Selenium Setup ---
load_dotenv()
LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

def get_driver():
    options = webdriver.FirefoxOptions()
    # User-agent rotation
    try:
        ua = UserAgent()
        user_agent = ua.random
        print(f"Using User-Agent: {user_agent}")
        options.set_preference("general.useragent.override", user_agent)
    except Exception as e:
        print(f"UserAgent error: {e}. Using default user-agent.")
    # Uncomment below for headless mode
    # options.add_argument('--headless')
    # Add more options as needed (proxy, etc.)
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    return driver

# --- Main Scraper Logic ---
def infinite_scroll(driver, max_scrolls=20, scroll_pause=2, randomize_delay=True):
    """
    Scrolls down the page to trigger LinkedIn's infinite scroll.
    Waits for new post elements to load after each scroll.
    Stops after max_scrolls or if no new content loads.
    Adds randomized delays if randomize_delay is True.
    """
    last_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.feed-shared-update-v2'))
            )
        except Exception as e:
            print(f"Timeout waiting for new posts: {e}")
        # Randomized delay between scrolls
        delay = scroll_pause
        if randomize_delay:
            delay = random.uniform(scroll_pause, scroll_pause + 2)
        print(f"Sleeping for {delay:.2f} seconds before next scroll...")
        time.sleep(delay)
        new_height = driver.execute_script("return document.body.scrollHeight")
        print(f"Scroll {i+1}/{max_scrolls}: Page height = {new_height}")
        if new_height == last_height:
            print("No more new content loaded. Stopping scroll.")
            break
        last_height = new_height

def extract_emails_from_posts(driver):
    """
    Extracts emails from all visible LinkedIn post elements on the page.
    Uses a robust regex to find emails in post text.
    """
    # Adjust selector as needed for LinkedIn posts
    post_elements = driver.find_elements(By.CSS_SELECTOR, 'div.feed-shared-update-v2')
    email_regex = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    found_emails = set()
    for post in post_elements:
        try:
            text = post.text
            emails = email_regex.findall(text)
            for email in emails:
                found_emails.add(email)
        except Exception as e:
            print(f"Error extracting from post: {e}")
    print(f"\nExtracted {len(found_emails)} unique emails:")
    for email in found_emails:
        print(email)
    return found_emails

def extract_emails_from_page_source(driver):
    """
    Extracts emails from the entire page source (HTML) after scrolling.
    Uses a robust regex to find emails anywhere in the HTML.
    """
    page_source = driver.page_source
    email_regex = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    emails = set(email_regex.findall(page_source))
    print(f"\nExtracted {len(emails)} unique emails from page source:")
    for email in emails:
        print(email)
    return emails

def load_existing_emails(filename="extracted_emails.csv"):
    """
    Loads existing emails from the CSV file if it exists.
    Returns a set of emails.
    """
    try:
        df = pd.read_csv(filename)
        return set(df["email"].dropna().astype(str))
    except FileNotFoundError:
        return set()
    except Exception as e:
        print(f"Error loading existing emails: {e}")
        return set()

def save_emails_to_csv(emails, filename="extracted_emails.csv"):
    """
    Saves a set of emails to a CSV file with timestamp, merging with existing emails for deduplication.
    """
    existing_emails = load_existing_emails(filename)
    all_emails = existing_emails.union(emails)
    df = pd.DataFrame({"email": list(all_emails)})
    df["extracted_at"] = datetime.now().isoformat()
    df.to_csv(filename, index=False)
    print(f"Saved {len(all_emails)} unique emails to {filename} (including previous runs)")

def linkedin_login(driver):
    """
    Logs into LinkedIn using credentials from environment variables if login page is detected.
    Types credentials slowly and submits with ENTER to mimic human behavior.
    """
    login_url = "https://www.linkedin.com/login"
    driver.get(login_url)
    try:
        username_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        password_input = driver.find_element(By.ID, "password")
        username_input.clear()
        for char in LINKEDIN_USERNAME:
            username_input.send_keys(char)
            time.sleep(0.05)  # Slow typing
        password_input.clear()
        for char in LINKEDIN_PASSWORD:
            password_input.send_keys(char)
            time.sleep(0.05)
        password_input.send_keys(Keys.RETURN)
        print("Login form submitted. Waiting for login to complete...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "global-nav"))
        )
        print("Login successful.")
    except Exception as e:
        print(f"Login failed or not required: {e}")
        raise

def build_linkedin_search_url(query, location):
    """
    Constructs a LinkedIn search URL for posts with the given query and location.
    """
    from urllib.parse import quote_plus
    base_url = "https://www.linkedin.com/search/results/content/?"
    params = f"keywords={quote_plus(query)}"
    if location:
        params += f"&location={quote_plus(location)}"
    params += "&origin=SWITCH_SEARCH_VERTICAL"
    return base_url + params

def run_scraper(query="Hiring Full Stack", location="India", target=10, max_scrolls=20):
    """
    Orchestrates the scraping process with given parameters.
    """
    search_url = build_linkedin_search_url(query, location)
    print(f"Search URL: {search_url}")

    driver = get_driver()
    try:
        # Login to LinkedIn if credentials are provided
        if LINKEDIN_USERNAME and LINKEDIN_PASSWORD:
            linkedin_login(driver)
        # Only after successful login, proceed to search
        print(f"Navigating to: {search_url}")
        pre_load_delay = random.uniform(2, 5)
        print(f"Sleeping for {pre_load_delay:.2f} seconds before loading page...")
        time.sleep(pre_load_delay)
        driver.get(search_url)
        time.sleep(5)  # Wait for page to load (adjust as needed)
        print("Page loaded. Starting infinite scroll...")
        infinite_scroll(driver, max_scrolls=max_scrolls, scroll_pause=2, randomize_delay=True)
        print("Scrolling complete. Extracting emails from posts...")
        post_emails = extract_emails_from_posts(driver)
        print("Extracting emails from full page source...")
        page_emails = extract_emails_from_page_source(driver)
        all_emails = post_emails.union(page_emails)
        limited_emails = set(list(all_emails)[:target])
        print(f"\nTotal unique emails found: {len(all_emails)}; Saving up to {target} emails.")
        save_emails_to_csv(limited_emails)
    finally:
        driver.quit()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="LinkedIn Email Scraper")
    parser.add_argument('--query', type=str, default="Hiring Full Stack", help="Search query (default: 'Hiring Full Stack')")
    parser.add_argument('--location', type=str, default="India", help="Location filter (default: 'India')")
    parser.add_argument('--target', type=int, default=10, help="Target number of unique emails to collect (default: 10)")
    parser.add_argument('--max-scrolls', type=int, default=20, help="Maximum number of scrolls (default: 20)")
    args = parser.parse_args()
    run_scraper(
        query=args.query,
        location=args.location,
        target=args.target,
        max_scrolls=args.max_scrolls
    ) 