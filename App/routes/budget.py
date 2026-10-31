from datetime import timedelta
from typing import Annotated
from bson import ObjectId
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Path
from fastapi.security import OAuth2PasswordRequestForm

from App.schemas.budget import Budget, BudgetRequest
from App.schemas.users import UserRequest
from App.utils.utils import checkID, hash_password, checkIfExist
from App.utils.auth import (
    get_current_user,
    create_access_token,
    authenticate_user,
    user_dependency,
)
from App.database.database import (
    income_collection,
    category_collection,
    budget_collection,
)
from App.schemas.token import Token

router = APIRouter(prefix="/api/budget", tags=["Budget"])


# Method: POST
# Route: /api/budget/
# Description: Add a budget
@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_budget(user: user_dependency, budgetRequest: BudgetRequest):
    # Owner id field equals to the logged user
    new_budget = Budget(
        name=budgetRequest.name,
        limit=budgetRequest.limit,
        month=budgetRequest.month,
        year=budgetRequest.year,
        owner_id=user["id"],
    )

    res = new_budget.model_dump()

    # Await and insert into db
    await budget_collection.insert_one(res)
    # Returns success
    return {"message": "Budget added successfully"}


# Method: GET
# Route: /api/budget/
# Description: get all budgets
@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_budgets(user: user_dependency):

    pipeline = [
        {"$match": {"owner_id": user["id"]}},
        {
            "$project": {
                "_id": 0,
                "id": {"$toString": "$_id"},
                "name": 1,
                "limit": 1,
                "month": 1,
                "year": 1,
                "category_id": 1,
            }
        },
    ]

    cursor = await budget_collection.aggregate(pipeline)
    result = await cursor.to_list(length=None)
    return {"Budgets": result}
