import logging
import sys

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.cors import CORSMiddleware
from tech_test import controller
from tech_test.core.config import get_settings
from tech_test.models.database import engine
env = get_settings()

logger = logging.getLogger('uvicorn')


def create_app() -> FastAPI:
    if env.debug:
        local_config = dict(
            servers=[
                {"url": f"http://127.0.0.1:{env.port}", "description": "Local environment"},
                {"url": "https://api.maxpool.ir", "description": "Development environment"},
                {"url": "https://api.mybitmax.com", "description": "Staging environment"},
            ],
            root_path=f"/{env.service_name}",
        )
        origins = env.origin.split() + ['*']
    else:
        local_config = dict(servers=[
            {"url": "https://api.maxpool.ir", "description": "Development environment"},
            {"url": "https://api.mybitmax.com", "description": "Staging environment"},
            {"url": "https://api.bitmax.ir", "description": "Production environment"},
        ], docs_url=None,
            root_path=f"/{env.service_name}",
        )
        origins = env.origin.split()
    app = FastAPI(**local_config, )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    setup_otel(app)
    if env.debug:
        logger.warning("Running app in DEBUG mode")
    else:
        logger.warning("Running app in production mode")

    # Base.metadata.create_all(bind=engine)
    app.include_router(controller.route)
    app.add_middleware(SentryAsgiMiddleware)
    return app


def setup_otel(app):
    if "pytest" in sys.modules:
        return  # Not Running  in test
    resource = Resource(attributes={"service.name": env.service_name})
    FastAPIInstrumentor().instrument(excluded_urls="status")
    trace.set_tracer_provider(TracerProvider(resource=resource))
    tracer = trace.get_tracer(__name__)
    if not env.debug:
        otlp_exporter = OTLPSpanExporter(endpoint=env.otel_server, insecure=True)
        span_processor = BatchSpanProcessor(otlp_exporter)
        trace.get_tracer_provider().add_span_processor(span_processor)
    LoggingInstrumentor().instrument(set_logging_format=True)
    SQLAlchemyInstrumentor().instrument(engine=engine)
