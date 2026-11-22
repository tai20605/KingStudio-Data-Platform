from ads.bronze import build_bronze_rows


def test_build_bronze_rows_wraps_raw_row():
    row = {"ad_id": "1", "spend": "12.34"}

    result = build_bronze_rows(
        [row], "meta", "123", "2026-11-18", "2026-11-19T07:31:00+00:00"
    )

    assert len(result) == 1
    assert result[0]["raw"] == row
    assert result[0]["source"] == "meta"
    assert result[0]["account_id"] == "123"
    assert result[0]["report_date"] == "2026-11-18"
    assert result[0]["extracted_at"] == "2026-11-19T07:31:00+00:00"


def test_build_bronze_rows_empty():
    assert (
        build_bronze_rows([], "meta", "123", "2026-11-18", "2026-11-19T07:31:00+00:00")
        == []
    )
