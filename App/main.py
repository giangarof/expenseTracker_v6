from fastapi import FastAPI
from App.routes.user import router as UserRouter
from App.routes.income import router as IncomeRouter
from App.routes.expenses import router as ExpenseRouter
from App.routes.admin import router as AdminRouter

app = FastAPI(
    title="Expense Tracker API",
)

app.include_router(UserRouter)
app.include_router(IncomeRouter)
app.include_router(ExpenseRouter)
app.include_router(AdminRouter)
