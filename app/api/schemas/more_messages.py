from pydantic import BaseModel


class MoreMessagesErrorSchema(BaseModel):
    message: str
    error: str