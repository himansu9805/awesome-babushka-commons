"""Common module for MongoDB database."""

from pymongo import MongoClient

from commons.models import SingletonMeta


class MongoConnect(metaclass=SingletonMeta):
    """MongoDB connection class using Singleton pattern."""

    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name: str):
        """Get a collection from the database."""
        return self.db[collection_name]

    def close(self):
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()
