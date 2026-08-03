from github import Github, Auth
from loguru import logger

from Settings import Settings

settings = Settings()
class GithubCrawler:

    def __init__(self):
        try:
            auth = Auth.Token(settings.GITHUB_API_KEY)

            self._client = Github(auth=auth)

            logger.success("GitHub authentication successful")

        except Exception as e:
            logger.exception(f"GitHub authentication failed: {e}")
            raise

    def get_profile(self, username: str):
        return self._client.get_user(username)
    def get_repo(self,username: str):
        return self._client.get_repo(username)
githubClient = GithubCrawler()