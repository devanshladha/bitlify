from dotenv import load_dotenv
import redis.asyncio as redis
import os

load_dotenv()

REDIS_URL = os.environ.get("REDIS_URL")

redis_client = redis.from_url(REDIS_URL, decode_responses = True)

async def get_redis():
    return redis_client