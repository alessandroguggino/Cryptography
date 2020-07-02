from Crypto.Util.number import getPrime
import math

#kth root of the number n
def iroot(k, n):
    u, s = n, n+1
    while u < s:
        s = u
        t = (k-1) * s + n // pow(s, k-1)
        u = t // k
    return s


n_length = 400

p1 = getPrime(n_length)
p2 = getPrime(n_length)
n = p1 * p2

e = 17 # small

phi = (p1-1)*(p2-1)

d = pow(e, -1, phi)

pk = (e, n)
sk = (d, n)

# plaintext
m = b'hello' # small
m_int = int.from_bytes(m, byteorder='big')
print(m_int)

# ciphertext: c = m^e < n -> no reminder
c = pow(m_int, e, n)
print(c)

# decrypt: m = c^(1/e)
dec = pow(c, 1/e)
print(dec)
print(math.ceil(dec).to_bytes(n_length, byteorder='big').decode())

dec = iroot(e, c)
print(dec)
print(dec.to_bytes(n_length, byteorder='big').decode())
