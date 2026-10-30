from datetime import timedelta
from typing import Annotated
from bson import ObjectId
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status, Path

from App.schemas.category import Category, CategoryRequest
from App.utils.utils import checkID, hash_password, checkIfExist
from App.utils.auth import (
    get_current_user,
    create_access_token,
    authenticate_user,
    user_dependency,
)
from App.database.database import category_collection

router = APIRouter(prefix="/api/category", tags=["Category"])


# Method: GET
# Route: /api/category/
# Description: List all categories that belong to the user
@router.get("/", status_code=status.HTTP_200_OK)
async def my_categories(user: user_dependency):

    # Fetch all categories
    categories = await category_collection.find({"owner_id": user["id"]}).to_list(
        length=100
    )

    # Loops over each ObjectId to replace ObjectId to plain str
    for category in categories:
        category["id"] = str(category.pop("_id"))

    # Returns success
    return {"message": "All your categories", "data": categories}


# Method: POST
# Route: /api/category/
# Description: Add a category
@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_category(user: user_dependency, categoryRequest: CategoryRequest):
    # Owner id field equals to the logged user
    new_category = Category(categoryRequest.name, categoryRequest.type, user["id"])
    # Await and insert into db
    await category_collection.insert_one(new_category.model_dump())
    # Returns success
    return {"message": "Category added successfully"}


# Method: PUT
# Route: /api/category/{id}
# Description: update one category by id
@router.put("/", status_code=status.HTTP_200_OK)
async def update_category(
    user: user_dependency, categoryRequest: CategoryRequest, id: str
):
    # Check ID format
    checkID(id)

    # Fetch it
    theCategory = await category_collection.find_one(
        {"_id": ObjectId(id), "owner_id": user["id"]}
    )

    # Check if exist
    checkIfExist(theCategory, "category does not exist")

    # Update if exist
    updateCategory = categoryRequest.model_dump()
    await category_collection.update_one(
        {"_id": ObjectId(id), "owner_id": user["id"]},
        {"$set": updateCategory},
    )

    # Returns message
    return {"message": "Income updated successfully"}


# Route: /api/category/{id}
# Description: get one category by id
@router.get("/{id}", status_code=status.HTTP_200_OK)
async def getOne_category(user: user_dependency, id: str):

    # Check ID format
    checkID(id)

    # Fetch
    theCategory = await category_collection.find_one(
        {"_id": ObjectId(id), "owner_id": user["id"]}
    )

    # Check if exist
    checkIfExist(theCategory, "Category does not exist")

    # The id might look likt this: ObjectId("671234567890123456789012")
    # .pop() takes the ObjectId and convert it into: "671234567890123456789012"
    theCategory["id"] = str(theCategory.pop("_id"))

    # Returns message
    return {"message": "Income", "data": theCategory}


# Method: DELETE
# Route: /api/category/{id}
# Description: delete one category by id
@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_category(user: user_dependency, id: str):

    # Check ID format
    checkID(id)

    # Fetch it
    theCategory = await category_collection.find_one(
        {"_id": ObjectId(id), "owner_id": user["id"]}
    )

    # Check if exist
    checkIfExist(theCategory, "Category does not exist")

    # Delete it
    await category_collection.delete_one(
        {
            "_id": ObjectId(id),
            "owner_id": user["id"],
        }
    )

    # Returns message
    return {"message": "deleted successfully"}
