from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from .routers import auth_router, search_router, transcribe_router, extract_router
from .models import BaseResponseModel

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    try:
        error_messages = []
        for error in exc.errors():
            if "msg" in error:
                error_messages.append(error["msg"])
            else:
                error_messages.append(str(error))
        error_message = (
            "; ".join(error_messages) if error_messages else "Validation error"
        )
    except Exception:
        error_message = "Validation error occurred"

    return JSONResponse(
        status_code=422,
        content=BaseResponseModel(
            success=False, message=error_message, data=None
        ).model_dump(),
    )


@app.exception_handler(HTTPException)
async def validation_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=BaseResponseModel(
            success=False, message=exc.detail, data=None
        ).model_dump(),
    )


@app.get("/")
async def index():
    return {
        "success": True,
        "message": "Hello World! Server is up and running!",
        "data": None,
    }


app.include_router(auth_router)
app.include_router(search_router)
app.include_router(transcribe_router)
app.include_router(extract_router)
