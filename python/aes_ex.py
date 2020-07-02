from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

plaintext = b'This is the secret message to encrypt'

key = get_random_bytes(32) # key for AES256
iv = get_random_bytes(AES.block_size)

cipher = AES.new(key, AES.MODE_CBC, iv)

padded_data = pad(plaintext, AES.block_size) # add data at the end - PKCS#7
print(padded_data)
ciphertext = cipher.encrypt(padded_data)
print(ciphertext)


# Receiver
cipher2 = AES.new(key, AES.MODE_CBC, cipher.iv)

decrypted_data = cipher2.decrypt(ciphertext)
print(decrypted_data)
unpadded_data = unpad(decrypted_data, AES.block_size)

assert(plaintext == unpadded_data)
