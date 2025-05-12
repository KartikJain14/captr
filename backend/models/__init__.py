from .auth import *
from .user import *
from pydantic import BaseModel
from typing import Any


class BaseResponseModel(BaseModel):
    success: bool
    message: str
    data: Any
