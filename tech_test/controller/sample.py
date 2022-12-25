import redis
from fastapi import APIRouter, Depends
from tech_test.services import user_service
from tech_test.models.schemas import UserBase, LoginUserBase, UpdateUserBase
from tech_test.models.database import get_db

route = APIRouter()


# @route.get('', response_model=schemas.ResponseModel)
# def get_order_list(r: redis.Redis = Depends(get_redis)):
#     return service_sample.get_all_samples(r)

@route.get('/')
def get():
    return {"lets start"}


@route.post('/register_user')
async def register_user(user: UserBase, db=Depends(get_db)):
    return await user_service.register(db, user)


@route.post('/login')
async def login_user(user: LoginUserBase, db=Depends(get_db)):
    return await user_service.login(db, user.username, user.password)


@route.put('/update/{username_id}')
async def update_user(username_id: str, user: UpdateUserBase, db=Depends(get_db)):
    return await user_service.update(db, user, username_id)


@route.get('/all')
async def get_all_user(db=Depends(get_db)):
    return await user_service.get_all_user(db)