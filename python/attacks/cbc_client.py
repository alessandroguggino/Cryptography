from Crypto.Cipher import AES
import os
os.environ['PWNLIB_NOTERM'] = 'True'  # Configuration patch to allow pwntools to be run inside of an IDE
os.environ['PWNLIB_SILENT'] = 'True'  # reduce logging info of pwntools on stdin
from pwn import *

from mysecrets import HOST,PORT, cbc_oracle_iv as iv
from mysecrets import cbc_oracle_ciphertext as ciphertext

def num_blocks(ciphertext, block_size):
    return math.ceil(len(ciphertext)/block_size)

#first block is 0
def get_nth_block(ciphertext, n, block_size):
    return ciphertext[(n)*block_size:(n+1)*block_size]

def get_n_blocks_from_m(ciphertext, n, m, block_size):
    return ciphertext[(m)*block_size:(m+n)*block_size]


def guess_byte(p, c, ciphertext, block_size):
    # build the payload
    # current index
    # append up to the index from the ciphertext
    # byte to guess
    # process all the previously guessed bytes in the block

    # if I already guessed y bytes --> there are y elements in p
    #                              --> padding now will be y+1
    padding_value = len(p) + 1
    n = num_blocks(ciphertext, AES.block_size)

    # starting part --> 0 - n-2 | (16-len(p) bytes of b n-1) | guessing value | len(p) | last block
    #                                                                     1            16
    current_byte_index = len(ciphertext) -1 -block_size - len(p)

    plain = b'\x00'
    p_prime = 0
    for i in range(256):
        # build the payload
        # current index
        # append up to the index from the ciphertext
        # byte to guess
        # process all the previously guessed bytes in the block

        ca = bytearray()
        ca += ciphertext[:current_byte_index]
        ca += i.to_bytes(1, byteorder='big')

        for x in p:
            ca += (x ^ padding_value).to_bytes(1,byteorder='big')

        ca += get_nth_block(ciphertext, n-1, AES.block_size)

        if response == b'OK':
            print("found = ", end=' ')
            print(i)

            p_prime = padding_value ^ i
            plain = bytes([p_prime ^ ciphertext[current_byte_index]]) #  prev[-1] --> c15
            # print(c_prime15)
            # print(p_prime15)
            # print(pn15)
            c.insert(0,i)
            p.insert(0,p_prime)
            break

    return plain


if __name__ == '__main__':
    # first step
    server = remote(HOST, PORT)
    server.send(iv)
    server.send(ciphertext)
    response = server.recv(1024)
    print("Oracle said: " + response.decode()) # it should be OK

    # second step
    server = remote(HOST, PORT)
    server.send(iv)
    c2 = bytearray()
    c2 += ciphertext[:-1] # all ciphertext except last byte
    c2 += bytes([ciphertext[-1] ^ 1]) # last byte of ciphertext xor 1
    server.send(c2)
    response = server.recv(1024)
    print("Oracle said: " + response.decode()) # it should be NO

    # split the ciphertext
    n = num_blocks(ciphertext, AES.block_size) # n blocks
    start = get_n_blocks_from_m(ciphertext, n-2, 0, AES.block_size) # get n-2 blocks (not the last n and the previous n-1)
    prev = get_nth_block(ciphertext, n-2, AES.block_size) # block n-1
    last = get_nth_block(ciphertext, n-1, AES.block_size) # block n

    ba = bytearray()
    ba += start
    ba += prev
    ba += last

    print(ciphertext)
    print(ba)

    # assemble the payload
    # start + 15 bytes of prev + guess value + last
    # send to server
    # check if OK then obtain the payload
    plaintext = bytearray()

    for c_prime15 in range(0, 256):
        pn15 = bytearray() # init

        server = remote(HOST, PORT)
        server.send(iv)

        # build the payload
        ca = bytearray()
        ca += start # start
        ca += prev[:-1] # 15 bytes of prev
        ca += c_prime15.to_bytes(1, byteorder='big') # guess value (big endian representation)
        ca += last # last

        #print(ca)

        # talk to the oracle
        server.send(ca)
        response = server.recv(1024)

        # if padding is ok
        if response == b'OK':
            print("found = ", end='')
            print(c_prime15)

            p_prime15 = 1 ^ c_prime15 # 1 (fixed) xor c_prime15 (guessed)
            pn15 = bytes([p_prime15 ^ prev[-1]]) # pn15 = p_prime_15 xor c15 (prev[-1] = c15)
            print(c_prime15)
            print(p_prime15)
            print(pn15)
            break # end of for

    plaintext += pn15
    print('plaintext = ' + str(plaintext))

    # guess the second byte of the block n
    c_second15 = 2 ^ p_prime15

    # build the payload
    # starting part: 0 - n-2 | (14 bytes of b_n-1) | guess value | c_second15 | last block
    #                                                               1 byte      16 byte
    current_byte_index = -AES.block_size -2 # starting to end (-16 -1 -1 bytes)

    for c_prime14 in range(0, 256):
        pn14 = bytearray()  # init

        server = remote(HOST, PORT)
        server.send(iv)

        # build the payload
        ca = bytearray()
        ca += ciphertext[:current_byte_index] # ciphertext until current index
        ca += c_prime14.to_bytes(1, byteorder='big') # guess value
        ca += c_second15.to_bytes(1, byteorder='big') # c_second15
        ca += get_nth_block(ciphertext, n-1, AES.block_size) # last block of ciphertext

        #print(ca)

        # talk to the oracle
        server.send(ca)
        response = server.recv(1024)

        # if padding is ok
        if response == b'OK':
            print("found = ", end='')
            print(c_prime14)

            p_prime14 = 2 ^ c_prime14 # 2 (fixed) xor c_prime14 (guessed)
            pn14 = bytes([p_prime14 ^ ciphertext[current_byte_index]]) # pn14 = p_prime14 xor c14 (ciphertext[current_byte_index] = c14)
            print(c_prime14)
            print(p_prime14)
            print(pn14)
            break # end of for

    plaintext[0:0] += pn14 # append at the beginning
    print('plaintext = ' + str(plaintext))
