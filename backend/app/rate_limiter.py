from fastapi import Request, HTTPException, Depends
import redis.asyncio as redis
from . import cache 

class RateLimiter:
    def __init__(self, request_limit : int, time_window : int):
        self.request_limit = request_limit
        self.time_window = time_window

    async def __call__(self, request: Request, redis_conn: redis.Redis = Depends(cache.get_redis)):
        client_id = request.client.host
        key = f"rate_limit:{client_id}:{request.url.path}"
        current_count = await redis_conn.incr(key)
        if current_count == 1:
            await redis_conn.expire(key, self.time_window)
        
        if current_count > self.request_limit:
            raise HTTPException(
                status_code=429, 
                detail="Too Many Requests. Please try again later."
            )