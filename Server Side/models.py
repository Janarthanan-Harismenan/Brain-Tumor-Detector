from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    password = Column(String)

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    image_data = Column(LargeBinary)  # Store image as binary data
    probability = Column(Float)
    tumor_detected = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship("User")
