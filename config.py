from pydantic import BaseSettings, HttpUrl


class Config(BaseSettings):
    base_url: HttpUrl
    recipient: str = 'hello@gmail.com'


config = Config(_env_file='.env')
