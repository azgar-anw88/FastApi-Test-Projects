from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    email: str

    class Config:
        from_attributes = True

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True
