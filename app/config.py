
from pydantic.v1 import BaseSettings


class PostgresSettings(BaseSettings):
    RW_DSN: str = "postgresql://postgres:postgres@127.0.0.1:55432/log_messages"

