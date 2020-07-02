from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import sys
import base64
import json

from mysecrets import aes_key

iv = get_random_bytes(AES.block_size)
cipher = AES.new(aes_key, AES.MODE_CBC, iv)

f_input = open(sys.argv[1], "rb")

# pycryptodome does not support update functions for block ciphers
ciphertext = cipher.encrypt(pad(f_input.read(), AES.block_size))

# base64 used to represent IV and ciphertext in strings instead of binary objects
# JSON used to go easily on the web
ivb64 = base64.b64encode(cipher.iv).decode('utf-8') # string good for JSON objects
ciphertextb64 = base64.b64encode(ciphertext).decode('utf-8') # string good for JSON objects
json_object = json.dumps({'IV': ivb64, 'ciphertext': ciphertextb64})

print(json_object)

# Receiver
b64 = json.loads(json_object) # split JSON object to manipulate it
cipher2 = AES.new(aes_key, AES.MODE_CBC, base64.b64decode(b64['IV']))
plaintext_dec = cipher2.decrypt(base64.b64decode(b64['ciphertext']))
plaintext_dec_unpadded = unpad(plaintext_dec, AES.block_size)

print(plaintext_dec_unpadded)

#f_output = open(sys.argv[2], "wb")
#f_output.write(ciphertext)
