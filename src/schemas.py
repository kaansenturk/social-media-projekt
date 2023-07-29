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


class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

class LoginBase(BaseModel):
    pass

class LoginCreate(LoginBase):
    pass

class Login(LoginBase):
    id: int
    user_id: int
    login_time: str
    ip: str

    class Config:
        orm_mode = True
