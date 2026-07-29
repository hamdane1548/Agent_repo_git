from loguru import logger
from pydantic_settings import BaseSettings , SettingsConfigDict
from zenml.client import Client

class Settings(BaseSettings):
    # Load the Variabale environment
    """Mistral Api Or another Model Ai"""
    MISTRAL_API_KEY  : str

    """Data Werhouse Mongo Db"""
    DATABASE_MONGO_HOST : str
    DATABASE_MONOG_NAME : str
    GITHUB_API_KEY : str
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    @classmethod
    def load_settings(cls)->"Settings":
        try:
            logger.info("Loading Settings from the zenml store")
            settings_secret = Client().get_secret("settings")
            settings = Settings(**settings_secret.secret_values)
        except Exception:
            logger.warning(
                "Failed to load settings from the ZenML secret store. Defaulting to loading the settings from the '.env' file."
            )
            settings = Settings()
            logger.success(f"Load the settings from the .env file. {settings.MISTRAL_API_KEY}")
        return settings
    def export(self)->None:
        env_vars = self.model_dump()
        for key,value in env_vars.items():
            env_vars[key] = str(value)
        client = Client()
        try:
            client.create_secret(name="settings",values=env_vars)
            logger.success(f"Export the settings to the .env file.")
        except Exception:
            logger.warning(f"Failed to export the settings to the .env file.")
settings = Settings

