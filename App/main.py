from fastapi import FastAPI
from App.routes.user import router as UserRouter
from App.routes.income import router as IncomeRouter
from App.routes.expenses import router as ExpenseRouter
from App.routes.category import router as CategoryRouter
from App.routes.summary import router as SummaryRouter
from App.routes.budget import router as BudgetRouter
from App.routes.admin import router as AdminRouter

app = FastAPI(
    title="Expense Tracker API",
)

app.include_router(UserRouter)
app.include_router(IncomeRouter)
app.include_router(ExpenseRouter)
app.include_router(CategoryRouter)
app.include_router(SummaryRouter)
app.include_router(AdminRouter)
app.include_router(BudgetRouter)
