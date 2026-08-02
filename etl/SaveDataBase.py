from zenml import step
from infrastructure.base.Mongo import connection
from Settings import Settings
settings = Settings()


@step
def SaveTheDataBase(data)->None:
    db = connection[settings.MONGO_DATABASE]
    collection = db[settings.MONGO_COLLECTION_JOB_DESCRIPTION]
    data = data.model_dump(mode = "json")
    collection.insert_one(data)
