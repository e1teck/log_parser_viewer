from sqlalchemy.orm import DeclarativeBase

from .meta import meta


class Base(DeclarativeBase):

    metadata = meta