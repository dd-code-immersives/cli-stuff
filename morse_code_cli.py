import argparse

from morse_code import decode_morse, encode_morse

def run_cli():

	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-d','--decode', action='store', help="This option tells the user to decode the message")
	group.add_argument('-e','--encode', action='store', help="This option tells the user to encode the message")
	args = parser.parse_args()

	if args.decode:
		msg = decode_morse(args.decode)
		print(f"Decoded Message: {msg}")

	elif args.encode:
		msg = encode_morse(args.encode)
		print(f"Encoded Message: {msg}")




if __name__ == '__main__':
	run_cli()
