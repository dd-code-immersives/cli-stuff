"""
File contains all functions and logics for contact-book-cli
"""
import os
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contact_book_models import Users, User_Pswd

PATH = os.getcwd()

class FileHandler():
    '''
    Reads and writes to files
    '''

    def __init__(self, infile):
        '''Initialized the class with the input file'''
        self.infile = infile
        self.df_ = DfConstructor().csv_to_df(self.infile)

    def user_search(self, args_lst):
        '''Filters the entire file/df through the key words passed (e.g., email or last_name'''
        if 'id' in args_lst:
            i_d = int(args_lst[args_lst.index('id') + 1])
            msg = f"\n{'_'*5} Showing result for ID {i_d}. \
                All other key words were ignored {'_'*5}\n"
            res = print(msg, self.df_.loc[i_d, :])
        else:
            # for num in range(len(args_lst)):
            for num, arg in enumerate(args_lst):
                if num % 2 == 0:
                    # if args_lst[num] != 'id':
                    #     self.df_ = self.df_[self.df_[args_lst[num]]
                    #                       == args_lst[num + 1]]
                    if arg != 'id':
                        self.df_ = self.df_[self.df_[arg]
                                            == args_lst[num + 1]]
            if not self.df_.empty:
                res = print(self.df_)
            else:
                res = print("No User Found")
        return res

    def update(self, args_lst):
        '''Filters the df by the user's id. Make changes to only one user at a time'''
        columns = self.df_.columns
        if 'id' in args_lst:
            i_d = int(args_lst[args_lst.index('id') + 1])
            if isinstance(i_d, int):
                for num in range(0, len(args_lst), 2):
                    if args_lst[num] != 'id':
                        if args_lst[num] in columns:
                            self.df_.loc[i_d, args_lst[num]] = args_lst[num + 1]
                        else:
                            raise Exception(
        f"{'*'*5} Passed arguments contain faulty column name(s) update cancelled {'*'*5}"
                                )
                print(self.df_.loc[i_d, :])
                if self.__confirmation():
                    self.df_.to_csv(self.infile)
                    print(f"\n{'_'*10} Update Complete {'_'*10}\n")
                else:
                    raise Exception(f"\n{'*'*10} Update Cancelled {'*'*10}\n")
            else:
                raise Exception(f"\n{'*'*10} ID data type != int {'*'*10}\n")
        else:
            raise Exception(
                f"\n{'*'*10} Need ID Number to Make Changes {'*'*10}\n")

    def browse(self, nums):
        '''
        Uses the integers passed as the user id or \
            range of id to return user(s) with the id matches the integer(s)
        '''
        cnt = len(nums)
        if cnt < 2:
            # '''When one number digit is passed'''
            print(self.df_.loc[nums[0], :])
        elif cnt == 2:
            # '''When two numbers are pasased'''
            print(self.df_.loc[nums[0]:nums[1], :])
        elif cnt > 2:
            # '''When three numbers are pasased'''
            print(self.df_.loc[nums[0]:nums[1]:nums[2], :])

    def __confirmation(self):
        res = input("Save Changes? type yes or no: ")
        return res.lower() == 'yes'


