import time
import re
import random
import os
from pathlib import Path
from datetime import datetime
from urllib.parse import quote_plus

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from dotenv import load_dotenv
import pandas as pd

from logger import get_logger

log = get_logger(__name__)

# .env: check scripts/../.env then scripts/../../.env (repo root)
for _candidate in [
    Path(__file__).parent.parent / ".env",
    Path(__file__).parent.parent.parent / ".env",
]:
    if _candidate.exists():
        load_dotenv(dotenv_path=_candidate)
        log.debug("Loaded .env from: %s", _candidate)
        break

LINKEDIN_USERNAME = os.getenv("LINKEDIN_USERNAME")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

DESKTOP_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.2210.61",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.2; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")


def get_driver() -> webdriver.Firefox:
    log.info("Initializing Firefox WebDriver")
    options = webdriver.FirefoxOptions()
    ua = random.choice(DESKTOP_USER_AGENTS)
    options.set_preference("general.useragent.override", ua)
    log.debug("User-Agent: %s", ua)
    driver = webdriver.Firefox(
        service=FirefoxService(GeckoDriverManager().install()),
        options=options,
    )
    log.info("Firefox WebDriver ready")
    return driver


def _find_in_viewport(driver, css_selector: str, timeout: int = 15):
    """
    DOM analysis of debug_login_failure.html shows LinkedIn renders TWO login forms:
      Form 1 (mobile, hidden off-screen) - first in DOM
      Form 2 (desktop, visible)          - second in DOM

    is_displayed() is unreliable here because both forms report as 'displayed'.
    getBoundingClientRect() is the ground truth - if width/height/top are all
    positive and top < innerHeight, the element is actually on-screen.
    """
    def _check(d):
        return d.execute_script(
            """
            var els = document.querySelectorAll(arguments[0]);
            var vh  = window.innerHeight;
            for (var i = 0; i < els.length; i++) {
                var r = els[i].getBoundingClientRect();
                if (r.width > 0 && r.height > 0 && r.top >= 0 && r.top < vh) {
                    return els[i];
                }
            }
            return null;
            """,
            css_selector,
        )
    return WebDriverWait(driver, timeout).until(
        _check,
        message=f"No viewport-visible element for: {css_selector}",
    )


def _human_click(driver, element) -> None:
    """Move the mouse to the element and click — exactly as a human would."""
    ActionChains(driver) \
        .move_to_element(element) \
        .pause(random.uniform(0.15, 0.40)) \
        .click() \
        .perform()
    time.sleep(random.uniform(0.20, 0.40))


def _human_type(driver, text: str) -> None:
    """
    Type into whichever element currently has focus, one character at a time,
    with randomised inter-keystroke delay. Sends to the active element, not to
    a specific element reference, so there is no risk of hitting the wrong twin.
    """
    for char in text:
        ActionChains(driver).send_keys(char).perform()
        time.sleep(random.uniform(0.06, 0.18))


