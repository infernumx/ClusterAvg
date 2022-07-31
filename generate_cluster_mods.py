import requests
from pprint import pprint
import re
import json

headers = {
    'Origin': 'https://www.pathofexile.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0 Win64 x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/87.0.4280.141 Safari/537.36'
}

r = requests.get(
    url='https://www.pathofexile.com/api/trade/data/stats',
    headers=headers
)

if js := r.json():
    mods = js['result']
    ret = {}
    for x in mods:
        if x['label'] != 'Explicit':
            continue
        for mod in x['entries']:
            if e := re.search(r'1 Added Passive Skill is (.*)',
                              mod['text']):
                ret[e.group(1)] = mod['id']

    with open('mod_dump.json', 'w+') as f:
        json.dump(ret, f, indent=4)
