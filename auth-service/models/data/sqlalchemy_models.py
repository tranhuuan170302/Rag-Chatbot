from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from db_config.sqlalchemy_connect import Base

class Signup(Base):
    __tablename__ = 'signup'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=False, index=False)
    email = Column(String, unique=True, index=False)
    password = Column(String, unique=False, index=False)

class Login(Base): 
    __tablename__ = "login"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=False, index=False)
    password = Column(String, unique=False, index=False)
    passphrase = Column(String, unique=False, index=False)
    approved_date = Column(Date, unique=False, index=False)

    # Mối quan hệ với Profile
    profiles = relationship('Profile', back_populates="login")  # Trỏ đến Profile

class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, unique=False, index=False)
    lastname = Column(String, unique=False, index=False)
    age = Column(Integer, unique=False, index=False)
    login_id = Column(Integer, ForeignKey('login.id'), unique=False, index=False)  # Định nghĩa ForeignKey
    status = Column(Integer, unique=False, index=False)

    # Mối quan hệ với Login
    login = relationship('Login', back_populates="profiles")  # Trỏ đến Login
