from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
from starlette.responses import RedirectResponse
import sqlite3
import httpx
from fastapi.responses import JSONResponse

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
    
@app.post('/login_try')
async def login_try(request: Request):
    # Retrieve the username and password from the request's JSON body
    login_data = await request.json()
    username = login_data.get('username')
    password = login_data.get('password')
    # Perform authentication checks
    # You can implement your own logic here to verify the credentials
    # For example, you might check against a database or compare with hardcoded values
    if username.lower() == '' and password == '':
        # Authentication successful
        return JSONResponse(content={'success': True}, status_code=200)
    else:
        # Authentication failed
        raise HTTPException(status_code=401, detail='Authentication failed')
