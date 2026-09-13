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
from pipline.Rag_EmbeddingPipeling import EmbeddingsRag

@pipeline
def github_profile_pipeline(
          profile: list[str] | None = None,
    jobDescriptoin: str = "",
    tech: list[str] | None = None,
    request_id: str = "",
        ):
    #logger.info(f"profile : {profile} , jobDescriptoin : {jobDescriptoin} , tech : {tech}")
    if(jobDescriptoin == "" or tech == [] or profile == []):
        logger.warning("The jobDescription or the tech or the profile is cann't be empty")
        profile=["hamdane1548"]
        request_id = request_id
        jobDescriptoin="""
        We are looking for a Backend Engineer to develop and maintain scalable web applications. The ideal candidate has experience building RESTful APIs with Spring Boot and Spring Security, designing relational databases with PostgreSQL or MySQL, and developing modern user interfaces using React.
        
        You will be responsible for implementing authentication and authorization, integrating third-party services, and ensuring high application performance and security. Experience with Docker, Git, Redis, and CI/CD pipelines is highly valued.
        
        As part of our AI initiatives, you will also collaborate on projects involving Python, LangChain, Large Language Models (LLMs), RAG (Retrieval-Augmented Generation), vector databases, and AI agents to build intelligent features into our products.
        
        Required Skills: Spring Boot, Spring Security, Java, React, TypeScript, REST APIs, PostgreSQL, Git, Docker.
        """
        tech=["spring boot", "spring security", "java", "React", "TypeScript","llm"]
    # Step 1

    """Check the tech write is mismatch the job description with AI Agent """
    logger.info(f"the job description is ",jobDescriptoin,"the tech stack is",tech)
    TechStack = AiAgent_checkTech(jobDescription=jobDescriptoin, tech=tech)
    """First_step create Get the Profile information from the Github"""
    # Step  1
    logger.info(f"pipeline REQUEST ID = {request_id}")

    profiles_fin = process_profiles(profile,jobDescriptoin,TechStack,request_id)
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
    value = SaveTheDataBase(job)
    EmbeddingsRag(value)
    """Step Embedding the data lake"""
