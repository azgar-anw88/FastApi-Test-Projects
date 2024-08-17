from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import ItemCreate, Item as ItemSchema
from crud import get_item, get_items, create_item, update_item, delete_item
from auth import create_jwt_token, get_current_user
from datetime import timedelta
from pydantic import BaseModel

app = FastAPI()

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

class LoginData(BaseModel):
    username: str
    password: str

@app.post("/login")
def login_for_access_token(login_data: LoginData):
    user = authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_jwt_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/items/", response_model=ItemSchema)
def create_item_endpoint(item: ItemCreate, db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    return create_item(db=db, item=item)

@app.get("/items/{item_id}", response_model=ItemSchema)
def read_item(item_id: int, db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    db_item = get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.get("/items/", response_model=list[ItemSchema])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    return get_items(db, skip=skip, limit=limit)

@app.put("/items/{item_id}", response_model=ItemSchema)
def update_item_endpoint(item_id: int, item: ItemCreate, db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    db_item = update_item(db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.delete("/items/{item_id}", response_model=ItemSchema)
def delete_item_endpoint(item_id: int, db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    db_item = delete_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
