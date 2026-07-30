from zenml import get_step_context, step
from loguru import logger
from crawler.profile_crawler import crawler
from data_access import GitHubProfile


@step
def createUser(user_name:str)->GitHubProfile:
    logger.success(f"create user {user_name}")
    if user_name == '':
        logger.warning("the username is empty")
        raise
    try:
        user  = crawler.crawl_profile(user_name)
        githubuser = GitHubProfile(
            username=user.name,
            bio=user.bio,
            location=user.location,
            followers=user.followers,
            following=user.following,
        )
        print(f"github user {githubuser}")
        logger.success(f"create user {user_name}")
        return githubuser
    except Exception as e:
        logger.error(e)
        raise
