import os

from dotenv import load_dotenv
from pymongo import AsyncMongoClient

load_dotenv()
DB_URI = os.getenv("DB_URI")

if not DB_URI:
    raise RuntimeError("DB_URL is not set")


# Create the MongoDB client
client = AsyncMongoClient(DB_URI, tls=True)

# Select the database
db = client["expense_tracker"]

# Select the collection
users_collection = db["users"]
income_collection = db["incomes"]
expense_collection = db["expenses"]
category_collection = db["category"]
budget_collection = db["budget"]


# Create unique indexes
async def create_indexes():
    await users_collection.create_index("username", unique=True)
    await users_collection.create_index("email", unique=True)


try:
    client.admin.command("ping")
    print("✅ MongoDB connected successfully!")
except Exception as e:
    print("❌ MongoDB connection failed:", e)
