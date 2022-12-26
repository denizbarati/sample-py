run worker in linux:

    celery -A matchengine worker -l INFO

run app on linux:

    uvicorn matchengine:webapp

sample env file:

    redis_url="redis://172.22.164.55:6379/0"

run celery:

    celery -A tasks.celery_app worker --loglevel=INFO

run flower:

    celery -A tasks.celery_app flower --port=5555

run project:

    1 - python3.9 -m venv venv
    2 - . venv/bin/activate
    3 - pip freeze
    4 - pip install -r requirment.txt
    5 - pip install -e .
