from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)

# Access the database
db = client["assessment_db"]

#Employee collection
employees_collection = db["employees"]

#User collection
users_collection = db["users"]


# index on employee_id
async def init_indexes():
    await employees_collection.create_index("employee_id", unique=True)

