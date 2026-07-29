from typing import Generic, TypeVar

from pydantic import BaseModel
from abc import ABC

from Settings import settings
from infrastructure.base import connection

_databaseconnection = connection.get_database(settings.DATABASE_MONGO_HOST)
T = TypeVar('T', bound=BaseModel)
class NoSqlDocumentBase(BaseModel,Generic[T],ABC):
