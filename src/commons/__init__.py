"""Commons package for awesome-babushka projects."""

from .database.mongo import MongoConnect
from .models import SingletonMeta

__version__ = "0.1.0"
__all__ = ["SingletonMeta", "MongoConnect"]
