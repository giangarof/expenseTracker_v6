from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from App.exports import JWT_SECRET_KEY, algorithm, oauth2_bearer
from App.utils.utils import verify_password
from App.database.database import users_collection


from jose import JWTError, jwt


async def authenticate_user(username_or_email: str, password: str):
    user = await users_collection.find_one(
        {
            "$or": [
                {"username": username_or_email},
                {"email": username_or_email.lower()},
            ]
        }
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    verify_password(password, user["password"])

    return user


def create_access_token(
    username: str, user_id: str, role: str, expires_delta: timedelta
):
    encode = {"sub": username, "role": role, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, JWT_SECRET_KEY, algorithm=algorithm)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[algorithm])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        role: str = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {"username": username, "id": user_id, "role": role}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


user_dependency = Annotated[dict, Depends(get_current_user)]
