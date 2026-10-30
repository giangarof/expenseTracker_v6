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
