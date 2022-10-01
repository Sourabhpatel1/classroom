from sqlalchemy import Column, String, Integer, DateTime, Boolean
from datetime import datetime

# Base class from which the models will inherit
from database import Base


class User(Base):
    
    __tablename__ = "users"

    # User Information

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow())

    # User Roles

    is_admin = Column(Boolean, default=False)
    is_creator = Column(Boolean, default=False)