

from fastapi import HTTPException

class ManyLogRecords(HTTPException):
    def __init__(self, detail="Сообщений больше чем 100"):
        super().__init__(status_code=200, detail={"message": detail, "error": "Many messages, more then 100 records"})
