from pwn import *
from math import ceil
from mysecrets import HOST, PORT

BLOCK_SIZE = 16
#BLOCK_SIZE_HEX = 32

server = remote(HOST, PORT)

# message = "This is what I received: " + input0 + " -- END OF MESSAGE"
start_str = 'This is what I received: ' # 25 char
pad_len = ceil(len(start_str)/BLOCK_SIZE)*BLOCK_SIZE-len(start_str) # 32 - 25 = 7
print(pad_len)

# 2 entire blocks + msg padding
msg = 'A'*(16*2 + pad_len) # plaintext message to send to the server
print('Sending: ' + msg)
server.send(msg)

ciphertext = server.recv(1024)
#ciphertext_hex = ciphertext.hex()

server.close()

# check the second print (from 32 to 64 = block3 and block4)
for i in range(0, int(len(ciphertext)/BLOCK_SIZE)):
    print(ciphertext[i*BLOCK_SIZE : (i+1)*BLOCK_SIZE])

# prefix | prefix+padding | block | block | don't care
# 0         16              32      48

# check if block3 == block4 : ECB, else CBC
if ciphertext[2*BLOCK_SIZE:3*BLOCK_SIZE] == ciphertext[3*BLOCK_SIZE:4*BLOCK_SIZE]:
    mode = 'ECB'
else:
    mode = 'CBC'

print('Selected mode is: ' + mode)
