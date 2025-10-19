"""
MongoDB database connection using Motor (async MongoDB driver)
"""
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import asyncio
import logging

try:
    from app.config import settings
except ImportError:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from app.config import settings

logger = logging.getLogger(__name__)

mongo_client: Optional[AsyncIOMotorClient] = None
database = None
_db_ready: bool = False


async def connect_to_mongo(retries: int = 3, backoff_seconds: float = 1.0) -> None:
    """Connect to MongoDB with retry logic"""
    global mongo_client, database, _db_ready
    
    attempt = 0
    while attempt <= retries:
        try:
            # Simple connection for local MongoDB
            mongo_client = AsyncIOMotorClient(
                settings.MONGODB_URL,
                serverSelectionTimeoutMS=5000
            )
            database = mongo_client[settings.DATABASE_NAME]

            # Test connection
            await mongo_client.admin.command("ping")
            print(f"✅ Connected to MongoDB: {settings.DATABASE_NAME}")
            logger.info(f"Connected to MongoDB: {settings.DATABASE_NAME}")

            # Create indexes
            try:
                await database.users.create_index("email", unique=True)
                await database.internships.create_index("company")
                await database.internships.create_index("domain")
                logger.info("Database indexes created successfully")
            except Exception as e:
                logger.warning(f"Failed to create indexes: {e}")

            _db_ready = True
            return

        except Exception as e:
            attempt += 1
            _db_ready = False
            logger.warning(f"Attempt {attempt}/{retries}: Error connecting to MongoDB: {e}")
            
            if attempt > retries:
                logger.error("❌ Exceeded maximum MongoDB connection attempts")
                print(f"❌ Could not connect to MongoDB after {retries} attempts")
                print(f"   Error: {str(e)}")
                print(f"   Make sure MongoDB is running: net start MongoDB")
                return
            
            await asyncio.sleep(backoff_seconds * (2 ** (attempt - 1)))


async def close_mongo_connection() -> None:
    """Close MongoDB connection"""
    global mongo_client, _db_ready
    
    if mongo_client:
        try:
            mongo_client.close()
            print("✅ MongoDB connection closed")
            logger.info("MongoDB connection closed")
        except Exception as e:
            logger.error(f"Error closing MongoDB client: {e}")
        finally:
            mongo_client = None
            _db_ready = False


def is_db_ready() -> bool:
    """Check if database is ready"""
    return bool(_db_ready and database is not None)


def get_database():
    """Get database instance"""
    if not _db_ready:
        logger.warning("Database requested but connection is not ready")
    return database