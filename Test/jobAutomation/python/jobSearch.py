from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import time

# Setup headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=chrome_options)

# LinkedIn Job URL
url = "https://www.linkedin.com/jobs/search/?keywords=frontend%20developer&location=India&f_TPR=r86400&sortBy=DD"
driver.get(url)
time.sleep(3)

# Scroll to load more jobs
scroll_pause_time = 2
last_height = driver.execute_script("return document.body.scrollHeight")

for _ in range(10):  # Scroll 10 times (adjust as needed)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Now parse the fully loaded page
soup = BeautifulSoup(driver.page_source, 'html.parser')
job_links = [a['href'] for a in soup.select("a.base-card__full-link")]

driver.quit()

# Save to file
date_str = datetime.now().strftime("%Y-%m-%d")
filename = f"{date_str}.txt"

with open(filename, "w", encoding="utf-8") as f:
    for link in job_links:
        f.write(link + "\n")

print(f"✅ Saved {len(job_links)} job links to: {filename}")
