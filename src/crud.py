from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData, Table
from datetime import datetime
import socket
import models, schemas, database

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

# method to get a user from table "users" by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# method to get all data from table "users" (max. 100 entries)
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# method to create a user into table "users"
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

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
    db_login = models.Login(login_time=current_date, user_id=owner_id, ip=hostname + " " + IPAddr)
    db.add(db_login)
    db.commit()
    db.refresh(db_login)
    return db_login

# method to return all logins in table "login" (max. 100 entries)
def get_logins(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Login).offset(skip).limit(limit).all()

# method to validate login
def check_login(db: Session, user: schemas.User, pw: str):
    

    
