from typing import Optional, Union, List, Dict
from pydantic import BaseModel


class ResponseModel(BaseModel):
    class Config:
        orm_mode = True

    error: bool
    number: Optional[int]
    message: Union[List, Dict, str]


class UserBase(BaseModel):
    username: str
    password: str
    name: str
    familyname: str


class LoginUserBase(BaseModel):
    username: str
    password: str


class UpdateUserBase(BaseModel):
    name: str
    familyname: str
