import uuid

from zenml import pipeline , step
from typing import List

from data_access import GitHubProfile, JobDescription
from etl import AiAgent_checkTech, createJobDescription, AiAgent_RepoSelect
from etl.PrepareProfiles import process_profiles
from etl.SaveDataBase import SaveTheDataBase
from etl.create_user import createUser
from loguru import logger
from concurrent.futures import ThreadPoolExecutor
from etl.crawler_link import ProfileGithub

@pipeline
def github_profile_pipeline(
        profile : list[str],
        jobDescriptoin : str ,
        tech : list[str] ,
        request_id : str
        ):
    #logger.info(f"profile : {profile} , jobDescriptoin : {jobDescriptoin} , tech : {tech}")
    if(jobDescriptoin == "" or tech == [] or profile == []):
        logger.warning("The jobDescription or the tech or the profile is cann't be empty")
        raise
    # Step 1

    """Check the tech write is mismatch the job description with AI Agent """
    #logger.info(f"the job description is ",jobDescriptoin,"the tech stack is",tech)
    TechStack = AiAgent_checkTech(jobDescription=jobDescriptoin, tech=tech)
    """First_step create Get the Profile information from the Github"""
    # Step  1
    logger.info(f"pipeline REQUEST ID = {request_id}")

    profiles_fin = process_profiles(profile,jobDescriptoin,TechStack,request_id)
    #logger.debug("profiles_fin:{}",profiles_fin)
    #### get the repo
    #logger.info(len(profiles_fin))
    #Step 3
    """Creat the job descscption and the the profiles"""

    job = createJobDescription(tech = TechStack,job_description=jobDescriptoin,profile = profiles_fin)
    #print(job)
    #Step 4
    #logger.info(job)
    """Save the Data inot the data Base"""
    SaveTheDataBase(job)
