"""Load the campaign catalog (campaigns/seed_data.py) into benchmark.db.

Idempotent: upserts on (bank, name, start_date), so re-running never
duplicates rows and picks up edits to seed_data.py.
"""

import json
import logging
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import DB_PATH, SCHEMA_PATH  # noqa: E402
from seed_data import CAMPAIGNS  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)


def ensure_schema(conn):
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()


def load(conn):
    rows = [
        (
            c["bank"], c["name"], c["language"], c["start_date"], c.get("end_date"),
            c["date_confidence"], c.get("agency"), c["campaign_type"],
            json.dumps(c["target_fiches"]) if c.get("target_fiches") else None,
            c.get("channels"), c.get("source_url"), c.get("notes"),
        )
        for c in CAMPAIGNS
    ]

    conn.executemany(
        """
        INSERT INTO campaigns
            (bank, name, language, start_date, end_date, date_confidence,
             agency, campaign_type, target_fiches, channels, source_url, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT (bank, name, start_date) DO UPDATE SET
            language = excluded.language,
            end_date = excluded.end_date,
            date_confidence = excluded.date_confidence,
            agency = excluded.agency,
            campaign_type = excluded.campaign_type,
            target_fiches = excluded.target_fiches,
            channels = excluded.channels,
            source_url = excluded.source_url,
            notes = excluded.notes
        """,
        rows,
    )
    conn.commit()
    log.info("Loaded %d campaigns (%d KBC, %d CBC, %d ING).", len(rows),
              sum(1 for c in CAMPAIGNS if c["bank"] == "KBC"),
              sum(1 for c in CAMPAIGNS if c["bank"] == "CBC"),
              sum(1 for c in CAMPAIGNS if c["bank"] == "ING"))


def main():
    conn = sqlite3.connect(DB_PATH)
    ensure_schema(conn)
    load(conn)
    conn.close()


if __name__ == "__main__":
    main()
