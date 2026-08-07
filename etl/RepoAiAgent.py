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
import tempfile
from git import Repo
from data_access.Repository import Repository, RepositoryList
from data_access.ResumeRepo import ResumeRepo, ResumeList
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
    - Select just max 2 top repo and 2 min repo 
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
    agent2 = create_agent(
        model=model,
        response_format=ResumeList
    )
    messages = prompts.invoke({
        "tech": tech,
        "job_descriptions" : jobDescriptoin,
        "tech_repo": profile.repository_url
    })
    result = agent.invoke({
        "messages": messages.to_messages(),
    })
    prompts2  = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are a technical recruiter.
            Your task:
            - liste les fichier de directory 
            - esage de compredner l'architecutre de project 
            - read le file Readme File if exists dans le directory 
            - genre une resume de project 
            - u can access to like specifi folder pour comprndre le user comment ecrire le code pas tous les ficiher de code just ou max 2 
            - preivlige les filed api et de security et de architecutre et de reamdfile
            - aussie les ficher de conversiton
            - construie une resume de project avec like 7 a 8 queation paropre a le project pour evalue le condidat 
            """
        ),
        (
            "human",
            """
            Technologies post:
            {tech}
            Job Descriptiion : 
            {job_descriptions}
            Repositories condidata directory:
            {directory}
            """
        )
    ])
    destination = "./gitclone"
    profiles_fin: list[ResumeRepo] = []
    profile.repository_url = result["structured_response"].repositories
    for repoClone in profile.repository_url:
        with tempfile.TemporaryDirectory() as tempdir:
            subprocess.run(["git", "clone", repoClone.repo_url, tempdir],check=True)
            messagest = prompts2.invoke({
                "tech": tech,
                "job_descriptions": jobDescriptoin,
                "directory": tempdir,
            })
            result = agent2.invoke({
                "messages": messagest.to_messages(),
            })
            profiles_fin.extend(result["structured_response"].repositories)
    profile.resume_url = profiles_fin
    return profile




