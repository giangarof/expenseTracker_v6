from datetime import timedelta
from typing import Annotated
from bson import ObjectId
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Path
from fastapi.security import OAuth2PasswordRequestForm

from App.schemas.expense import ExpenseRequest
from App.schemas.users import UserRequest
from App.utils.utils import hash_password, checkIfExist
from App.utils.auth import (
    get_current_user,
    create_access_token,
    authenticate_user,
    user_dependency,
)
from App.database.database import expense_collection
from App.schemas.token import Token

router = APIRouter(prefix="/api/expenses", tags=["Expenses"])

current = get_current_user


@router.get("/")
async def my_expenses(user: user_dependency):

    # Fetch all expenses
    expenses = await expense_collection.find({"owner_id": user["id"]}).to_list(
        length=100
    )

    # Loops over each ObjectId to replace ObjectId to plain str
    for expense in expenses:
        expense["id"] = str(expense.pop("_id"))

    # Returns success
    return {"message": "All your expenses", "data": expenses}


@router.get("/{id}")
async def get_one(user: user_dependency, id: str):

    # Fetch
    theExpense = await expense_collection.find_one(
        {"_id": ObjectId(id), "owner_id": user["id"]}
    )

    # Check if exist
    checkIfExist(theExpense)

    # The id might look likt this: ObjectId("671234567890123456789012")
    # .pop() takes the ObjectId and convert it into: "671234567890123456789012"
    theExpense["id"] = str(theExpense.pop("_id"))

    # Returns message
    return {"message": "Income", "data": theExpense}


@router.post("/")
async def add_expense(user: user_dependency, expenseRequest: ExpenseRequest):

    # Convert the request into dictionary
    expense = expenseRequest.model_dump()

    # Owner id field equals to the logged user
    expense["owner_id"] = user["id"]

    # Await and insert into db
    await expense_collection.insert_one(expense)

    # Returns success
    return {"message": "Income added successfully"}


@router.put("/{id}")
async def update_expense(
    user: user_dependency, expenseRequest: ExpenseRequest, id: str
):

    # Fetch it
    theExpense = await expense_collection.find_one(
        {"_id": ObjectId(id), "owner_id": user["id"]}
    )

    # Check if exist
    checkIfExist(theExpense)

    # Update if exist
    updateExpense = expenseRequest.model_dump()
    await expense_collection.update_one(
        {"_id": ObjectId(id), "owner_id": user["id"]},
        {"$set": updateExpense},
    )

    # Returns message
    return {"message": "Income updated successfully"}


@router.delete("/{id}")
async def delete_income(user: user_dependency, id: str):

    # Fetch it
    theExpense = await expense_collection.find_one(
        {"_id": ObjectId(id), "owner_id": user["id"]}
    )

    # Check if exist
    checkIfExist(theExpense)

    # Delete it
    await expense_collection.delete_one(
        {
            "_id": ObjectId(id),
            "owner_id": user["id"],
        }
    )

    # Returns message
    return {"message": "deleted successfully"}
