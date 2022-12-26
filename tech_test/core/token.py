import enum
import json
from base64 import b64decode
from functools import wraps
from typing import Optional, Tuple, Union
from datetime import datetime, timedelta
import redis as redis
from fastapi import Depends, HTTPException
from jose import JWTError, constants, jwt
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request
from fastapi_login import LoginManager

from .config import Settings, get_redis, get_settings

role_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Operation not permitted",
    headers={"WWW-Authenticate": "Bearer"},
)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

forbidden_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Could not validate request token",
    headers={"WWW-Authenticate": "Bearer"},
)


class Role(enum.Enum):
    user = 'USER'
    admin = 'ADMIN'


class Auth(BaseModel):
    username: str
    familyname: str = ""
    anme: str = ""

    def __json__(self, **options):
        return self.json()


def auth_required(permissions):
    def outer_wrapper(function):
        @wraps(function)
        def inner_wrapper(*args, **kwargs):
            if 'user' in kwargs:
                if kwargs['user'].user_type in permissions:
                    return function(*args, **kwargs)
                else:
                    raise role_exception
            else:
                raise forbidden_exception

        return inner_wrapper

    return outer_wrapper


def get_current_user(request: Request, settings: Settings = Depends(get_settings)) -> Union[Auth, None]:
    if 'authorization' in request.headers:

        try:
            key = settings.jwt_pubkey
            tkn = request.headers['Authorization'].split(' ')[1]
            payload = jwt.decode(tkn, key,
                                 algorithms=[constants.ALGORITHMS.ES256, ])
            username: str = payload.get("user_id")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = payload
        if user is None:
            raise credentials_exception
        return Auth(user_id=payload['user_id'], kyc_level=payload['kyc_level'],
                    email=payload['email'], phone_number=payload['phone_number'], user_type=payload['user_type'])
    return None


"""For developer users who want to use api key"""


def get_authorization_scheme_param(authorization_header_value: str) -> Tuple[str, str]:
    if not authorization_header_value:
        return "", ""
    scheme, _, param = authorization_header_value.partition(" ")
    return scheme, param


def get_special_user(request: Request, redis_client: redis.Redis = Depends(get_redis), ) -> Union[Auth, None]:
    if ('authorization' in request.headers or 'AUTHORIZATION' in request.headers or
        'Authorization' in request.headers) and len(
            request.headers['authorization'].split(' ')) == 2:
        token_type = request.headers['authorization'].split(' ')[0].upper()
        if token_type == 'BASIC':
            authorization: str = request.headers.get("Authorization")
            scheme, param = get_authorization_scheme_param(authorization)
            data = b64decode(param).decode("ascii")
            current_api_key, separator, current_secret_key = data.partition(":")
            data = redis_client.hget("APIKEY", current_api_key)
            if not data:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect api_key or secret_key",
                    headers={"WWW-Authenticate": "Basic"},
                )
            correct_secret_key = json.loads(data)['secret_key']
            if correct_secret_key == current_secret_key:
                user_data = json.loads(data)
                return Auth(user_id=user_data['user_id'],
                            kyc_level=user_data['kyc_level'],
                            phone_number=user_data['phone_number'],
                            email=user_data['email'])
        raise credentials_exception
    raise forbidden_exception


def create_token(secret: str, url: str, username: str):
    manager = LoginManager(secret, url)
    access_token = manager.create_access_token(
        data={'sub': username}
    )
    return {'access_token': access_token}


def generate_token(_type: str, expire: int, data: Auth, settings: Settings) -> str:
    key = settings.jwt_pri_key
    payload = {
        "sub": str(data.username),
        "type": _type,
        "username": data.username,
        "name": data.name,
        "familyname": data.familyname,
    }
    token = jwt.encode(payload, key, 'HS256')
    return {"token": token}
