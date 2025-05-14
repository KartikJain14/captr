from pydantic import BaseModel, BeforeValidator
from typing import Annotated
from .user import UserModel
from ..utils.validators import validate_password, validate_email


class LoginRequest(BaseModel):
    email: Annotated[str, BeforeValidator(validate_email)]
    password: Annotated[str, BeforeValidator(validate_password)]


class LoginData(BaseModel):
    token: str
    user: UserModel


class LoginResponse(BaseModel):
    success: bool
    message: str
    data: LoginData


class RegisterRequest(BaseModel):
    name: str
    email: Annotated[str, BeforeValidator(validate_email)]
    password: Annotated[str, BeforeValidator(validate_password)]


class RegisterResponse(BaseModel):
    success: bool
    message: str
    data: None = None


class VerificationResponse(BaseModel):
    success: bool
    message: str = "User verified successfully"
    data: None = None


class UserDetails(BaseModel):
    user: UserModel


class UserDetailsResponse(BaseModel):
    success: bool
    message: str = "User data fetched successfully"
    data: UserDetails
