from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import scrypt
from Crypto.Protocol.KDF import HKDF as HKDF_pycrypto
from Crypto.Random import get_random_bytes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, constant_time
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

# generate DH parameters (shared with other party)
parameters = dh.generate_parameters(generator=2, key_size=1024, backend=default_backend())

# generate server keys (backend)
server_private_key = parameters.generate_private_key()
server_public_key = server_private_key.public_key()

# generate client keys (frontend)
client_private_key = parameters.generate_private_key()
client_public_key = client_private_key.public_key()

# key exchange:
# >>> server
# private is x & (g, n)
# public is g^x mod n & (g, n)
# >>> client
# private is y & (g, n)
# public is g^y mod n & (g, n)
# >>> session key is g^(xy) mod n
server_shared_material = server_private_key.exchange(client_public_key)
client_shared_material = client_private_key.exchange(server_public_key)

# check if the shared materials are the same
print(constant_time.bytes_eq(server_shared_material, client_shared_material))

# KDF functions to generate the actual keys
# with pycryptodome
salt = b'' # or salt = get_random_bytes(16)
hkey_server = HKDF_pycrypto(server_shared_material, 32, salt, SHA512, 1) # 32 --> SHA512 : twice the size
hkey_client = HKDF_pycrypto(client_shared_material, 32, salt, SHA512, 1)
print(constant_time.bytes_eq(hkey_server, hkey_client))

# with hazmat
#key_hazmat_server = HKDF(algorithm=hashes.SHA512, length=32, salt=None, info=server_shared_material, backend=default_backend())
#key_hazmat_client = HKDF(algorithm=hashes.SHA512, length=32, salt=None, info=client_shared_material, backend=default_backend())


# ephemeral
# never reuse the same private key
server_private_key2 = parameters.generate_private_key()
server_public_key2 = server_private_key2.public_key()
client_private_key2 = parameters.generate_private_key()
client_public_key2 = client_private_key2.public_key()

server_shared_material2 = server_private_key2.exchange(client_public_key2)
client_shared_material2 = client_private_key2.exchange(server_public_key2)

salt = b''
hkey_server2 = HKDF_pycrypto(server_shared_material2, 32, salt, SHA512, 1)
hkey_client2 = HKDF_pycrypto(client_shared_material2, 32, salt, SHA512, 1)
print(constant_time.bytes_eq(hkey_server2, hkey_client2))
