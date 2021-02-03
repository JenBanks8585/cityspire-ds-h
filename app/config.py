from pydantic import BaseSettings, SecretStr

class Settings(BaseSettings):

    api_key: SecretStr 
    host: str
    pollution_api_key: SecretStr 
    openweathermap_api: SecretStr 
    
    class Config:
        env_file = ".env"


settings = Settings()
print(settings)
