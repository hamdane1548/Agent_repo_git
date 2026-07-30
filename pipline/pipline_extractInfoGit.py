from zenml import pipeline
from etl.create_user import createUser
from loguru import logger
@pipeline
def github_profile_pipeline(user_name: str):
    logger.success(f"create user {user_name}")
    user = createUser(user_name=user_name)


