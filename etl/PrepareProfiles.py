from zenml import step

from data_access import GitHubProfile
from etl import createUser, AiAgent_RepoSelect
from concurrent.futures import ThreadPoolExecutor
from loguru import logger
def creat_User(profile):
    user = createUser(profile)
    return user
def process_url_github(user, job,tech):
    crawler_github_user = AiAgent_RepoSelect(tech,job,user)
    return crawler_github_user
@step
def process_profiles(profile: list , job_descriptoin: str,techStack)->list[GitHubProfile]:
    profiles_fin :GitHubProfile= []
    for profiles in profile:
            user = creat_User(profiles)
            resultes = AiAgent_RepoSelect(techStack,job_descriptoin,user)
            profiles_fin.append(resultes)
    logger.debug("profiles_fin:{}",profiles_fin)
    return profiles_fin
