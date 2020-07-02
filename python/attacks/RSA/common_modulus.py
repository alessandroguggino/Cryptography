from Crypto.Util.number import getPrime

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


n_length = 40

p1 = getPrime(n_length)
p2 = getPrime(n_length)
n = p1 * p2

e1 = 65537
e2 = 17

phi = (p1-1)*(p2-1)

d1 = pow(e1, -1, phi)
d2 = pow(e2, -1, phi)

pk1 = (e1, n)
sk1 = (d1, n)
pk2 = (e2, n)
sk2 = (d2, n)

# plaintext
plaintext = b'message'
p_int = int.from_bytes(plaintext, byteorder='big')

# ciphertexts: m^e mod n
c1 = pow(p_int, e1, n)
c2 = pow(p_int, e2, n)

res = egcd(e1, e2)
print(res[0]) # if =1 --> e1, e2 coprime
u = res[1]
v = res[2]

# if e1, e2 coprime
# c1^u mod n * c2^v mod n (mod n) = m^(e1*u + e2*v) = m (mod n)
decrypted = pow(c1, u, n) * pow(c2, v, n) % n
print(decrypted.to_bytes(n_length, byteorder='big').decode())
