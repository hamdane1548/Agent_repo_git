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
        user_name="hamdane1548"
    )
if __name__ == "__main__":
    main()
