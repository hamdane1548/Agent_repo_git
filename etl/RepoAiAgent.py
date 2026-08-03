from pyexpat.errors import messages
from zenml import get_step_context, step
from loguru import logger
from crawler.profile_crawler import crawler
from data_access import GitHubProfile
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent
from Settings import Settings
import subprocess

from data_access.Repository import Repository
from data_access.TechStack import TechStack
settings = Settings()
@step
def AiAgent_RepoSelect(tech : list[str],jobDescriptoin:str,profile : GitHubProfile)->GitHubProfile:
    prompts = ChatPromptTemplate.from_messages([
        (
            "System",
            "You are a technial recuriter",
            "Your Role is slect the repos is match the job description and the tech "
            "Return only matching Repository",
            "your final role is like return the url of the github account that mismtach the job descrition and the tech stack"
            "i give list of the repositories with les langage utilise with job descsription and list of tech",
        ),
        (
            "human",
            """
            Technologie for the job description:
            {tech}
            Job description:
            {job_descriptions}
            tech use in the repo  :
            {tech_repo}
            """
        )
    ])
    model = ChatMistralAI(
        model="mistral-medium-latest",
        api_key=settings.MISTRAL_API_KEY,
        temperature=1,
    )
    agent = create_agent(
        model=model,
        response_format=Repository
    )
    messages = prompts.invoke({
        "tech": tech,
        "job_descriptions" : jobDescriptoin,
        "tech_repo": profile.repository_url
    })
    result = agent.invoke({
        "messages": messages,
    })
    profile.repository_url = result["structured_response"].tech_stac
    return profile




