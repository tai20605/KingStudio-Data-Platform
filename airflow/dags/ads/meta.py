import os

import requests

BASE_URL = os.environ.get("META_API_BASE_URL", "https://graph.huydata.com/v21.0")


class MetaApiError(Exception):
    """Raised when Meta returns an error. Never includes the token."""


def _get(path, token, params):
    resp = requests.get(
        BASE_URL + path,
        params=params,
        headers={"Authorization": f"Bearer {token}"},
        timeout=30,
    )
    body = resp.json()
    if "error" in body:
        error = body["error"]
        raise MetaApiError(f"Meta API error {error['code']}: {error['message']}")
    return body


def list_ad_accounts(token):
    params = {"fields": "id,account_id,name,promoted_app_store_url", "limit": 100}
    body = _get("/me/adaccounts", token, params)
    if "next" in body.get("paging", {}):
        raise MetaApiError("Expected all ad accounts in one page, but got paging next")
    return body.get("data", [])
