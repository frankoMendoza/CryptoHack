from Crypto.Cipher import AES
from hashlib import md5

import requests
import hashlib
import sys
import binascii 


#list_words = requests.get('https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words')



result = requests.get('https://aes.cryptohack.org/passwords_as_keys/encrypt_flag')
ciphertext_hex = result.json()["ciphertext"]
print('cipertext: '+ciphertext_hex)
with open('words.txt', 'r') as f:
    for word in f:
        print('word: ', word)
        word = word.strip()
        attempted_key = hashlib.md5(word.encode()).hexdigest()

        ciphertext = bytes.fromhex(ciphertext_hex)
        key = bytes.fromhex(attempted_key)
        cipher = AES.new(key, AES.MODE_ECB)
        try:
            decrypted = cipher.decrypt(ciphertext)
            result = binascii.unhexlify(decrypted.hex())
            if result.startswith('crypto{'.encode()):
                print("key is %s" % word)
                print(result.decode('utf-8'))
                sys.exit(0)
        except ValueError as e:
            continue
