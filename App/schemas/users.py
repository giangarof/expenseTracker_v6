from pydantic import BaseModel, Field
from typing import Literal


class User(BaseModel):
    name: str
    username: str
    email: str
    password: str
    role: Literal["basic", "admin"] = "basic"

    def __init__(self, name, username, email, password, role="basic"):
        super().__init__(
            name=name,
            username=username,
            email=email,
            password=password,
            role=role,
        )


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
