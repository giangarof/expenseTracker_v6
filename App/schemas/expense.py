from pydantic import BaseModel


class Expense(BaseModel):
    name: str
    amount: int
    category_id: str | None = None
    owner_id: str

    # This part is not necessary. Pydantic does create __init__ behind scenes
    def __init__(self, name, amount, owner_id):
        super().__init__(name=name, amount=amount, owner_id=owner_id)


class ExpenseRequest(BaseModel):
    name: str
    amount: int
    category_id: str | None = None

    model_config = {
        "json_schema_extra": {"example": {"name": "groceries", "amount": 250}}
    }
