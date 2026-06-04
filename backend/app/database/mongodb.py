from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = AsyncIOMotorClient(MONGODB_URL)

database = client[DATABASE_NAME]

users_collection = database["users"]
applications_collection = database["applications"]


async def connect_to_mongo():
    try:
        await client.admin.command("ping")
        print("MongoDB Connected Successfully")
    except Exception as e:
        print("MongoDB Connection Failed")
        print(e)