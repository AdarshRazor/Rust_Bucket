from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import time
import re
import random
import pandas as pd
from playwright.sync_api import sync_playwright
import urllib.robotparser
import urllib.parse

# LinkedIn credentials (replace with your own)
LINKEDIN_EMAIL = "your_email@example.com"
LINKEDIN_PASSWORD = "your_password"

# Firecrawl API key (replace with your own)
FIRECRAWL_API_KEY = "your_firecrawl_api_key"

# Proxy configuration (optional, replace with your proxy service details)
PROXY = {
    "http": "http://your_proxy:port",
    "https": "http://your_proxy:port"
}

# Updated user agent list (modernized for 2025)
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36'
]

# Initialize Firecrawl
try:
    from firecrawl import FirecrawlApp
    firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
except ImportError:
    print("Firecrawl not installed. Skipping Firecrawl scraping.")
    firecrawl = None

# Function to check robots.txt
def is_scraping_allowed(url, user_agent):
    rp = urllib.robotparser.RobotFileParser()
    robots_url = urllib.parse.urljoin(url, '/robots.txt')
    try:
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception as e:
        print(f"Error reading robots.txt: {e}")
        return True

# Initialize Selenium WebDriver with Playwright-like features
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # Uncomment to use proxy
    # chrome_options.add_argument(f'--proxy-server={PROXY["http"]}')
    service = Service('path/to/chromedriver')  # Replace with your ChromeDriver path
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# Function to login to LinkedIn
def linkedin_login(driver):
    driver.get("https://www.linkedin.com/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    driver.find_element(By.ID, "username").send_keys(LINKEDIN_EMAIL)
    driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD)
    driver.find_element(By.CSS_SELECTOR, ".login__form_action_container button").click()
    time.sleep(random.uniform(3, 5))

# Function to extract emails from text using regex
def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)

# Main scraping function with Playwright
def scrape_linkedin_posts(url, max_posts=40):
    user_agent = random.choice(USER_AGENTS)
    if not is_scraping_allowed(url, user_agent):
        print(f"Scraping not allowed by {url}/robots.txt for user agent: {user_agent}")
        return []

    driver = init_driver()
    try:
        linkedin_login(driver)
        driver.get(url)
        time.sleep(random.uniform(3, 5))

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--disable-blink-features=AutomationControlled'])
            context = browser.new_context(user_agent=user_agent)
            page = context.new_page()
            page.goto(url)
            page.wait_for_load_state('networkidle')

            posts_collected = 0
            emails = []
            last_height = page.evaluate("return document.body.scrollHeight")

            while posts_collected < max_posts:
                page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(2, 4))

                soup = BeautifulSoup(page.content(), 'html.parser')
                post_elements = soup.find_all('div', class_='feed-shared-update-v2')

                for post in post_elements[posts_collected:]:
                    if posts_collected >= max_posts:
                        break
                    post_text = post.get_text(strip=True)
                    post_emails = extract_emails(post_text)
                    if post_emails:
                        emails.extend(post_emails)
                    posts_collected += 1

                new_height = page.evaluate("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            browser.close()
            return emails

    finally:
        driver.quit()

# Firecrawl scraping function
def scrape_with_firecrawl(url):
    if not firecrawl:
        return []
    user_agent = random.choice(USER_AGENTS)
    if not is_scraping_allowed(url, user_agent):
        print(f"Scraping not allowed by {url}/robots.txt for user agent: {user_agent}")
        return []

    try:
        result = firecrawl.scrape_url(url, params={"pageOptions": {"onlyMainContent": True}})
        content = result.get('content', '')
        emails = extract_emails(content)
        return emails
    except Exception as e:
        print(f"Firecrawl error: {e}")
        return []

# Save emails to CSV
def save_to_csv(emails, filename="linkedin_emails.csv"):
    df = pd.DataFrame(emails, columns=["Email"])
    df.to_csv(filename, index=False)
    print(f"Saved {len(emails)} emails to {filename}")

# Main execution
if __name__ == "__main__":
    target_url = "https://www.linkedin.com/search/results/content/?keywords=hiring%20full%20stack&origin=FACETED_SEARCH&sid=PTu&sortBy=%22date_posted%22"
    
    print("Scraping with Selenium/Playwright...")
    selenium_emails = scrape_linkedin_posts(target_url, max_posts=40)
    
    print("Scraping with Firecrawl...")
    firecrawl_emails = scrape_with_firecrawl(target_url)
    
    all_emails = list(set(selenium_emails + firecrawl_emails))
    
    if all_emails:
        save_to_csv(all_emails)
    else:
        print("No emails found.")