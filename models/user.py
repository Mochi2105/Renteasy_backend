from pydantic import BaseModel
from typing import Optional, List

class User(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    birth_date: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    _id: str
    first_name: str
    last_name: str
    username: str
    email: str
    birth_date: str
    profile_picture: str
    favorite_flats: List[str]
    role: str

class UpdateUser(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    birth_date: Optional[str] = None
    profile_picture: Optional[str] = None
    favorite_flats: Optional[List[str]] = None
