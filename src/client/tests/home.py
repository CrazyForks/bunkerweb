import json

home = [
    {
        "type": "card",
        "link": "https://panel.bunkerweb.io/?utm_campaign=self&utm_source=ui#pro",
        "containerColumns": {"pc": 4, "tablet": 6, "mobile": 12},
        "widgets": [
            {
                "type": "Stat",
                "data": {
                    "title": "home_version",
                    "subtitle": "home_upgrade_to_pro",
                    "subtitleColor": "warning",
                    "stat": "home_free",
                    "iconName": "key",
                },
            }
        ],
    },
    {
        "type": "card",
        "link": "https://github.com/bunkerity/bunkerweb",
        "containerColumns": {"pc": 4, "tablet": 6, "mobile": 12},
        "widgets": [
            {
                "type": "Stat",
                "data": {
                    "title": "home_version_number",
                    "subtitle": "home_update_available",
                    "subtitleColor": "warning",
                    "stat": "1.5.8",
                    "iconName": "wire",
                },
            }
        ],
    },
    {
        "type": "card",
        "link": "/instances",
        "containerColumns": {"pc": 4, "tablet": 6, "mobile": 12},
        "widgets": [
            {
                "type": "Stat",
                "data": {
                    "title": "home_instances",
                    "subtitle": "home_total_number",
                    "subtitleColor": "info",
                    "stat": 1,
                    "iconName": "box",
                },
            }
        ],
    },
    {
        "type": "card",
        "link": "/services",
        "containerColumns": {"pc": 4, "tablet": 6, "mobile": 12},
        "widgets": [
            {
                "type": "Stat",
                "data": {
                    "title": "home_services",
                    "subtitle": "home_all_methods_included",
                    "subtitleColor": "info",
                    "stat": 2,
                    "iconName": "disk",
                },
            }
        ],
    },
    {
        "type": "card",
        "link": "/plugins",
        "containerColumns": {"pc": 4, "tablet": 6, "mobile": 12},
        "widgets": [
            {
                "type": "Stat",
                "data": {
                    "title": "home_plugins",
                    "subtitle": "home_no_error",
                    "subtitleColor": "success",
                    "stat": "42",
                    "iconName": "puzzle",
                },
            }
        ],
    },
]

# store on a file
with open("home.json", "w") as f:
    json.dump(home, f, indent=4)
