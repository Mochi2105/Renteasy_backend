from models.user import User, UserLogin
from database.mongo import db
from fastapi import HTTPException, Response, status
from settings.keys import secret_key
import bcrypt
import jwt

db_user = db['users']
salt = bcrypt.gensalt()

def create_user(user: User):
    data_user = user.model_dump()
    result_exist = db_user.find_one({'email': data_user['email']})
    if result_exist:
        raise HTTPException(status_code=409, detail="User already exists")

    data_user['password'] = bcrypt.hashpw(data_user['password'].encode('utf-8'), salt).decode('utf-8')
    print("data_user:",data_user)

    try:
        db_user.insert_one(data_user)
    except AttributeError:
        raise HTTPException(status_code=500, detail="Error inserting user into the database")
    return {"message": "User created correctly"}

def login_user(user_login: UserLogin, response: Response):
    try:
        user_data = db_user.find_one({"email": user_login.email})

        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User or password incorrect",
            )

        user_data["_id"] = str(user_data["_id"])

        check = bcrypt.checkpw(
            password= user_login.password.encode("utf8"),
            hashed_password=user_data["password"].encode("utf8")
        )

        if not check:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User or password incorrect",
            )

        payload = {
            "_id": user_data["_id"],
            "email": user_data["email"],
            "firstname": user_data["firstname"],
            "lastname": user_data["lastname"],
            "profile_picture": user_data.get("profile_picture", ""),
            "role": user_data["role"],
            "favorite_flats": user_data.get("favorite_flats", [])
        }

        encoded_jwt = jwt.encode(payload, "secret", algorithm="HS256")

        response.set_cookie(
            key="access_token",
            value=f"Bearer {encoded_jwt}",
            httponly=True,
            samesite="lax",
            secure=False,
            expires=604800,
            path="/"
        )

        return {
            "message": f"Welcome {user_data['firstname']} {user_data['lastname']}",
            "user": payload
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {e}"
        )

def logout_user(response: Response):
    try:
       response.delete_cookie(
           key="access_token",
           httponly=True,
           samesite="lax",
           secure=False,
           path="/"
       )
       return {"message": "User logged out"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {e}"
        )
