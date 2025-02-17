from datetime import datetime

from sqlalchemy import Index, TIMESTAMP, text, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base



# CREATE TABLE message (
# created TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL, # already without timezone
# SELECT column_name, data_type
# FROM information_schema.columns
# WHERE table_name = 'messages';
# id VARCHAR NOT NULL,
#
# int_id CHAR(16) NOT NULL,
# in postgres will BPCHAR with spaces better use VARCHAR(16)
# char_field      | length
# ----------------+-------
# 'hello        ' |    16
#
# str VARCHAR NOT NULL,
# status BOOL,
# CONSTRAINT message_id_pk PRIMARY KEY(id)
# );
# CREATE INDEX message_created_idx ON message (created);
# CREATE INDEX message_int_id_idx ON message (int_id);

class MessageModel(Base):
    __tablename__ = "message"
    __table_args__ = (
        Index("message_created_idx", "created"),
        Index("message_int_id_idx", "int_id"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    created: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        server_default=text("CURRENT_TIMESTAMP(0)"),
        nullable=False
    )
    int_id: Mapped[str] = mapped_column(String(16), nullable=False)
    str_value: Mapped[str] = mapped_column(String, nullable=False, key="str",name="str")
    status: Mapped[bool]
