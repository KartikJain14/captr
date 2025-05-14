from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from ..models import (
    LoginResponse,
    LoginRequest,
    RegisterResponse,
    RegisterRequest,
    VerificationResponse,
    LoginData,
    UserModel,
    UserDetailsResponse,
    UserDetails,
)
from ..utils.hashing import hash_password, check_password
import os
from dotenv import load_dotenv
import jwt
from ..utils.email import send_email
from datetime import timezone, datetime, timedelta
from bson import objectid
from ..utils.db import user_collection
from ..middlewares.auth import get_current_user

url = "http://localhost:8000"
jwt_secret = os.getenv("JWT_SECRET")

load_dotenv()
auth_router = APIRouter(prefix="/auth")


@auth_router.post("/login", response_model=LoginResponse)
async def login(login_request: LoginRequest):
    user = user_collection.find_one({"email": login_request.email})
    print(user)
    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid email or password",
        )
    if not check_password(login_request.password, user.get("password")):
        raise HTTPException(
            status_code=400,
            detail="Invalid email or password",
        )
    if not user.get("is_verified"):
        raise HTTPException(
            status_code=400,
            detail="Email not verified",
        )
    token = jwt.encode(
        {
            "id": str(user.get("_id")),
        },
        jwt_secret,
        algorithm="HS256",
    )
    del user["password"]
    return LoginResponse(
        success=True,
        message="Login successful",
        data=LoginData(token=token, user=UserModel(**user)),
    )


@auth_router.post("/register")
async def register(
    register_request: RegisterRequest,
) -> RegisterResponse:
    if user_collection.find_one({"email": register_request.email}) is not None:
        raise HTTPException(
            status_code=400,
            detail="Email address already exists",
        )
    register_request.password = hash_password(register_request.password)
    user = user_collection.insert_one(
        {"is_verified": False, **register_request.model_dump()}
    )
    token = jwt.encode(
        {
            "id": str(user.inserted_id),
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=10),
        },
        jwt_secret,
        algorithm="HS256",
    )
    send_email(
        register_request.email,
        "Email Verification for Captr",
        f"Please click on this link: {url}/auth/verify?token={token}",
    )
    return RegisterResponse(
        success=True,
        message="Registered Successfully",
    )


@auth_router.get("/verify")
def verify(token: str) -> VerificationResponse:
    try:
        decoded = jwt.decode(token, jwt_secret, algorithms=["HS256"])
    except jwt.exceptions.ExpiredSignatureError as e:
        raise HTTPException(
            detail="This link has expired, please request for a new verification link",
            status_code=400,
        )
    user = user_collection.find_one({"_id": objectid.ObjectId(decoded.get("id"))})
    if not user:
        raise HTTPException(
            detail="User not found",
            status_code=404,
        )
    user_collection.update_one(
        {"_id": objectid.ObjectId(decoded.get("id"))},
        {"$set": {"is_verified": True}},
    )
    return VerificationResponse(success=True)


@auth_router.get("/me", response_model=UserDetailsResponse)
async def get_me(current_user: UserModel = Depends(get_current_user)):
    return UserDetailsResponse(
        success=True,
        message="User details fetched successfully",
        data=UserDetails(user=current_user),
    )
