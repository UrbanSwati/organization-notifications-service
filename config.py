from pydantic import BaseSettings, HttpUrl


class Config(BaseSettings):
    base_api_url: HttpUrl
    recipient: str = "email@domain.com"
    smtp_password: str
    smtp_port: int = 587
    smtp_sender_email: str
    smtp_server: str
    org_name: str


config = Config(_env_file=".env")
