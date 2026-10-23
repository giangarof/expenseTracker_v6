from pydantic import BaseModel, Field


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
