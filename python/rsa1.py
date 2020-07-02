from Crypto.Util import number

# manually implement trivial RSA

n_length = 1024

p1 = number.getPrime(n_length)
print(p1)

p2 = number.getPrime(n_length)
print(p2)

# modulus
n = p1 * p2
print(n)

# public exponent
e = 65537

phi = (p1-1)*(p2-1)
print(phi)

# private exponent: e*d ~= 1 mod phi
d = pow(e, -1, phi)
print(d)

print((e*d)%phi)

public_key = (e, n)
private_key = (d, n)

# trivial encryption
m = b'This is the message to encrypt'

# RSA works with integers
m_int = int.from_bytes(m, byteorder='big')
print(m_int)

# m_int must be less than n
if m_int >= n:
        raise ValueError

# encryption (with public key)
C = pow(m_int, e, n)
print(C)

# decryption (with private key)
D = pow(C, d, n)
print(D)

m_decrypted = D.to_bytes(n_length, byteorder='big')
print(m_decrypted.decode())
