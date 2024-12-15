from pydantic_settings import BaseSettings

class Settings(BaseSettings): # Pydantic Model- will see this as insensitive perspective, so we don't necessarily captalize it. 
    # performs validation too.
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

# it will then store the model in the settings var.
settings = Settings() # instance of setting class.