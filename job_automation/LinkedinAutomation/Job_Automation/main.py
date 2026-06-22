"""
Job Automation Pipeline
=======================
Phase 1  →  LinkedIn scraper  →  output/extracted_emails.csv
Phase 2  →  Gemma LLM cleaner →  emails/contacts.csv
Phase 3  →  Email outreach    →  sends emails, updates contacts.csv

Usage:
    python main.py                          # full pipeline
    python main.py --skip-scrape            # clean + send only
    python main.py --skip-scrape --skip-clean  # send only
    python main.py --query "Hiring Python" --location "Bangalore" --target 100
"""
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from scraper import run_scraper
from cleaner import clean_and_prepare_contacts
from outreach import send_bulk_emails
from logger import get_logger

log = get_logger(__name__)

BANNER = """
╔══════════════════════════════════════════════╗
║       Job Automation Pipeline  🚀            ║
║  Scrape → Clean (Gemma) → Send Emails        ║
╚══════════════════════════════════════════════╝
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Job Automation Pipeline")
    parser.add_argument("--query", type=str, default="Hiring AI Engineer",
                        help="LinkedIn search query (default: 'Hiring AI Engineer')")
    parser.add_argument("--location", type=str, default="India",
                        help="LinkedIn location filter (default: India)")
    parser.add_argument("--target", type=int, default=50,
                        help="Max emails to extract per scrape run (default: 10000)")
    parser.add_argument("--max-scrolls", type=int, default=20,
                        help="Max scroll iterations for LinkedIn feed (default: 50)")
    parser.add_argument("--batch-size", type=int, default=50,
                        help="Emails per LLM batch in cleaning phase (default: 50)")
    parser.add_argument("--delay", type=int, default=10,
                        help="Seconds between emails in outreach phase (default: 10)")
    parser.add_argument("--skip-scrape", action="store_true",
                        help="Skip Phase 1 — use existing output/extracted_emails.csv")
    parser.add_argument("--skip-clean", action="store_true",
                        help="Skip Phase 2 — use existing emails/contacts.csv")
    parser.add_argument("--skip-send", action="store_true",
                        help="Skip Phase 3 — do not send emails")
    args = parser.parse_args()

    print(BANNER)
    log.info("=== Pipeline Started ===")

    # ── Phase 1: Scrape LinkedIn ───────────────────────────────────────────
    if not args.skip_scrape:
        log.info("━━━ Phase 1: LinkedIn Scraping ━━━")
        result = run_scraper(
            query=args.query,
            location=args.location,
            target=args.target,
            max_scrolls=args.max_scrolls,
        )
        if not result:
            log.error("Scraping failed — aborting pipeline")
            sys.exit(1)
        log.info("Phase 1 complete → %s", result)
    else:
        log.info("Phase 1 skipped (--skip-scrape)")

    # ── Phase 2: Clean & prepare contacts via Gemma ────────────────────────
    if not args.skip_clean:
        log.info("━━━ Phase 2: LLM Email Cleaning (Gemma) ━━━")
        contacts = clean_and_prepare_contacts(batch_size=args.batch_size)
        if not contacts:
            log.error("Cleaning failed — aborting pipeline")
            sys.exit(1)
        log.info("Phase 2 complete → %s", contacts)
    else:
        log.info("Phase 2 skipped (--skip-clean)")

    # ── Phase 3: Send emails ───────────────────────────────────────────────
    if not args.skip_send:
        log.info("━━━ Phase 3: Email Outreach ━━━")
        send_bulk_emails(delay_seconds=args.delay)
        log.info("Phase 3 complete")
    else:
        log.info("Phase 3 skipped (--skip-send)")

    log.info("=== Pipeline Complete ===")
    print("\nThanks for using Job Automation Pipeline 🔥\n")


if __name__ == "__main__":
    main()
