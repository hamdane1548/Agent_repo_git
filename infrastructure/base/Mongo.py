from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from loguru import logger
from Settings import Settings, settings

settings = Settings()

class Mongo:
    _instance = None
    def __new__(cls, *args, **kwargs)->MongoClient:
      if cls._instance is None:
          try:
              cls._instance = MongoClient(settings.DATABASE_MONGO_HOST)
              logger.success(f"Connection to DataBase successful {settings.DATABASE_MONGO_HOST}")
          except ConnectionFailure as e:
              logger.error(f"Couldn't connect to the database: {e!s}")
              raise
      return cls._instance
connection  = Mongo()
