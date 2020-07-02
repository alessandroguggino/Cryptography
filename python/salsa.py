from Crypto.Cipher import Salsa20
from Crypto.Random import get_random_bytes
import base64

plaintext = b'This is the secret message to encrypt'
plaintext2 = b'And this is the second part of the secret message to encrypt'

key = get_random_bytes(32)
nonce = get_random_bytes(8) # if nonce is omitted it will be generated inside the cipher

cipher = Salsa20.new(key=key, nonce=nonce) # object ready to encrypt
ciphertext = cipher.encrypt(plaintext)
ciphertext += cipher.encrypt(plaintext2)

# base64: used to encode binary data
b64 = base64.b64encode(ciphertext)
print("Ciphertext = " + b64.decode('utf-8'))
print("Nonce = " + base64.b64encode(cipher.nonce).decode('utf-8'))

# Receiver
cipher2 = Salsa20.new(key=key, nonce=cipher.nonce) # key shared in some secure way
plaintext_dec = cipher2.decrypt(ciphertext)

print("Plaintext = " + plaintext_dec.decode('utf-8'))
