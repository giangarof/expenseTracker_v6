from datetime import timedelta
from typing import Annotated
from bson import ObjectId
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Path
from fastapi.security import OAuth2PasswordRequestForm

from App.schemas.expense import Expense, ExpenseRequest
from App.utils.utils import checkID, checkIfExist
from App.utils.auth import (
    get_current_user,
    create_access_token,
    authenticate_user,
    user_dependency,
)
from App.database.database import expense_collection, category_collection
from App.schemas.token import Token

router = APIRouter(prefix="/api/expenses", tags=["Expenses"])


@router.get("/", status_code=status.HTTP_200_OK)
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


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_one(user: user_dependency, id: str):

    # Check ID format
    checkID(id)

    # Fetch
    theExpense = await expense_collection.find_one(
        {"_id": ObjectId(id), "owner_id": user["id"]}
    )

    # Check if exist
    checkIfExist(theExpense, "Expense ID does not exist")

    # The id might look likt this: ObjectId("671234567890123456789012")
    # .pop() takes the ObjectId and convert it into: "671234567890123456789012"
    theExpense["id"] = str(theExpense.pop("_id"))

    # Returns message
    return {"message": "Income", "data": theExpense}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_expense(user: user_dependency, expenseRequest: ExpenseRequest):

    # Owner id field equals to the logged user
    new_expense = Expense(
        name=expenseRequest.name, amount=expenseRequest.amount, owner_id=user["id"]
    )
    # Await and insert into db
    await expense_collection.insert_one(new_expense.model_dump())
    # Returns success
    return {"message": "Expense added successfully"}


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_expense(
    user: user_dependency, expenseRequest: ExpenseRequest, id: str
):
    # Check ID format
    checkID(id)

    # Fetch it
    theExpense = await expense_collection.find_one(
        {"_id": ObjectId(id), "owner_id": user["id"]}
    )
    # Check if exist
    checkIfExist(theExpense, "Expense ID does not exist")

    # Prepare format to update
    updateExpense = expenseRequest.model_dump()

    # IF category_id is not None -  Workflow
    if expenseRequest.category_id is not None:
        # Check category_id format
        checkID(expenseRequest.category_id)

        # if category_id exist
        category = await category_collection.find_one(
            {
                "_id": ObjectId(expenseRequest.category_id),
                "owner_id": user["id"],
            }
        )

        # Check if category exist
        checkIfExist(category, "Category does not exist")

    # Update if exist
    await expense_collection.update_one(
        {"_id": ObjectId(id), "owner_id": user["id"]},
        {"$set": updateExpense},
    )

    # Returns message
    return {"message": "Expense updated successfully"}


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_expense(user: user_dependency, id: str):

    # Check ID format
    checkID(id)

    # Fetch it
    theExpense = await expense_collection.find_one(
        {"_id": ObjectId(id), "owner_id": user["id"]}
    )

    # Check if exist
    checkIfExist(theExpense, "Expense ID does not exist")

    # Delete it
    await expense_collection.delete_one(
        {
            "_id": ObjectId(id),
            "owner_id": user["id"],
        }
    )

    # Returns message
    return {"message": "deleted successfully"}
