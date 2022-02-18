from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, VARCHAR, Integer, Column, Date, Float
import os

PATH = os.getcwd()
DATA_PATH = PATH+"/data"
os.chdir(DATA_PATH)

Base = declarative_base()

engine = create_engine("sqlite:///contact_book.db")

Base.metadata.bind = engine
Base.metadata.create_all(engine)
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

class Users(Base):
    __tablename__ = 'user_info'
    '''id,first_name,last_name,email,phone_number,city'''

    id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR(30), nullable=False)
    last_name = Column(VARCHAR(30), nullable=False)
    email = Column(VARCHAR(50), nullable=False)
    phone_number = Column(VARCHAR(20), nullable=True)
    city = Column(VARCHAR(50), nullable=False)

class User_Pswd(Base):
    __tablename__ = "user_password"

    user_id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR(30), nullable=False)
    last_name = Column(VARCHAR(30), nullable=False)
    pswd = Column(VARCHAR(20), nullable=False)