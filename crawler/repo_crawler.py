from crawler.github_crawler import  githubClient
class RepositoryCrawler:
    def __init__(self):
        self.github_client = githubClient
    def repo_profile(self,username : str):
        return self.github_client.get_repo(username)
crawler = RepositoryCrawler()