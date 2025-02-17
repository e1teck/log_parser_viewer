from datetime import datetime

from pydantic import BaseModel


class MessageDto(BaseModel):
    id: str
    created: datetime
    int_id: str
    str_value: str
    status: bool

    model_config = {
        "from_attributes": True
    }
