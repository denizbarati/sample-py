from tech_test.models.schemas import UserBase
from sqlalchemy.orm.session import Session
from tech_test.models import models
from tech_test.core.config import get_settings
from tech_test.core import errors
from tech_test.core import token


#
# class UserService:
#     def __init__(self):
#         self.settings = get_settings()

async def register(db: Session, user_req: UserBase):
    user = models.UserModel(
        username=user_req.username,
        password=user_req.password,
        name=user_req.name,
        familyname=user_req.familyname
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user_req


async def login(db: Session, username: str, password: str):
    SECRET = 'deniz123'
    is_user_exist = db.query(models.UserModel).filter(models.UserModel.username == username).first()
    if is_user_exist:
        if password != is_user_exist.password:
            return {"password or username is wrong"}
    else:
        return {"user not found"}

    return token.create_token(SECRET, '/login', username)


async def update(db: Session, user_req: UserBase, username: str):
    user = db.query(models.UserModel).filter(models.UserModel.username == username)
    print(">>>>>", user)
    user.update({
        models.UserModel.name: user_req.name,
        models.UserModel.familyname: user_req.familyname,
        # models.UserModel.username: user_req.username,
        # models.UserModel.password: user_req.password,
    })
    db.commit()
    return 'user has been updated'


async def get_all_user(db: Session):
    return db.query(models.UserModel).all()
