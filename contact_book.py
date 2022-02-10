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
            msg = f"{'*'*5} Showing result for ID {i_d}. All other key words were ignored {'*'*5}\n"
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
                            print("Chages to ID Prohibitted")
                print(df.loc[i_d, :])
                confirmation = input("Save changes? type yes or no: ")
                if confirmation.lower() == 'yes':
                    df.to_csv(self.infile)
                else:
                    return print("Update Cancelled")
            else:
                raise Exception("ID data type != int")
        else:
            raise Exception("Need ID Number to Make Changes")
