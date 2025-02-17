from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, text, TIMESTAMP, Index, Integer

from app.db.base import Base


# CREATE TABLE log (
# created TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
#
# table needs id as a primary_key
# id serial4 NOT NULL,
#
# int_id CHAR(16) NOT NULL,
# in postgres will BPCHAR with spaces better use VARCHAR(16)
# char_field      | length
# ----------------+-------
# 'hello        ' |    16

# str VARCHAR,
# address VARCHAR
# );
# CREATE INDEX log_address_idx ON log USING hash (address);

class LogModel(Base):
    __tablename__ = "log"
    __table_args__ = (Index("log_address_idx", "address", postgresql_using="hash"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        server_default=text("CURRENT_TIMESTAMP(0)"),
        nullable=False
    )
    int_id: Mapped[str] = mapped_column(String(16), nullable=False)
    str_value: Mapped[str] = mapped_column(String, nullable=False, key="str",name="str")
    address: Mapped[str]
