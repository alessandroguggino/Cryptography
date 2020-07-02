from Crypto.PublicKey import RSA
from pwn import *

import os
os.environ['PWNLIB_NOTERM'] = 'True'  # Configuration patch to allow pwntools to be run inside of an IDE
os.environ['PWNLIB_SILENT'] = 'True'

from mysecrets import HOST,PORT
from mysecrets import lsb_n as n, lsb_e as e
from mysecrets import lsb_ciphertext as ciphertext
from mysecrets import lsb_plaintext

def to_bytes(m,l=n.bit_length()):
    return int.to_bytes(m, l, byteorder='big')

def to_int(b):
    return int.from_bytes(b,byteorder='big')

def print_bounds(low, up):
    print("[" + str(low) + "," + str(up) + "]")


# test the connection
# server = remote(HOST, PORT)
# server.send(to_bytes(ciphertext))
# bit = server.recv(1024)
# print(bit)
# server.close()


# loop
lower_bound = 0
upper_bound = n
print_bounds(lower_bound, upper_bound)

k = pow(2, e, n) # 2^e mod n

c = ciphertext

for i in range(n.bit_length()):
    c = (k * c) % n # c' = 2^e * m^e = (2m)^e

    # interact with the LSB Oracle
    server = remote(HOST, PORT)
    server.send(to_bytes(c))
    bit = server.recv(1024)
    server.close()
    #print(bit)

    if bit[0] == 1: # 2m > n --> m is in [n/2,n]
        lower_bound = (upper_bound+lower_bound) // 2
    else: # 2m < n --> m is in [0, n/2]
        upper_bound = (upper_bound+lower_bound) // 2

    print_bounds(lower_bound, upper_bound)

print(to_bytes(lower_bound, n.bit_length()).decode())
print(to_bytes(upper_bound, n.bit_length()).decode())

# correction
print(lsb_plaintext - lower_bound)
final = lower_bound ^ 32
print(to_bytes(final, n.bit_length()).decode())
