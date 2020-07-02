from Crypto.Hash import SHA256

hash_object = SHA256.new()

plaintext = b'This is the message to encrypt'
plaintext2 = b'And this is the second part'

hash_object.update(plaintext)
hash_object.update(plaintext2)

print(hash_object.digest())
print("Digest = " + hash_object.hexdigest())
