import argparse
import random as rn


def random_cli():

	# build CLI 
	parser = argparse.ArgumentParser(description="Guess The Number game, try to guess the number between a given range")
	#parser.add_argument("-n","--number",action='store', type=int, help="generates n random numbers", default=0)
	parser.add_argument("--nrange",action='store', help="specifies max number", nargs=2, type=int, default=[1,5])
	args = parser.parse_args()

	print("Welcome to guess the number!")

	start_r = args.nrange[0]
	end_r = args.nrange[1]

	# generate the number 
	random_num = rn.randrange(args.nrange[0], args.nrange[1])
	print(f"Random number generated! Between the range of {start_r} and {end_r}")

	while True:
		try:
			guessed_num = int(input(f"Guess number between {start_r}-{end_r}:"))
		except Exception as e:
			raise e

		if guessed_num != random_num:
			print("Sorry try again!")
		else:
			print("you guessed correctly!")
			break  


def main():
	while True:
		random_cli()
		response = input("Play again? y/n")
		if response ==  "n":
			print("goodbye!")
			break 




if __name__ == '__main__':
	main()

