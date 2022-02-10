import argparse
from word_info import LetterCounts

def word_info_cli():

	"""
	word info CLI 
	"""
	colors = ['red', 'blue', 'green', 'purple', 'yellow']
	
	parser = argparse.ArgumentParser()   
	parser.add_argument('word', action='store', help='Word for Analysis')
	parser.add_argument('-a','--all', action='store_true', help="Run all available analysis on string WORD")
	parser.add_argument('-lc','--letter_count', action= 'store_true', help="count number of letters in WORD")
	parser.add_argument('-vc','--vowel_count', action= 'store_true', help="count number of vowels in WORD")
	parser.add_argument('-cc','--consonants_count', action= 'store_true', help="count number of consonants in WORD")
	args = parser.parse_args()

	lcounts = LetterCounts(args.word)

	if args.all:

		print(f'letter counts{ lcounts.count_letters() }')
		print(f'The number of vowels is { lcounts.count_vowels() }')
		print(f'The number of consonants is { lcounts.count_consonants() }')

	if args.letter_count and not args.all:
	    print(f'letter counts{ lcounts.count_letters() }')
	    
	if args.vowel_count and not args.all:
	    print(f'The number of vowels is { lcounts.count_vowels() }')

	if args.consonants_count and not args.all:
	    print(f'The number of consonants is { lcounts.count_consonants() }')

if __name__ == '__main__':
	word_info_cli()