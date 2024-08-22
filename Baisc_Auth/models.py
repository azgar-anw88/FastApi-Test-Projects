from sqlalchemy import Column, Integer, String
from database import Base,engine

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    
Base.metadata.create_all(engine)