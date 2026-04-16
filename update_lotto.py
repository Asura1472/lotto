#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import urllib.request

REMOTE_ALL_URL = "https://smok95.github.io/lotto/results/all.json"
REMOTE_LATEST_URL = "https://smok95.github.io/lotto/results/latest.json"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ALL_JSON = os.path.join(BASE_DIR, "all.json")
LATEST_JSON = os.path.join(BASE_DIR, "latest.json")


def load_local_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_local_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def fetch_json(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=20) as res:
        text = res.read().decode("utf-8", errors="replace").strip()
    return json.loads(text)


def main():
    remote_all = fetch_json(REMOTE_ALL_URL)
    remote_latest = fetch_json(REMOTE_LATEST_URL)

    if not isinstance(remote_all, list):
        raise Exception("원격 all.json 형식이 list가 아님")

    if not isinstance(remote_latest, dict):
        raise Exception("원격 latest.json 형식이 dict가 아님")

    local_all = load_local_json(ALL_JSON, [])

    local_draws = {item.get("draw_no") for item in local_all if isinstance(item, dict)}
    added = 0

    for item in remote_all:
        draw_no = item.get("draw_no")
        if draw_no not in local_draws:
            local_all.append(item)
            local_draws.add(draw_no)
            added += 1

    local_all.sort(key=lambda x: x.get("draw_no", 0))

    save_local_json(ALL_JSON, local_all)
    save_local_json(LATEST_JSON, remote_latest)

    print(f"done, added={added}, latest={remote_latest.get('draw_no')}")


if __name__ == "__main__":
    main()
