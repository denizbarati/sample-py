from tech_test.task_manager import celery_app
from tech_test.models.schemas import UserBase
from sqlalchemy.orm.session import Session
from tech_test.models import models
import time
from tech_test.models.database import get_db


@celery_app.task()
def add_ip_user_in_db( username, ip):
    db = get_db().__next__()
    time.sleep(5)
    user = models.UserIpModel(
        username=username,
        userip=ip,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
