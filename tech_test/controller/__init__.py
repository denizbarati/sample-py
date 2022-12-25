import logging

from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError

from .sample import route as sample_route
from tech_test import __version__
from tech_test.models.database import get_conn
from tech_test.core.errors import ok
from tech_test.core.redis import redis

logger = logging.getLogger('uvicorn.error')
route = APIRouter()
route.include_router(sample_route, prefix="/sample", tags=['sample'])


@route.get("/status")
async def home():
    db_connection = is_db_available()
    # redis_connection = is_redis_available(r)
    redis_connection = await redis.ping()
    return ok({"version": __version__, "database": db_connection, "redis": redis_connection})


def is_db_available():
    try:
        db_conn = get_conn()
    except SQLAlchemyError as err:
        logger.exception(err.__cause__)
        logger.exception("DB connection error!")
        return "DB connection error!"
    except:
        logger.exception("DB connection error!")
        return "DB connection error!"
    else:
        return db_conn


def is_redis_available(r):
    try:
        r.ping()
    except:
        logger.exception("Redis connection error!")
        return "Redis connection error!"
    else:
        return r.info()
