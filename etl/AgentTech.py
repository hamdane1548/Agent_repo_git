from zenml import get_step_context, step
from loguru import logger
from Services import invoke_with_retry
from crawler.profile_crawler import crawler
from data_access import GitHubProfile
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent
from Settings import Settings
from langchain_ollama import ChatOllama
from data_access.TechStack import TechStack
settings = Settings()
@step
def AiAgent_checkTech(tech:list[str],jobDescription: str)->list[str]:
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
    #logger.success(f"mistral api key is {settings.MISTRAL_API_KEY}")
    model = ChatOllama(
    model="qwen2.5:3b",
    temperature=0.1,
    max_retries=5,
    )
    structured_model = model.with_structured_output(TechStack)
    message = prompt.invoke({
    "tech": tech,
    "job_description": jobDescription,
    })
    
    result = invoke_with_retry(
        structured_model,
        message
    )
    logger.info(f"the response from the llm is the ",result)
    #logger.info(f"the Result of the {result["structured_response"].tech_stac}")
    return result.tech_stac