class DataBase:
    '''
    Establishes db from specified file(s)
    Contains user_search and user_update functions.
    '''

    def __init__(self, infile='CONTACT_DATA.csv',
                 pswdfile='contact_passwords.csv'):
        '''
        Initialize the file and data_base.
        '''
        self.infile = infile
        self.pswdfile = pswdfile
        self.__setup_sqlalchemy_db()

    def user_search(self, args):
        '''
        Makes sql query using the parameters passed.
        Converts the result in to pd Series for easier view before returning.
        '''
        data = self.session.query(Users)
        msg = ""
        for num, arg in enumerate(args):
            if num % 2 == 0:
                # key = args[num]
                key = arg
                value = args[num + 1]
                if key == 'id':
                    msg = f"\n{'_'*5} Showing result for ID {value}. \
                        All other key words were ignored {'_'*5}\n\n"
                    res = DfConstructor().sql_pd_series_single(
                        data.filter(
                            Users.id == value).all()[0],
                        index=[
                            'user_id',
                            'fisrt_name',
                            'last_name',
                            'email',
                            'phone_number',
                            'city'])
                    print(msg, res)
                else:
                    if key == 'first_name':
                        data = data.filter(Users.first_name == value)
                    elif key == 'last_name':
                        data = data.filter(Users.last_name == value)
                    elif key == 'email':
                        data = data.filter(Users.email == value)
                    elif key == 'phone_number':
                        data = data.filter(Users.phone_number == value)
                    elif key == 'city':
                        data = data.filter(Users.city == value)
        if self.__authenticator(data):
            # res = self.__sql_pd_series_multi(data, \
            # index=['user_id', 'fisrt_name', 'last_name', 'email',
            # 'phone_number', 'city'])
            res = DfConstructor().sql_pd_df(
                data,
                cols=[
                    'user_id',
                    'fisrt_name',
                    'last_name',
                    'email',
                    'phone_number',
                    'city'],
                set_index='user_id')
        else:
            res = "No Users Found"
        return print(msg, res, '\n')

    def user_update(self, args):
        '''
        Makes sql query based on the id passed.
        Make updates in accordance to the cloumn(s) and value(s) passed.
        Converts the result in to pd Series for easier view before returning.
        '''
        res = ''
        if 'id' in args:
            i_d = args[args.index('id') + 1]
            data = self.session.query(Users).filter(Users.id == i_d)
            secured_data = self.session.query(
                User_Pswd).filter(User_Pswd.user_id == i_d)
            # '''
            # Check if the given id exists in both tables \
            #     one containing user info and the other containing pswd
            # '''
            if self.__authenticator(
                    data) and self.__authenticator(secured_data):
                org = DfConstructor().sql_pd_series_single(
                    data.all()[0],
                    index=[
                        'user_id',
                        'fisrt_name',
                        'last_name',
                        'email',
                        'phone_number',
                        'city'])
                for num, arg in enumerate(args):
                    if num % 2 == 0:
                        key = arg
                        value = args[num + 1]
                        if key == 'first_name':
                            data.update({'first_name': value})
                            secured_data.update({'first_name': value})
                        elif key == 'last_name':
                            data.update({'last_name': value})
                            secured_data.update({'last_name': value})
                        elif key == 'email':
                            data.update({'email': value})
                        elif key == 'phone_number':
                            data.update({'email': value})
                        elif key == 'city':
                            data.update({'city': value})
            else:
                res = print("No User Found. Invalid User ID")

            # '''Puts the data after update into pd Series \
            #     for easier viewing and prints "before and after"'''
            new = DfConstructor().sql_pd_series_single(
                data.all()[0],
                index=[
                    'user_id',
                    'fisrt_name',
                    'last_name',
                    'email',
                    'phone_number',
                    'city'])
            print(f"\n{'*'*10} Original {'*'*10}\n", org, '\n')
            print(f"\n{'*'*10} Updated {'*'*10}\n", new, '\n')

            # '''Asks for confirmation. Anything by "yes" will abort the update'''
            if self.__confirmation():
                if self.__update_executer(i_d):

                    # '''If matched, changes will be commited and session will close'''
                    res = self.__success()
                else:
                    cnt = 1
                    while cnt < 6:
                        print(
                            (f"\n{'*'*10} You've Entered Incorrect Password {'*'*10}\n"))
                        if self.__update_executer(i_d):
                            return self.__success()
                        cnt += 1
                    # '''When attemp limit is reached, the process is automatically cancelled'''
                res = \
                    f"\n{'*'*5} Too Many Times Attempts, Update Cancelled {'*'*5}\n"
            else:
                res = f"\n{'*'*10} Update Cancelled {'*'*10}\n"
        else:
            res = Exception(
            f"\n{'*'*10} Need User ID to Make Changes {'*'*10}\n")
        return print(res)

    def __setup_sqlalchemy_db(self, engine_path="sqlite:///contact_book.db"):
        '''
        Setup sqlalchemy defaults
        '''
        os.chdir(PATH)
        self.base = declarative_base()
        self.engine = create_engine(engine_path)
        self.base.metadata.bind = self.engine
        self.base.metadata.create_all(self.engine)
        self.dbsession = sessionmaker(bind=self.engine)
        self.session = self.dbsession()

        try:
            # '''Check to see if there's data base and/or table exists'''
            self.__authenticator(Users)
        except BaseException:
            # '''If the table or the data base exists, creates one'''
            df_user = pd.read_csv(self.infile, index_col=['id'])
            df_user.to_sql(
                "user_info",
                con=self.engine,
                if_exists="append",
                index="id")
        try:
            # '''Check to see if there's data base and/or table exists'''
            self.__authenticator(User_Pswd)
        except BaseException:
            # '''If the table or the data base exists, creates one'''
            df_pswd = pd.read_csv(self.pswdfile, index_col=['user_id'])
            df_pswd.to_sql(
                "user_password",
                con=self.engine,
                if_exists="append",
                index="user_id")

    def __authenticator(self, arg):
        '''
        Checks if the query returns any data
        '''
        if isinstance(arg, sqlalchemy.orm.query.Query):
            res = arg.first()
        elif isinstance(arg, sqlalchemy.orm.decl_api.DeclarativeMeta):
            res = self.session.query(arg).first()
        return res

    def __update_executer(self, user_id):
        '''
        Asks the user for confirmation and verifies password
        '''
        in_pswd = input("Please Enter User Password: ")
        pswd = self.session.query(User_Pswd).filter(
            User_Pswd.user_id == user_id).all()[0].pswd
        return in_pswd == pswd

    def __success(self):
        return self.session.commit(), print(
            f"\n{'_'*10} Update Complete {'_'*10}\n")

    def __confirmation(self):
        res = input("Save Changes? type yes or no: ")
        return res.lower() == 'yes'

class DfConstructor:
    '''
    Creates pandas dataframe
    '''
    def csv_to_df(self, file):
        '''Reads the file and returns a pd DataFrame'''
        return pd.read_csv(file, index_col=['id'])

    def sql_pd_df(self, query, **kwargs):
        '''Return a pd.DataFrame'''
        res = []
        data = query.all()
        for datum in data:
            res.append([datum.id, datum.first_name, datum.last_name,
                       datum.email, datum.phone_number, datum.city])
        return pd.DataFrame(res, columns=kwargs['cols']).set_index(
            kwargs['set_index'])

    def sql_pd_series_multi(self, query, **kwargs):
        '''Returns a list of series. Use when there are multiple data sets'''
        res = []
        data = query.all()
        for item in data:
            datum = item
            res.append(pd.Series([datum.id,
                                  datum.first_name,
                                  datum.last_name,
                                  datum.email,
                                  datum.phone_number,
                                  datum.city],
                                 index=kwargs['index']))
        return res

    def sql_pd_series_single(self, datum, **kwargs):
        '''Return a single pd.Series. Use when there is only one set of data'''
        return pd.Series([datum.id,
                          datum.first_name,
                          datum.last_name,
                          datum.email,
                          datum.phone_number,
                          datum.city],
                         index=kwargs['index'])
