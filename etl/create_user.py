from zenml import get_step_context, step
from loguru import logger
from crawler.profile_crawler import crawler
from data_access import GitHubProfile
from data_access.Repository import Repository


@step
def createUser(user_name:str)->GitHubProfile:
    logger.success(f"create user {user_name}")
    if user_name == '':
        logger.warning("the username is empty")
        raise
    try:
        profiles_fin: list[Repository] = []

        user  = crawler.crawl_profile(user_name)
        for users in user.get_repos():
            repositry = Repository(
                repo_url = users.html_url,
                name = users.name,
                description = users.description,
                langaage=list(users.get_languages().keys())
            )
            profiles_fin.append(repositry)
        githubuser = GitHubProfile(
            username=user.name,
            bio=user.bio,
            location=user.location,
            followers=user.followers,
            following=user.following,
            repository_url = profiles_fin
        )
        print(f"github user {githubuser}")
        logger.success(f"create user {user_name}")
        return githubuser
    except Exception as e:
        logger.error(e)
        raise
