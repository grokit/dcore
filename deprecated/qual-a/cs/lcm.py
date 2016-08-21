"""
Least Common Multiple
"""

from . import gcd

def lcm(a, b):
    assert type(a) == int
    assert type(b) == int
    return int(int(abs(a*b)) / gcd.gcd(a, b))

