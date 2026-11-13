import pytest

from ads.meta import MetaApiError, _get, list_ad_accounts


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


def use_fake_api(monkeypatch, payload):
    calls = []

    def fake_get(url, params=None, headers=None, timeout=None):
        calls.append({"url": url, "params": params, "headers": headers})
        return FakeResponse(payload)

    monkeypatch.setattr("requests.get", fake_get)
    return calls


def test_get_success(monkeypatch):
    calls = use_fake_api(monkeypatch, {"data": [{"id": "act_1"}]})
    assert _get("/me/adaccounts", "secret-token", {}) == {"data": [{"id": "act_1"}]}
    assert calls[0]["headers"] == {"Authorization": "Bearer secret-token"}


def test_get_raises_on_api_error(monkeypatch):
    use_fake_api(monkeypatch, {"error": {"code": 190, "message": "Invalid token"}})
    with pytest.raises(MetaApiError) as exc_info:
        _get("/me/adaccounts", "secret-token", {})
    assert "190" in str(exc_info.value)
    assert "secret-token" not in str(exc_info.value)


def test_list_ad_accounts_one_page(monkeypatch):
    accounts = [{"id": "act_1", "account_id": "1"}, {"id": "act_2", "account_id": "2"}]
    calls = use_fake_api(monkeypatch, {"data": accounts, "paging": {"cursors": {"after": "b"}}})
    assert list_ad_accounts("secret-token") == accounts
    assert calls[0]["url"].endswith("/me/adaccounts")
