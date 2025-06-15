import requests
import time
import random
import urllib.robotparser
import urllib.parse
from playwright.sync_api import sync_playwright
import json
from proxy_manager import ProxyManager

def get_random_user_agent():
    """Returns a random user agent string."""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Android 11; Mobile; rv:89.0) Gecko/89.0 Firefox/89.0'
    ]
    return random.choice(user_agents)

def is_scraping_allowed(url, user_agent):
    """
    Checks the website's robots.txt file to see if scraping is allowed
    for the given user agent and URL.
    """
    rp = urllib.robotparser.RobotFileParser()
    robots_url = urllib.parse.urljoin(url, '/robots.txt')
    try:
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception as e:
        print(f"Error reading robots.txt: {e}")
        return True # Assume allowed if robots.txt cannot be read

def make_get_request(url, session=None):
    """
    Makes an HTTP GET request to the given URL with a random user agent
    and a random delay. Implements basic error handling.
    """
    headers = {
 'User-Agent': get_random_user_agent(),
 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' # Add a common Accept header
    }

    delay = random.uniform(2, 10)
    print(f"Waiting for {delay:.2f} seconds before making the request...")
    time.sleep(delay)

    try:
        if session:
            response = session.get(url, headers=headers)
        else:
            response = requests.get(url, headers=headers)

        status_code = response.status_code
        print(f"Request to {url} returned status code: {status_code}")

        if status_code == 200:
            print("Request successful.")
            # You can process the response.text here if needed
            # return response.text
        elif status_code == 403:
            print("Error: Forbidden. The server understood the request but refuses to authorize it.")
        elif status_code == 429:
            print("Error: Too Many Requests. You have sent too many requests in a given amount of time.")
        elif status_code >= 500:
            print(f"Error: Server Error ({status_code}). The server encountered an unexpected condition.")
        else:
            print(f"Request completed with status code {status_code}.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")

def save_data_to_json(data, filename):
    """
    Saves data (dictionary or list of dictionaries) to a local JSON file.
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data successfully saved to {filename}")

def scrape_dynamic_content(url, session=None):
    """
    Scrapes dynamic content from a URL using Playwright.
    """
    print(f"Scraping dynamic content from: {url}")
    try:
        user_agent = get_random_user_agent()
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True,
                                        args=['--disable-blink-features=AutomationControlled']) # Basic stealth option
            # Consider using a Playwright stealth plugin here for more advanced mitigation
            # Example: from playwright_stealth import stealth_sync
            # stealth_sync(page)

            # Use a persistent context for session management if needed
            # Alternatively, handle cookies manually by getting/setting them from the context
            context = browser.new_context(user_agent=user_agent,
                                        # Example of setting cookies if you had them from a requests session
                                        # storage_state={'cookies': session.cookies.get_dict() if session else []}
                                        )
            page = context.new_page()
            page.goto(url)
            page.wait_for_load_state('networkidle') # Wait until no network requests for 500ms
            html_content = page.content()
            browser.close()
            return html_content
    except Exception as e:
        print(f"An error occurred during dynamic scraping: {e}")
        return None

def scrape_linkedin_jobs(job_title, location, time_posted, num_rows, proxy_manager=None):
    """
    Scrapes LinkedIn jobs from a replica site based on provided parameters.

    Args:
        job_title (str): The job title to search for.
        location (str): The location to search in.
        time_posted (str): The time frame for job postings (e.g., "24 hours", "past week").
                       This will need to be handled based on the replica's UI.
        num_rows (int): The maximum number of job listings to scrape.
        proxy_manager (ProxyManager, optional): Instance of ProxyManager for proxy rotation.
    """
    print(f"Scraping LinkedIn jobs for: {job_title} in {location}, posted {time_posted}")

    # --- Configuration ---
    # **IMPORTANT:** Replace with the actual URL of your LinkedIn replica job search page
    replica_url = "https://www.linkedin.com/jobs"

    # **IMPORTANT:** Update these selectors based on your replica's HTML structure
    selectors = {
        "job_title_input": 'input[aria-label="Job title"]',
        "location_input": 'input[aria-label="Location"]',
        "time_posted_filter": 'YOUR_TIME_POSTED_FILTER_SELECTOR',
        "job_listing": ".job-listing",
        "job_title": ".job-title",
        "company_name": ".company-name",
        "job_location": ".job-location",
        "date_posted": ".date-posted",
        "job_url": "a.job-link",
    }

    scraped_jobs = []
    
    with sync_playwright() as p:
        browser_options = {
            "headless": True,
            "args": ["--disable-blink-features=AutomationControlled"]
        }
        
        # Add proxy if available
        if proxy_manager:
            proxy = proxy_manager.get_proxy()
            if proxy:
                browser_options["proxy"] = {
                    "server": f"http://{proxy}"
                }

        browser = p.chromium.launch(**browser_options)
        page = browser.new_page(user_agent=get_random_user_agent())

        try:
            print(f"Navigating to replica URL: {replica_url}")
            page.goto(replica_url)
            page.wait_for_load_state("networkidle")

            print("Entering search parameters...")
            page.fill(selectors["job_title_input"], job_title)
            page.fill(selectors["location_input"], location)

            print(f"Attempting to apply time posted filter: {time_posted}")

            print("Scrolling to load more results...")
            while len(scraped_jobs) < num_rows:
                initial_job_count = len(scraped_jobs)
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                
                try:
                    page.wait_for_selector(selectors["job_listing"], state="attached", timeout=5000)
                    time.sleep(random.uniform(2, 5))
                except:
                    print("No new job listings loaded or timeout reached.")
                    break

                job_listings = page.query_selector_all(selectors["job_listing"])
                print(f"Found {len(job_listings)} job listings after scroll.")

                for listing in job_listings[initial_job_count:]:
                    try:
                        title = listing.query_selector(selectors["job_title"]).innerText().strip()
                        company = listing.query_selector(selectors["company_name"]).innerText().strip()
                        location = listing.query_selector(selectors["job_location"]).innerText().strip()
                        date_posted = listing.query_selector(selectors["date_posted"]).innerText().strip()
                        job_url = listing.query_selector(selectors["job_url"]).get_attribute("href")

                        scraped_jobs.append({
                            "title": title,
                            "company": company,
                            "location": location,
                            "date_posted": date_posted,
                            "job_url": job_url,
                        })
                    except Exception as e:
                        print(f"Error extracting job data from a listing: {e}")
                        continue

                if len(scraped_jobs) == initial_job_count:
                    print("No new jobs were added after scrolling. Assuming end of results.")
                    break

            print(f"Finished scraping. Scraped {len(scraped_jobs)} jobs.")

        except Exception as e:
            print(f"An error occurred during scraping: {e}")
            if proxy_manager:
                proxy_manager.mark_proxy_failed(proxy)

        finally:
            browser.close()

    if scraped_jobs:
        save_data_to_json(scraped_jobs, "linkedin_jobs.json")
        print("Scraped data saved to linkedin_jobs.json")
    else:
        print("No jobs were scraped.")

    return scraped_jobs

if __name__ == "__main__":
    # Example usage with proxy manager
    proxy_mgr = ProxyManager()
    proxy_mgr.fetch_proxies()  # Initialize proxies
    scrape_linkedin_jobs("react developer", "India", "r86400", 1000, proxy_mgr)