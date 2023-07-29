from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
from starlette.responses import RedirectResponse
import sqlite3

from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine
import httpx
from fastapi.responses import JSONResponse

logging.basicConfig(filename='../logs/api.log', encoding='utf-8',format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

logger=logging.getLogger("fast_api_logger")

logger.setLevel(logging.INFO)

models.Base.metadata.create_all(bind=engine)

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

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.get("/user_data")
def get_all_users():
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS testTable (name TEXT, number IINTEGER)''')
    c.execute('''INSERT INTO testTable (name, number) VALUES ("John", 3)''')
    c.execute('''SELECT * FROM testTable;''')
    results = c.fetchall()

    print(results)
    
    conn.commit()
    conn.close()

    return results   

@app.post("/dbTest")
def testDB():
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS testTable (name TEXT, number IINTEGER)''')
    c.execute('''INSERT INTO testTable (name, number) VALUES ("John", 3)''')
    c.execute('''SELECT * FROM testTable;''')
    results = c.fetchall()

    print(results)
    
    conn.commit()
    conn.close()

    return results

@app.post("/createUser")
def createUser(first_name, last_name , email, birthday, username):
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()

    c.execute('''INSERT INTO users (first_name, last_name, email, birthday, username) VALUES ()''')

    conn.commit()
    conn.close()
    
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