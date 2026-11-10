
import requests
import json

API_URL = "https://property-listings-api.vercel.app/api/v1/properties"

limit = 20
offset = 0
all_properties = []

while True:
    response = requests.get(
        API_URL,
        params={
            "limit": limit,
            "offset": offset
        },
        timeout=20
    )

    response.raise_for_status()

    result = response.json()

    properties = result.get("data", [])

    if not properties:
        break

    all_properties.extend(properties)

    pagination = result.get("meta", {}).get("pagination", {})

    if not pagination.get("hasMore"):
        break

    offset += limit

# Save all retrieved properties into JSON
with open("properties_data.json", "w", encoding="utf-8") as file:
    json.dump(
        {
            "success": True,
            "data": all_properties,
            "meta": {
                "pagination": {
                    "total": len(all_properties)
                }
            }
        },
        file,
        indent=4,
        ensure_ascii=False
    )

print("Properties saved:", len(all_properties))
