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

from data_access.Repository import Repository, RepositoryList
from data_access.TechStack import TechStack
settings = Settings()
@step
def AiAgent_RepoSelect(tech : list[str],jobDescriptoin:str,profile : GitHubProfile)->GitHubProfile:
    prompts = ChatPromptTemplate.from_messages([
        (
            "system",
            """
    You are a technical recruiter.

    Your task:
    - Compare the job description with the candidate's repositories.
    - Select only repositories matching the required technologies.
    - Ignore unrelated repositories.

    Return only the matching repositories.
    """
        ),
        (
            "human",
            """
    Technologies:
    {tech}

    Job Description:
    {job_descriptions}

    Repositories:
    {tech_repo}
    """
        )
    ])
    model = ChatMistralAI(
        model="mistral-medium-latest",
        api_key=settings.MISTRAL_API_KEY,
        temperature=0.1,
    )
    agent = create_agent(
        model=model,
        response_format=RepositoryList
    )
    messages = prompts.invoke({
        "tech": tech,
        "job_descriptions" : jobDescriptoin,
        "tech_repo": profile.repository_url
    })
    result = agent.invoke({
        "messages": messages.to_messages(),
    })
    print(result["structured_response"])
    profile.repository_url = result["structured_response"].repositories
    return profile




