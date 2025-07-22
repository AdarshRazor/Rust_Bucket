# LinkedIn Email Scraping Automation

## ⚠️ Legal Disclaimer

**Warning:** This project is for educational and research purposes only. Automated scraping of LinkedIn is strictly prohibited by LinkedIn's User Agreement and may result in permanent account bans, IP blacklisting, and potential legal action. The only legally compliant method for data access is via the official LinkedIn API. Proceeding with scraping is at your own risk.

## Project Overview

This project automates the extraction of email addresses from recent LinkedIn posts related to 'Hiring Full Stack' in India. It is designed to help users build targeted outreach lists efficiently by mimicking human browsing behavior and evading anti-bot detection.

## Core Features
- **Targeted Search:** Configure search queries and location filters (e.g., "Hiring Full Stack" in India).
- **Quantity Control:** Specify the number of unique emails to collect.
- **Dynamic Navigation:** Handles infinite scroll and lazy-loaded content.
- **Email Extraction:** Uses robust regex to extract and validate emails from posts and comments.
- **Data Storage:** Saves emails with metadata (post URL, date, snippet) and deduplicates results.
- **Export:** Supports CSV and JSON export formats.
- **Anti-Detection:** Implements user-agent rotation, randomized delays, and (optionally) proxy support.

## Non-Functional Requirements
- **Robustness:** Anti-bot evasion (IP/user-agent rotation, human-like actions).
- **Performance:** Optimized for speed and minimal resource usage.
- **Maintainability:** Modular, well-documented, and adaptable to LinkedIn changes.
- **Scalability:** Microservices-ready architecture for concurrent tasks.
- **Security:** No login required; IP and identity masking recommended.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd LinkedinAutomation
   ```
2. **Create and activate a Python virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the scraper:**
   ```bash
   python main.py --query "Hiring Full Stack" --location "India" --target 10 --max-scrolls 20
   ```

## Usage

- Configure your search parameters and desired email quantity in the main script or config file (to be implemented).
- Run the scraper script (to be implemented).
- Export results as CSV or JSON.

## Roadmap
- [x] Project setup and dependency installation
- [x] Legal and ethical review
- [x] Proof of concept: Selenium scraper, infinite scroll, email extraction
- [ ] Anti-detection and proxy integration
- [ ] Microservices refactor and containerization

## Contributing
Pull requests are welcome. Please ensure any code changes are well-documented and tested.

## License
This project is provided for educational purposes only. No license is granted for commercial or scraping use against LinkedIn or any other service in violation of their terms. 