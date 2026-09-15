-- KBC vs ING Google Trends benchmark schema.
-- trends_data is created by collectors/trends_collector.py; kept here too
-- for reference and so a fresh database can be built from this file alone.

CREATE TABLE IF NOT EXISTS trends_data (
    product_id TEXT NOT NULL,
    product_label TEXT NOT NULL,
    term TEXT NOT NULL,
    bank TEXT NOT NULL,
    language TEXT NOT NULL,
    date TEXT NOT NULL,
    value INTEGER NOT NULL,
    UNIQUE (product_id, term, date)
);

CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    product_label TEXT NOT NULL,
    term_count INTEGER NOT NULL
);

-- anomaly_type: 'isolated_spike' (a single flagged week) or
-- 'sustained_trend' (two or more consecutive flagged weeks). See
-- analysis/anomaly_detection.py for the exact detection logic.
CREATE TABLE IF NOT EXISTS anomalies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id TEXT NOT NULL,
    term TEXT NOT NULL,
    bank TEXT NOT NULL,
    date TEXT NOT NULL,
    value INTEGER NOT NULL,
    anomaly_type TEXT NOT NULL CHECK (anomaly_type IN ('isolated_spike', 'sustained_trend')),
    deviation_score REAL NOT NULL,
    UNIQUE (product_id, term, date)
);
