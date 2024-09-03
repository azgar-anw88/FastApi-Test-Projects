from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import ItemCreate, Item as ItemSchema
from crud import get_item, get_items, create_item, update_item, delete_item
from auth import create_jwt_token, get_current_user
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

auth_type = os.getenv("AUTH_TYPE", "jwt_auth") 
auth_type = os.getenv("AUTH_TYPE", "basic_auth")

if auth_type == "basic_auth":
    security = HTTPBasic()
elif auth_type == "jwt_auth":
    security = OAuth2PasswordBearer(tokenUrl="token")
else:
    raise ValueError("Invalid AUTH_TYPE in configuration")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

users_db = {
    "azgar": {
        "username": "azgar",
        "password": "azgar123"
    }
}

def authenticate_user(username: str, password: str):
    user = users_db.get(username)
    if user and user["password"] == password:
        return user
    return None

@app.post("/token", include_in_schema=False)
def login_for_access_token(formdata: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(formdata.username, formdata.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_jwt_token(
        data={"sub": user["username"]},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user_depends(credentials: HTTPBasicCredentials = Depends(security), token: str = Depends(security)):
    if auth_type == 'basic_auth':
        user = authenticate_user(credentials.username, credentials.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"username": credentials.username}
    elif auth_type == 'jwt_auth':
        return get_current_user(token)
    else:
        raise HTTPException(status_code=500, detail="Invalid AUTH_TYPE in configuration")


@app.post("/items/", response_model=ItemSchema)
def create_item_endpoint(item: ItemCreate, db: Session = Depends(get_db), _: dict = Depends(get_current_user_depends)):
    return create_item(db=db, item=item)

@app.get("/items/{item_id}", response_model=ItemSchema)
def read_item(item_id: int, db: Session = Depends(get_db), _: dict = Depends(get_current_user_depends)):
    db_item = get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.get("/items/", response_model=list[ItemSchema])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), _: dict = Depends(get_current_user_depends)):
    return get_items(db, skip=skip, limit=limit)

@app.put("/items/{item_id}", response_model=ItemSchema)
def update_item_endpoint(item_id: int, item: ItemCreate, db: Session = Depends(get_db), _: dict = Depends(get_current_user_depends)):
    db_item = update_item(db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.delete("/items/{item_id}", response_model=ItemSchema)
def delete_item_endpoint(item_id: int, db: Session = Depends(get_db), _: dict = Depends(get_current_user_depends)):
    db_item = delete_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

