import sys

from dotenv import load_dotenv
from loguru import logger
from starlette.config import Config
from starlette.datastructures import Secret

load_dotenv()
config = Config(".env")

IP = config("IP", str, "0.0.0.0")
PORT = config("PORT", int, 8080)

LOG_LEVEL = config("LOG_LEVEL", str, "DEBUG")

POSTGRES_HOST = config("POSTGRES_HOST", str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", Secret)
POSTGRES_USER = config("POSTGRES_USER", str)
POSTGRES_DB = config("POSTGRES_DB", str)

NDVI_PALETTE = [
    "0c0c0c",
    "5d576b",
    "fc440f",
    "ffc914",
    "71b340",
    "669d31",
    "598b2c",
    "3c5a14",
    "11270b",
]
GEE_SERVICE_EMAIL = config("GEE_SERVICE_EMAIL", str)
GEE_CREDENTIALS_FILE = config("GEE_CREDENTIALS_FILE", str)

logger.remove()
log_format = (
    "<level>{level: <8}</level> | "
    "{time:YYYY-MM-DD HH:mm:ss} | "
    "{name}:{function}:{line} > <level>{message}</level>"
)

logger.add(
    sys.stderr,
    format=log_format,
    level=LOG_LEVEL,
)
