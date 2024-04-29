from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base  = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id  = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    phone = Column(String)
    email = Column(String, unique=True)
    amount = Column(Integer,default=0)
    # account = relationship("UserAccount", back_populates="owner")
 
    __table_args__ = (
        UniqueConstraint('email'),  # Unique constraint on email column
    )
 
# class UserAccount(Base):
#     __tablename__ = "user_account"
#     id = Column(Integer,primary_key=True,index=True)
#     username = Column(String)
#     amount = Column(Integer,default=0)
#     description = Column(String, index=True,nullable=True)
#     user_id  = Column(Integer, ForeignKey("user.id"))
 
#     owner = relationship("User",back_populates=("account"))
 

class Wallet(Base):
    __tablename__ = "wallet"
    id = Column(Integer,primary_key=True,index=True)
    transfer_to = Column(String)
    amount=Column(Integer)
    sender_id=Column(Integer, ForeignKey("user.id"))
    receiver_id=Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
    
class ActivityTracker(Base):
    __tablename__ = "activity_tracker"
    id = Column(Integer,primary_key=True,index=True)
    transfer_type = Column(String)
    description = Column(String)
    sender_to=Column(Integer, ForeignKey("user.id"))
    received_by=Column(Integer, ForeignKey("user.id"))
    transaction_time = Column(DateTime, default=datetime.utcnow)
    
    sender = relationship("User", foreign_keys=[sender_to])
    receiver = relationship("User", foreign_keys=[received_by])
    
    
    
    
