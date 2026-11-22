-- Bronze table for raw Meta ad insights. Append-only, one row per API row.
CREATE TABLE IF NOT EXISTS `bronze_dev.meta_ad_insights` (
  source STRING NOT NULL,
  account_id STRING NOT NULL,
  report_date DATE NOT NULL,
  extracted_at TIMESTAMP NOT NULL,
  raw JSON NOT NULL
)
PARTITION BY report_date;
