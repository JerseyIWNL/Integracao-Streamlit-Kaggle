from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    kaggle_username: str
    kaggle_key: str
    
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


    


configuracoes = Settings()

print(configuracoes)