import argparse
import sys
import csv
import random as rn


def obfuscate_cli():


	# set up CLI
	parser = argparse.ArgumentParser()
	#parser.add_argument('--infile', action='store')
	parser.add_argument('--infile', type=argparse.FileType('r'))
	parser.add_argument('--outfile', type=argparse.FileType('w'))

	args = parser.parse_args()
	if args.infile and args.outfile:
		data = csv.DictReader(args.infile)
		for line in data:
			new_row = ",".join([line['id'], line['username'], obfuscate_password(line['password']), line['email'], '\n'])
			args.outfile.write(new_row)

def obfuscate_password(pw):
	return ''.join(['*' for i in range(rn.randint(3, 20))])
	

def main():
	obfuscate_cli()


if __name__ == '__main__':
	main()