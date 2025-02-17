from datetime import datetime

from pydantic import BaseModel


class LogDto(BaseModel):
    created: datetime
    int_id: str
    str_value: str
    address: str

    model_config = {
        "from_attributes": True
    }
