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

# class Transactions(Base):
#     __tablename__ = "patient_transactions"

#     id = Column(Integer, primary_key=True)
#     emp_id = Column(VARCHAR(20), nullable=False)
#     trans_id = Column(VARCHAR(15), nullable=False)
#     procedure_date = Column(Date, nullable=False)
#     medical_code = Column(VARCHAR(10), nullable=False)
#     procedure_price = Column(Float, nullable=False)