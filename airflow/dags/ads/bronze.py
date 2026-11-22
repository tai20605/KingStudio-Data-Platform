from google.cloud import bigquery

BRONZE_SCHEMA = [
    bigquery.SchemaField("source", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("account_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("report_date", "DATE", mode="REQUIRED"),
    bigquery.SchemaField("extracted_at", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("raw", "JSON", mode="REQUIRED"),
]


def build_bronze_rows(
    rows: list[dict],
    source: str,
    account_id: str,
    report_date: str,
    extracted_at: str,
) -> list[dict]:
    """Add Bronze metadata and audit columns to raw API rows."""
    return [
        {
            "raw": row,
            "source": source,
            "account_id": account_id,
            "report_date": report_date,
            "extracted_at": extracted_at,
        }
        for row in rows
    ]


def load_bronze_rows(client: bigquery.Client, table_id: str, rows: list[dict]) -> int:
    """Append Bronze rows to a BigQuery table."""
    if not rows:
        return 0
    job_config = bigquery.LoadJobConfig(
        schema=BRONZE_SCHEMA,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )
    load_job = client.load_table_from_json(rows, table_id, job_config=job_config)
    load_job.result()
    return load_job.output_rows
