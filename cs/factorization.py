"""
Prime number factorization is O(log(n)).

@@todo move to cs/*
@@todo: gcd.py, factorize.py, prime.py, n_choose_k.py.

# Links

- https://en.wikipedia.org/wiki/Integer_factorization
- https://en.wikipedia.org/wiki/Prime_factor
"""

import functools
import random

__primesBetween0To1000 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

def primeFactorization(n):
	"""
	This is the slow, by trial O(n) algorithm.
	"""
	for i in range(2, n):
		if n % i == 0:
			return [i] + primeFactorization(n//i)
	if n != 1:
		return [n]
	return []

def sumMult(A):
	if A == []:
		return 1
	return functools.reduce(lambda x,y: x*y, A)

def testRandom():
	primes = []
	for i in range(random.randint(0, 100)):
		j = random.randint(0, len(__primesBetween0To1000)-1)
		primes.append(__primesBetween0To1000[j])
	primes.sort()
	sm = sumMult(primes)
	pf = primeFactorization(sm)
	assert primes == pf

def unitTest():
	assert primeFactorization(864) == [2,2,2,2,2,3,3,3]
	# http://math.stackexchange.com/questions/47156/prime-factorization-of-1
	assert primeFactorization(1) == []

	for p in __primesBetween0To1000:
		assert primeFactorization(p) == [p]

	random.seed(1234)
	for z in range(100):
		testRandom()

if __name__ == '__main__':
	unitTest()


