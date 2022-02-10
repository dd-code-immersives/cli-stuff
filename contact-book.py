
import argparse
import csv
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


"""

parser = argparse.ArgumentParser(description="Tool for managing CSV file of Contact Data")
parser.add_argument('-in','--infile', action='store', type=argparse.FileType('r'))
args = parser.parse_args()

if args.infile:
	data = csv.reader(args.infile)
	for row in data:
		print(row)