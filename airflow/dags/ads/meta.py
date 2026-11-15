import json
import os

import requests

BASE_URL = os.environ.get("META_API_BASE_URL", "https://graph.huydata.com/v21.0")
INSIGHT_FIELDS = [
    "account_id",
    "account_name",
    "campaign_id",
    "campaign_name",
    "adset_id",
    "adset_name",
    "ad_id",
    "ad_name",
    "objective",
    "date_start",
    "date_stop",
    "spend",
    "impressions",
    "reach",
    "frequency",
    "clicks",
    "ctr",
    "cpc",
    "cpm",
    "actions",
    "action_values",
    "cost_per_action_type",
    "purchase_roas",
    "video_play_actions",
]


class MetaApiError(Exception):
    """Raised when Meta returns an error. Never includes the token."""


def _get(path, token, params):
    """Send a GET to the Meta API and return the JSON body."""
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
    """Return all ad accounts the token can access."""
    params = {"fields": "id,account_id,name,promoted_app_store_url", "limit": 100}
    body = _get("/me/adaccounts", token, params)
    if "next" in body.get("paging", {}):
        raise MetaApiError("Expected all ad accounts in one page, but got paging next")
    return body.get("data", [])


def get_ad_insights(token, account_id, day):
    """Return every raw insights row for one ad account on one day."""
    params = {
        "fields": ",".join(INSIGHT_FIELDS),
        "time_range": json.dumps({"since": day, "until": day}),
        "time_increment": 1,
        "level": "ad",
        "breakdowns": "country",
        "limit": 500,
    }
    rows = []
    while True:
        body = _get(f"/act_{account_id}/insights", token, params)
        rows.extend(body.get("data", []))
        paging = body.get("paging", {})
        if "next" not in paging:
            break
        params["after"] = paging["cursors"]["after"]
    return rows

