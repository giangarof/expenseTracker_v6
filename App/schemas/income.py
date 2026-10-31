from datetime import datetime, timezone

from pydantic import BaseModel, Field


class Income(BaseModel):
    name: str
    amount: float
    owner_id: str
    category_id: str | None = None
    date_added: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Pydantic handles init
    # def __init__(self, name, amount, owner_id):
    #     self.name = name
    #     self.amount = amount
    #     self.owner_id = owner_id


class IncomeRequest(BaseModel):
    name: str
    amount: int
    category_id: str | None = None
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "main income",
                "amount": 50000,
            }
        }
    }
