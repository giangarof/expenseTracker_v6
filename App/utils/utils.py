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


def checkIfExist(data):
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Income does not exist..."
        )


def checkIfAdmin(data):
    if data["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not allowed to perform this task...",
        )


def checkIfInt(data):
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID not provided..."
        )


def checkIfNone(data):
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="ID does not exist..."
        )
