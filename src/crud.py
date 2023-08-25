from http.client import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData, Table, LargeBinary
from datetime import datetime
from fastapi import UploadFile
import socket
import models, schemas, database
import geocoder

# method to delete the table "users"
def delete_users(db: Session):
    metadata = MetaData()
    table = Table("users", metadata, autoload_with=database.engine)
    table.drop(database.engine)
    metadata.create_all(database.engine)

# method to delete a single user in table "users"
def delete_user(db: Session, user_id: int):
    metadata = MetaData()
    #user = Table("users", metadata, autoload_with=database.engine).delete().where(id=user_id)
    table = Table("users", metadata, autoload_with=database.engine)
    
    table.drop(database.engine)
    metadata.create_all(database.engine)

# method to get a user from table "users" by id
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()
# method to get a user from table "users" by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# method to get all data from table "users" (max. 100 entries)
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# method to create a user into table "users"
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, password=user.password, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_by_username(db: Session, username: str, updated_data: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    
    if db_user:
        # Update attributes
        db_user.username = updated_data.username
        db_user.email = updated_data.email
        db_user.password = updated_data.password
        db_user.is_active = updated_data.is_active
        
        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        raise HTTPException(status_code=404, detail="User not found")
# method
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

# method 
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# method to create a login entry into table "login"
def create_login(db: Session, login: schemas.LoginCreate, owner_id: int):
    now = datetime.now()
    current_date = now.strftime("%D %H:%M:%S")
    hostname=socket.gethostname() 
    IPAddr=socket.gethostbyname(hostname)
    g = geocoder.ip('me')
    db_login = models.Login(login_time=current_date, location="lat:" + str(g.lat) + ", lng:" + str(g.lng), user_id=owner_id, ip=hostname + " " + IPAddr)
    db.add(db_login)
    db.commit()
    db.refresh(db_login)
    return db_login

# method to return all logins in table "login" (max. 100 entries)
def get_logins(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Login).offset(skip).limit(limit).all()

# method to return all logins of a user in table "login"
def get_logins_by_user_id(db: Session, owner_id: int):
    return db.query(models.Login).filter(models.Login.user_id == owner_id).all()

# method to validate login
def check_login(db: Session, user: schemas.User, pw: str):
    pass

# method to create a follow
def create_follow(db: Session, followee_id: int, follower_id: int):
    now = datetime.now()
    current_date = now.strftime("%D %H:%M:%S")
    db_follow = models.Follows(created_at=current_date, followee_id=followee_id, user_id=follower_id)
    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)
    return db_follow

# method to return all logins of a user in table "login"
def get_logins_by_user_id(db: Session, owner_id: int):
    return db.query(models.Login).filter(models.Login.user_id == owner_id).all()

# method to return the number of followers from a user
def get_number_of_followers(db: Session, id: int):
    return len(db.query(models.Follows).filter(models.Follows.followee_id == id).all())

# method to return all followers from a user
def get_all_followers(db: Session, id: int):
    return db.query(models.Follows).filter(models.Follows.followee_id == id).all()

# method to return the number of followees from a user
def get_number_of_followees(db: Session, id: int):
    return len(db.query(models.Follows).filter(models.Follows.user_id == id).all())

# method to return all followees from a user
def get_all_followees(db: Session, id: int):
    return db.query(models.Follows).filter(models.Follows.user_id == id).all()

# method to unfollow a user
def unfollow(db: Session, followee_id: int, user_id: int):
    follow_entry = db.query(models.Follows).filter(models.Follows.followee_id == followee_id, models.Follows.user_id == user_id).first()
    if follow_entry:
        db.delete(follow_entry)
        db.commit()
        print("Follow deleted successfully.")
    else:
        print("Follow not found.")
    db.close()

#method to create a post
def create_post(db: Session, user_id: int, caption: str):#, photo_id: int, video_id: int):
    now = datetime.now()
    current_date = now.strftime("%D %H:%M:%S")
    g = geocoder.ip('me')
    db_post = models.Post(user_id=user_id, created_at=current_date, location="lat:" + str(g.lat) + ", lng:" + str(g.lng), caption=caption)#, photo_id=photo_id, video_id=video_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# method to return all posts from a user
def get_all_posts(db: Session, id: int):
    return db.query(models.Post).filter(models.Post.user_id == id).all()

# method to delete a post
def delete_post(db: Session, post_id):
    post_entry = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post_entry:
        db.delete(post_entry)
        db.commit()
        print("Post deleted successfully.")
    else:
        print("Post not found.")
    db.close()
    return post_entry

# method to create a post_like_entry
def create_post_like(db: Session, user_id: int, post_id: int):
    now = datetime.now()
    current_date = now.strftime("%D %H:%M:%S")
    db_post_like = models.Post_Likes(user_id=user_id, created_at=current_date, post_id=post_id)
    db.add(db_post_like)
    db.commit()
    db.refresh(db_post_like)
    return db_post_like

# method to get post_like amount
def get_post_like_amount(db: Session, post_id: int):
    return len(db.query(models.Post_Likes).filter(models.Post_Likes.post_id == post_id).all())

# method to create a comment
def create_comment(db: Session, post_id: int, user_id: int, comment_text: str):
    now = datetime.now()
    current_date = now.strftime("%D %H:%M:%S")
    db_comment = models.Comments(comment_text=comment_text, user_id=user_id, created_at=current_date, post_id=post_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# method to get comments of post
def get_comments_of_post(db: Session, post_id: int):
    return db.query(models.Comments).filter(models.Comments.post_id == post_id).all()

# method to create a comment like
def create_comment_like(db: Session, comment_id: int, user_id):
    now = datetime.now()
    current_date = now.strftime("%D %H:%M:%S")
    db_comment_like = models.Comment_Likes(user_id=user_id, created_at=current_date, comment_id=comment_id)
    db.add(db_comment_like)
    db.commit()
    db.refresh(db_comment_like)
    return db_comment_like

# method to upload a phtoto
async def upload_photo(db: Session, title: str, image_data: UploadFile):
    file_content = await image_data.read()
    #file_content_data = await file_content
    now = datetime.now()
    current_date = now.strftime("%D %H:%M:%S")
    async def store_data():
        db_photo = models.Photos(created_at=current_date, title=title, image_data=file_content)
        db.add(db_photo)
        db.commit()
        db.refresh(db_photo)

    await store_data()
    return {"message": "File uploaded and stored."}

# method to read a photo entry
def read_photo(db: Session, id: int):
    return db.query(models.Photos).filter(models.Photos.id == id).first()

def create_message(db: Session, sender_id: int, receiver_id: int, content: str):
    now = datetime.now()
    current_date = now.strftime("%D %H:%M:%S")
    db_message = models.Message(sender=sender_id, receiver=receiver_id, content=content, created_at=current_date)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_user_messages(db: Session, user: str):
    user_messages = db.query(models.Message).filter(models.Message.sender == user or models.Message.receiver == user).all()
    return user_messages

