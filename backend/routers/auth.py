from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from ..models import (
    LoginResponse,
    LoginRequest,
    RegisterResponse,
    RegisterRequest,
    VerificationResponse,
)
from ..utils.hashing import hash_password, check_password
import os
import pymongo
from dotenv import load_dotenv
import logging
from pymongo.errors import CollectionInvalid
import jwt
from ..utils.email import send_email

url = "http://localhost:8000"
jwt_secret = os.getenv("JWT_SECRET")

load_dotenv()
auth_router = APIRouter(prefix="/auth")
mongo_uri = os.getenv("MONGO_URI")
print(mongo_uri)
client = pymongo.MongoClient(mongo_uri)

try:
    user_collection = client.users.create_collection("users")
except CollectionInvalid:
    logging.info("Users Collection already exists, skipping creation")
    user_collection = client.users.users


@auth_router.post("/login", response_model=LoginResponse)
async def login(login_request: LoginRequest):
    pass


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
    token = jwt.encode({"id": str(user.inserted_id)}, jwt_secret)
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
    print(token)
