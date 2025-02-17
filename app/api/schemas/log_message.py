from datetime import datetime

from pydantic import BaseModel, Field


class LogMessageResponse(BaseModel):
    created: datetime
    str_value: str

