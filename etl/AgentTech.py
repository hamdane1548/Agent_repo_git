from zenml import get_step_context, step
from loguru import logger
from crawler.profile_crawler import crawler
from data_access import GitHubProfile
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent
from Settings import Settings
from data_access.TechStack import TechStack
settings = Settings()
@step
def AiAgent_checkTech (tech:list[str],jobDescription: str)->list[str]:
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a technical recruiter. "
            "Compare the candidate's tech stack with the job description. "
            "Return only the matching technologies."
        ),
        (
            "human",
            """
    Candidate technologies:
    {tech}

    Job description:
    {job_description}
    """
        )
    ])
    model = ChatMistralAI(
        model = "mistral-medium-latest",
        api_key= settings.MISTRAL_API_KEY,
        temperature=1,
    )
    agent =  create_agent(
        model=model,
        response_format=TechStack,
    )
    message = prompt.invoke({
        "tech": tech,
        "job_description": jobDescription,
    })
    result = agent.invoke({
        "message": message,
    })
    return result



