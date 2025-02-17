from typing import Dict

from sqlalchemy import insert, text, select

from app.db.models.message import MessageModel
from app.dto import MessageDto


class MessageRepository:

    def create_message(self, session, message: MessageDto) -> None | Dict:
        if self.get_message(session, message.id) is not None:
            return None

        stmt = (
            insert(MessageModel)
            .values(**message.dict())
            .returning(text("*"))
        )

        result = session.execute(stmt)
        result_resp = [row._asdict() for row in result] if result is not None else []
        return result_resp[0] if result_resp else None

    def get_message(self, session, message_id: str) -> None | Dict:

        stmt = (
            select(MessageModel).where(MessageModel.id==message_id)
        )

        result = session.execute(stmt)
        result_resp = [row._asdict() for row in result] if result is not None else []
        return result_resp[0] if result_resp else None
