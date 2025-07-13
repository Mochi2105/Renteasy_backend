from models.user import User, UserLogin
from database.mongo import db
from fastapi import HTTPException
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

def login_user(user: UserLogin):
    data_user = user.model_dump() #viene del postman
    result_exist = db_user.find_one({'email':data_user['email']})
    if not result_exist:
        raise HTTPException(status_code=403, detail="Invalid email or password")

 # Chequear el password con el metodo bcrypt
    user_password = data_user['password'] #password from the request (without encryption)
    db_user_password = result_exist['password'] #password from the database (with encryption)

    check_password = bcrypt.checkpw(password=user_password.encode('utf-8'),hashed_password= db_user_password.encode('utf-8'))
    if not check_password:
        raise HTTPException(status_code=403, detail="Invalid email or password")

    data_token = {
        "email": result_exist['email'],
        "first_name": result_exist['first_name'],
        "last_name": result_exist['last_name']
    }
    token = jwt.encode(data_token, secret_key, algorithm='HS256')

    return {"message": "Login successful", "token": token}




