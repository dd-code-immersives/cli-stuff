from re import T
from contact_book_models import *
import pandas as pd
import csv, os
from sqlalchemy.engine.base import Connection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, VARCHAR, Integer, Column, and_, Date, desc, asc, extract, Float, text
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql import func

"""
File contains all functions and logics for contact-book-cli
"""
PATH = os.getcwd()
# DATA_PATH = PATH+"/data/"

class DataFrameConstructor:
    
    def sql_pd_df(query, **kwargs):
        '''Return a pd.DataFrame'''
        res = []
        data = query.all()
        for num in range(len(data)):
            datum = data[num]
            res.append([datum.id, datum.first_name, datum.last_name, datum.email, datum.phone_number, datum.city])
        return pd.DataFrame(res, columns=kwargs['cols']).set_index(kwargs['set_index'])
    
    def sql_pd_series_multi(query, **kwargs):
        '''Returns a list of series. Use when there are multiple data sets'''
        res = []
        data = query.all()
        for num in range(len(data)):
            datum = data[num]
            res.append(pd.Series([datum.id, datum.first_name, datum.last_name, datum.email, datum.phone_number, datum.city], index=kwargs['index']))
        return res

    def sql_pd_series_single(datum, **kwargs):
        '''Return a single pd.Series. Use when there is only one set of data'''
        return pd.Series([datum.id, datum.first_name, datum.last_name, datum.email, datum.phone_number, datum.city], index=kwargs['index'])


class FileHandler():

    def __init__(self, infile):
        '''Initialized the class with the input file'''
        self.infile = infile
    
    def csv_to_df(self):
        '''Reads the file and returns a pd DataFrame'''
        return pd.read_csv(self.infile, index_col=['id'])
        
    def user_search(self, args_lst):
        '''Filters the entire file/df through the key words passed (e.g., email or last_name'''
        df = self.csv_to_df()
        if 'id' in args_lst:
            i_d = int(args_lst[args_lst.index('id')+1])
            msg = f"\n{'_'*5} Showing result for ID {i_d}. All other key words were ignored {'_'*5}\n"
            res = print(msg,df.loc[i_d, :])
        else:
            for num in range(len(args_lst)):
                if num%2 == 0:
                    if args_lst[num] != 'id':
                        df = df[df[args_lst[num]] == args_lst[num+1]]
            if not df.empty:
                res = print(df)
            else:
                res = print("No User Found")
        return res
    
    def update(self, args_lst):
        '''Filters the df by the user's id. Make changes to only one user at a time'''
        df = self.csv_to_df()
        if [True for i in args_lst if not i in df.columns]:
            raise Exception(f"{'*'*5} Passed arguments contain faulty column name(s) update cancelled {'*'*5}")
        '''Saves the 'id' value'''
        if 'id' in args_lst:
            i_d = int(args_lst[args_lst.index('id')+1])
            if type(i_d) == int:
                '''Avoid running the following code when the data type of i_d was altered for unknown & unexected reasons: safety precaution'''
                for num in range(len(args_lst)):
                    if num%2 == 0:
                        if args_lst[num] != 'id':
                            df.loc[i_d, args_lst[num]] = args_lst[num+1]
                        else:
                            print(f"{'*'*5} Chages to ID Prohibitted {'*'*5}")
                print(df.loc[i_d, :])
                confirmation = input("Save changes? type yes or no: ")
                if confirmation.lower() == 'yes':
                    df.to_csv(self.infile)
                    print(f"\n{'_'*10} Update Complete {'_'*10}\n")
                else:
                    return print(f"\n{'*'*10} Update Cancelled {'*'*10}\n")
            else:
                raise Exception(f"\n{'*'*10} ID data type != int {'*'*10}\n")
        else:
            raise Exception(f"\n{'*'*10} Need ID Number to Make Changes {'*'*10}\n")

    def browse(self, nums):
        df = self.csv_to_df()
        cnt = len(nums)
        if cnt < 2:
            '''When one number digit is passed'''
            print(df.loc[nums[0], :])
        elif cnt == 2:
            '''When two numbers are pasased'''
            print(df.loc[nums[0]:nums[1], :])
        elif cnt > 2:
            '''When three numbers are pasased'''
            print(df.loc[nums[0]:nums[1]:nums[2], :])

