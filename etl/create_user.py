from zenml import get_step_context, step
from loguru import logger
from crawler.profile_crawler import crawler
from data_access import GitHubProfile


@step
def createUser(user_name:str)->dict:
    logger.success(f"create user {user_name}")
    if user_name == '':
        logger.warning("the username is empty")
        raise
    try:
        profile_github  = crawler.crawl_profile(user_name)
        logger.success(f"create user {user_name}")
        return profile_github
    except Exception as e:
        logger.error(e)
        raise
