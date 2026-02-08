import asyncio
from datetime import datetime, timedelta, timezone
from . import mongo, cache

async def flush_analytics_to_mongo():
    """
    Runs periodically. 
    Scans Redis for 'stats:*' keys and upserts them into MongoDB.
    """

    redis = await cache.get_redis()
    mongo_db = await mongo.get_mongo_db()

    # 1. Scan for analytics keys in redis
    keys = []
    async for key in redis.scan_iter("stats:*:*"):
        keys.append(key)

    if not keys:
        return 
    
    print(f"Flushing {len(keys)} analytics keys to Mongo...")

    for key in keys:
        # Key format: stats:short_key:hour_string
        parts = key.split(":")
        short_code = parts[1]
        hour_str = parts[2]

        # getting data from redis
        data = await redis.hgetall(key)
        if not data:
            continue

        update_doc = {
            "$inc": {}
        }

        for field, count in data.items():
            count = int(count)
            if field == "total":
                update_doc["$inc"]["total_clicks"] = count
            elif field.startswith("ua:"):
                browser = field.split(":")[1]
                update_doc["$inc"][f"browsers.{browser}"] = count
            elif field.startswith("ref:"):
                ref = field.split(":")[1].replace(".", "_")
                update_doc["$inc"][f"referers.{ref}"] = count
            elif field.startswith("country:"):
                country = field.split(":")[1]
                update_doc["$inc"][f"locations.countries.{country}"] = count
            elif field.startswith("city:"):
                city = field.split(":")[1].replace(".", "_")
                update_doc["$inc"][f"locations.cities.{city}"] = count

        await mongo_db.hourly_stats.update_one(
            {
                "short_code": short_code, 
                "hour": hour_str
            },
            update_doc,
            upsert=True
        )

        await redis.delete(key)

    print("Analytics Flush Complete.")