def linkedin_login(driver) -> bool:
    """
    Step-by-step human login flow.

    DOM findings (from debug_login_failure.html inspection):
    ┌─────────────────────────────────────────────────────────────────┐
    │ INPUT 0  type=email    autocomplete='username'         ← HIDDEN │
    │ INPUT 1  type=password autocomplete='current-password' ← HIDDEN │
    │ INPUT 3  type=email    autocomplete='username webauthn'← VISIBLE │
    │ INPUT 4  type=password autocomplete='current-password' ← VISIBLE │
    └─────────────────────────────────────────────────────────────────┘
    Desktop email field is uniquely identified by autocomplete='username webauthn'.
    Password fields share the same autocomplete; use viewport check to get visible one.

    Returns True on success, False on failure (browser left open for inspection).
    """
    log.info("--- LOGIN START ---")
    driver.get("https://www.linkedin.com/login")

    # Let React fully hydrate before touching anything
    time.sleep(random.uniform(3.0, 5.0))
    log.debug("Page settled | URL: %s", driver.current_url)

    try:
        # ── Step 1: Click the visible email field ──────────────────────────
        # 'username webauthn' is ONLY on the desktop (visible) form.
        # The hidden mobile form uses plain 'username' — never target that.
        log.info("Step 1 | Finding desktop email field (autocomplete='username webauthn')")
        email_el = _find_in_viewport(driver, "input[autocomplete='username webauthn']", timeout=15)
        log.info("Step 1 | Email field in viewport — moving mouse + clicking")
        _human_click(driver, email_el)

        # ── Step 2: Type email ─────────────────────────────────────────────
        log.info("Step 2 | Typing email (%d chars)", len(LINKEDIN_USERNAME))
        _human_type(driver, LINKEDIN_USERNAME)
        time.sleep(random.uniform(0.5, 1.0))

        # ── Step 3: Click the visible password field ───────────────────────
        # Both forms share autocomplete='current-password'; use viewport check.
        log.info("Step 3 | Finding visible password field")
        pwd_el = _find_in_viewport(driver, "input[autocomplete='current-password']", timeout=10)
        log.info("Step 3 | Password field in viewport — moving mouse + clicking")
        _human_click(driver, pwd_el)

        # ── Step 4: Type password ──────────────────────────────────────────
        log.info("Step 4 | Typing password (%d chars)", len(LINKEDIN_PASSWORD))
        _human_type(driver, LINKEDIN_PASSWORD)
        time.sleep(random.uniform(0.5, 1.0))

        # ── Step 5: Click the visible 'Sign in' button ─────────────────────
        # Find by innerText + viewport so we never hit the hidden-form button.
        log.info("Step 5 | Finding visible Sign in button")
        sign_in_btn = driver.execute_script(
            """
            var btns = document.querySelectorAll("button");
            var vh   = window.innerHeight;
            for (var i = 0; i < btns.length; i++) {
                var r    = btns[i].getBoundingClientRect();
                var text = btns[i].innerText.trim();
                if (text === 'Sign in' && r.width > 0 && r.height > 0
                        && r.top >= 0 && r.top < vh) {
                    return btns[i];
                }
            }
            return null;
            """
        )
        if sign_in_btn:
            log.info("Step 5 | Sign in button found — moving mouse + clicking")
            _human_click(driver, sign_in_btn)
        else:
            log.warning("Step 5 | Button not found — pressing RETURN as fallback")
            ActionChains(driver).send_keys(Keys.RETURN).perform()

        # ── Step 6: Detect successful login ────────────────────────────────
        # LinkedIn removed id="global-nav" in their 2026 redesign.
        # Checking the URL leaving /login/ is the most reliable signal.
        log.info("Step 6 | Waiting for redirect away from /login/ (up to 30s)...")
        WebDriverWait(driver, 30).until(
            lambda d: "/login" not in d.current_url
        )
        log.info("--- LOGIN SUCCESS | landed on: %s ---", driver.current_url)
        return True

    except Exception as e:
        log.error("Login failed: %s", e)
        log.error("URL at failure: %s", driver.current_url)
        _save_debug_page(driver, "debug_login_failure.html")
        return False


def _save_debug_page(driver, filename: str) -> None:
    debug_path = Path(__file__).parent.parent / "logs" / filename
    try:
        debug_path.write_text(driver.page_source, encoding="utf-8")
        log.info("Saved debug page source to: %s", debug_path)
    except Exception as ex:
        log.warning("Could not save debug page: %s", ex)


def build_linkedin_search_url(query: str, location: str) -> str:
    base = "https://www.linkedin.com/search/results/content/?"
    params = f"keywords={quote_plus(query)}"
    if location:
        params += f"&location={quote_plus(location)}"
    params += "&origin=SWITCH_SEARCH_VERTICAL"
    url = base + params
    log.debug("Search URL: %s", url)
    return url


