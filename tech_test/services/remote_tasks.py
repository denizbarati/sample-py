from typing import Union

import logging
from tech_test.task_manager import celery_app
logger = logging.getLogger('uvicorn.error')

# def new_order_set(order_id):
#     logger.info(f"EVENT rt.sampleRoute {order_id}")
#     app.send_task('omRT.sampleRoute', kwargs={"order_id": order_id})
