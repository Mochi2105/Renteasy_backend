from fastapi import APIRouter, Response
from services.user_service import create_user, login_user, logout_user
from models.user import User, UserLogin

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/signup")
def create_user_route(user: User):
    return create_user(user)

@router.post("/login")
def login_user_route(user_login: UserLogin ): #{"email": "asdasd@asdsa.com", "password:" "asdasd"}
    return login_user(user_login)

@router.post("/logout")
def logout_user_route(response: Response):
    return logout_user(response)
