import time
import os
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from . import models
from dotenv import load_dotenv
from datetime import datetime, timezone
import geoip2.database

load_dotenv()

# 1. Base62 Encoder (Converts ID -> "abc")
# We use this alphabet to keep codes alphanumeric
BASE62 = "0123456789abcdefghijklmnopqrstuvwxyz"

def encode_base62(num: int) -> str:
    if num == 0:
        return BASE62[0]
    arr = []
    base = len(BASE62)
    while num:
        num, rem = divmod(num, base)
        arr.append(BASE62[rem])
    arr.reverse()
    return ''.join(arr)

# 2. Snowflake ID Generator (Generates ID: 18239...)
# Custom Epoch (Jan 1, 2024)
EPOCH = 170406720000

class SnowflakeGenerator:
    def __init__(self, machine_id=1):
        self.machine_id = machine_id
        self.sequence = 0
        self.last_timestamp = -1
        
        self.machine_id_bits = 0
        self.sequence_bits = 3
        
        self.machine_id_shift = self.sequence_bits
        self.timestamp_shift = self.sequence_bits + self.machine_id_bits
        self.sequence_mask = (1 << self.sequence_bits) - 1

    def _current_timestamp(self):
        return int(time.time() * 100)

    def next_id(self):
        timestamp = self._current_timestamp()

        if timestamp < self.last_timestamp:
            raise Exception("Clock moved backwards!")

        if self.last_timestamp == timestamp:
            self.sequence = (self.sequence + 1) & self.sequence_mask
            if self.sequence == 0:
                while timestamp <= self.last_timestamp:
                    timestamp = self._current_timestamp()
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        return (
            ((timestamp - EPOCH) << self.timestamp_shift) |
            (self.machine_id << self.machine_id_shift) |
            self.sequence
        )

# Create a singleton instance
generator = SnowflakeGenerator(machine_id=1)

def get_snowflake_id():
    return generator.next_id()


#------------------------ Google safe browsing --------------------------------#


GOOGLE_SAFE_BROWSING_API_KEY = os.environ.get("SAFE_BROWSING_KEY")
SAFE_BROWSING_URL = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_SAFE_BROWSING_API_KEY}"

async def scan_url_background(url_id: int, original_url: str, db: AsyncSession):
    """
    Checks URL against Google Safe Browsing. 
    If malicious, disables the link in the DB.
    """
    payload = {
        "client": {
            "clientId": "bitlify",
            "clientVersion": "1.0.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": original_url}
            ]
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(SAFE_BROWSING_URL, json=payload)
        data = response.json()

    # If 'matches' key exists, it's a threat
    if "matches" in data:
        url_obj = await db.get(models.Url, url_id)
        if url_obj:
            url_obj.status = "banned"
            await db.commit()


# --------------------- click tracking ---------------------- # 
GEOIP_PATH = os.path.join(os.path.dirname(__file__), "GeoLite2-City.mmdb")
geo_reader = None

try:
    geo_reader = geoip2.database.Reader(GEOIP_PATH)
except FileNotFoundError:
    print("GeoIP database not found.")

async def track_click_background(
    url_id : int,
    short_code: str,
    ip: str, 
    user_agent: str, 
    referer: str, 
    mongo_db,
    redis_conn
):
    """
    Increments counters in Redis for the current hour.
    """

    current_hour = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H")
    redis_key = f"stats:{short_code}:{current_hour}"

    # User agent information
    ua_simplified = "Other"
    if "Chrome" in user_agent: ua_simplified = "Chrome"
    elif "Firefox" in user_agent: ua_simplified = "Firefox"
    elif "Safari" in user_agent: ua_simplified = "Safari"
    elif "Edge" in user_agent: ua_simplified = "Edge"
    elif "Mobile" in user_agent: ua_simplified = "Mobile"

    # Referer information
    ref_simplified = "Direct"
    if referer:
        try:
            ref_simplified = referer.split("/")[2]
        except:
            pass

    country = "Unknown"
    city = "Unknown"
    
    if geo_reader and ip != "127.0.0.1":
        try:
            response = geo_reader.city(ip)
            country = response.country.iso_code or "Unknown" # e.g. "US", "IN"
            city = response.city.name or "Unknown"           # e.g. "New York"
        except Exception:
            pass
    
    async with redis_conn.pipeline() as pipe:
        # Increment Total
        pipe.hincrby(redis_key, "total", 1)
        pipe.hincrby(redis_key, f"ua:{ua_simplified}", 1)
        pipe.hincrby(redis_key, f"ref:{ref_simplified}", 1)
        pipe.hincrby(redis_key, f"country:{country}", 1)
        pipe.hincrby(redis_key, f"city:{city}", 1)
        
        # Expiry (2 hours in Redis)
        pipe.expire(redis_key, 7200) 
        
        await pipe.execute()