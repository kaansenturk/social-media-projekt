from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
from starlette.responses import RedirectResponse
import sqlite3
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from fastapi.responses import JSONResponse

logging.basicConfig(filename='../logs/api.log', encoding='utf-8',format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

logger=logging.getLogger("fast_api_logger")

logger.setLevel(logging.INFO)

#
models.Base.metadata.create_all(bind=engine)

#
app = FastAPI()

origins = ["*"]

#
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DBNAME = 'social_media.db'

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# post method to delete table "users"
@app.post("/deleteUsers/")
def delete_users(db: Session = Depends(get_db)):
    db_delete_users = crud.delete_users(db)
    if db_delete_users:
        raise HTTPException(status_code=400, detail="Not Found")
    #return crud.get_users(db=db, skip=0, limit=100)

# post method to delete a single user from table "users" by id
@app.post("deleteUser")
def delete_user(db: Session = Depends(get_db)):
    db_delete_user = crud.delete_user(db)
    if db_delete_user:
        raise HTTPException(status_code=400, detail="Not Found")

# post method to create a user into table "users"
@app.post("/createUser/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/getUsers/", response_model=list[schemas.User])
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

@app.post("/login/", response_model=schemas.Login)
def create_login(user_id: int, login: schemas.LoginCreate, db: Session = Depends(get_db)):
    #db_logins = crud.get_logins(db, 0, 100)
    #if db_logins:
        #raise HTTPException(status_code=400, detail="No entries found")
    return crud.create_login(db=db, login=login, owner_id=user_id)

@app.get("/getLogins/", response_model=list[schemas.Login])
def read_logins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logins = crud.get_logins(db, skip=skip, limit=limit)
    return logins

@app.get("/getLoginByUser_ID/", response_model=list[schemas.Login])
def read_logins(user_id: int, db: Session = Depends(get_db)):
    logins = crud.get_logins_by_user_id(db, owner_id=user_id)
    return logins

@app.get("/login/validation")
def check_login(email: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    
    
    if user:
        raise HTTPException(status_code=400, detail="Email does not exist")


@app.post('/login_try')
async def login_try(request: Request):
 
    login_data = await request.json()
    username = login_data.get('username')
    password = login_data.get('password')

    if username.lower() == '' and password == '':

        return JSONResponse(content={'success': True}, status_code=200)
    else:

        raise HTTPException(status_code=401, detail='Authentication failed')
    
@app.post('/createFollower')
def create_follow(followee: int, owner_id: int, db: Session = Depends(get_db)):
    return crud.create_follow(db=db, followee_id=followee, follower_id=owner_id)

@app.get('/getAllFollowers')
def get_all_followers(followee: int, db: Session = Depends(get_db)):
    return crud.get_all_followers(db=db, id=followee)

@app.get('/readFollowers')
def number_of_followers(followee: int, db: Session = Depends(get_db)):
    return crud.get_number_of_followers(db=db, id=followee)

@app.get('/getAllFollowees')
def get_all_followees(user_id: int, db: Session = Depends(get_db)):
    return crud.get_all_followees(db=db, id=user_id)

@app.get('/readFollowees')
def number_of_followers(user_id: int, db: Session = Depends(get_db)):
    return crud.get_number_of_followees(db=db, id=user_id)

@app.post('/unfollowUser')
def unfollow(followee_id: int, user_id: int, db: Session = Depends(get_db)):
    return crud.unfollow(db=db, followee_id=followee_id, user_id=user_id)

@app.post('/cratePost')
def create_post(user_id: int, caption: str, db: Session = Depends(get_db)):#,photo_id: int, video_id: int):
    return crud.create_post(db=db, user_id=user_id, caption=caption)#, photo_id=photo_id, video_id=video_id)

@app.get('/getPosts')
def get_posts(user_id: int, db: Session = Depends(get_db)):
    return crud.get_all_posts(db=db, id=user_id)

@app.post('/deletePost')
def delete_post(post_id: int, db: Session = Depends(get_db)):
    return crud.delete_post(post_id=post_id, db=db)

@app.post('/createPostLike')
def create_post_like(user_id: int, post_id: int, db: Session = Depends(get_db)):
    return crud.create_post_like(user_id=user_id, post_id=post_id, db=db)

@app.get('/getPostLikeAmount')
def get_post_like_amount(post_id: int, db: Session = Depends(get_db)):
    return crud.get_post_like_amount(db=db, post_id=post_id)

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

# @app.get("/user_data")
# def get_all_users():
#     conn = sqlite3.connect(DBNAME)
#     c = conn.cursor()

#     c.execute('''CREATE TABLE IF NOT EXISTS testTable (name TEXT, number IINTEGER)''')
#     c.execute('''INSERT INTO testTable (name, number) VALUES ("John", 3)''')
#     c.execute('''SELECT * FROM testTable;''')
#     results = c.fetchall()

#     print(results)
    
#     conn.commit()
#     conn.close()

#     return results   

# @app.post("/dbTest")
# def testDB():
#     conn = sqlite3.connect(DBNAME)
#     c = conn.cursor()

#     c.execute('''CREATE TABLE IF NOT EXISTS testTable (name TEXT, number IINTEGER)''')
#     c.execute('''INSERT INTO testTable (name, number) VALUES ("John", 3)''')
#     c.execute('''SELECT * FROM testTable;''')
#     results = c.fetchall()
    
#     conn.commit()
#     conn.close()

#     return results

# @app.post("/createUser")
# def createUser(first_name, last_name , email, birthday, username):
#     conn = sqlite3.connect(DBNAME)
#     c = conn.cursor()

#     c.execute('''INSERT INTO users (first_name, last_name, email, birthday, username) VALUES ()''')

#     conn.commit()
#     conn.close()

