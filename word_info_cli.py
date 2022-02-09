import argparse
from word_info import LetterCounts

def word_info_cli():

	"""
	word info CLI 
	"""
	
	parser = argparse.ArgumentParser()   
	parser.add_argument('word', action='store', help='Word for Analysis')
	parser.add_argument('--letter_count', action= 'store_true', help="count number of letters")
	parser.add_argument('--vowel_count', action= 'store_true', help="count number of vowels")
	parser.add_argument('--consonants_count', action= 'store_true', help="count number of consonants")
	args = parser.parse_args()

	lcounts = LetterCounts(args.word)

	if args.letter_count:
	    print(f'letter counts{ lcounts.count_letters() }')
	    
	if args.vowel_count:
	    print(f'The number of vowels is { lcounts.count_vowels() }')

	if args.consonants_count:
	    print(f'The number of consonants is { lcounts.count_consonants() }')

if __name__ == '__main__':
	word_info_cli()