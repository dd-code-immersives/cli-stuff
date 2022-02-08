import argparse
import random as rn

# DEFAULTS
START_RANGE = 1 
END_RANGE = 5 


def random_cli():

	# build CLI 
	parser = argparse.ArgumentParser(description="Random Number Generator")
	parser.add_argument("-n","--number",action='store', type=int, help="generates n random numbers")
	parser.add_argument("--nrange",action='store', help="specifies max number", nargs=2, type=int)
	args = parser.parse_args()


	# handle user input from CLI
	if args.nrange:
		START_RANGE = args.nrange[0]
		END_RANGE  = args.nrange[1]

	if args.number > 1:
		for i in range(args.number):
			print(rn.randrange(START_RANGE, END_RANGE)) 
	else:
		print(rn.randrange(START_RANGE,END_RANGE))


def main():
	random_cli()

if __name__ == '__main__':
	main()

