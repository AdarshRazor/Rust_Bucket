import sys
import argparse
from pathlib import Path

# Add scripts/ to path so main.py can import from it cleanly
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from scraper import run_scraper
from logger import get_logger

log = get_logger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LinkedIn Email Scraper")
    parser.add_argument("--query", type=str, default="Hiring Full Stack")
    parser.add_argument("--location", type=str, default="India")
    parser.add_argument("--target", type=int, default=10)
    parser.add_argument("--max-scrolls", type=int, default=20)
    args = parser.parse_args()

    log.info("=== LinkedIn Scraper Started ===")
    log.info("Query=%s | Location=%s | Target=%d | MaxScrolls=%d",
             args.query, args.location, args.target, args.max_scrolls)

    run_scraper(
        query=args.query,
        location=args.location,
        target=args.target,
        max_scrolls=args.max_scrolls,
    )

    log.info("=== LinkedIn Scraper Finished ===")
