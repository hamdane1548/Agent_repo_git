from Settings import Settings
from loguru import logger
from crawler.profile_crawler import crawler
def main():
    print("Hello from ai-git-agent!")
    #settings = Settings()
    #settings.export()
    """Test to load the conf from setting"""
    settings = Settings.load_settings()
    if(settings == None):
        logger.warning("Settings not loaded")
    else:
        logger.success(f"Settings loaded {settings.MISTRAL_API_KEY}")

    user  = crawler.crawl_profile("torvalds")
    print(user)
    logger.success(f"Crawling user {user.name}")
if __name__ == "__main__":
    main()
