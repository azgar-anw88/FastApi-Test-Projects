from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()

def authentication_user(credentials:HTTPBasicCredentials = Depends(security)):
    if credentials.username == 'testuser' and credentials.password == 'testpass':
        return True
    
    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    
@app.get("/basic-auth")
def get_basic_auth(credentials:HTTPBasicCredentials=Depends(authentication_user)):
    return {"message":"Authenticated Successfully"}


from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Item
from schemas import ItemCreate, Item
from crud import get_item, get_items, create_item, update_item, delete_item

app = FastAPI()
auth = HTTPBasic()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def authentication_user(credentials: HTTPBasicCredentials = Depends(auth)):
    if credentials.username == 'azgar' and credentials.password == 'azgar123':
        return True
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

@app.post("/items/", response_model=Item)
def create_item_endpoint(item: ItemCreate, db: Session = Depends(get_db), _: bool = Depends(authentication_user)):
    return create_item(db=db, item=item)

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, db: Session = Depends(get_db), _: bool = Depends(authentication_user)):
    db_item = get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.get("/items/", response_model=list[Item])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), _: bool = Depends(authentication_user)):
    return get_items(db, skip=skip, limit=limit)

@app.put("/items/{item_id}", response_model=Item)
def update_item_endpoint(item_id: int, item: ItemCreate, db: Session = Depends(get_db), _: bool = Depends(authentication_user)):
    db_item = update_item(db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.delete("/items/{item_id}", response_model=Item)
def delete_item_endpoint(item_id: int, db: Session = Depends(get_db), _: bool = Depends(authentication_user)):
    db_item = delete_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
