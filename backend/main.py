from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def index():
    return {"success": True, "message": "Hello World! Server is up and running!", "data": None}
