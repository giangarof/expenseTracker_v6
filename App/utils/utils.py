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
