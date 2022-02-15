
"""
implement morse code
words and phrases
""" 


SPECIAL_CODES = {'···−−−···': 'SOS'}
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

THREE_SPACES = " " * 3



def lookup_morse_char(ch):
     for k,v in MORSE_CODE_DICT.items(): 
          if ch == v:
               return k
     return str()


def encode_morse(message="HEY JUDE"):
     morse_wds = []
     for wd in message.split():
          morse_msg = str()
          for ch in wd:
               morse_msg += MORSE_CODE_DICT[ch]
               morse_msg += " "
          morse_wds.append(morse_msg.strip())

     return THREE_SPACES.join(morse_wds)

     

def decode_morse(message):

     """
     decodes morse into clear text
     """
     if message in SPECIAL_CODES:

          return SPECIAL_CODES[message]

     decrypted_wds = []
     for wd in message.split(THREE_SPACES):
          str_ = "".join([ lookup_morse_char(ch) for ch in wd.split()])
          decrypted_wds.append(str_)
     return " ".join(decrypted_wds)


if __name__ == '__main__':
     #print(decode_morse('.... . -.--   .--- ..- -.. .'))
     encoded = encode_morse('HEY JUDE')
     print(f"Encoded message: {encoded}")
     print(f"Decoded Message: {decode_morse(encoded)}")

