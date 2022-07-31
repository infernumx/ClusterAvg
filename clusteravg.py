import requests
import copy
import time
import json
import sys

SEARCH_DELAY = 0  # delay between each search in seconds
LEAGUE = "Sentinel"

base_query = {
    "query": {
        "status": {"option": "online"},
        "stats": [{"type": "and", "filters": [], "disabled": False}],
    },
    "sort": {"price": "asc"},
}

with open("mod_dump.json") as f:
    stats = json.load(f)

with open(f"configs/{sys.argv[1]}.json") as f:
    clusters = json.load(f)

headers = {
    "Content-Type": "application/json",
    "Origin": "https://www.pathofexile.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0 Win64 x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/87.0.4280.141 Safari/537.36",
}


def poeninja_currency():
    r = requests.get(
        url=f"https://poe.ninja/api/data/currencyoverview?league={LEAGUE}"
        "&type=Currency"
    )
    if r.status_code == 200:
        if j := r.json():
            data = {}
            for c in j["lines"]:
                data[c["currencyTypeName"]] = c["chaosEquivalent"]
            return data

    return {}


def get_cluster_avg(data):
    r = requests.post(
        url=f"https://www.pathofexile.com/api/trade/search/{LEAGUE}",
        headers=headers,
        data=json.dumps(data),
    )

    if not (js := r.json()):
        return

    ids = ",".join(js["result"][:10])
    r = requests.get(
        url="https://www.pathofexile.com/api/trade/fetch/" f'{ids}?query={js["id"]}',
        headers={
            "Origin": "https://www.pathofexile.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0 Win64 x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/87.0.4280.141 Safari/537.36",
        },
    )

    if not (js := r.json()):
        return

    ex_price = poeninja_currency()["Exalted Orb"]
    total = 0
    count = 0

    for item in js["result"]:
        amt = item["listing"]["price"]["amount"]
        c_type = item["listing"]["price"]["currency"]
        if c_type == "exalted":
            total += float(f"{amt * ex_price:.2f}")
            count += 1
        elif c_type == "chaos":
            total += amt
            count += 1

    return float(f"{total / count:.2f}")


for cluster in clusters:
    data = copy.deepcopy(base_query)
    data["query"]["stats"][0]["filters"] = [
        {"id": stats[mod], "disabled": False} for mod in cluster
    ]

    avg = get_cluster_avg(data)
    header = "\n".join("* " + mod for mod in cluster)
    ex_price = poeninja_currency()["Exalted Orb"]
    print(f"{header}\n  Avg: {avg}c ({avg / ex_price:.2f} ex)\n")
    time.sleep(SEARCH_DELAY)
