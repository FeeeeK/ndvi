import uvicorn  # type: ignore
from fastapi import FastAPI

from src.api import router
from src.config import IP, PORT
from src.utils import create_tables

app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    await create_tables()


uvicorn.run(app, host=IP, port=PORT)
