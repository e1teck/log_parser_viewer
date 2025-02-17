from typing import Dict, List

from sqlalchemy import select, text, union_all, column
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import coalesce

from app.db.models.log import LogModel
from app.db.models.message import MessageModel


class LogMessages:

    def get_log_messages_by_address(self, address: str, session: Session, limit: int = 100) -> None | List[Dict]:

        stmt = union_all(
            select(MessageModel.created, MessageModel.str_value,  MessageModel.int_id)
            .where(MessageModel.str_value.like(f"%{address}%")),

            select(LogModel.created, LogModel.str_value, LogModel.int_id)
            .where(LogModel.address == address)
        )
        stmt = (select(stmt.c.created, stmt.c.str_value, stmt.c.int_id)
                .order_by(stmt.c.created, stmt.c.int_id).limit(limit))

        result = session.execute(stmt).mappings().all()

        return [row for row in result] if result is not None else []
