
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, MetaData, Table, LargeBinary, delete
from datetime import datetime
from fastapi import UploadFile, HTTPException
import socket
import models, schemas, database
import geocoder
import bcrypt
from typing import Optional

# method to delete the table "users"
def delete_users(db: Session):
    metadata = MetaData()
    table = Table("users", metadata, autoload_with=database.engine)
    table.drop(database.engine)
    metadata.create_all(database.engine)

# method to delete a single user in table "users"
def delete_user(db: Session, username: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    # Delete all follow relationships where the user is a follower or a followee 
    follow_entries_follower = db.query(models.Follows).filter(models.Follows.user_id == user.id).all()
    follow_entries_followee = db.query(models.Follows).filter(models.Follows.followee_id == user.id).all()

    for entry in follow_entries_follower:
        db.delete(entry)

    for entry in follow_entries_followee:
        db.delete(entry)

    db.delete(user)
    db.commit()
    return "User and associated follow relationships deleted successfully"

# method to get a user from table "users" by id
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()
# method to get a user from table "users" by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# method to get all data from table "users" (max. 100 entries)
def get_users(db: Session, query: str = '', limit: int = 100):
    users = db.query(models.User).filter(models.User.username.like(f"%{query}%")).limit(limit).all()
    return [u.__dict__ for u in users]

# method to create a user into table "users"
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.User(email=user.email, password=hashed_password, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return schemas.User.from_orm(db_user).dict()

def update_user_by_username(db: Session, username: str, updated_data: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    
    if db_user:
        if updated_data.username:
            db_user.username = updated_data.username
        if updated_data.email:
            db_user.email = updated_data.email

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
def create_login(db: Session, login: schemas.LoginCreate, owner_id: int, location: dict):
    now = datetime.now()
    current_date = now
    hostname=socket.gethostname() 
    IPAddr=socket.gethostbyname(hostname)
    db_login = models.Login(
        login_time=current_date, 
        location=location,
        user_id=owner_id
    )
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
    # Check if both users exist
    follower = db.query(models.User).filter(models.User.id == follower_id).first()
    followee = db.query(models.User).filter(models.User.id == followee_id).first()

    if not follower or not followee:
        raise HTTPException(status_code=400, detail="User not found.")
    
    now = datetime.now()
    current_date = now.strftime("%D %H:%M:%S")
    db_follow = models.Follows(created_at=current_date, followee_id=followee_id, user_id=follower_id)
    
    try:
        db.add(db_follow)
        db.commit()
        db.refresh(db_follow)
        return db_follow
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="You are already following this user.")

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
def create_post(db: Session, user_id: int, caption: str, photo_id: Optional[int] = None, video_id: Optional[int] = None):
    # Generate current date
    now = datetime.now()
    current_date = now.strftime("%D %H:%M:%S")
    
    # Get location data
    g = geocoder.ip('me')
    location = f"lat:{g.lat}, lng:{g.lng}"
    
    # Create Post
    db_post = models.Post(
        created_at=current_date,
        location=location,
        caption=caption,
        user_id=user_id,
        photo_id=photo_id,
        video_id=video_id
    )
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    return db_post

# method to return all posts from a user
def get_all_posts(db: Session, id: int):
    return db.query(models.Post).filter(models.Post.user_id == id).all()

# method to return all posts from a user
def get_post(db: Session, id: int):
    return db.query(models.Post).filter(models.Post.id == id).first()

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

def is_post_liked(db: Session, post_id: int, user_id: int):
    response = db.query(models.Post_Likes).filter(models.Post_Likes.post_id == post_id, models.Post_Likes.user_id == user_id).first()
    if(response):
        return True
    else:
        return False

def unlike_post(db: Session, post_id: int, user_id: int):
    response = db.query(models.Post_Likes).filter(models.Post_Likes.post_id == post_id, models.Post_Likes.user_id == user_id).first()
    if response:
        db.delete(response)
        db.commit()
        print("Unliked Post successfully.")
    else:
        print("Post Like not found.")
    db.close()

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

# method to get comments of post amount
def get_comments_of_post_amount(db: Session, post_id: int):
    return len(db.query(models.Comments).filter(models.Comments.post_id == post_id).all())

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
async def upload_photo(db: Session, title: str, image_data: UploadFile, user_id: int):
    file_content = await image_data.read()
    now = datetime.now()
    current_date = now.strftime("%D %H:%M:%S")

    db_photo = models.Photos(created_at=current_date, title=title, image_data=file_content, user_id=user_id)
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)

    return db_photo.id

# method to read a photo entry
def read_photo(db: Session, id: int):
    return db.query(models.Photos).filter(models.Photos.id == id).first()

# method to create a message entry
def create_message(db: Session, sender_id: int, receiver_id: int, content: str):
    now = datetime.now()
    current_date = now.strftime("%D %H:%M:%S")
    db_message = models.Message(sender_id=sender_id, receiver_id=receiver_id, content=content, created_at=current_date)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_user_messages(db: Session, logged_user: str, recipient: str):
    
    conversation = db.query(models.Message).filter(
        (models.Message.sender_id == logged_user) & (models.Message.receiver_id == recipient) |
        (models.Message.sender_id == recipient) & (models.Message.receiver_id == logged_user)
    ).all()
    
    return conversation

# method to update a user's password
def update_user_password(db: Session, username: str, current_password: str, new_password: str):
 
    db_user = get_user_by_username(db, username)
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    current_password_bytes = current_password.encode('utf-8')
    stored_password_bytes = db_user.password if isinstance(db_user.password, bytes) else db_user.password.encode('utf-8')
    
    if bcrypt.checkpw(current_password_bytes, stored_password_bytes):

        hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        db_user.password = hashed_new_password
        db.commit()
        db.refresh(db_user)
        return {"message": "Password updated successfully"}
    else:
        raise HTTPException(status_code=400, detail="Incorrect current password")
# Method to set the profile picture of a user, set the relationship between foto and user
def set_user_profile_picture(db: Session, username: str, photo_id: int):

    db_user = db.query(models.User).filter(models.User.username == username).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_photo = db.query(models.Photos).filter(models.Photos.id == photo_id).first()

    if not db_photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    db_user.photo_id = photo_id

    db.commit()

    db.refresh(db_user)
    
    return db_user
