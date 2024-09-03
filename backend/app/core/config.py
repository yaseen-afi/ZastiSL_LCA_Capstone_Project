from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URI: str
    MONGODB_NAME: str
    OPENAI_API_KEY:str

    class Config:
        env_file = ".env"  # This automatically loads the .env file

settings = Settings()
