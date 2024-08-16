from sqlalchemy.orm import Session
from models import Item
from schemas import ItemCreate

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: ItemCreate):
    db_item = Item(name=item.name, email=item.email)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: ItemCreate):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db_item.name = item.name
        db_item.email = item.email
        db.commit()
        db.refresh(db_item)
        return db_item
    return None

def delete_item(db: Session, item_id: int):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return db_item
    return None
