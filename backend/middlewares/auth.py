import os
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from bson import ObjectId
from dotenv import load_dotenv

from ..models.user import UserModel
from ..utils.db import user_collection

load_dotenv()

jwt_secret = os.getenv("JWT_SECRET")

bearer_token = HTTPBearer()


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(bearer_token),
) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token.credentials, jwt_secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise credentials_exception

    user_id: str = payload.get("id")
    if user_id is None:
        raise credentials_exception

    user_data = user_collection.find_one({"_id": ObjectId(user_id)})
    if user_data is None:
        raise credentials_exception

    if not user_data.get("is_verified"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is not verified.",
        )

    if "password" in user_data:
        del user_data["password"]

    return UserModel(**user_data)
