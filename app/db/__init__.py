from contextlib import contextmanager
from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import PostgresSettings


settings = PostgresSettings()
engine = create_engine(str(settings.RW_DSN))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as sql_ex:
        db.rollback()
        raise sql_ex
    else:
        db.commit()
    finally:
        db.close()

@contextmanager
def use_db_session():
    return get_db_session()

