from zenml import pipeline
from typing import List

from data_access import GitHubProfile
from etl import AiAgent_checkTech, createJobDescription, AiAgent_RepoSelect
from etl.SaveDataBase import SaveTheDataBase
from etl.create_user import createUser
from loguru import logger
from etl.crawler_link import ProfileGithub
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
    for profiles in profile:
        user = createUser(profiles)
        github_with_repo=AiAgent_RepoSelect(jobDescriptoin=jobDescriptoin,tech=TechStack,profile=user)
        profiles_fin.append(github_with_repo)
    if (len(profiles) <= 0):
        logger.warning("we can't fint any profiles form github")
        raise
    #### get the repo
    logger.info(len(profiles_fin))

    #Step 3
    """Creat the job descscption and the the profiles"""

    job = createJobDescription(tech = TechStack,job_description=jobDescriptoin,profile = profiles_fin)
    #print(job)
    #Step 4
    logger.info(job)
    """Save the Data inot the data Base"""
    SaveTheDataBase(job)
