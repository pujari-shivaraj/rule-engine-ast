import motor.motor_asyncio
from app.core.config import settings
from fastapi import HTTPException
import logging

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class MongoDBClient:
    def __init__(self, db_url: str, db_name: str):
        """
        MongoDB Client that manages the connection and provides access to collections.
        :param db_url: MongoDB connection string
        :param db_name: Name of the database
        """
        self.db_url = db_url
        self.db_name = db_name
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.db_url)
        self.db = self.client[self.db_name]

    async def get_collection(self, collection_name: str):
        """
        Get a collection from the MongoDB database.
        :param collection_name: Name of the collection
        :return: The MongoDB collection object
        """
        try:
            return self.db.get_collection(collection_name)
        except Exception as e:
            logger.error(f"Error accessing collection '{collection_name}': {str(e)}")
            raise HTTPException(status_code=500, detail="Error accessing the collection")

# Instantiate the MongoDB client globally
mongo_client = MongoDBClient(db_url=settings.MONGO_URL, db_name="rule_engine")

# Provide a method for accessing the 'rules' collection
async def get_rules_collection():
    """
    Accessor function to get the 'rules' collection.
    This function returns the collection object without closing the connection after each call.
    """
    return await mongo_client.get_collection("rules")
