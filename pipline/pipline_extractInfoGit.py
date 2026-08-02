from zenml import pipeline
from typing import List
from etl import AiAgent_checkTech, createJobDescription
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
    logger.info(f"profile : {profile} , jobDescriptoin : {jobDescriptoin} , tech : {tech}")
    if(jobDescriptoin == "" or tech == [] or profile == []):
        logger.warning("The jobDescription or the tech or the profile is cann't be empty")
        raise
    """First_step create Get the Profile information from the Github"""
    #Step  1
    profiles_fin: list[ProfileGithub] = []
    for profiles in profile:
        user = createUser(profiles)
        profiles_fin.append(user)
    if (len(profiles) <= 0):
        logger.warning("we can't fint any profiles form github")
        raise
    #Step 2
    """Check the tech write is mismatch the job description with AI Agent """
    TechStack = AiAgent_checkTech(jobDescriptoin,tech=tech)

    #Step 3
    """Creat the job descscption and the the profiles"""
    job = createJobDescription(tech = TechStack,job_description=jobDescriptoin,profile = profiles_fin)

    #Step 4
    """Save the Data inot the data Base"""
    SaveTheDataBase(job)





