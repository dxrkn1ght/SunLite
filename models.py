from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime
Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String, default='')
    lang = Column(String(2), default='uz')
    balance = Column(Integer, default=0)
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    kind = Column(String, default='rank')
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(Text, default='')
class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Integer, nullable=False)
    status = Column(String, default='pending')
    type = Column(String, default='topup')
    meta = Column(Text, default='')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    nickname = Column(String, nullable=False)
    status = Column(String, default='pending')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
