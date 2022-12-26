import redis
from fastapi import APIRouter, Depends, Request
from tech_test.services import user_service, bscscan
from tech_test.models.schemas import UserBase, LoginUserBase, UpdateUserBase
from tech_test.models.database import get_db
from tech_test.tasks import tasks

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
async def login_user(user: LoginUserBase, request: Request, db=Depends(get_db)):
    return await user_service.login(db, user.username, user.password, request)


@route.put('/update/{username_id}')
async def update_user(username_id: str, user: UpdateUserBase, db=Depends(get_db)):
    return await user_service.update(db, user, username_id)


@route.get('/all')
async def get_all_user(db=Depends(get_db)):
    return await user_service.get_all_user(db)


@route.get('/block/user/{username}')
async def block_user(username: str, request: Request):
    header = request.headers.get('x-service-key')
    return await user_service.block_user(username, header)


@route.get('/get/balance')
async def get_balance_address(address: str):
    return await bscscan.get_balance(address)
