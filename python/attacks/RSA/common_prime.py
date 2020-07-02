from Crypto.Util.number import getPrime

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


n_length = 1024

p1 = getPrime(n_length)
p2 = getPrime(n_length)
p3 = getPrime(n_length)
print(p1)
print(p2)
print(p3)

n1 = p1 * p2
n2 = p1 * p3

f = egcd(n1, n2)[0] # f = p1
print(f)

f1 = n1 // f # f1 = n1/p1 = p2
f2 = n2 // f # f2 = n2/p1 = p3
print(f1)
print(f2)
