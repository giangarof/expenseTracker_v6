from fastapi import FastAPI
from App.routes.user import router as UserRouter

app = FastAPI(
    title="Expense Tracker API",
)

app.include_router(UserRouter)
