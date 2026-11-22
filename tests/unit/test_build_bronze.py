from google.cloud import bigquery

from ads.bronze import BRONZE_SCHEMA, build_bronze_rows, load_bronze_rows

META = ("meta", "123", "2026-11-18", "2026-11-19T07:31:00+00:00")


class FakeJob:
    output_rows = 1

    def result(self):
        pass


class FakeClient:
    def __init__(self):
        self.calls = []

    def load_table_from_json(self, rows, table_id, job_config):
        self.calls.append((rows, table_id, job_config))
        return FakeJob()


def test_build_rows():
    row = {"ad_id": "1", "spend": "12.34"}
    assert build_bronze_rows([row], *META) == [
        {
            "raw": row,
            "source": "meta",
            "account_id": "123",
            "report_date": "2026-11-18",
            "extracted_at": "2026-11-19T07:31:00+00:00",
        }
    ]


def test_build_rows_empty():
    assert build_bronze_rows([], *META) == []


def test_load_rows_appends_with_schema():
    client = FakeClient()
    assert load_bronze_rows(client, "t", [{"x": 1}]) == 1
    config = client.calls[0][2]
    assert config.write_disposition == bigquery.WriteDisposition.WRITE_APPEND
    assert config.schema == BRONZE_SCHEMA


def test_load_rows_empty_skips_bigquery():
    client = FakeClient()
    assert load_bronze_rows(client, "t", []) == 0
    assert client.calls == []
