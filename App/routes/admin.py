from datetime import timedelta
from typing import Annotated
from bson import ObjectId
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Path
from fastapi.security import OAuth2PasswordRequestForm

from App.schemas.expense import ExpenseRequest
from App.schemas.income import IncomeRequest
from App.schemas.users import UserRequest, User
from App.utils.utils import checkIfInt, checkIfNone, hash_password, checkIfAdmin
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
)
from App.schemas.token import Token

router = APIRouter(prefix="/api/admin", tags=["Admin"])


# Incomes
@router.get("/income/{id}")
async def get_income_byID(user: user_dependency, id: str):

    # Check if the user is admin
    checkIfAdmin(user)

    # Check if id is provided
    checkIfInt(id)

    # Fetch and return
    income = await income_collection.find_one({"_id": ObjectId(id)})
    checkIfNone(income)

    # Replace ObjectID to plain string
    income["id"] = str(income.pop("_id"))

    # Return income
    return income


@router.put("/income/{id}")
async def update_income_byID(
    user: user_dependency, incomeRequest: IncomeRequest, id: str
):

    # Check if the user is admin
    checkIfAdmin(user)

    # Check if id is provided
    checkIfInt(id)

    # Check if exist
    income = await income_collection.find_one({"_id": ObjectId(id)})
    checkIfNone(income)

    # Update if exist
    updateIncome = incomeRequest.model_dump()
    await income_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": updateIncome},
    )

    # Returns message
    return {"message": "Income updated successfully"}


@router.delete("/income/{id}")
async def delete_income_byID(user: user_dependency, id: str):
    # Check if the user is admin
    checkIfAdmin(user)

    # Check if id is provided
    checkIfInt(id)

    # Check if exist
    income = await income_collection.find_one({"_id": ObjectId(id)})
    checkIfNone(income)

    # Delete if exist
    await income_collection.delete_one(
        {
            "_id": ObjectId(id),
        }
    )

    # Returns message
    return {"message": "deleted successfully"}


# Expenses
@router.get("/expense/{id}")
async def get_expense_byID(user: user_dependency, id: str):

    # Check if the user is admin
    checkIfAdmin(user)

    # Check if id is provided
    checkIfInt(id)

    # Fetch and return
    expense = await expense_collection.find_one({"_id": ObjectId(id)})
    checkIfNone(expense)

    # Replace ObjectID() with plain string
    expense["id"] = str(expense.pop("_id"))

    # Returns success
    return expense


@router.put("/expense/{id}")
async def update_expense_byID(
    user: user_dependency, expenseRequest: ExpenseRequest, id: str
):
    # Check if the user is admin
    checkIfAdmin(user)

    # Check if id is provided
    checkIfInt(id)

    # Check if exist
    expense = await expense_collection.find_one({"_id": ObjectId(id)})
    checkIfNone(expense)

    # Update if exist
    updateExpense = expenseRequest.model_dump()
    await expense_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": updateExpense},
    )

    # Returns message
    return {"message": "Expense updated successfully"}


@router.delete("/expense/{id}")
async def delete_expense_byID(user: user_dependency, id: str):
    # Check if the user is admin
    checkIfAdmin(user)

    # Check if id is provided
    checkIfInt(id)

    # Check if exist
    expense = await expense_collection.find_one({"_id": ObjectId(id)})
    checkIfNone(expense)

    # Delete if exist
    await expense_collection.delete_one(
        {
            "_id": ObjectId(id),
        }
    )

    # Returns message
    return {"message": "deleted successfully"}


# Users
@router.get("/user/{id}")
async def get_user_byID(user: user_dependency, id: str):
    # Check if the user is admin
    checkIfAdmin(user)

    # Check if id is provided
    checkIfInt(id)

    # Fetch and return
    users = await users_collection.find_one({"_id": ObjectId(id)})
    checkIfNone(users)

    # Replace ObjectID with plain str
    users["id"] = str(users.pop("_id"))

    # Returns success
    return {"message": "User found", "user": users}


@router.put("/user/{id}")
async def update_user_byID(user: user_dependency, userRequest: UserRequest, id: str):
    # Check if the user is admin
    checkIfAdmin(user)

    # Check if id is provided
    checkIfInt(id)

    # Check if exist
    users = await users_collection.find_one({"_id": ObjectId(id)})
    checkIfNone(users)

    # Update if exist
    updateUser = userRequest.model_dump()

    # Hash password
    updateUser["password"] = hash_password(userRequest.password)

    await users_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": updateUser},
    )

    # Returns message
    return {"message": "Expense updated successfully"}


@router.delete("/user/{id}")
async def delete_user_byID(user: user_dependency, id: str):
    # Check if the user is admin
    checkIfAdmin(user)

    # Check if id is provided
    checkIfInt(id)

    # Check if exist
    users = await users_collection.find_one({"_id": ObjectId(id)})
    checkIfNone(users)

    # Delete if exist
    await users_collection.delete_one(
        {
            "_id": ObjectId(id),
        }
    )

    # Returns message
    return {"message": "deleted successfully"}
