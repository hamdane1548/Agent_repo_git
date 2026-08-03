from zenml import step
from infrastructure.base.Mongo import connection
from Settings import Settings
settings = Settings()
from  loguru import logger
from pydantic import TypeAdapter
@step
def SaveTheDataBase(data)->None:
    logger.info(f"Save the data to MongoDB {data}")
    db = connection[settings.MONGO_DATABASE]
    collection = db[settings.MONGO_COLLECTION_JOB_DESCRIPTION]
    data = TypeAdapter(dict).dump_python(data, mode="json")
    collection.insert_one(data)
