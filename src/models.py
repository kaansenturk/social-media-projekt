from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, LargeBinary
from sqlalchemy.orm import relationship

# import Base to create classes that inherit from it
from database import Base

# Class to create db tables named "users"
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")
    # posts = relationship("Post", back_populates="owner")

    # def verify_password(self, password):
    #     pwhash = bcrypt.hashpw(password, self.password)
    #     return self.password == pwhash

# Class for sqlalchemy to create db tables named "items"
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

# Class for sqlalchemy to create db tables named "login"
class Login(Base):
    __tablename__="login"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, index=True)
    location = Column(String, index=True)
    login_time = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

# Class for sqlalchemy to create db tables named "post"
class Post(Base):
    __tablename__="post"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(String, index=True)
    location = Column(String, index=True)
    caption = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    photo_id = Column(Integer, ForeignKey("photos.id"))
    video_id = Column(Integer, ForeignKey("videos.id"))

class Post_Likes(Base):
    __tablename__="post_likes"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("post.id"))

class Comments(Base):
    __tablename__="comment"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(String, index=True)
    comment_text = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("post.id"))

# Class for sqlalchemy to create db tables named "comment_likes"
class Comment_Likes(Base):
    __tablename__="comment_likes"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    comment_id = Column(Integer, ForeignKey("comment.id"))

# Class for sqlalchemy to create db tables named "photos"
class Photos(Base):
    __tablename__="photos"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(String, index=True)
    title = Column(String, index=True)
    image_data = Column(LargeBinary)

# Class for sqlalchemy to create db tables named "videos"
class Videos(Base):
    __tablename__="videos"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(String, index=True)
    video_url = Column(String, index=True)
    size = Column(Integer, index=True)
    post_id = Column(Integer, ForeignKey("post.id"))

# Class for sqlalchemy to create db tables named "follows"
class Follows(Base):
    __tablename__="follows"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(String, index=True)
    followee_id = Column(Integer, ForeignKey("users.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

