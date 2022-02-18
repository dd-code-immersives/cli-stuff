'''
1. Write a CLI that interacts with a csv file.
2. Allows you to save contact information in the CSV file.

-Allow user to look up a contact by email, first/last name or phone number.
-Allow user to update an entry in the file
-Allow user to display all email addresses, first names, last names etc.

examples:

Show al the emails in the csv file:

IN: python3 contact-book.py --infile contacts.csv --all-emails
OUT:

user1@gmail.com
user2@yahoo.com
...

IN: python3 contact-book.py --infile contacts.csv, \
--user user1@gmail.com --first-name Dom  --update NAME


# get all first names that start with capital A
python3 contact-book-cli.py data/CONTACT_DATA.csv -af | sort | grep -e "^A"

#get last 5 entries
python3 contact-book-cli.py data/CONTACT_DATA.csv -fe first_name | sort | tail

#get first 5 entries
python3 contact-book-cli.py data/CONTACT_DATA.csv -fe first_name | sort | head

NOTE_: separate the CLI from the logic
'''

import argparse
import pathlib
from contact_book_1_0 import FileHandler, DataBase


def contact_book_cli():
    """
    cli for contact_book.py
    """
    parser = argparse.ArgumentParser(
        description="Tool for managing CSV file of Contact Data")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--infile', type=pathlib.Path,
                        help="Input file name/path is required")
    parser.add_argument('--search', action='store', nargs='+', help="When an ID number is given,\
		will ignore the rest of the arguments")
    parser.add_argument('--update', action='store', nargs='+', help='Requires ID number \
		and will not run without one')
    parser.add_argument('--browse', action='store', type=int, nargs='+',
                        help="Single number returns df.loc[num, :], \
			two-three numberes returns df.loc[num_1:num_2:num_3(default=1), :]")
    group.add_argument('--sql', action='store_true')
    parser.add_argument('--user_search', action='store', nargs='+',
                        help="When an ID number is given, will ignore the rest of the arguments")
    parser.add_argument('--user_update', action='store', nargs='+', help='Requires User ID \
		and will not run without one')
    parser.add_argument('--test', action='store_true')
    args = parser.parse_args()

    if args.infile:
        data_file = FileHandler(args.infile)
        # Check to see args.search has, at least, one Column - Key Word pair
        if args.search:
            if len(args.search) > 1:
                data_file.user_search(args.search)
            else:
                raise Exception(
                    "Need Column - Key Word Pair to Seach. No Column - Key Word Pair Found")
        elif args.update:
            if len(args.update) > 1:
                data_file.update(args.update)
            else:
                raise Exception("Need Column - New Information Pair to Update,\
					No Column - New Information Pair Found")
        elif args.browse:
            data_file.browse(args.browse)
    elif args.sql:
        d_b = DataBase()
        if args.user_search and len(args.user_search) > 1:
            d_b.user_search(args.user_search)
        elif args.user_update and len(args.user_update) > 2:
            d_b.user_update(args.user_update)
        # else:
        #     raise Exception("Need Column-New Information or Column-Key Word Pair")



if __name__ == "__main__":
    contact_book_cli()
