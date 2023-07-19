from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from starlette.responses import RedirectResponse
import sqlite3

logging.basicConfig(filename='../logs/api.log', encoding='utf-8',format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

logger=logging.getLogger("fast_api_logger")

logger.setLevel(logging.INFO)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DBNAME = 'social_media.db'

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.get("/user_data")
def get_all_users():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()