def set_sort_to_latest(driver) -> None:
    log.info("Setting sort order to 'Latest'")
    try:
        # DOM analysis (debug_search_page.html): Sort button is a <div role="button">
        # with componentkey="SearchResults_filter_pill_sortBy" — NOT a <button> element.
        # componentkey is derived from the React component name, stable across CSS rebuilds.
        sort_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "[componentkey='SearchResults_filter_pill_sortBy']")
            )
        )
        log.info("Sort button found via componentkey — clicking")
        _human_click(driver, sort_button)
        time.sleep(2)

        # Capture the open dropdown so we can refine the 'Latest' selector if needed.
        _save_debug_page(driver, "debug_sort_open.html")

        # Try multiple selectors for the 'Latest' option in the dropdown.
        latest_xpaths = [
            "//label[normalize-space()='Latest']",
            "//label[contains(text(),'Latest')]",
            "//span[normalize-space()='Latest']",
            "//*[@role='option' and contains(.,'Latest')]",
            "//*[@role='radio' and contains(.,'Latest')]",
            "//li[contains(.,'Latest')]",
        ]
        latest_option = None
        for xpath in latest_xpaths:
            try:
                latest_option = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                log.info("'Latest' option found via: %s", xpath)
                break
            except Exception:
                log.debug("Not found: %s", xpath)

        if latest_option:
            _human_click(driver, latest_option)
            log.info("Sort: 'Latest' selected — looking for 'Show results' button")
            time.sleep(1)

            # DOM analysis (debug_sort_open.html): "Show results" is an <a> tag,
            # not a <button>. The href always contains FACETED_SEARCH after selecting
            # a filter — most stable anchor across LinkedIn redesigns.
            show_results_xpaths = [
                "//a[contains(@href,'FACETED_SEARCH')]",
                "//a[.//span[normalize-space()='Show results']]",
                "//a[normalize-space(.)='Show results']",
            ]
            show_results_btn = None
            for xpath in show_results_xpaths:
                try:
                    show_results_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    log.info("'Show results' found via: %s", xpath)
                    break
                except Exception:
                    log.debug("'Show results' not found via: %s", xpath)

            if show_results_btn:
                _human_click(driver, show_results_btn)
                log.info("Sort set to 'Latest' — waiting for results to reload")
                time.sleep(3)
            else:
                log.warning("'Show results' button not found — filter may not have applied; check debug_sort_open.html")
        else:
            log.warning("'Latest' option not found — check debug_sort_open.html for actual dropdown HTML")
    except Exception as e:
        log.warning("Could not set sort to Latest: %s", e)
        _save_debug_page(driver, "debug_sort_failure.html")


def _expand_see_more(driver) -> int:
    """
    Click all visible '...see more' / 'see more' buttons on the current page
    so truncated post bodies are fully expanded before we harvest emails.
    Uses JS click to avoid scroll-into-view overhead on each button.
    """
    expanded = 0
    try:
        buttons = driver.find_elements(
            By.XPATH,
            "//button[contains(normalize-space(.), 'see more')]"
            " | //span[normalize-space(text())='…see more']"
        )
        for btn in buttons:
            try:
                driver.execute_script("arguments[0].click();", btn)
                expanded += 1
                time.sleep(random.uniform(0.05, 0.20))
            except Exception:
                pass
    except Exception as e:
        log.debug("_expand_see_more error: %s", e)
    if expanded:
        log.debug("Expanded %d 'see more' button(s)", expanded)
    return expanded


def infinite_scroll(driver, max_scrolls: int = 20) -> None:
    log.info("Starting infinite scroll (max=%d)", max_scrolls)

    def _post_count() -> int:
        return len(driver.find_elements(
            By.CSS_SELECTOR, "[data-testid='lazy-column'] a[componentkey]"
        ))

    last_count = _post_count()
    log.info("Initial post count: %d", last_count)
    stable_streak = 0

    for i in range(max_scrolls):
        # Scroll the last loaded post card into view — this fires LinkedIn's
        # intersection observers that trigger the next batch fetch, which
        # window.scrollTo(0, scrollHeight) misses because it teleports past them.
        posts = driver.find_elements(
            By.CSS_SELECTOR, "[data-testid='lazy-column'] a[componentkey]"
        )
        if posts:
            driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                posts[-1]
            )
        else:
            driver.execute_script(f"window.scrollBy(0, {random.randint(400, 800)});")

        # Expand any truncated posts while waiting for new ones to load
        _expand_see_more(driver)

        # Human-like pause: 20% chance of a longer "reading" stop
        if random.random() < 0.20:
            pause = random.uniform(4.0, 7.0)
            log.debug("Scroll %d/%d — reading pause %.1fs", i + 1, max_scrolls, pause)
        else:
            pause = random.uniform(1.5, 3.5)
            log.debug("Scroll %d/%d — pause %.1fs", i + 1, max_scrolls, pause)
        time.sleep(pause)

        # Small randomised nudge after the pause to catch the lazy-load sentinel
        driver.execute_script(f"window.scrollBy(0, {random.randint(80, 250)});")
        time.sleep(random.uniform(0.4, 0.9))

        new_count = _post_count()
        log.debug("Post count after scroll %d: %d", i + 1, new_count)

        if new_count == last_count:
            stable_streak += 1
            if stable_streak >= 3:
                log.info("Post count stable at %d after %d checks — stopping", new_count, stable_streak)
                break
            log.debug("No new posts (%d) — streak %d/3", new_count, stable_streak)
        else:
            stable_streak = 0
            log.info("Scroll %d: +%d posts (total %d)", i + 1, new_count - last_count, new_count)
        last_count = new_count

    # Final pass: expand any remaining truncated posts before extraction
    expanded = _expand_see_more(driver)
    log.info("Scroll phase complete | final post count: %d | final expansions: %d", last_count, expanded)


