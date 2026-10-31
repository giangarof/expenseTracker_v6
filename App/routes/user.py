from datetime import timedelta
from typing import Annotated
from bson import ObjectId
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Path
from fastapi.security import OAuth2PasswordRequestForm

from App.schemas.users import UserRequest, User
from App.utils.utils import hash_password
from App.utils.auth import (
    get_current_user,
    create_access_token,
    authenticate_user,
    user_dependency,
)
from App.database.database import (
    users_collection,
    income_collection,
    expense_collection,
    category_collection,
)
from App.schemas.token import Token

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await authenticate_user(form_data.username, form_data.password)

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


@router.post("/signup", status_code=status.HTTP_201_CREATED)
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

    new_user = User(
        name=userRequest.name,
        username=userRequest.username,
        email=userRequest.email,
        password=userRequest.password,
    )
    await users_collection.insert_one(new_user.model_dump())

    return {"message": "User created successfully"}


@router.post("/logout")
def logout():
    pass


@router.get("/profile", status_code=status.HTTP_200_OK)
async def profile(user: user_dependency):
    # incomes = await income_collection.find({"owner_id": user["id"]}).to_list(length=100)
    # expenses = await expense_collection.find({"owner_id": user["id"]}).to_list(
    #     length=100
    # )
    # totalIncome = 0
    # totalExpense = 0

    # for income in incomes:
    #     # income["id"] = str(income.pop("_id"))
    #     totalIncome += income["amount"]

    # for expense in expenses:
    #     # income["id"] = str(income.pop("_id"))
    #     totalExpense += expense["amount"]

    return {
        "message": "profile",
        "user": user,
        # "Total income": totalIncome,
        # "Total expense": totalExpense,
    }


@router.put("/update", status_code=status.HTTP_200_OK)
async def update(user: user_dependency, userRequest: UserRequest):

    userRequest.password = hash_password(userRequest.password)
    update_data = userRequest.model_dump()

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])}, {"$set": update_data}
    )
    return update_data


@router.delete("/delete_account", status_code=status.HTTP_200_OK)
async def delete_user(user: user_dependency):
    user_id = user["id"]

    # Delete user's incomes
    await income_collection.delete_many({"owner_id": user_id})

    # Delete user's expenses
    await expense_collection.delete_many({"owner_id": user_id})

    # Delete user's categories
    await category_collection.delete_many({"owner_id": user_id})

    # Delete user
    await users_collection.delete_one({"_id": ObjectId(user_id)})

    return {"message": "Account deleted successfully"}


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
