from zenml import get_step_context, step
from loguru import logger
from crawler.profile_crawler import crawler
from data_access import GitHubProfile
from data_access.JobDescription import JobDescription

@step
def createJobDescription(
    job_description: str,
    profile: list[GitHubProfile],
    tech: list[str],
) -> dict:
    logger.info("createJobDescription")

    if job_description is None:
        raise ValueError("job_description is None")

    try:
        logger.info(f"{job_description} , {tech} , {profile} ")
        job_description_save = JobDescription(
            jobDescription=job_description,
            tech=tech,
            profile=profile,
        )

        logger.success(f"JobDescription created successfully. {job_description_save}")
        return job_description_save.model_dump()
    except Exception:
        logger.exception("Failed to create JobDescription")
        raise