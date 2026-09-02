from zenml import step

from data_access import GitHubProfile
from etl import createUser, AiAgent_RepoSelect
from concurrent.futures import ThreadPoolExecutor
from loguru import logger

from PorcessingKf.ConsumerCheckResult import wait_for_Response
from PorcessingKf.Producer import send_location_updates

def process_url_github(user, job,tech):
    crawler_github_user = AiAgent_RepoSelect(tech,job,user)
    return crawler_github_user
@step
def process_profiles(profile: list , job_descriptoin: str,techStack)->list[GitHubProfile]:
    #for profiles in profile:
    #      user = creat_User(profiles)
    #      resultes = AiAgent_RepoSelect(techStack,job_descriptoin,user)
    #      profiles_fin.append(resultes)
    request_id = send_location_updates(profile=profile,job_descriptoin=job_descriptoin,techStack=techStack)
    profiles_fin = wait_for_Response(request_id)
    logger.info(f"the profiles {profiles_fin}")
    logger.debug("profiles_fin:{}",profiles_fin)
    return profiles_fin
