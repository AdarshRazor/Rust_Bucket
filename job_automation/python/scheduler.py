import schedule
import time
from scraper import scrape_linkedin_jobs
from proxy_manager import ProxyManager

# Initialize proxy manager
proxy_mgr = ProxyManager()
proxy_mgr.fetch_proxies()

def scrape_task():
    """
    Daily scraping task that scrapes LinkedIn jobs.
    """
    print("Running scheduled scraping task...")
    try:
        # Add your job search parameters here
        scrape_linkedin_jobs(
            job_title="react developer",
            location="India",
            time_posted="r86400",
            num_rows=1000,
            proxy_manager=proxy_mgr
        )
    except Exception as e:
        print(f"Error in scraping task: {e}")

# Schedule the scrape_task to run every day at 10:30
schedule.every().day.at("10:30").do(scrape_task)

# For testing, you can uncomment this to run every minute
# schedule.every(1).minutes.do(scrape_task)

if __name__ == "__main__":
    print("Scheduler started. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(1)