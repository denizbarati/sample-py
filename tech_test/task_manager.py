from celery import Celery

from tech_test.core.config import get_settings

settings = get_settings()


def create_celery_app() -> Celery:
    app = Celery('tech_test',
                 broker=settings.redis_url,
                 backend=settings.redis_url,
                 include=['tech_test.tasks'])

    # Optional configuration, see the application user guide.
    app.conf.update(
        result_expires=3600,
    )
    app.conf.task_routes = {'me.*': {'queue': 'me'}, 'om.*': {'queue': 'om'}}
    return app


app = create_celery_app()
