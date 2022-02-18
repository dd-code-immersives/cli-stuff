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

class MorseCode:

    def __init__(self, msg):
        self.msg = msg

    def _morse_finder(self, string):
        for k, v in MORSE_CODE_DICT.items():
            if string == v:
                return k

    def _morse_special(self, message):
        try:
            res = MORSE_SPECIAL.get(message)
        except:
            res = False
        return res


    def decode_morse(self):
        res = ""
        message = self.msg.split(THREE_SPACES)
        for code in message:
            '''
            Checks if the message falls under specail service codes.
            If not, starts decoding.
            '''
            if self._morse_special(code):
                res += self._morse_special(code)+" "
            else:
                word = code.split()
                for letter in word:
                    res += self._morse_finder(letter)
                res += " "
        return '\n'+res+'\n'

    def encode_morse(self):
        res = ""
        for word in self.msg.split():
            word = word.upper()
            if word in MORSE_SPECIAL.values():
                for key in MORSE_SPECIAL.keys():
                    if MORSE_SPECIAL[key] == word:
                        res += key+THREE_SPACES
            else:
                for letter in word:
                        res += MORSE_CODE_DICT[letter]+" "
                res += THREE_SPACES
        return '\n'+res+'\n'