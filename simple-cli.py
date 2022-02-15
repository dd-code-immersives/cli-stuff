import argparse
from base64 import decode
from ctypes import resize
import random as rn

MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-'}

MORSE_SPECIAL = {'...---...': 'SOS'}

THREE_SPACES = 3*' '

def random_cli(num_one, num_two):

	print("Welcome to guess the number!")

	start_r = int(num_one)
	end_r = int(num_two)

	# generate the number 
	random_num = rn.randrange(start_r, end_r)
	print(f"Random number generated! Between the range of {start_r} and {end_r}")

	while True:
		try:
			guessed_num = int(input(f"\nPick a number between {start_r}-{end_r}:"))
		except Exception as e:
			raise e

		if guessed_num != random_num:
			print(f"\nNope, it was: {random_num}")
			break
		else:
			print("\nThat's right!")
			break  

def num_series(num_str):
	num = int(num_str)
	return print('\n'+"{0:.2f}".format(sum([1/(3*n+1) for n in range(num)]))+'\n')

def sq_everything(num):
	return print("\n"+"".join([str(int(i)**2) for i in num])+"\n")

def decode_morse(message):
	res = ""
	message = message.split(THREE_SPACES)
	for code in message:
		'''
		Checks if the message falls under specail service codes.
		If not, starts decoding.
		'''
		if code in MORSE_SPECIAL:
			res += MORSE_SPECIAL[code]+" "
		else:
			word = code.split()
			for letter in word:
				for key,value in MORSE_CODE_DICT.items():
					if letter == value:
						res += key
			res += " "
	return '\n'+res+'\n'

def encode_morse(clear_text):
	res = ""
	for word in clear_text.split():
		word = word.upper()
		if word in MORSE_SPECIAL.values():
			for key in MORSE_SPECIAL.keys():
				if MORSE_SPECIAL[key] == word:
					res += key+THREE_SPACES
		else:
			for letter in word:
				for key, value in MORSE_CODE_DICT.items():
					if key == letter:
						res += value+" "
			res += THREE_SPACES
	return '\n'+res+'\n'

def main(var_x, var_y):
	while True:
		random_cli(var_x, var_y)
		response = input("\nPlay again? y/n   ").lower()
		if response ==  "n" or response == 'no':
			print("\ngoodbye!\n")
			break


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--number', action='store', type=str)
	parser.add_argument("--nrange",action='store', help="specifies max number", nargs=2, type=int, default=[1,5])
	parser.add_argument('--sq_em', action='store', nargs=1)
	parser.add_argument('--demorse', action='store')
	parser.add_argument('--enmorse', action='store')
	args = parser.parse_args()
	if args.number:
		num_series(args.number)
	elif args.sq_em:
		sq_everything(args.sq_em[0])
	elif args.demorse:
		print(decode_morse(args.demorse))
	elif args.enmorse:
		print(encode_morse(args.enmorse))
	else:
		main(args.nrange[0], args.nrange[1])

