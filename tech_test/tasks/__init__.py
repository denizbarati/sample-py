import json
from typing import Union

from tech_test.core.config import get_redis
from tech_test.core.token import Auth
from tech_test.models import schemas
from tech_test.services import sample as service_sample
from tech_test.task_manager import app

r = get_redis().__next__()


@app.task(name="me.getSampleList")
def get_order_list():
    return service_order.get_sample_list(r)


