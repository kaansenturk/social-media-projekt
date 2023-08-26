from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    username: str
    password: str


class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []
    # posts: list[Post] = []

class LoginBase(BaseModel):
    login_time: str
    ip: str
    location: str

class LoginCreate(LoginBase):
    pass

class Login(LoginBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
class LoginRequest(BaseModel):
    user: str
    password: str
    
class FollowBase(BaseModel):
    login_time: str
    ip: str
    

class FollowCreate(FollowBase):
    pass

class Follow(FollowBase):
    id: int
    user_id: int
    followee_id: int

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    created_at: str
    location: str
    caption: str
    photo_id: int
    video_id: int

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: str
    email: str