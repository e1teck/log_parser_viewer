import asyncio
import logging
import re
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path

from app.db import get_db_session, use_db_session
from app.dto import LogDto, MessageDto
from app.repository.log import LogRepository
from app.repository.messge import MessageRepository


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("email_parser")


class MessageStatusEnum(Enum):
    RECEIVED = '<='
    NORMAL = '=>'
    ANOTHER_ADDRESS = '->'
    BAD_DELIVERY = '**'
    DELAYED = '=='
    UNKNOWN = 'UNKNOWN'

    @classmethod
    def get_key(cls, value):
        if value in cls._value2member_map_:
            return cls._value2member_map_.get(value)
        return cls.UNKNOWN



async def run(file_path: str):
    log_cnt = 0
    log_unknown = 0
    log_pattern = re.compile(
        r'(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) (?P<int_id>\S+) '
        r'(?P<flag>[<=>\*\*==]+) (?P<address><?\S+@?\S*>?)?(?P<log_text> .+)?'
    )
    email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+')
    message_id_pattern = re.compile(r'id=(\S+)')

    with use_db_session() as session:
        with open(file_path, "r") as file:
            for line in file:
                match = log_pattern.match(line)
                if not match:
                    continue

                log_data = match.groupdict()
                timestamp = f"{log_data['date']} {log_data['time']}"
                int_id = log_data["int_id"]
                address = log_data["address"] if log_data["address"] else None
                log_text = log_data["log_text"].strip() if log_data["log_text"] else ""
                flag = log_data["flag"]
                message_status = MessageStatusEnum.get_key(flag)

                clean_log = f"{int_id} {flag} {address if address else ''} {log_text}".strip()

                if message_status is MessageStatusEnum.RECEIVED:
                    msg_id_match = message_id_pattern.search(log_text)
                    msg_id = msg_id_match.group(1) if msg_id_match else None
                    if not msg_id:
                        log_unknown += 1
                        logger.warning(f"Can't parse line from log: {line}")
                        continue
                    message = MessageDto(
                        id=msg_id, created=datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
                        int_id=int_id, str_value=clean_log, status=True)
                    res = MessageRepository().create_message(session, message)
                    log_cnt += 1
                else:
                    if address and '@' not in address:
                        match_email_address = email_pattern.search(line)
                        if match_email_address:
                            address = match_email_address.group()
                    log = LogDto(created=datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
                                 int_id=int_id, str_value=clean_log, address=address)
                    res = LogRepository().create_log(session, log)
                    log_cnt += 1

    logger.info(f"Messages has been loaded in DB: {log_cnt}")
    logger.warning(f"not parsed lines: {log_unknown}")



if __name__ == '__main__':

    filename: str = "out"
    if len(sys.argv) > 2:
        filename = sys.argv[1]
    file_path = Path.cwd().joinpath(Path(filename))
    if file_path.is_file() and file_path.exists():
        asyncio.run(run(str(file_path)))
    sys.exit(0)
