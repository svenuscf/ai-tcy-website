#!/usr/bin/env python3
"""Add multi-track CMS support and patch only records that contain playlists."""

from __future__ import annotations

import argparse
import os

from seed_wix_cms import COLLECTION_ID, SITE, api, query_all, work_records


def collection_fields(response: dict) -> list[dict]:
    collection = response.get("collection") or response.get("dataCollection") or {}
    return collection.get("fields", [])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-id", required=True)
    parser.add_argument("--token-env", default="TCY_WIX_TOKEN")
    args = parser.parse_args()
    token = os.environ.get(args.token_env)
    if not token:
        parser.error(f"missing token environment variable {args.token_env}")

    schema = api(token, args.site_id, "GET", f"/wix-data/v2/collections/{COLLECTION_ID}")
    if not any(field.get("key") == "audioTracks" for field in collection_fields(schema)):
        api(token, args.site_id, "POST", "/wix-data/v2/collections/create-field", {
            "dataCollectionId": COLLECTION_ID,
            "field": {
                "key": "audioTracks",
                "displayName": "Audio Tracks (agent-managed)",
                "type": "OBJECT",
                "description": "Ordered audio players for works containing more than one track.",
            },
        })

    desired: dict[str, dict] = {}
    for language, prefix in (("zh", SITE), ("en", SITE / "en")):
        for page_key in ("compositions", "reconstruction", "cds-and-books"):
            for record in work_records(page_key, language, prefix / page_key / "index.html"):
                tracks = record.get("audioTracks", {}).get("tracks", [])
                if len(tracks) > 1:
                    desired[str(record["recordKey"])] = record["audioTracks"]

    existing = {item.get("data", {}).get("recordKey"): item for item in query_all(token, args.site_id)}
    missing = set(desired) - set(existing)
    if missing:
        raise RuntimeError(f"CMS records missing: {sorted(missing)}")

    for record_key, audio_tracks in desired.items():
        item = existing[record_key]
        item_id = item.get("id") or item.get("data", {}).get("_id")
        api(token, args.site_id, "PATCH", f"/wix-data/v2/items/{item_id}", {
            "dataCollectionId": COLLECTION_ID,
            "patch": {
                "dataItemId": item_id,
                "fieldModifications": [{
                    "fieldPath": "audioTracks",
                    "action": "SET_FIELD",
                    "setFieldOptions": {"value": audio_tracks},
                }],
            },
        })

    verified = {item.get("data", {}).get("recordKey"): item for item in query_all(token, args.site_id)}
    for record_key, expected in desired.items():
        actual = verified[record_key].get("data", {}).get("audioTracks")
        if actual != expected:
            raise RuntimeError(f"CMS verification failed for {record_key}: {actual!r}")
    print(f"Updated {len(desired)} multilingual playlist records with {sum(len(value['tracks']) for value in desired.values())} tracks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
