import unicodedata
import string
from vigenere import Vigenere
import cProfile

def unit_test():
    key_size=6
    text_size=1500
    key=Vigenere.generate_key(key_size)
    v=Vigenere(key)
    clear = open("data/Vigenere.txt",'r', encoding='utf8').read()
    # clear = ''.join(clear[0:text_size])
    normalized=''.join([c for c in unicodedata.normalize('NFKD',clear.upper()) if not unicodedata.combining(c)]).translate(str.maketrans('','',string.punctuation))
    payload=''.join([c for c in normalized if c not in 'Œ123456789-– \n\'’'])
    for c in payload:
        if c not in string.ascii_uppercase:
            raise Exception(f"{c} not in {string.ascii_uppercase}")

    ciphered = v.cipher(payload)
    assert(v.decipher(ciphered) == payload)
    cracked_keys=Vigenere.crack(ciphered, max_occurences = 10, max_divisors = 20, deep=0)
    assert(v.key in cracked_keys)

def unit_test2():
    import pytesseract
    import PIL
    ciphered=open('data/vigenere_concours.txt').read()
    img = PIL.Image.open('data/vigenere_concours.png')
    config=f"-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ -l FRENCH --psm 6"
    ciphered_ocr=pytesseract.image_to_string(img, config=("txt "+config))
    ciphered_ocr=''.join([c for c in ciphered_ocr if c not in ['\n']])
    errors=0
    tmp=''
    for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        if ciphered_ocr.count(i)!=ciphered.count(i):
            errors+=1
            tmp+=i
    print(f"errors {errors} ({''.join(i for i in tmp)})")
    
    # assert(ciphered_ocr == ciphered)
    cracked_keys=Vigenere.crack(ciphered, lang=Vigenere.frequence_lang['french'], max_occurences = 1,max_block_size =5, max_divisors=5, deep=0)
    print(Vigenere(cracked_keys[-1]).decipher(ciphered))
    assert('SCUBA' in cracked_keys)

def unit_test3():
    clear = open("data/online.txt",'r', encoding='utf8').read()
    normalized=''.join([c for c in unicodedata.normalize('NFKD',clear.upper()) if not unicodedata.combining(c)]).translate(str.maketrans('','',string.punctuation))
    payload=''.join([c for c in normalized if c not in 'Œ123456789-– \n\'’'])
    for c in payload:
        if c not in string.ascii_uppercase:
            raise Exception(f"{c} not in {string.ascii_uppercase}")

    # ciphered = v.cipher(payload)
    payload = payload
    # assert(v.decipher(ciphered) == payload)
    cracked_keys=Vigenere.crack(payload, lang=Vigenere.frequence_lang['english'], max_occurences = 10, max_divisors = 20, deep=1)
    pass #todo

unit_test()
unit_test2()
# unit_test3()
