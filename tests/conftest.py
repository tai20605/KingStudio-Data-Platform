import pytest


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


@pytest.fixture
def fake_api(monkeypatch):
    """Replace requests.get with a fake that returns one payload per call."""

    def setup(*payloads):
        calls = []
        queue = list(payloads)

        def fake_get(url, params=None, headers=None, timeout=None):
            calls.append({"url": url, "params": dict(params or {}), "headers": headers})
            return FakeResponse(queue.pop(0))

        monkeypatch.setattr("requests.get", fake_get)
        return calls

    return setup
