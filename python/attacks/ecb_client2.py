# server response:
# message = '''Here is the msg:{0}- the secret is:{1}'''.format(input0, ecb_oracle_secret)

#0:15  Here is the msg:
#16:31 {0}
#32:47 padding 15 bytes --> -
#48:63  the secret is:s0
#64:79 s1 .. s15 pad

#0:15  Here is the msg:
#16:31  the secret is:? --> iterate on the last char
#32:47 padding 15 bytes --> -
#48:63  the secret is:s0
#64:79 s1 .. s15 pad

#0:15  Here is the msg:
#16:31 the secret is:S? --> iterate on the last char, S already discovered
#32:47 padding 14 bytes --> -
#48:63 the secret is:Ss1
#64:79 s1 .. s15 pad


from pwn import *
import string

ADDRESS = 'localhost'
PORT = 12347
SECRET_LEN = 16

secret = ''
fix = ' the secret is:'

print(fix)
print(len(fix))

for i in range(0, SECRET_LEN):
    # msg = fix + secret + current_character + pad
    pad = 'A' * (SECRET_LEN - 1 - i)

    for letter in string.printable:
        server = remote(ADDRESS, PORT)
        msg = fix + secret + letter + pad
        print('Sending: ' + msg)
        server.send(msg)
        ciphertext = server.recv(1024)
        server.close()
        # check if enc_msg sent == enc_key received
        if ciphertext[16:32] == ciphertext[48:64]:
            secret += letter
            fix = fix[1:]
            print('Found new character: ' + letter)
            break

print('I discovered the secret: ' + secret)
