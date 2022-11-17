import itertools
import math
import random
from sympy import isprime
   

def generate_random_prime(size):
    p = (random.getrandbits(size) | (1 << size)) | 1        
    for i in itertools.count(1):
        if isprime(p):
            return p
        else:
            if i % (size * 2) == 0:
                p = (random.getrandbits(size) | (1 << size)) | 1
            else:
                p += 2
   

def get_bezout_coeffs(a, b):
    # ax + by = gcd(a, b)
    x, x_, y, y_ = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, x_ = x_, x - x_ * q
        y, y_ = y_, y - y_ * q
    return x, y


def multiplicative_inverse(a, b):
    x, _ = get_bezout_coeffs(a, b)
    if x < 0:
        return b + x
    return x


def generate_keys(size):
    p = generate_random_prime(size // 2)
    q = generate_random_prime(size // 2)
    while q == p:
        q = generate_random_prime(size // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    while True:
        e = random.randint(1, phi - 1)
        # e = 65537
        if math.gcd(e, phi) == 1:
            break
    # d * e = 1 mod phi
    d = multiplicative_inverse(e, phi)
    return (e, n), (d, n)


def rsa_encrypt(message, key):
    e, n = key
    x = [pow(ord(a), e, n) for a in message]
    return x


def rsa_decrypt(message, key):
    d, n = key
    x = [pow(a, d, n) for a in message]
    return ''.join(chr(a) for a in x)


if __name__ == '__main__':
    public_key, private_key = generate_keys(256)

    print(f"\nPublic key: {public_key}")
    print(f"Private key: {private_key}")

    with open("input.txt") as file:
        text = file.read()

    print(f"Input: {text}")
    encrypted = rsa_encrypt(text, public_key)
    print(f"Encrypted array: {encrypted}")
    print(f"Decrypted: {rsa_decrypt(encrypted, private_key)}\n")
