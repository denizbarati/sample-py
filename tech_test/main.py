import logging

import uvicorn
from fastapi import FastAPI
import sentry_sdk

from tech_test.core.main import create_app
from tech_test.core.config import get_redis
from tech_test.models.database import get_db

sentry_sdk.init("")
logger = logging.getLogger("uvicorn.error")

app: FastAPI = create_app()


@app.on_event("startup")
async def startup_event():
    for i in ["uvicorn.access", "uvicorn", "uvicorn.error"]:
        my_logger = logging.getLogger(i)
        if not my_logger:
            continue
        formatter = uvicorn.logging.ColourizedFormatter(
            "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] "
            "[trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"
            , use_colors=False)
        if not len(my_logger.handlers):
            continue
        my_logger.handlers[0].setFormatter(formatter)


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8002)
