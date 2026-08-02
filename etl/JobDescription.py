from zenml import get_step_context, step
from loguru import logger
from crawler.profile_crawler import crawler
from data_access import GitHubProfile
from data_access.JobDescription import JobDescription

@step
def createJobDescription(job_description:str, profile:list[GitHubProfile],tech : list[str])->JobDescription:
    logger.info("createJobDescription")
    if (job_description == None):
        logger.error("createJobDescription: job_description is None")
        raise
    try:
      job_description_save = JobDescription(
          job_description=job_description,
          profile=profile,
          tech =tech
      )
      logger.success(f"CreateJobDescription success {job_description_save}")
      return job_description_save
    except Exception as ex:
        logger.error("error when we wont to create the job description",ex)
