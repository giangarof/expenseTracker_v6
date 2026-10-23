from pydantic import BaseModel


class Income(BaseModel):
    id: str
    name: str
    amount: float
    owner_id: str

    def __init__(self, name, amount, owner_id):
        self.name = name
        self.amount = amount
        self.owner_id = owner_id


class IncomeRequest(BaseModel):
    name: str
    amount: int
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "main income",
                "amount": 50000,
            }
        }
    }
