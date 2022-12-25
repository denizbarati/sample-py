run worker in linux:

    celery -A matchengine worker -l INFO

run app on linux:

    uvicorn matchengine:webapp

sample env file:

    redis_url="redis://172.22.164.55:6379/0"
