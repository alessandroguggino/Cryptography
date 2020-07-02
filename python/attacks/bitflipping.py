from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes

plaintext = b'This is the message to encrypt and this a number to change 12345. Bye!'

key = get_random_bytes(32)
nonce = get_random_bytes(12)

cipher = ChaCha20.new(key=key, nonce=nonce)

ciphertext = cipher.encrypt(plaintext)

###########
# Attacker
# want to change the number 1 to number 9 in the plaintext

# generate bit flipping mask
index = plaintext.index(b'1')
print("index: " + str(index))
print("plaintext[i] = ", end='')
print(chr(plaintext[index]))

# text in bytes is immutable --> switch to array
ciphertext_array = bytearray(ciphertext) # this can be manipulated
print("ciphertext[i] = ", end='')
print(chr(ciphertext_array[index]))

# build the mask (xor) a ^ b = c --> c ^ b = a
old_byte = chr(plaintext[index])
new_byte = '9'
mask = ord(old_byte) ^ ord(new_byte) # xor
print("old byte: " + str(old_byte))
print("new byte: " + str(new_byte))
print("mask: " + str(mask))

# modify ciphertext
ciphertext_array[index] = ciphertext_array[index] ^ mask
print("ciphertext[i] = ", end='')
print(ciphertext_array[index])


###########
# Victim

# print the plaintext modified through ciphertext modifying
cipher_dec = ChaCha20.new(key=key, nonce=nonce)
print(cipher_dec.decrypt(ciphertext_array))
