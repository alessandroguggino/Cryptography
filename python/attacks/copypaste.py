from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from pwn import *
from mysecrets import HOST, PORT

# cookie = "|email=aaaaaaa@b.|com&UID=10&role=|user"
#           | first block    | second block   | last block |

if __name__ == '__main__':
    # first connection: exclude user by isolating it in a different block
    server = remote(HOST, PORT)
    email1 = 'aaaaaaa@b.com'
    server.send(email1)
    c1 = server.recv(1024)
    server.close()

    # second connection: ask to create the last block needed
    # email=aaaaaaaaaa --> length=16
    # admin padded \x0b = 11 times --> length=16
    server = remote(HOST, PORT)
    email2 = 'aaaaaaaaaa' + pad('admin'.encode(), AES.block_size).decode()
    server.send(email2)
    c2 = server.recv(1024)
    server.close()

    ciphertext_attack = bytearray()
    ciphertext_attack += c1[0:2*AES.block_size] # first and second block (email=aaaaaaa@b.com&UID=10&role=)
    ciphertext_attack += c2[AES.block_size:2*AES.block_size] # last block (admin + padding)

    # test
    test = remote(HOST, PORT+100)
    test.send(ciphertext_attack)
    msg = test.recv(1024)
    print(msg.decode())
    test.close()
