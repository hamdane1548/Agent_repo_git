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
def process_profiles(profile: list, job_descriptoin: str, techStack) -> list[GitHubProfile]:

    logger.info("========== PROCESS_PROFILES START ==========")
    logger.info(f"profiles",profile)
    request_id = send_location_updates(
        profile=profile,
        job_descriptoin=job_descriptoin,
        techStack=techStack
    )

    logger.info(f"========== REQUEST ID: {request_id} ==========")

    logger.info("========== CALLING WAIT ==========")

    profiles_fin = wait_for_Response(request_id)

    logger.info(f"========== RESPONSE: {profiles_fin} ==========")

    return profiles_fin