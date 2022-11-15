import random
from sympy import *


def random_prime_number():
    while True:
        number = random.randrange(10000, 100000)
        if isprime(number):
            break
    return number


def primitive_root(number):
    o = 1
    r = 0
    while r < number:
        k = pow(r, o, number)
        while k > 1:
            o = o + 1
            k = (k * r) % number
        if o == (number - 1):
            return r
        o = 1
        r += 1
    return None


def are_relatively_prime(a, b):
    for n in range(2, min(a, b) + 1):
        if a % n == b % n == 0:
            return False
    return True


def get_relatively_prime(n):
    while True:
        res = random.randint(2, n - 1)
        if are_relatively_prime(res, n):
            return res


def get_keys():
    p = random_prime_number()
    print('\np: ' + str(p))
    g = primitive_root(p)
    print('g: ' + str(g))
    assert g is not None
    x = get_relatively_prime(p - 1)
    print('x: ' + str(x))
    y = (g ** x) % p
    return p, g, x, y


def encrypt(p, g, y, text):
    key = random.randint(2, p - 2)
    for M in text:
        if ord(M) > p:
            print("M should be more than p")
    a = (g ** key) % p
    b = []
    for i in range(len(text)):
        b.append(y ** key * ord(text[i]) % p)
    return a, b


def decrypt(p, x, a, b):
    res = []
    for bi in b:
        res.append(chr(int(bi * a ** (p - 1 - x) % p)))
    return ''.join(res)


if __name__ == '__main__':
    file = open("text.txt", "r")
    text = file.read()
    file.close()
    p, g, x, y = get_keys()
    a, b = encrypt(p, g, y, text)
    res_text = decrypt(p, x, a, b)
    print('\nEncrypted data\n' + '\na: ' + str(a) + '\nb:\n' + str(b))
    print('\nDecrypted data\n\n' + str(res_text) + '\n')