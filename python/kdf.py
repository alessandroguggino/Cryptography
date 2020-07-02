# KEY DERIVATION FUNCTION: KDF
# password: string --> key (proper size) + add entropy --> salt
# KDF must be slow (for dictionary attacks) and use a lot of RAM (for dictionary made with GPU or ASIC/FPGA)
# bcrypt and scrypt: competition (AES, SHA3, STREAM)

from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes

password = b'p4ssw0rd1'
salt = get_random_bytes(16) # minimum size = 16 bytes

# N = cpu/memory cost; r = block size; p = parallelization
# N=2**14 r=8 p=1 for interactive logins --> ~ms for each pw
# N=2**20 r=8 p=1 for keys in encryption algorithm (disk enc, file enc) --> ~5s for each pw
key = scrypt(password, salt, key_len=32, N=2**20, r=8, p=1)

print(key)
