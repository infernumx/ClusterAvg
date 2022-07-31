# ClusterAvg
Path of Exile tool which price checks cluster jewels with specific mod combinations

## Requirements
- Python 3.8+

## Usage
- Run `python generate_cluster_mods.py` to dump all cluster mod names and their respective trade API stat keys
- Create desired configs under `/configs` using mod names from `mod_dump.json`
- Run `python clusteravg.py <config_name>` and let the program do the work for you


## Example

JSON Config for popular physical cluster mod combinations
```json
[
    ["Battle-Hardened", "Force Multiplier", "Iron Breaker"],
    ["Battle-Hardened", "Force Multiplier", "Master the Fundamentals"],
    ["Battle-Hardened", "Furious Assault", "Master the Fundamentals"],
    ["Master the Fundamentals", "Force Multiplier", "Iron Breaker"]
]
```

![](https://void.s-ul.eu/xd2lelhN)