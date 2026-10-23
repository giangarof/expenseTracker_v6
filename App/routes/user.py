from datetime import timedelta
from typing import Annotated
from bson import ObjectId
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Path
from fastapi.security import OAuth2PasswordRequestForm

from App.schemas.users import UserRequest
from App.utils.utils import hash_password
from App.utils.auth import (
    get_current_user,
    create_access_token,
    authenticate_user,
    user_dependency,
)
from App.database.database import users_collection
from App.schemas.token import Token

router = APIRouter(prefix="/api/auth", tags=["Auth"])

current = get_current_user


@router.post("/login")
def login():
    pass


@router.post("/signup")
async def signup(userRequest: UserRequest):

    existing_user = await users_collection.find_one(
        {
            "$or": [
                {"username": userRequest.username},
                {"email": str(userRequest.email).lower()},
            ]
        }
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email/username already associated",
        )

    # Hashing the password
    userRequest.password = hash_password(userRequest.password)

    new_user = userRequest.model_dump()

    await users_collection.insert_one(new_user)

    return {"message": "User created successfully"}


@router.post("/logout")
def logout():
    pass


@router.get("/profile")
async def profile(user: user_dependency):
    return user


@router.put("/update")
async def update(user: user_dependency, userRequest: UserRequest):

    userRequest.password = hash_password(userRequest.password)
    update_data = userRequest.model_dump()

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])}, {"$set": update_data}
    )
    return update_data


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await authenticate_user(
        form_data.username,
        form_data.password,
    )

    token = create_access_token(
        username=user["username"],
        user_id=str(user["_id"]),
        role=user.get("role", "basic"),
        expires_delta=timedelta(minutes=20),
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }
