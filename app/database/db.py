"""MongoDB database connection using Motor (async MongoDB driver)."""

from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import asyncio
import logging

logger = logging.getLogger(__name__)

# Global MongoDB client and database instances
mongo_client = None
database = None
# Readiness flag indicating whether DB is available
_db_ready = False


async def connect_to_mongo(retries=3, backoff_seconds=1.0):
    """Attempt to connect to MongoDB with retries and exponential backoff.

    If the connection cannot be established after the configured attempts,
    the function returns with the internal readiness flag set to False so
    the application can report 503s from health checks instead of crashing.
    """
    global mongo_client, database, _db_ready
    attempt = 0
    while attempt <= retries:
        try:
            mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
            database = mongo_client[settings.DATABASE_NAME]

            # Test connection
            await mongo_client.admin.command("ping")
            logger.info("Connected to MongoDB: %s", settings.DATABASE_NAME)

            # Best-effort index creation
            try:
                await database.users.create_index("email", unique=True)
                await database.internships.create_index("company")
                await database.internships.create_index("domain")
            except Exception:
                logger.exception("Failed to create indexes (continuing)")

            _db_ready = True
            return

        except Exception as e:
            attempt += 1
            _db_ready = False
            logger.warning("Attempt %d/%d: Error connecting to MongoDB: %s", attempt, retries, e)
            if attempt > retries:
                logger.error("Exceeded maximum MongoDB connection attempts; continuing with db_ready=False")
                return
            await asyncio.sleep(backoff_seconds * (2 ** (attempt - 1)))


async def close_mongo_connection():
    """Close the MongoDB client and mark DB as not ready."""
    global mongo_client, _db_ready
    if mongo_client:
        try:
            mongo_client.close()
        except Exception:
            logger.exception("Error closing MongoDB client")
        finally:
            mongo_client = None
            _db_ready = False
            logger.info("MongoDB connection closed")


def is_db_ready():
    """Return True if DB connection was established and is available."""
    return bool(_db_ready and database is not None)


def get_database():
    """Return the Motor database instance (or None if not connected)."""
    return database
"""
MongoDB database connection using Motor (async MongoDB driver)
"""
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import asyncio
import logging

logger = logging.getLogger(__name__)

# Global MongoDB client and database instances
mongo_client = None
database = None
# Readiness flag indicating whether DB is available
_db_ready = False


async def connect_to_mongo(retries=3, backoff_seconds=1.0):
    """Connect to MongoDB on application startup with retries.

    Attempts to connect `retries` times with exponential backoff. Does not
    raise on failure; instead sets an internal readiness flag so the app can
    respond with 503s until the DB becomes available.
    """
    global mongo_client, database, _db_ready
    attempt = 0
    while attempt <= retries:
        try:
            mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
            database = mongo_client[settings.DATABASE_NAME]

            # Test connection
            await mongo_client.admin.command("ping")
            logger.info("Connected to MongoDB: %s", settings.DATABASE_NAME)

            # Create indexes for better query performance (best-effort)
            try:
                await database.users.create_index("email", unique=True)
                await database.internships.create_index("company")
                await database.internships.create_index("domain")
            except Exception:
                logger.exception("Failed to create indexes (continuing)")

            _db_ready = True
            return

        except Exception as e:
            attempt += 1
            _db_ready = False
            logger.warning(
                "Attempt %d/%d: Error connecting to MongoDB: %s",
                attempt,
                retries,
                e,
            )
            if attempt > retries:
                logger.error("Exceeded maximum MongoDB connection attempts; continuing with db_ready=False")
                return
            # exponential backoff
            await asyncio.sleep(backoff_seconds * (2 ** (attempt - 1)))


async def close_mongo_connection():
    """Close MongoDB connection on application shutdown"""
    global mongo_client, _db_ready
    if mongo_client:
        try:
            mongo_client.close()
        except Exception:
            logger.exception("Error closing MongoDB client")
        finally:
            mongo_client = None
            _db_ready = False
            logger.info("MongoDB connection closed")


def is_db_ready():
    """Return whether the database connection is healthy/ready."""
    return bool(_db_ready and database is not None)


def get_database():
    """Get database instance (may be None if not connected)."""
    return database
"""
MongoDB database connection using Motor (async MongoDB driver)
"""

from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import asyncio
import time
import logging

logger = logging.getLogger(__name__)

# Global MongoDB client and database instances
mongo_client: AsyncIOMotorClient = None
database = None
# Readiness flag indicating whether DB is available
_db_ready: bool = False


async def connect_to_mongo(retries: int = 3, backoff_seconds: float = 1.0):
    """Connect to MongoDB on application startup with retries.

    This function will attempt to connect `retries` times with exponential backoff.
    It will set an internal readiness flag instead of raising immediately so the
    application can start and return controlled 503 responses from health checks.
    """
    global mongo_client, database, _db_ready
    attempt = 0
    while attempt <= retries:
        try:
            mongo_client = AsyncIOMotorClient(settings.MONGODB_URL)
            database = mongo_client[settings.DATABASE_NAME]

            # Test connection
            await mongo_client.admin.command("ping")
            logger.info("Connected to MongoDB: %s", settings.DATABASE_NAME)

            # Create indexes for better query performance (best-effort)
            try:
                await database.users.create_index("email", unique=True)
                await database.internships.create_index("company")
                await database.internships.create_index("domain")
            except Exception:
                logger.exception("Failed to create indexes (continuing)")

            _db_ready = True
            return

        except Exception as e:
            attempt += 1
            _db_ready = False
            logger.warning(
                "Attempt %d/%d: Error connecting to MongoDB: %s",
                attempt,
                retries,
                e,
            )
            if attempt > retries:
                logger.error("Exceeded maximum MongoDB connection attempts; continuing with db_ready=False")
                return
            # exponential backoff
            await asyncio.sleep(backoff_seconds * (2 ** (attempt - 1)))




async def close_mongo_connection():
    """Close MongoDB connection on application shutdown"""
    global mongo_client
    if mongo_client:
        mongo_client.close()

async def close_mongo_connection():
    """Close MongoDB connection on application shutdown"""
    global mongo_client, _db_ready
    if mongo_client:
        mongo_client.close()
        mongo_client = None
        _db_ready = False
        logger.info("MongoDB connection closed")


        print("✅ MongoDB connection closed")




def is_db_ready() -> bool:
    """Return whether the database connection is healthy/ready."""
    return bool(_db_ready and database is not None)
def get_database():
    """Get database instance"""
    return database