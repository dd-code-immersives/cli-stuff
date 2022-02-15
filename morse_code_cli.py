import argparse

from pprint import pprint 
from morse_code import MorseCode, SPECIAL_CODES

def run_cli():

	parser = argparse.ArgumentParser()

	parser.add_argument("message", help="pass a string")

	# create exclusive group for encode/decode
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-d','--decode', action='store_true', help="This option tells the user to decode the message")
	group.add_argument('-e','--encode', action='store_true', help="This option tells the user to encode the message")
	

	parser.add_argument('-s', '--special_codes', action='store_true', help="Helps us view all the special morse messages")
	args = parser.parse_args()

	morse = MorseCode(args.message)

	if args.special_codes:
		print("SPECIAL MORSE CODES:", end="\n")
		print("-------------------------",)
		pprint(SPECIAL_CODES)
		print("-------------------------",)

	if args.decode:
		msg = morse.decode_morse()
		print(f"Decoded Message: {msg}")

	elif args.encode:
		msg = morse.encode_morse()
		print(f"Encoded Message: {msg}")


if __name__ == '__main__':
	run_cli()
