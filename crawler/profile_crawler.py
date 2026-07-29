from crawler.github_crawler import githubClient

class ProfileCrawler:
    def __init__(self):
        self.github = githubClient
    def crawl_profile(self, username: str):
        return self.github.get_profile(username)
crawler = ProfileCrawler()