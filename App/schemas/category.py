from typing import Literal

from pydantic import BaseModel


class Category(BaseModel):
    name: str
    type: Literal["Expense", "Income"]
    owner_id: str

    def __init__(self, name, type, owner_id):
        super().__init__(name=name, type=type, owner_id=owner_id)


class CategoryRequest(BaseModel):
    name: str
    type: Literal["Expense", "Income"]
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Food",
                "type": "Expense",
            }
        }
    }
