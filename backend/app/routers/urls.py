from fastapi import APIRouter, Depends, HTTPException, Body, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .. import schemas, database, models, auth, utils, cache, rate_limiter, mongo
import redis.asyncio as redis
import json
from datetime import datetime, timezone
from fastapi import BackgroundTasks

router = APIRouter(tags=["URLs"])

@router.post("/shorten", response_model=schemas.UrlResponse, dependencies = [Depends(rate_limiter.RateLimiter(request_limit=2, time_window=60))])
async def create_url(
    url_data: schemas.UrlCreate, 
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    # 1. Generate the unique Snowflake ID
    new_id = utils.get_snowflake_id()

    query = select(models.Url).where(
        models.Url.original_url == str(url_data.original_url),
        models.Url.user_id == current_user.id
    )
    result_duplicate = await db.execute(query)
    existing_url = result_duplicate.scalars().first()
    
    if existing_url:
        return existing_url
    
    # 2. Determine the Short Code
    if url_data.custom_alias:
        query = select(models.Url).where(models.Url.short_code == url_data.custom_alias)
        result = await db.execute(query)
        if result.scalars().first():
            raise HTTPException(status_code=400, detail="Alias already taken")
        short_code = url_data.custom_alias
        print(url_data.custom_alias, short_code)
    else:
        # Auto-generate from the ID
        short_code = utils.encode_base62(new_id)
        print(new_id, short_code)

    # 3. Create the Database Object
    new_url = models.Url(
        id=new_id,
        original_url=str(url_data.original_url),
        short_code=short_code,
        user_id=current_user.id,
        pin = url_data.pin,
        expiry_date = url_data.expiry_date,
        status = "working"
    )

    # 4. Save to DB
    db.add(new_url)
    await db.commit()
    await db.refresh(new_url)

    background_tasks.add_task(
        utils.scan_url_background, 
        new_url.id, 
        str(url_data.original_url), 
        db
    )

    return new_url

@router.get("/{short_code}")
async def redirect_to_url(
    short_code: str, 
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(database.get_db), 
    redis_conn: redis.Redis = Depends(cache.get_redis),
    mongo_db = Depends(mongo.get_mongo_db)
):
    # 1. find the URL in Redis
    cached_url = await redis_conn.get(f"url:{short_code}")
    url_entry = None
    
    if cached_url:
        url_entry = json.loads(cached_url)

    if not url_entry :
        # 2. Find the URL by short code
        query = select(models.Url).where(models.Url.short_code == short_code)
        result = await db.execute(query)
        
        url_entry = result.scalars().first()

        # 3. If not found, return 404
        if not url_entry:
            raise HTTPException(status_code=404, detail="URL not found")
        
        url_entry = {
            "id": url_entry.id,
            "original_url": url_entry.original_url,
            "expiry_date": url_entry.expiry_date.isoformat() if url_entry.expiry_date else None,
            "pin": url_entry.pin,
            "status": url_entry.status
        }
        
        # 4. Adding codurl_datae and url to redis
        await redis_conn.set(
            f"url:{short_code}",
            json.dumps(url_entry),
            ex=3600
        )

    # A. Check Status
    current_status = url_entry.get("status", "working")
    if current_status != "working":
         raise HTTPException(status_code=403, detail="Link is disabled")

    # B. Check Expiry
    expiry_str = url_entry.get("expiry_date")
    if expiry_str:
        expiry_dt = datetime.fromisoformat(expiry_str)
        if expiry_dt < datetime.now(timezone.utc):
            raise HTTPException(status_code=410, detail="Link has expired")
        
    # C. Check PIN 
    if url_entry.get("pin"):
        raise HTTPException(status_code=401, detail="PIN_REQUIRED")
    if request.method == "GET":
        u_id = url_entry.get("id")
        background_tasks.add_task(
            utils.track_click_background,
            u_id,
            short_code,    
            request.client.host,
            request.headers.get("User-Agent", "Unknown"),
            request.headers.get("Referer", None),
            None,           
            redis_conn
        )     

    # 5. Redirect the user (307 Temporary Redirect is standard)
    return RedirectResponse(url=url_entry.get("original_url"), status_code=307)

@router.post("/{short_code}/verify")
async def verify_pin(
    short_code : str,
    pin_input : int = Body(..., embed = True),
    db : AsyncSession = Depends(database.get_db),
    redis_conn: redis.Redis = Depends(cache.get_redis)
):
    url_entry = None

    cached_url = await redis_conn.get(f"url:{short_code}")

    if cached_url:
        url_entry = json.loads(cached_url)


    if not url_entry:
        query = select(models.Url).where(models.Url.short_code == short_code)
        result = await db.execute(query)
        url_entry = result.scalars().first()

        url_entry = {
            "original_url":url_entry.original_url,
            "pin":url_entry.pin
        }

    if not url_entry:
        raise HTTPException(status_code=404, detail="URL not found")

    if not url_entry.get("pin"):
        return {"original_url": url_entry['original_url']}
    
    if url_entry.get("pin") != pin_input:
        raise HTTPException(status_code=401, detail="Incorrect PIN")
    
    return {"original_url": url_entry['original_url']}


# --- 3. Analytics Endpoint ---

def parse_redis_hash(data: dict) -> dict:
    """
    Converts Redis flat hash {'ua:Chrome': '5', 'total': '10'} 
    into nested dict {'browsers': {'Chrome': 5}, 'total_clicks': 10}
    """
    result = {
        "total_clicks": int(data.get("total", 0)),
        "browsers": {},
        "referers": {},
        "locations": { "countries": {}, "cities": {} }
    }
    
    for key, value in data.items():
        if key.startswith("ua:"):
            browser = key.split(":")[1]
            result["browsers"][browser] = int(value)
        elif key.startswith("ref:"):
            referer = key.split(":")[1]
            result["referers"][referer] = int(value)
        elif key.startswith("country:"):
            country = key.split(":")[1]
            result["locations"]["countries"][country] = int(value)
        elif key.startswith("city:"):
            city = key.split(":")[1]
            result["locations"]["cities"][city] = int(value)
            
    return result

# --- 1. LVIE ENDPOINT REDIS ---
@router.get("/{short_code}/analytics/live", response_model=schemas.LiveAnalytics)
async def get_live_analytics(
    short_code: str,
    redis_conn: redis.Redis = Depends(cache.get_redis),
    current_user: models.User = Depends(auth.get_current_user)
):
    # 1. Get Current Hour Key
    current_hour = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H")
    redis_key = f"stats:{short_code}:{current_hour}"

    # 2. Fetch Raw Data
    raw_data = await redis_conn.hgetall(redis_key)
    
    # 3. Parse & Return
    parsed_data = parse_redis_hash(raw_data)
    
    return {
        "total_clicks": parsed_data["total_clicks"],
        "browsers": parsed_data["browsers"],
        "referers": parsed_data["referers"],
        "locations": parsed_data["locations"],
        "last_updated": datetime.now(timezone.utc)
    }

# --- 2. HISTORICAL ENDPOINT FROM MONGODB --- 
@router.get("/{short_code}/analytics/", response_model=schemas.HistoricalAnalytics)
async def get_historical_analytics(
    short_code: str,
    db: AsyncSession = Depends(database.get_db),
    mongo_db = Depends(mongo.get_mongo_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # 1. Verify Ownership (Postgres)
    query = select(models.Url).where(models.Url.short_code == short_code)
    result = await db.execute(query)
    url_obj = result.scalars().first()

    if not url_obj:
        raise HTTPException(status_code=404, detail="URL not found")
    
    if url_obj.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # 2. Query MongoDB (Last 48 hours)
    cursor = mongo_db.hourly_stats.find({"short_code": short_code})
    cursor.sort("hour", -1).limit(48)
    
    history_data = await cursor.to_list(length=48)

    # 3. Format Response
    total_clicks = 0
    formatted_history = []

    for doc in history_data:
        # Summing up historical total
        clicks = doc.get("total_clicks", 0)
        total_clicks += clicks
        loc_data = doc.get("locations", {})
        
        formatted_history.append({
            "hour": doc.get("hour"),
            "total_clicks": clicks,
            "browsers": doc.get("browsers", {}),
            "referers": doc.get("referers", {}),
            "locations": {
                "countries": loc_data.get("countries", {}),
                "cities": loc_data.get("cities", {})
            }
        })

    return {
        "total_historical_clicks": total_clicks,
        "history": formatted_history
    }