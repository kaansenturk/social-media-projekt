from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

class Login(Base):
    __tablename__="login"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, index=True)
    login_time = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

class Post(Base):
    __tablename__="post"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(String, index=True)
    location = Column(String, index=True)
    caption = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    photo_id = Column(Integer, ForeignKey("photos.id"))
    video_id = Column(Integer, ForeignKey("videos.id"))

#class Post_Likes(Base):
    #__tablename__="post_likes"

    #created_at = Column(String, index=True)
    #user_id = Column(Integer, ForeignKey("users.id"))
    #post_id = Column(Integer, ForeignKey("post.id"))

class Comments(Base):
    __tablename__="comment"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(String, index=True)
    comment_text = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("post.id"))

#class Comment_Likes(Base):
    #__tablename__="comment_likes"

    #created_at = Column(String, index=True)
    #user_id = Column(Integer, ForeignKey("users.id"))
    #comment_id = Column(Integer, ForeignKey("comment.id"))

class Photos(Base):
    __tablename__="photos"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(String, index=True)
    photo_url = Column(String, index=True)
    size = Column(Integer, index=True)
    post_id = Column(Integer, ForeignKey("post.id"))

class Videos(Base):
    __tablename__="videos"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(String, index=True)
    video_url = Column(String, index=True)
    size = Column(Integer, index=True)
    post_id = Column(Integer, ForeignKey("post.id"))

class Follows(Base):
    __tablename__="follows"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(String, index=True)
    followee_id = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

