from pyexpat.errors import messages
from zenml import get_step_context, step
from loguru import logger
from crawler.profile_crawler import crawler
from data_access import GitHubProfile
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from Settings import Settings
import subprocess
import tempfile
from git import Repo
from data_access.Otuput import CandidateRepositoryAnalysis
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
    - Select just max 5 top repo and 5 min repo 
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
    model = ChatOllama(
        model="qwen2.5:3b",
        temperature=0.1,
        max_retries=5,
    )
    logger.info("the step icic")
    structured_model = model.with_structured_output(RepositoryList)
    structured_model2 = model.with_structured_output(ResumeList)
    print(profile.repository_url)
    messages = prompts.invoke({
        "tech": tech,
        "job_descriptions" : jobDescriptoin,
        "tech_repo": profile.repository_url
    })
    result = structured_model.invoke(messages)
    prompts2 = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert technical recruiter and software engineering evaluator.

        Your task is to analyze each candidate repository and evaluate how relevant
        it is to the provided Job Description and required technologies.

        For EACH repository:

        1. List the files and folders present in the repository directory.
        2. Try to understand the project's architecture and how the main components
           interact.
        3. Read the README file if it exists.
        4. Generate a concise summary of the project and explain its main purpose.
        5. Identify the main technologies, frameworks, libraries, databases,
           infrastructure and tools used.
        6. You can inspect specific folders when necessary to understand how the
           candidate implemented the project.
        7. DO NOT read all source-code files.
           Inspect a maximum of 2 representative source-code files per repository.
        8. Prioritize files related to:
           - APIs / REST controllers
           - Security / Authentication / Authorization
           - Application architecture
           - Main business logic
           - Database / repositories
           - Configuration
           - Docker / Infrastructure
           - CI/CD
           - Tests
           - README / documentation
           - Messaging / event-driven architecture
        9. Also inspect configuration files when they help understand the
           architecture or deployment of the project.

        ============================================================
        REPOSITORY JOB MATCHING
        ============================================================

        For EACH repository, calculate a REPOSITORY MATCH SCORE from 0 to 100.

        The score must measure how relevant THIS repository is to the
        provided Job Description.

        Use the following scoring criteria:

        - Technology Match: 25 points
          How closely the technologies used in the repository match the
          technologies required by the job.

        - Architecture & Software Engineering: 20 points
          Quality and relevance of the architecture, design and engineering
          practices demonstrated by the project.

        - Job Responsibility Match: 20 points
          How well the project demonstrates responsibilities mentioned in
          the Job Description.

        - Relevant Technical Features: 15 points
          APIs, security, databases, distributed systems, AI, messaging,
          cloud, DevOps or other features relevant to the position.

        - Code Quality & Engineering Practices: 10 points
          Code organization, maintainability, design patterns and good
          software engineering practices.

        - Testing / CI/CD / DevOps: 5 points
          Tests, CI/CD pipelines, Docker, deployment and infrastructure.

        - Documentation: 5 points
          README quality and documentation of the project.

        TOTAL = 100 POINTS

        IMPORTANT:
        The score must represent relevance to the JOB, not simply the quality
        or complexity of the project.

        A technically complex project can receive a low score if it is not
        relevant to the Job Description.

        ============================================================
        SCORE LEVEL
        ============================================================

        90-100 = Excellent Match
        75-89  = Strong Match
        60-74  = Good Match
        40-59  = Partial Match
        20-39  = Weak Match
        0-19   = Very Weak Match

        ============================================================
        OUTPUT FOR EACH REPOSITORY
        ============================================================

        For every repository, generate:

        Repository Name:
        <repository name>

        Repository Match Score:
        <score>/100

        Match Level:
        <Excellent / Strong / Good / Partial / Weak / Very Weak>

        Project Summary:
        <short summary>

        Architecture:
        <explain the architecture and main components>

        Technologies:
        <list the important technologies>

        Job Requirements Matched:
        <list the job requirements demonstrated by this repository>

        Missing / Weak Requirements:
        <list important requirements that are not demonstrated>

        Evidence:
        <explain which files/folders provide evidence for the evaluation>

        Code Analysis:
        <analyze up to 2 representative source-code files>

        Engineering Evaluation:
        <evaluate the candidate's engineering practices>

        Interview Questions:
        Generate 7-8 technical questions based specifically on:
        - this repository
        - the technologies used
        - the architecture
        - the Job Description

        Questions should verify that the candidate actually understands
        and built the project.

        Questions should include topics such as:
        - Architecture decisions
        - Technology choices
        - API design
        - Security
        - Database
        - Scalability
        - Performance
        - Trade-offs
        - Possible improvements

        ============================================================
        IMPORTANT RULES
        ============================================================

        - Do not invent technologies or features.
        - Do not assume that a technology is used unless there is evidence.
        - Clearly distinguish observed facts from reasonable inferences.
        - Do not read every source-code file.
        - Maximum 2 detailed source-code files per repository.
        - Prioritize README, API, Security, Architecture and configuration files.
        - The Job Description is the primary reference for calculating the score.
        - A repository with many technologies does NOT automatically receive a
          high score.
        - Relevance to the Job Description is more important than complexity.
        - Evaluate every repository independently.

        ============================================================
        FINAL REPOSITORY COMPARISON
        ============================================================

        After analyzing all repositories, rank them:

        Repository Ranking:
        1. <repository> — <score>/100
        2. <repository> — <score>/100
        3. <repository> — <score>/100
        ...

        Identify:

        Best Repository:
        <repository with the highest relevance>

        Why:
        <short explanation>

        Overall Repository Recommendation:
        <Strongly Relevant / Relevant / Potentially Relevant /
         Weakly Relevant / Not Relevant>
        """
    ),
    (
        "human",
        """
        Technologies required by the job:

        {tech}

        Job Description:

        {job_descriptions}

        Candidate Repositories Directory:

        {directory}
        """
    )
    ])
    destination = "./gitclone"
    profiles_fin: list[ResumeRepo] = []
    logger.info(f"the output from th model is {result.repositories}")
    profile.repository_url = result.repositories
    structured_llm = model.with_structured_output(
        CandidateRepositoryAnalysis
    )
    chaines = prompts2 | structured_llm
    for repoClone in profile.repository_url:
        with tempfile.TemporaryDirectory() as tempdir:
            subprocess.run(["git", "clone", repoClone.repo_url, tempdir],check=True)
            messagest = chaines.invoke({
                "tech": tech,
                "job_descriptions": jobDescriptoin,
                "directory": tempdir,
            })
            result = structured_model2.invoke(messagest)
            profiles_fin.extend(result.repositories)
    profile.resume_url = profiles_fin
    return profile




