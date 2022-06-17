from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str
    app_discription: str
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()
