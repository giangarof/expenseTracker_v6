from pydantic import BaseModel, Field


class Budget(BaseModel):
    name: str
    limit: float = Field(gt=0)
    month: int = Field(ge=1, le=12)
    year: int
    category_id: str | None = None
    owner_id: str


class BudgetRequest(BaseModel):
    name: str
    limit: float = Field(gt=0)
    month: int = Field(ge=1, le=12)
    year: int
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Budget for food",
                "limit": 500,
                "month": 11,
                "year": 2026,
            }
        }
    }
