
import argparse
import csv

from contact_book import ContactBook
"""
Write a CLI that interacts with a csv file, that allows you to save contact information in the CSV file. 

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

IN: python3 contact-book.py --infile contacts.csv --user user1@gmail.com --first-name Dom  --update NAME


NOTE: separate the CLI from the logic 


python3 contact-book.py --infile contacts.csv --feature email user_name



-s, --show FIELD


	show columns


	i.e. -s email user_name

-f, --filter dictionary of values

	show entries by filtering values 

	-f {'username': 'John'}


FIELD:
[id,first_name,last_name,email,phone_number,city | all to show all]

"""

parser = argparse.ArgumentParser(description="Tool for managing CSV file of Contact Data")
parser.add_argument('infile', action='store', type=argparse.FileType('r'), help="CSV contact data file")
parser.add_argument('-o','--outfile', action='store', type=argparse.FileType('w'), help="CSV contact data file", default="out.csv")
parser.add_argument('-s', '--show', action='store', nargs='+' ,help="Input fields you want to show i.e. email, user_name")
parser.add_argument('-f', '--filter', action='store',help="filter by fields")
parser.add_argument('-u', '--update', action='store', nargs=2,help="update fields")
args = parser.parse_args()

if args.infile:
	
	if args.show:
		cb = ContactBook(args.infile, fields_=args.show)
	else:
		cb = ContactBook(args.infile)

	if args.filter:
		cb.filter_entries(args.filter)


	if args.update:
		cb.update_entry(args.update[0], args.update[1])
	
	


