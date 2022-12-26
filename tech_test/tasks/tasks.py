from tech_test.task_manager import celery_app
from tech_test.models.schemas import UserBase
from sqlalchemy.orm.session import Session
from tech_test.models import models

@celery_app.task(name='save_user_ip', bind=True)
def add_ip_user_in_db(db: Session, username: str, ip: str):
    user = models.UserIpModel(
        username=username,
        userip=ip,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
