import os
from pymongo import AsyncMongoClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.environ.get("MONGODB_URL")

client : AsyncMongoClient = None
db = None 

async def connect_to_mongo():
    global client, db
    client = AsyncMongoClient(MONGODB_URL)
    db = client.bitlify_analytics
    try:
        await client.admin.command('ping')
        print("mongo connection ok")
    except Exception as e:
        print(f"MongoDB Connection Failed: {e}")

async def close_mongo_connection():
    global client 
    if client:
        await client.close()
        print("Mongo connection is closed")

async def get_mongo_db():
    return db