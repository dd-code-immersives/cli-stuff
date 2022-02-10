

""" 
Functions for counting letters, vowels, etc.

"""

class LetterCounts():

    VOWELS = 'aeiou'

    def __init__(self, letters):

        self.letters = letters

    def count_letters(self):
        """ 

        counts letters , 
        returns dictionary of counts
        """
        unique_letters = {}
        for lett in self.letters:
            if lett not in unique_letters:
                unique_letters[lett] = 1
            else:
                unique_letters[lett] +=1
        return unique_letters, 'something else'


    def count_vowels(self):
        """ 

        counts vowels , 
        returns dictionary of counts
        """
        unique_vowels = {}
        for lett in self.letters:
            if lett in self.VOWELS:
                if lett not in unique_vowels:
                    unique_vowels[lett] = 1
                else:
                    unique_vowels[lett] +=1
        value_sum = sum(unique_vowels.values())
        return value_sum


    def count_consonants(self):
        unique_consonant = {}
        for lett in self.letters:
            if lett not in self.VOWELS:
                if lett not in unique_consonant:
                    unique_consonant[lett] = 1
                else:
                    unique_consonant[lett] +=1
        value_sum = sum(unique_consonant.values())
        return value_sum