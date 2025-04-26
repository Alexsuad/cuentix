# config/settings.py

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DEEPSEEK_API_KEY: str = Field(..., env="DEEPSEEK_API_KEY")
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    ELEVENLABS_API_KEY: str = Field(..., env="ELEVENLABS_API_KEY")
    WHISPER_MODEL_SIZE: str = Field("base", env="WHISPER_MODEL_SIZE")
    TTS_ENGINE: str = Field("gtts", env="TTS_ENGINE")
    OPENAI_PROJECT_ID: str = Field(..., env="OPENAI_PROJECT_ID")
    ELEVENLABS_VOICE_ID: str = Field("EXAVITQu4vr4xnSDxMaL", env="ELEVENLABS_VOICE_ID") 

    class Config:
        env_file = ".env"
        extra = "forbid"
        populate_by_name = True

settings = Settings()

