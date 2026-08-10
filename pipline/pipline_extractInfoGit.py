from huggingface_hub.cli import jobs
from zenml import pipeline , step
from typing import List

from data_access import GitHubProfile, JobDescription
from etl import AiAgent_checkTech, createJobDescription, AiAgent_RepoSelect
from etl.SaveDataBase import SaveTheDataBase
from etl.create_user import createUser
from loguru import logger
from concurrent.futures import ThreadPoolExecutor
from etl.crawler_link import ProfileGithub
def invokeagent(profile):
    user = createUser(profile)
    return  user
def procees_url_github(user,job , tech):
    repouser = AiAgent_RepoSelect(tech=tech,job_description=job,profile=user)
    return repouser
@step
def process_profiles(profiles: list) -> list:
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(
            executor.map(invokeagent, profiles)
        )
    return results
@step
def process_reposiotory(profile:list,jobs,TechStack)->list:
      with ThreadPoolExecutor(max_workers=3) as executor:
          results = list(executor.map(procees_url_github,profile,jobs,TechStack))
      return results
@pipeline
def github_profile_pipeline(
        profile : list[str],
        jobDescriptoin : str ,
        tech : list[str] ,
        ):
    #logger.info(f"profile : {profile} , jobDescriptoin : {jobDescriptoin} , tech : {tech}")
    if(jobDescriptoin == "" or tech == [] or profile == []):
        logger.warning("The jobDescription or the tech or the profile is cann't be empty")
        raise
    # Step 1
    """Check the tech write is mismatch the job description with AI Agent """
    TechStack = AiAgent_checkTech(jobDescription=jobDescriptoin, tech=tech)
    """First_step create Get the Profile information from the Github"""
    # Step  1
    profiles_fin: list[GitHubProfile] = []
    profiles_fin = process_profiles(profile)
    profiles_fin = process_reposiotory(profiles_fin,jobDescriptoin,TechStack)
    logger.debug("profiles_fin:{}",profiles_fin)
    #### get the repo
    #logger.info(len(profiles_fin))
    #Step 3
    """Creat the job descscption and the the profiles"""

    job = createJobDescription(tech = TechStack,job_description=jobDescriptoin,profile = profiles_fin)
    #print(job)
    #Step 4
    logger.info(job)
    """Save the Data inot the data Base"""
    SaveTheDataBase(job)