def extract_emails_from_posts(driver) -> set:
    log.info("Extracting emails from post elements")
    containers = driver.find_elements(By.CSS_SELECTOR, "[data-testid='lazy-column']")
    if not containers:
        log.warning("lazy-column not found — falling back to page source only")
        return set()

    posts = containers[0].find_elements(By.XPATH, ".//a[@componentkey]")
    log.info("Found %d post cards in lazy-column", len(posts))

    found: set = set()
    for post in posts:
        try:
            # Use JS innerText rather than .text — catches expanded 'see more'
            # content that Selenium's .text property sometimes misses.
            text = driver.execute_script("return arguments[0].innerText;", post) or ""
            found.update(EMAIL_REGEX.findall(text))
        except Exception as e:
            log.debug("Error reading post card: %s", e)
    log.info("Post card extraction: %d unique emails", len(found))
    return found


def extract_emails_from_page_source(driver) -> set:
    log.info("Extracting emails from full page source")
    emails = set(EMAIL_REGEX.findall(driver.page_source))
    log.info("Page source extraction: %d unique emails", len(emails))
    return emails


def load_existing_emails(filename: str) -> set:
    try:
        df = pd.read_csv(filename)
        emails = set(df["email"].dropna().astype(str))
        log.info("Loaded %d existing emails from %s", len(emails), filename)
        return emails
    except FileNotFoundError:
        log.info("No existing file at %s — starting fresh", filename)
        return set()
    except Exception as e:
        log.warning("Could not load existing emails: %s", e)
        return set()


def save_emails_to_csv(emails: set, filename: str) -> None:
    existing = load_existing_emails(filename)
    all_emails = existing.union(emails)
    df = pd.DataFrame({"email": list(all_emails)})
    df["extracted_at"] = datetime.now().isoformat()
    df.to_csv(filename, index=False)
    log.info("Saved %d emails to %s (new this run: %d)",
             len(all_emails), filename, len(emails - existing))


def run_scraper(
    query: str = "Hiring Full Stack",
    location: str = "India",
    target: int = 10,
    max_scrolls: int = 20,
) -> None:
    log.info("=== run_scraper START | query=%s | location=%s | target=%d ===",
             query, location, target)

    if not LINKEDIN_USERNAME or not LINKEDIN_PASSWORD:
        log.error("LINKEDIN_USERNAME or LINKEDIN_PASSWORD missing in .env — aborting")
        return

    search_url = build_linkedin_search_url(query, location)
    output_file = str(OUTPUT_DIR / "extracted_emails.csv")

    driver = get_driver()
    try:
        if not linkedin_login(driver):
            log.error("Login failed — browser open 30s for manual inspection")
            time.sleep(30)
            return

        delay = random.uniform(2, 5)
        log.info("Pausing %.2fs before navigating to results", delay)
        time.sleep(delay)

        log.info("Navigating to search results")
        driver.get(search_url)
        time.sleep(6)

        log.info("Current URL after search nav: %s", driver.current_url)
        _save_debug_page(driver, "debug_search_page.html")

        set_sort_to_latest(driver)
        infinite_scroll(driver, max_scrolls=max_scrolls)

        post_emails = extract_emails_from_posts(driver)
        page_emails = extract_emails_from_page_source(driver)
        all_emails = post_emails.union(page_emails)

        limited = set(list(all_emails)[:target])
        log.info("Total found: %d | Saving up to target=%d", len(all_emails), target)
        save_emails_to_csv(limited, output_file)

    finally:
        log.info("Quitting WebDriver")
        driver.quit()
        log.info("=== run_scraper END ===")
