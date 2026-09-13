from zenml import step
from infrastructure.base.Mongo import connectiondbmongo
from Settings import Settings
settings = Settings()
from  loguru import logger
from pydantic import TypeAdapter
@step
def SaveTheDataBase(data)->bool:
    logger.info(f"Save the data to MongoDB {data}")
    db = connectiondbmongo[settings.MONGO_DATABASE]
    logger.info(f"Save the data to MongoDB {data}")
    collection = db[settings.MONGO_COLLECTION_JOB_DESCRIPTION]
    data = TypeAdapter(dict).dump_python(data, mode="json")
    result = collection.insert_one(data)
    if result.acknowledged:
        logger.info(
            f"Data successfully saved to MongoDB. "
            f"Inserted ID: {result.inserted_id}"
        )
        return True

    logger.error("MongoDB insertion was not acknowledged")
    return False
