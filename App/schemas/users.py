from datetime import datetime, timezone

from pydantic import BaseModel, Field
from typing import Literal


# Core model and fields admitted
# In mongoDB, the id is generated when inserting the document as _id
class User(BaseModel):
    name: str
    username: str
    email: str
    password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    role: Literal["basic", "admin"] = "basic"

    # Not necessary, Pydantic does handle it
    # def __init__(self, name, username, email, password, role="basic"):
    #     super().__init__(
    #         name=name,
    #         username=username,
    #         email=email,
    #         password=password,
    #         role=role,
    #     )


# Represents the User input
class UserRequest(BaseModel):
    name: str = Field(min_length=2, max_length=25)
    username: str = Field(min_length=2, max_length=25)
    email: str = Field(min_length=2, max_length=40)
    password: str = Field(min_length=8)
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "john doe",
                "username": "jdoe",
                "email": "jdoe@gmail.com",
                "password": "password",
            }
        }
    }
