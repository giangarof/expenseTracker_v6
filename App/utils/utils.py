from bson import ObjectId
from fastapi import HTTPException, status

from App.exports import bcrypt_context


def hash_password(data):
    hashed = bcrypt_context.hash(data)
    return hashed


def verify_password(password, hash_password):
    verify = bcrypt_context.verify(password, hash_password)

    if verify is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    return verify


def checkIfAdmin(data):
    if data["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to perform this task...",
        )


def checkIfExist(data, msg):
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{msg}")


# Check whether ID is ObjectID
def checkID(id):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID...")