class DataBase:

    def __init__(self):
        '''
        Initialize the file and data_base.
        '''
        self.infile = 'CONTACT_DATA.csv'
        os.chdir(PATH)
        self.Base = declarative_base()
        self.engine = create_engine("sqlite:///contact_book.db")
        self.Base.metadata.bind = self.engine
        self.Base.metadata.create_all(self.engine)
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()
        try:
            '''Check to see if there's data base and/or table exists'''
            self.session.query(Users).first()
        except:
            '''If no data base exists, creates one'''
            df = pd.read_csv(self.infile, index_col=['id'])
            df.to_sql("user_info", con=engine, if_exists="append", index="id")

    def user_search(self, args):
        '''
        
        '''
        data = self.session.query(Users)
        msg = ""
        for num in range(len(args)):
            if num%2 == 0:
                key = args[num]
                value = args[num+1]
                if key == 'id':
                    msg = f"\n{'_'*5} Showing result for ID {value}. All other key words were ignored {'_'*5}\n\n"
                    res = DataFrameConstructor.sql_pd_series_single(data.filter(Users.id == value).all()[0], index=['user_id', 'fisrt_name', 'last_name', 'email', 'phone_number', 'city'])
                    return print(msg, res)
                elif key == 'first_name':
                    data = data.filter(Users.first_name == value)
                elif args[num] == 'last_name':
                    data = data.filter(Users.last_name == value)
                elif args[num] == 'email':
                    data = data.filter(Users.email == value)
                elif args[num] == 'phone_number':
                    data = data.filter(Users.phone_number == value)
                elif args[num] == 'city':
                    data = data.filter(Users.city == value)
        if data.first():
            # res = DataFrameConstructor.sql_pd_series_multi(data, index=['user_id', 'fisrt_name', 'last_name', 'email', 'phone_number', 'city'])
            res = DataFrameConstructor.sql_pd_df(data, cols=['user_id', 'fisrt_name', 'last_name', 'email', 'phone_number', 'city'], set_index='user_id')
        else:
            res = "No Users Found"
        return print(msg, res, '\n')
    
    def user_update(self, args):
        res = ''
        if 'id' in args:
            i_d = args[args.index('id')+1]
            data = self.session.query(Users).filter(Users.id == i_d)
            if data.first():
                org = DataFrameConstructor.sql_pd_series_single(data.all()[0], index=['user_id', 'fisrt_name', 'last_name', 'email', 'phone_number', 'city'])
                for num in range(len(args)):
                    if num%2 == 0:
                        key = args[num]
                        value = args[num+1]
                        if key == 'first_name':
                            data.update({'first_name': value})
                        elif key == 'last_name':
                            data = data.update({'last_name': value})
                        elif key == 'email':
                            data = data.update({'email': value})
                        elif key == 'phone_number':
                            data = data.update({'email': value})
                        elif key == 'city':
                            data = data.update({'city': value})
            else:
                res = print("No User Found. Invalid User ID")
            new = DataFrameConstructor.sql_pd_series_single(data.all()[0], index=['user_id', 'fisrt_name', 'last_name', 'email', 'phone_number', 'city'])
            print(f"\n{'*'*10} Original {'*'*10}\n", org, '\n')
            print(f"\n{'*'*10} Updated {'*'*10}\n", new, '\n')
            confirmation = input("Save Changes? type yes or no: ")
            if confirmation.lower() == 'yes':
                res = self.session.commit(), print(f"\n{'_'*10} Update Complete {'_'*10}\n")
            else:
                return print(f"\n{'*'*10} Update Cancelled {'*'*10}\n")
        else:
            raise Exception(f"\n{'*'*10} Need User ID to Make Changes {'*'*10}\n")
        return res

