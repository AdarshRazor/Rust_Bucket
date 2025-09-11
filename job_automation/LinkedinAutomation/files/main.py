import argparse
from scraper import run_scraper

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LinkedIn Email Scraper Orchestrator")
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