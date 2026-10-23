from datetime import timedelta
from typing import Annotated
from bson import ObjectId
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Path
from fastapi.security import OAuth2PasswordRequestForm

from App.schemas.income import IncomeRequest, Income
from App.schemas.users import UserRequest
from App.utils.utils import hash_password, checkIfExist
from App.utils.auth import (
    get_current_user,
    create_access_token,
    authenticate_user,
    user_dependency,
)
from App.database.database import income_collection
from App.schemas.token import Token

router = APIRouter(prefix="/api/income", tags=["Income"])


@router.get("/")
async def my_incomes(user: user_dependency):

    # Fetch all incomes
    incomes = await income_collection.find({"owner_id": user["id"]}).to_list(length=100)

    # Loops over each ObjectId to replace ObjectId to plain str
    for income in incomes:
        income["id"] = str(income.pop("_id"))

    # Returns success
    return {"message": "All your incomes", "data": incomes}


@router.get("/{id}")
async def get_one(user: user_dependency, id: str):

    # Fetch
    theIncome = await income_collection.find_one(
        {"_id": ObjectId(id), "owner_id": user["id"]}
    )

    # Check if exist
    checkIfExist(theIncome)

    # The id might look likt this: ObjectId("671234567890123456789012")
    # .pop() takes the ObjectId and convert it into: "671234567890123456789012"
    theIncome["id"] = str(theIncome.pop("_id"))

    # Returns message
    return {"message": "Income", "data": theIncome}


@router.post("/")
async def add_income(user: user_dependency, incomeRequest: IncomeRequest):

    # Convert the request into dictionary
    income = incomeRequest.model_dump()

    # Owner id field equals to the logged user
    income["owner_id"] = user["id"]

    # Await and insert into db
    await income_collection.insert_one(income)

    # Returns success
    return {"message": "Income added successfully"}


@router.put("/{id}")
async def update_income(user: user_dependency, incomeRequest: IncomeRequest, id: str):

    # Fetch it
    theIncome = await income_collection.find_one(
        {"_id": ObjectId(id), "owner_id": user["id"]}
    )

    # Check if exist
    checkIfExist(theIncome)

    # Update if exist
    updateIncome = incomeRequest.model_dump()
    await income_collection.update_one(
        {"_id": ObjectId(id), "owner_id": user["id"]},
        {"$set": updateIncome},
    )

    # Returns message
    return {"message": "Income updated successfully"}


@router.delete("/{id}")
async def delete_income(user: user_dependency, id: str):

    # Fetch it
    theIncome = await income_collection.find_one(
        {"_id": ObjectId(id), "owner_id": user["id"]}
    )

    # Check if exist
    checkIfExist(theIncome)

    # Delete it
    await income_collection.delete_one(
        {
            "_id": ObjectId(id),
            "owner_id": user["id"],
        }
    )

    # Returns message
    return {"message": "deleted successfully"}
