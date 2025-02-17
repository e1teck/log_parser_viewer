from typing import List

from fastapi import APIRouter
from fastapi.params import Depends, Query
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.api.schemas.log_message import LogMessageResponse
from app.api.schemas.more_messages import MoreMessagesErrorSchema
from app.db import get_db_session
from app.errors.many_log_records import ManyLogRecords

from app.repository.log_messages import LogMessages

router = APIRouter(prefix="/log_messages", tags=["log_messages"])


@router.get(
    "",
    response_model=List[LogMessageResponse] | MoreMessagesErrorSchema | None,
    name="Получение сообщений по адресу",

)
async def get_log_messages_by_address(
        address: EmailStr = Query(..., description="Адрес для пооиска"),
        session: Session = Depends(get_db_session)):

    log_messages = LogMessages().get_log_messages_by_address(str(address), session, limit=101)
    if log_messages is None:
        return None

    if len(log_messages) > 100:
        raise ManyLogRecords()

    return log_messages

