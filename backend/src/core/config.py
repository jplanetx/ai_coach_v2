from pydantic_settings import BaseSettings
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Notion settings
    NOTION_API_KEY: str
    NOTION_TASKS_DATABASE_ID: str
    NOTION_AREAS_DATABASE_ID: str
    NOTION_PROJECTS_DATABASE_ID: str
    
    # OpenAI settings
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4-1106-preview"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def notion(self) -> dict:
        return {
            "api_key": self.NOTION_API_KEY,
            "tasks_database_id": self.NOTION_TASKS_DATABASE_ID,
            "areas_database_id": self.NOTION_AREAS_DATABASE_ID,
            "projects_database_id": self.NOTION_PROJECTS_DATABASE_ID,
        }

    @property
    def openai(self) -> dict:
        return {
            "api_key": self.OPENAI_API_KEY,
            "model": self.OPENAI_MODEL
        }