import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from tech_test.core.config import settings
logger = logging.getLogger('uvicorn.error')
# dialect+driver://username:password@host:port/database
# postgresql://deniz:123deniz@localhost/pyapp
engine = create_engine("postgresql://deniz:123deniz@localhost/pyapp")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

try:
    logger.info(f'Init Database from address: {settings.sqlalchemy_database_url.host}')
except AttributeError:
    logger.info("Init Database")

def get_conn():
    engine.connect()
    return engine.url.database


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
