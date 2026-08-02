import loguru

from data_access import GitHubProfile
from infrastructure.base.Mongo import connection
from Settings import Settings
settings = Settings()
from zenml import get_step_context, step

@step
def ProfileGithub(user):
    db = connection[settings.MONGO_DATABASE]
    collection = db[settings.MONGO_COLLECTION]
    data = user.model_dump(mode="json")
    collection.insert_one(data)

