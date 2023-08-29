from fastapi import FastAPI, HTTPException, Depends, Request, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import logging
from starlette.responses import RedirectResponse
import sqlite3
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from fastapi.responses import JSONResponse
import base64
import bcrypt


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
@app.post("/deleteUser/{username}")
def delete_user(username: str, db: Session = Depends(get_db)):
    db_delete_user = crud.delete_user(db, username)
    if db_delete_user:
        raise HTTPException(status_code=400, detail="Not Found")

# post method to create a user into table "users"
@app.post("/createUser/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/get_user/{username}")
async def get_user(username: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username)
    return user

@app.put("/update_user/{username}")
async def update_user(username: str, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user_by_username(db, username, user_update)
    return {"message": "User updated successfully"}

@app.get("/getUsers/", response_model=list[schemas.User])
def read_users(query: str = '', limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, query=query, limit=limit)
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

@app.post("/login/")
def user_login(login_request: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, login_request.user)
    
    if not user:
        raise HTTPException(status_code=400, detail="Email does not exist")

    if not  bcrypt.checkpw(login_request.password.encode('utf-8'), user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    # Creating a login record after successful authentication
    login_record = crud.create_login(db, user.id, user.id)  # Removed schemas.LoginCreate()

    if not login_record:
        raise HTTPException(status_code=500, detail="Could not create login record")
    
    return {
        "username": user.username,
        "email": user.email,
        "id": user.id,
        "is_active": user.is_active
    }


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
def create_follow(follower_data: schemas.CreateFollower, db: Session = Depends(get_db)):
    try:
        return crud.create_follow(db=db, followee_id=follower_data.followee, follower_id=follower_data.owner_id)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

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

@app.post('/createComment')
def create_comment(user_id: int, post_id: int, comment_text: str, db: Session = Depends(get_db)):
    return crud.create_comment(db=db, post_id=post_id, user_id=user_id, comment_text=comment_text)

@app.get('/getCommentsOfPost')
def get_comments_of_post(post_id: int, db: Session = Depends(get_db)):
    return crud.get_comments_of_post(post_id=post_id, db=db)

@app.post('/createCommentLike')
def create_comment_like(comment_id: int, user_id: int, db: Session = Depends(get_db)):
    return crud.create_comment_like(comment_id=comment_id, db=db, user_id=user_id)

@app.post("/uploadPhoto")
async def upload_photo(title: str = Form(...), image: UploadFile = File(...), db: Session = Depends(get_db)):
    return await crud.upload_photo(title=title, image_data=image, db=db)

@app.get('/getPhoto')
def read_photo(id: int, db: Session = Depends(get_db)):
    return crud.read_photo(id=id, db=db)

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.post("/send_message/")
async def send_message(sender_id: int, receiver_id: int, content: str, db: Session = Depends(get_db)):
    db_message = crud.create_message(db, sender_id, receiver_id, content)
    return {"message": "Message sent successfully"}

@app.get("/get_messages/{logged_user}/{recipient}")
async def get_messages(logged_user: str, recipient: str, db: Session = Depends(get_db)):
    conversation = crud.get_user_messages(db, logged_user, recipient)
    return conversation

@app.get("/get_user_location/{user_id}")
def get_user_location(user_id: int, db: Session = Depends(get_db)):
    login_record = db.query(models.Login).filter(models.Login.user_id == user_id).order_by(models.Login.login_time.desc()).first()
    
    if not login_record:
        raise HTTPException(status_code=404, detail="No login records found for this user.")
        
    return {"location": login_record.location}
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

