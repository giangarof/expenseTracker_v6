# Expense tracker V^

## About

- Sixth version of my Expense Tracker series.
- Continuation of V4, which introduced MongoDB for database management.
- Implements authentication and user verification.
- Expenses and incomes are now associated with users through a relationship with the user model.

## What this version does?

- The user can login and signup
- If the user is authenticated, the user can perform the following in the incomes and expenses:
  - Add
  - Update
  - Delete
  - Retrieve an element by id
  - Generate a analysis based on incomes and expenses
- Last version includes extra functionalities such as:
  - Budgeting expenses
  - Assign Categories to the budget and expenses
  - Summary reports

- This version implements role-based mode. Meaning that the user can have the `admin` or `basic` role.
  - The `admin` role perform extra capabilities across all the dataset

## Steps

- Clone the project
- Create a virtual environment: `python3 -m venv <name>`
- Activate the environment: `source <name>/bin/activate`
- Install dependencies: `pip install -r req.txt`
- To run: `cd App` > `fastapi run main.py --reload`

## Database setup

- You must create you cluster instance in mongo atlas.
- In your root directory, create a .env file with the next credentials

```
DB_USER = Your mongodb user
DB_PSW = Your mongodb password
DB_URL= Your mongodb URL
```

## All versions

- [v6](https://github.com/giangarof/expenseTracker_v6): Extension of v4. Implements user authentication and verification
- [v5](https://github.com/giangarof/expenseTracker_v5): Extension of v3. Implements user authentication and verification
- [v4](https://github.com/giangarof/expenseTracker_v4): This version implements FastAPI along with NoSQL (MongoDB)
- [v3](https://github.com/giangarof/expenseTracker_v3): This version implements FastAPI along with SQL (SQLAlchemy)
- [v2](https://github.com/giangarof/expenseTracker_v2): This version implements FastAPI
- [V1](https://github.com/giangarof/expenseTracker_v1): This version implements vanilla python. Can be used through the terminal.
