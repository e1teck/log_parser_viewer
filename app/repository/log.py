from typing import Dict

from sqlalchemy import insert, text, select

from app.db.models.log import LogModel
from app.dto import LogDto


class LogRepository:

    def create_log(self, session, log: LogDto) -> None | Dict:

        if self.get_log(session, log.str_value) is not None:
            return None

        stmt = (
            insert(LogModel)
            .values(**log.dict())
            .returning(text("*"))
        )

        result = session.execute(stmt)
        result_resp = [row._asdict() for row in result] if result is not None else []
        return result_resp[0] if result_resp else None

    def get_log(self, session, str_value: str) -> None | Dict:

        stmt = (
            select(LogModel).where(LogModel.str_value==str_value)
        )

        result = session.execute(stmt)
        result_resp = [row._asdict() for row in result] if result is not None else []
        return result_resp[0] if result_resp else None

