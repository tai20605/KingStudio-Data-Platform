import pytest

from ads.meta import MetaApiError, _get, get_ad_insights, list_ad_accounts


def test_get_success(fake_api):
    calls = fake_api({"data": [{"id": "act_1"}]})

    assert _get("/me/adaccounts", "secret-token", {}) == {"data": [{"id": "act_1"}]}
    assert calls[0]["headers"] == {"Authorization": "Bearer secret-token"}


def test_get_raises_on_api_error(fake_api):
    fake_api({"error": {"code": 190, "message": "Invalid token"}})
    with pytest.raises(MetaApiError) as exc_info:
        _get("/me/adaccounts", "secret-token", {})

    assert "190" in str(exc_info.value)
    assert "secret-token" not in str(exc_info.value)


def test_list_ad_accounts_one_page(fake_api):
    accounts = [{"id": "act_1", "account_id": "1"}, {"id": "act_2", "account_id": "2"}]
    calls = fake_api({"data": accounts, "paging": {"cursors": {"after": "b"}}})

    assert list_ad_accounts("secret-token") == accounts
    assert calls[0]["url"].endswith("/me/adaccounts")


def test_get_ad_insights_two_pages(fake_api):
    page1 = {"data": [{"ad_id": "1"}], "paging": {"cursors": {"after": "c1"}, "next": "x"}}
    page2 = {"data": [{"ad_id": "2"}]}
    calls = fake_api(page1, page2)
    rows = get_ad_insights("secret-token", "123", "2026-11-01")
    
    assert rows == [{"ad_id": "1"}, {"ad_id": "2"}]
    assert len(calls) == 2
    assert "after" not in calls[0]["params"]
    assert calls[1]["params"]["after"] == "c1"


def test_get_ad_insights_empty_day(fake_api):
    calls = fake_api({"data": []})
    rows = get_ad_insights("secret-token", "123", "2026-11-01")

    assert rows == []
    assert len(calls) == 1
    assert calls[0]["url"].endswith("/act_123/insights")