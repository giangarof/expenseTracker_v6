from pydantic import BaseModel


class ExpenseRequest(BaseModel):
    name: str
    amount: int
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "groceries",
                "amount": 250,
            }
        }
    }
