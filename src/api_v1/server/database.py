"""
this module is responsible for initializing the database connection and
setting up the Beanie ODM with the defined document models.
"""

import os

from beanie import init_beanie
from pymongo import AsyncMongoClient

from models.house import House

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "bnb")


async def init_db():
    """Initializes the MongoDB connection and sets up Beanie with the document models."""

    client = AsyncMongoClient(MONGO_URI)
    await init_beanie(database=client[MONGO_DB_NAME], document_models=[House])
