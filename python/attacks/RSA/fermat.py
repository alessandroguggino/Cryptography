import math
from sympy import nextprime
from Crypto.Util.number import getPrime

# p = a + b, q = a - b (b small)
# n = p*q = a**2 - b**2
# if a**2 - n = b**2 --> stop
def fermat(n):
    print("init")
    a = b = math.isqrt(n)
    x = pow(a, 2) - n

    print("a = " + str(a))
    print("b = " + str(b))

    print("cycle")
    while True:
        if x == pow(b,2):
            print("found")
            break
        else:
            a += 1
            x = pow(a, 2) - n
            b = math.isqrt(x)

            print("a = " + str(a))
            print("b = " + str(b))
            print("delta = " + str(n - pow(a,2) + pow(b,2)))

    p = a + b
    q = a - b

    return p, q

if __name__ == '__main__':
    n_length = 40
    p1 = getPrime(n_length)

    delta = 1000
    p2 = nextprime(p1 + delta)

    n = p1 * p2
    print(p1)
    print(p2)
    print(n)

    q1, q2 = fermat(n)
    print(q1)
    print(q2)
