import pandas as pd

"""
File contains all functions and logics for contact-book-cli
"""

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
                res = df
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
