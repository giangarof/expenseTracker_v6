from datetime import timedelta
from typing import Annotated
from bson import ObjectId
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Path

from App.schemas.income import IncomeRequest, Income
from App.schemas.users import UserRequest
from App.utils.utils import checkID, checkIfExist
from App.utils.auth import (
    user_dependency,
)
from App.database.database import (
    income_collection,
    category_collection,
    expense_collection,
)
from App.schemas.token import Token

router = APIRouter(prefix="/api/summary", tags=["Summary"])


# Method: GET
# Route: /api/summary
# Description: Overall summary
@router.get("/overall")
async def summary(user: user_dependency):
    # incomes = await income_collection.find({"owner_id": user["id"]}).to_list(length=100)

    pipeline_income = [
        {"$match": {"owner_id": user["id"]}},
        {"$group": {"_id": None, "total_income": {"$sum": "$amount"}}},
    ]
    pipeline_expense = [
        {"$match": {"owner_id": user["id"]}},
        {"$group": {"_id": None, "total_expenses": {"$sum": "$amount"}}},
    ]

    cursor_income = await income_collection.aggregate(pipeline_income)
    cursor_expense = await expense_collection.aggregate(pipeline_expense)

    result_income = await cursor_income.to_list(length=1)
    result_expenses = await cursor_expense.to_list(length=1)
    # print(result_income)

    total_income = result_income[0]["total_income"] if result_income else 0
    total_expenses = result_expenses[0]["total_expenses"] if result_expenses else 0

    balance = total_income - total_expenses

    return {
        "total_income": result_income,
        "total_expenses": result_expenses,
        "balance": balance,
    }


# Method: GET
# Route: /api/summary/income
# Description: Income by category
@router.get("/income_summary")
async def income_summary(user: user_dependency):

    pipeline = [
        {"$match": {"owner_id": user["id"]}},
        {"$group": {"_id": "$category_id", "total": {"$sum": "$amount"}}},
        {
            "$lookup": {
                "from": "category",
                "let": {"category_id": "$_id"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {"$eq": ["$_id", {"$toObjectId": "$$category_id"}]}
                        }
                    }
                ],
                "as": "category",
            }
        },
        {
            "$project": {
                "_id": 0,
                "category_name": {
                    "$ifNull": [
                        {"$arrayElemAt": ["$category.name", 0]},
                        "Uncategorized",
                    ]
                },
                "total": 1,
            }
        },
    ]

    cursor = await income_collection.aggregate(pipeline)
    result = await cursor.to_list(length=None)

    return {"income_by_category": result}


# Method: GET
# Route: /api/summary/expenses
# Description: Expenses by category
@router.get("/expenses_summary")
async def expenses_summary(user: user_dependency):
    pipeline = [
        {"$match": {"owner_id": user["id"]}},
        {"$group": {"_id": "$category_id", "total": {"$sum": "$amount"}}},
        {
            "$lookup": {
                "from": "category",
                "let": {"category_id": "$_id"},
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {"$eq": ["$_id", {"$toObjectId": "$$category_id"}]}
                        }
                    }
                ],
                "as": "category",
            }
        },
        {
            "$project": {
                "_id": 0,
                "category_name": {
                    "$ifNull": [
                        {"$arrayElemAt": ["$category.name", 0]},
                        "Uncategorized",
                    ]
                },
                "total": 1,
            }
        },
    ]

    cursor = await expense_collection.aggregate(pipeline)
    result = await cursor.to_list(length=None)
    return {"income_by_category": result}


# Method: GET
# Route: /api/summary/monthly
# Description: monthy summary
@router.get("/monthly")
async def summary_over_time(user: user_dependency):

    pipeline = [
        {"$match": {"owner_id": user["id"]}},
        {
            "$group": {
                "_id": {"$dateToString": {"format": "%Y-%m", "date": "$date_added"}},
                "total": {"$sum": "$amount"},
            }
        },
        {"$sort": {"_id": 1}},
    ]

    income_cursor = await income_collection.aggregate(pipeline)
    expense_cursor = await expense_collection.aggregate(pipeline)

    incomes = await income_cursor.to_list(length=None)
    expenses = await expense_cursor.to_list(length=None)

    return {"monthly_income": incomes, "monthly_expenses": expenses}
