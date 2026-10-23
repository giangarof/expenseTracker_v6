from dotenv import load_dotenv
import os
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
algorithm = "HS256"
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


if not JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is not set")
