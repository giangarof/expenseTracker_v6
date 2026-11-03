from datetime import datetime, timedelta
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
    expense_collection,
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
# Description: get all budgets that belong to the logged user
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


# Method: GET
# Route: /api/budget/{id}
# Description: get one budget by id
@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_budget_byID(user: user_dependency, id: str):
    pipeline = [
        {"$match": {"_id": ObjectId(id), "owner_id": user["id"]}},
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
    return {"Budget": result}


# Method: PUT
# Route: /api/budget/{id}
# Description: update budget by id
@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_budget_byID(
    user: user_dependency, budgetRequest: BudgetRequest, id: str
):

    # Check if Budget exist
    budget = await budget_collection.find_one(
        {"_id": ObjectId(id), "owner_id": user["id"]}
    )

    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Budget does not exist"
        )

    # Update budget

    update_budget = budgetRequest.model_dump(exclude_unset=True)

    await budget_collection.update_one(
        {"_id": ObjectId(id), "owner_id": user["id"]},
        {"$set": update_budget},
    )
    print(update_budget)
    return {"Message": "Budget updated succesfully"}


# Method: DELETE
# Route: /api/budget/{id}
# Description: delete budgets by id
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_budget_byID(user: user_dependency, id: str):
    budget = await budget_collection.find_one(
        {"_id": ObjectId(id), "owner_id": user["id"]}
    )

    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Does not exist"
        )

    # Delete it
    await budget_collection.delete_one(
        {
            "_id": ObjectId(id),
            "owner_id": user["id"],
        }
    )

    # Returns message
    return {"message": "deleted successfully"}


# Method: GET
# Route: /api/budget/{id}/progress
# Description: calculate progess
# Method: GET
# Route: /api/budget/{id}/progress
# Description: calculate progress
@router.get("/{id}/progress", status_code=status.HTTP_200_OK)
async def getBudgetProgress(user: user_dependency, id: str):

    # 1. Validate budget ID
    if not ObjectId.is_valid(id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid budget ID"
        )

    # 2. Retrieve the budget
    budget = await budget_collection.find_one(
        {"_id": ObjectId(id), "owner_id": user["id"]}
    )

    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Budget does not exist"
        )

    # 3. Retrieve budget and category information
    pipeline = [
        {"$match": {"_id": ObjectId(id), "owner_id": user["id"]}},
        {
            "$lookup": {
                "from": "category",
                "let": {"categoryId": "$category_id"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {"$eq": [{"$toString": "$_id"}, "$$categoryId"]}
                        }
                    }
                ],
                "as": "category",
            }
        },
        {"$unwind": {"path": "$category", "preserveNullAndEmptyArrays": True}},
        {
            "$project": {
                "_id": 0,
                "budget_id": {"$toString": "$_id"},
                "name": 1,
                "limit": 1,
                "category_id": 1,
                "category_name": {"$ifNull": ["$category.name", "Not assigned"]},
            }
        },
    ]

    cursor = await budget_collection.aggregate(pipeline)
    result = await cursor.to_list(length=1)

    budget_info = result[0]

    # 4. Build expense match
    expense_match = {"owner_id": user["id"]}

    if budget["category_id"] is not None:
        expense_match["category_id"] = budget["category_id"]

    # 5. Retrieve expenses
    expense_pipeline = [
        {"$match": expense_match},
        {"$project": {"_id": 0, "name": 1, "amount": 1, "date": 1}},
    ]

    expense_cursor = await expense_collection.aggregate(expense_pipeline)
    expenses = await expense_cursor.to_list(length=None)

    # 6. Calculate progress
    total_spent = sum(expense["amount"] for expense in expenses)

    total_expenses = len(expenses)

    budget_limit = budget["limit"]

    remaining = budget_limit - total_spent

    percentage_used = (total_spent / budget_limit) * 100 if budget_limit > 0 else 0

    # 7. Return response
    return {
        **budget_info,
        "total_expenses": total_expenses,
        "total_spent": total_spent,
        "remaining": remaining,
        "percentage_used": round(percentage_used, 2),
        "exceeded": total_spent > budget_limit,
        "expenses": expenses,
    }
