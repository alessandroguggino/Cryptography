from Crypto.Util.number import getPrime
from factordb.factordb import FactorDB

n_length = 5

p1 = getPrime(n_length)
p2 = getPrime(n_length)
n = p1 * p2
print(p1)
print(p2)
print(n)

print(">>> Factorization from n:")
f = FactorDB(n)
f.connect()
factors = f.get_factor_list()
print(factors)
