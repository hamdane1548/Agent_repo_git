from data_access import GitHubProfile
from infrastructure.base.Mongo import connection
from Settings import Settings
settings = Settings()
class GitHubPrfile():
    db = connection[settings.MONGO_DATABASE]
    collection = db[settings.MONGO_COLLECTION]
    @classmethod
    def create_user(cls, user):
        githubuser = GitHubProfile(
            username=user.name,
            bio=user.bio,
            location=user.location,
            followers=user.followers,
            following=user.following,
        )
        cls.collection.insert_one(githubuser)
crud_db = GitHubProfile()


