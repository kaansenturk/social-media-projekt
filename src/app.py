from fastapi import FastAPI, HTTPException, Depends, Request, Form, File, UploadFile, Body
from fastapi.middleware.cors import CORSMiddleware
import logging
from starlette.responses import RedirectResponse
import sqlite3
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from fastapi.responses import JSONResponse, StreamingResponse
import base64
import bcrypt
from typing import Optional
from io import BytesIO



logging.basicConfig(filename='../logs/api.log', encoding='utf-8',format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

logger=logging.getLogger("fast_api_logger")

logger.setLevel(logging.INFO)

#
models.Base.metadata.create_all(bind=engine)

#
app = FastAPI()

origins = ["*"]


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
    if db_delete_user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return {"message": "User deleted successfully", "status_code": 200}

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

    if not bcrypt.checkpw(login_request.password.encode('utf-8'), user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    print(login_request.location)
    # Creating a login record after successful authentication
    login_record = crud.create_login(db, user.id, user.id, login_request.location)  # Removed schemas.LoginCreate()

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

@app.post('/createFollower')
def create_follow(follower_data: schemas.CreateFollower, db: Session = Depends(get_db)):
    try:
        return crud.create_follow(db=db, followee_id=follower_data.followee, follower_id=follower_data.owner_id)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

@app.get('/getAllFollowers/{user_id}')
def get_all_followers(user_id: int, db: Session = Depends(get_db)):
    return crud.get_all_followers(db=db, id=user_id)

@app.get('/readFollowers/{user_id}')
def number_of_followers(user_id: int, db: Session = Depends(get_db)):
    return crud.get_number_of_followers(db=db, id=user_id)

@app.get('/getAllFollowees/{user_id}')
def get_all_followees(user_id: int, db: Session = Depends(get_db)):
    return crud.get_all_followees(db=db, id=user_id)

@app.get('/readFollowees/{user_id}')
def number_of_followers(user_id: int, db: Session = Depends(get_db)):
    return crud.get_number_of_followees(db=db, id=user_id)

@app.post('/unfollowUser')
def unfollow(followee_id: int, user_id: int, db: Session = Depends(get_db)):
    return crud.unfollow(db=db, followee_id=followee_id, user_id=user_id)

@app.post("/create_post/")
async def create_post_endpoint(
    caption: str, 
    user_id: int, 
    image_data: Optional[UploadFile] = None, 
    video_data: Optional[UploadFile] = None,
    db: Session = Depends(get_db)
):
    photo_id = None
    video_id = None
    
    if image_data:
        photo_id = await crud.upload_photo(db, caption, image_data, user_id)
        
    if video_data:
        # Assuming you would have a similar crud function for uploading video
        video_id = await crud.upload_video(db, video_data, user_id)
    
    post =   crud.create_post(db, user_id, caption, photo_id, video_id)
    
    return {"message": "Post created", "post": post}

@app.get('/getPosts')
def get_posts(user_id: int, db: Session = Depends(get_db)):
    return crud.get_all_posts(db=db, id=user_id)

@app.get('/getPost/{post_id}')
def get_post(post_id: int, db: Session = Depends(get_db)):
    return crud.get_post(db=db, id=post_id)

@app.post('/deletePost')
def delete_post(post_id: int, db: Session = Depends(get_db)):
    return crud.delete_post(post_id=post_id, db=db)

@app.post('/createPostLike/{post_id}/{user_id}')
def create_post_like(user_id: int, post_id: int, db: Session = Depends(get_db)):
    return crud.create_post_like(user_id=user_id, post_id=post_id, db=db)

@app.get('/getPostLikes/{post_id}')
def get_post_likes(post_id: int, db: Session = Depends(get_db)):
    return crud.get_post_likes(db=db, post_id=post_id)

@app.get('/getPostLikeAmount/{post_id}')
def get_post_like_amount(post_id: int, db: Session = Depends(get_db)):
    return crud.get_post_like_amount(db=db, post_id=post_id)

@app.get('/isPostLiked/{post_id}/{user_id}')
def is_post_liked(post_id: int, user_id: int, db: Session = Depends(get_db)):
    return crud.is_post_liked(db=db, post_id=post_id, user_id=user_id)

@app.post('/unlikePost/{post_id}/{user_id}')
def unlike_post(post_id: int, user_id: int, db: Session = Depends(get_db)):
    return crud.unlike_post(db=db, post_id=post_id, user_id=user_id)

@app.post('/createComment/{user_id}/{post_id}/{comment_text}')
def create_comment(user_id: int, post_id: int, comment_text: str, db: Session = Depends(get_db)):
    return crud.create_comment(db=db, post_id=post_id, user_id=user_id, comment_text=comment_text)

@app.get('/getComment/{comment_id}')
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    return crud.get_comment(db=db, id=comment_id)

@app.get('/getCommentsOfPost/{post_id}')
def get_comments_of_post(post_id: int, db: Session = Depends(get_db)):
    return crud.get_comments_of_post(post_id=post_id, db=db)

@app.get('/getCommentsOfPostAmount/{post_id}')
def get_comments_of_post(post_id: int, db: Session = Depends(get_db)):
    return crud.get_comments_of_post_amount(post_id=post_id, db=db)

@app.post('/createCommentLike/{comment_id}/{user_id}')
def create_comment_like(comment_id: int, user_id: int, db: Session = Depends(get_db)):
    return crud.create_comment_like(comment_id=comment_id, db=db, user_id=user_id)

@app.get('/getCommentLikes/{comment_id}')
def get_post_likes(comment_id: int, db: Session = Depends(get_db)):
    return crud.get_comment_likes(db=db, comment_id=comment_id)

@app.get('/getCommentLikeAmount/{comment_id}')
def get_post_like_amount(comment_id: int, db: Session = Depends(get_db)):
    return crud.get_comment_like_amount(db=db, comment_id=comment_id)

@app.get('/isCommentLiked/{comment_id}/{user_id}')
def is_post_liked(comment_id: int, user_id: int, db: Session = Depends(get_db)):
    return crud.is_comment_liked(db=db, comment_id=comment_id, user_id=user_id)

@app.post('/unlikeComment/{comment_id}/{user_id}')
def unlike_comment(comment_id: int, user_id: int, db: Session = Depends(get_db)):
    return crud.unlike_comment(db=db, comment_id=comment_id, user_id=user_id)

@app.post("/upload_photo/")
async def upload_photo_endpoint(title: str, image_data: UploadFile, user_id: int, db: Session = Depends(get_db)):
    return await crud.upload_photo(db, title, image_data, user_id)

@app.get("/getPhoto")
def read_photo(id: int, db: Session = Depends(get_db)):
    photo = crud.read_photo(id=id, db=db)
    if photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    return StreamingResponse(BytesIO(photo.image_data), media_type="image/png")

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

@app.put("/users/{username}/update_password/")
def update_password(username: str, password_update: schemas.PasswordUpdate = Body(...), db: Session = Depends(get_db)):
    try:
        return crud.update_user_password(db, username, password_update.current_password, password_update.new_password)
    except HTTPException as e:
        return {"error": e.detail}
    
@app.post("/set_profile_picture/")
def set_profile_picture(username: str, photo_id: int, db: Session = Depends(get_db)):
    return crud.set_user_profile_picture(db, username, photo_id)
