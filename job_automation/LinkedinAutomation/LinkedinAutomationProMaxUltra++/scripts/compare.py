from pathlib import Path
import pandas as pd
from logger import get_logger

log = get_logger(__name__)

OUTPUT_DIR = Path(__file__).parent.parent / "output"


def compare_and_save(
    extracted: str = str(OUTPUT_DIR / "extracted_emails.csv"),
    database: str = str(OUTPUT_DIR / "EmailDB.csv"),
    output: str = str(OUTPUT_DIR / "new.csv"),
) -> None:
    log.info("Starting email comparison")
    log.info("Extracted: %s | DB: %s", extracted, database)

    df1 = pd.read_csv(extracted)
    df2 = pd.read_csv(database)
    log.info("Extracted count: %d | DB count: %d", len(df1), len(df2))

    result = df1[~df1["EmailAddress"].isin(df2["EmailAddress"])]
    log.info("New unique emails found: %d", len(result))

    result.to_csv(output, index=False)
    log.info("Saved new emails to: %s", output)


if __name__ == "__main__":
    compare_and_save()
