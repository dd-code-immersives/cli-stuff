
"""
Logic for Contact Book


"""

import csv
import json
import os


class ContactBook:


	def __init__(self, infile, outfile=None,fields_=['id','first_name','last_name','email','phone_number','city']):
		self.infile = infile 
		self.outfile = outfile
		self.data = self.__load_csv_data()
		self.fields = fields_

	def show_columns(self):
		for row in self.data:
			print(self.__create_display_row(row))


	def filter_entries(self, filter_str):

		filter_dict = self.__convert_str_to_dict(filter_str)
		
		for row in self.data:
			if all(row[k] == v for k, v in filter_dict.items()):
				print(self.__create_display_row(row))


	def update_entry(self, id_,filter_str):

		filter_dict = self.__convert_str_to_dict(filter_str)

		for row in self.data:

			if row["id"] == id_:
				for k,v in filter_dict.items():
					row[k] = v

		self.show_columns()

		if self.outfile:
			self.__save_file()


	# Private Methods			
	def __load_csv_data(self):
		return csv.DictReader(self.infile)

	def __create_display_row(self, row):
		return ",".join([row[key] for key in self.fields])

	def __convert_str_to_dict(self, filter_dict):
		return json.loads(filter_dict)		

	def __save_file(self):	
		writer = csv.writer(self.outfile)
		for row in self.data:
			writer.writerow(row)
		
		orginal_file = self.infile.name
		os.rm(self.infile.name)
		os.rename(self.outfile.name, self.infile.name)



if __name__ == '__main__':


	with open('data/CONTACT_DATA.csv', 'r') as infile:
		cb = ContactBook(infile)
		for row in cb.data:
			print(row)