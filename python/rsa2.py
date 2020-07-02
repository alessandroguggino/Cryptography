from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP

# KEY GENERATION
# generate a RSA private key
key = RSA.generate(2048)
print(key.export_key(format='PEM', pkcs=8))

# write the key
f = open('myrsakey.pem', 'wb')
f.write(key.export_key(format='PEM', pkcs=8, passphrase='longlongpassphrasehere'))
f.close()

# read the key
f = open('myrsakey.pem', 'r')
key = RSA.import_key(f.read(), passphrase='longlongpassphrasehere')
f.close()

# key parameters
print(key.p)
print(key.q)
print(key.n)
print(key.e)
print(key.d)

# generate a RSA key from parameters
key2 = RSA.construct((key.n, key.e, key.d, key.p, key.q), consistency_check=True)

# key parameters
print(key2.p)
print(key2.q)
print(key2.n)
print(key2.e)
print(key2.d)

# extract the public key
public_key = key.publickey()
print(public_key)


# SIGNATURE
print('------------------')
message = b'This is the message to sign'

# manually compute the digest
h = SHA256.new(message)

# sign with pss object (probabilistic signature scheme)
signer = pss.new(key)
signature = signer.sign(h)

# verify
# received: message + signature
hv = SHA256.new(message)
verifier = pss.new(public_key)
try:
    verifier.verify(hv, signature)
    print('OK authentic')
except:
    print('NO not authentic')

# ENCRYPTION
print('------------------')
message = b'This is the message to encrypt'

# encrypt with public key
cipher_public = PKCS1_OAEP.new(public_key)
ciphertext = cipher_public.encrypt(message)

# decrypt = encrypt with private key
cipher_private = PKCS1_OAEP.new(key)
plaintext = cipher_private.decrypt(ciphertext)
print(plaintext)
