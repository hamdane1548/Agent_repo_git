import uuid

from pydantic import UUID1

from Settings import Settings
from loguru import logger
from crawler.profile_crawler import crawler
from infrastructure.base.Mongo import connection
from pipline import github_profile_pipeline


def main():
    print("Hello from ai-git-agent!")
    #settings = Settings()
    #settings.export()
    """Test to load the conf from setting"""
    github_profile_pipeline(
        profile = ["hamdane1548","Ayoub-glitsh","AnouarMohamed"],
       jobDescriptoin ="""
       We are looking for a Backend Engineer to develop and maintain scalable web applications. The ideal candidate has experience building RESTful APIs with Spring Boot and Spring Security, designing relational databases with PostgreSQL or MySQL, and developing modern user interfaces using React.

You will be responsible for implementing authentication and authorization, integrating third-party services, and ensuring high application performance and security. Experience with Docker, Git, Redis, and CI/CD pipelines is highly valued.

As part of our AI initiatives, you will also collaborate on projects involving Python, LangChain, Large Language Models (LLMs), RAG (Retrieval-Augmented Generation), vector databases, and AI agents to build intelligent features into our products.

Required Skills: Spring Boot, Spring Security, Java, React, TypeScript, REST APIs, PostgreSQL, Git, Docker.
       """,
        tech = ["spring boot","spring security","java","React","TypeScript"],
    )
if __name__ == "__main__":
    main()
