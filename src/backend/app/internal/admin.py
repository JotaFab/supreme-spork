from fastapi import APIRouter, status, Body, Depends, Cookie, Form, Security, HTTPException
from pydantic import BaseModel, EmailStr, Field, ValidationError
from ..db import get_redis_db, create_idx
from redis.commands.json.path import Path
from fastapi.encoders import jsonable_encoder
from redis.commands.search.field import TextField, TagField, NumericField 
import json
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter(prefix="/api/v1", tags=["Admin"], dependencies=[Depends(oauth2_scheme)])

class UserBase(BaseModel):
    username: str
    email : EmailStr
    full_name: str | None = None
    disabled: bool | None = None
    
class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str
    
def fake_decode_token(token):
    return UserBase(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user


@router.get("/users/me")
async def read_users_me(current_user: Annotated[UserBase, Depends(get_current_user)]):
    return current_user
    
    
#TODO: Add hashing
def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def password_hasher(raw_password: str):
    return "supersecret" + raw_password


def save_user(user_in: UserIn):

    hashed_password = password_hasher(user_in.password)
    user_id = f"{''.join(str(ord(c)) for c in user_in.username)}"
    user_in_db = UserInDB(**user_in.model_dump(),hashed_password=hashed_password)
    print(user_in_db)
    db = get_redis_db()
    db.json().set(f"user:{user_id}", Path.root_path(), obj=jsonable_encoder(user_in_db))
    user_in_db = db.json().get(f"user:{user_id}")
    return user_in_db

@router.post("/user/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserIn):
    user_saved = save_user(user_in)
    return user_saved

@router.get("/admin")
def admin():
    return {"message": "Hello World"}

@router.get("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username, "password": password}


    
@router.get("/users/")
async def users()-> dict:
    """
    Get a list of users from the API.

    - return: A dictionary containing user information.
    - rtype: dict
    """
    schema = (
            TextField("username"),
            TextField("email"),
            TextField("full_name"),
            TextField("password"),
        )
    create_idx("idx:users_json", "user:", schema)
    db = get_redis_db()
    response = db.ft("idx:users_json").search("*")
    try:
        if response.total == 0:
            return {"message": "No users found"}
        else:
            user_list = response.docs
            users_dict = {}
            for user in user_list:
                data = json.loads(user.json)
                user_name = data["username"]
                users_dict[f"name : {user_name}"] = f"http://localhost:8000/api/v1/user/{user.id}"
            return users_dict
    except Exception as e:
        print(e)
        
@router.get("/user/{user_id}")
async def get_user(user_id: str) -> UserOut:
    """
    Get user from Redis based on user ID.

    Args:
        user_id (str): ID of the user.

    Returns:
        dict: Dictionary containing the user details.
    """
    db = get_redis_db()
    return db.json().get(user_id)