import constants

def add_zeros(data, k):
    if len(data) <= k:
        zeros_size = k - len(data)
        data2 = [0 for i in range(zeros_size)] + data
        return data2


def string_to_bin_list(st):
    bin_str = ''.join('{0:08b}'.format(ord(x), 'b') for x in st)
    ans = [int(i) for i in bin_str]
    return ans


def bin_list_to_string(lst):
    if len(lst) % 8:
        zeros = [0 for i in range(8 - len(lst) % 8)]
        lst = zeros + lst
    res = ''
    for i in range(0, len(lst), 8):
        x = 0
        for j in range(i, i + 8):
            x = x * 2 + lst[j]
        res += chr(x)
    return res


def create_d(key):
    len_key = len(key)
    if len_key <= 128:
        return 4
    if 128 < len_key <= 192:
        return 6
    if 192 < len_key <= 258:
        return 8


def extension_key(key):
    d_counter = create_d(key)
    ext_key = []
    key = add_zeros(key, 256)
    for i in range(0, len(key), 32):
        ext_key.append(key[i:i + 32])
    if d_counter == 4:
        ext_key[4] = ext_key[0]
        ext_key[5] = ext_key[1]
        ext_key[6] = ext_key[2]
        ext_key[7] = ext_key[3]
    if d_counter == 6:
        ext_key[6] = f_ext_key_6(ext_key[0], ext_key[1], ext_key[2])
        ext_key[7] = f_ext_key_6(ext_key[3], ext_key[4], ext_key[5])
    return ext_key


def f_ext_key_6(a, b, c):
    res = add_zeros([0], 32)
    for i in range(32):
        res[i] = a[i] ^ b[i] ^ c[i]
    return res


def create_K(list_keys):
    K = []
    for i in range(7):
        for j in list_keys:
            K.append(j)
    return K


class STB:
    def __init__(self):
        self.H = constants.h

    def encrypt_function(self, data, key):
        tack_keys = extension_key(key)
        all_tack_keys = create_K(tack_keys)
        data = [1] + data
        m = ((len(data) // 128) + 1) * 128
        data = add_zeros(data, m)
        res = []
        for i in range(0, m, 128):
            res += self.encrypt_block(data[i:i + 128], all_tack_keys)
        return res

    def decrypt_function(self, data, key):
        tack_keys = extension_key(key)
        all_tack_keys = create_K(tack_keys)
        res = []
        for i in range(0, len(data), 128):
            res += self.decrypt_128(data[i:i + 128], all_tack_keys)
        while res[0] != 1:
            res = res[1:]
        return res[1:]

    def sum_mod(self, first, second):
        return (self.to_int(first) + self.to_int(second)) % (2 ** 32)

    def sub_mod(self, first, second):
        sub = self.to_int(first) - self.to_int(second)
        if sub < 0:
            sub += 2 ** 32
        return sub

    def func(self, a, b, c):
        for j in range(32):
            a[j] = b[j] ^ c[j]
        return a

    def to_int(self, lst):
        return int("".join(str(_) for _ in lst), 2)

    def to_list(self, n):
        return [int(i) for i in "{0:b}".format(n)]

    def encrypt_block(self, data, key):
        a = [int(i) for i in data[:32]]
        b = [int(i) for i in data[32:64]]
        c = [int(i) for i in data[64:96]]
        d = [int(i) for i in data[96:]]
        for i in range(8):
            ak = self.g(add_zeros(self.to_list(self.sum_mod(a, key[7 * (i) - 6])), 32), 5)
            b = self.func(b, b, ak)
            # 2
            dk = self.g(add_zeros(self.to_list(self.sum_mod(d, key[7 * (i) - 5])), 32), 21)
            c = self.func(c, c, dk)
            # 3
            bk = self.g(add_zeros(self.to_list(self.sum_mod(b, key[7 * (i) - 4])), 32), 13)
            diff = self.sub_mod(a, bk)
            a = add_zeros(self.to_list(diff), 32)
            # 4
            sum_bck = (self.to_int(b) + self.to_int(c) + self.to_int(key[7 * (i) - 3])) % (2 ** 32)
            bck = self.g(add_zeros(self.to_list(sum_bck), 32), 21)
            e = self.func(add_zeros([0], 32), bck, add_zeros(self.to_list(i + 1), 32))
            # 5
            b = add_zeros(self.to_list(self.sum_mod(b, e)), 32)
            # 6
            c = add_zeros(self.to_list(self.sub_mod(c, e)), 32)
            # 7
            ck = self.g(add_zeros(self.to_list(self.sum_mod(c, key[7 * (i) - 2])), 32), 13)
            d = add_zeros(self.to_list(self.sum_mod(d, ck)), 32)
            # 8
            ak = self.g(add_zeros(self.to_list(self.sum_mod(a, key[7 * (i) - 1])), 32), 21)
            b = self.func(b, b, ak)
            # 9
            ck1 = self.g(add_zeros(self.to_list(self.sum_mod(d, key[7 * (i)])), 32), 5)
            c = self.func(c, c, ck1)
            a, b = b, a
            c, d = d, c
            b, c = c, b
        y = b + d + a + c
        return y

    def decrypt_128(self, data, key):
        a = [int(i) for i in data[:32]]
        b = [int(i) for i in data[32:64]]
        c = [int(i) for i in data[64:96]]
        d = [int(i) for i in data[96:]]
        for i in reversed(range(8)):
            # 1) step 1
            g_ak = self.g(add_zeros(self.to_list(self.sum_mod(a, key[7 * (i)])), 32), 5)
            b = self.func(b, b, g_ak)
            # 2) step 2
            g_dk = self.g(add_zeros(self.to_list(self.sum_mod(d, key[7 * (i) - 1])), 32), 21)
            c = self.func(c, c, g_dk)
            # 3) step 3
            g_bk = self.g(add_zeros(self.to_list(self.sum_mod(b, key[7 * (i) - 2])), 32), 13)
            a = add_zeros(self.to_list(self.sub_mod(a, g_bk)), 32)
            # 4
            sum_bck = (self.to_int(b) + self.to_int(c) + self.to_int(key[7 * (i) - 3])) % (2 ** 32)
            g_bck = self.g(add_zeros(self.to_list(sum_bck), 32), 21)
            e = self.func(add_zeros([0], 32), g_bck, add_zeros(self.to_list(i + 1), 32))
            # 5
            b = add_zeros(self.to_list(self.sum_mod(b, e)), 32)
            # 6
            c = add_zeros(self.to_list(self.sub_mod(c, e)), 32)
            # 7
            ck = self.g(add_zeros(self.to_list(self.sum_mod(c, key[7 * (i) - 4])), 32), 13)
            d = add_zeros(self.to_list(self.sum_mod(d, ck)), 32)
            # 8
            g_ak = self.g(add_zeros(self.to_list(self.sum_mod(a, key[7 * (i) - 5])), 32), 21)
            b = self.func(b, b, g_ak)
            # 9
            g_dk = self.g(add_zeros(self.to_list(self.sum_mod(d, key[7 * (i) - 6])), 32), 5)
            c = self.func(c, c, g_dk)
            a, b = b, a
            c, d = d, c
            a, d = d, a
        y = c + a + d + b
        return y

    def g(self, u, r):
        x = [u[i:i + 8] for i in range(0, 32, 8)]
        res = []
        for u_i in x:
            u_right = self.to_int(u_i[:4])
            u_left = self.to_int(u_i[4:])
            num = self.to_list(self.H[u_right][u_left])
            res += add_zeros(num, 8)
        func_g = res[r:] + res[:r]
        return func_g


if __name__ == '__main__':
    stb = STB()
    file = open("text.txt", "r")
    text = file.read()
    file.close()
    KEY = 'SDFTasdfghjkl46778647dfghjk'
    print('\nText to encrypt and decrypt: \n\t' + text)
    print('\nKEY: \n\t' + KEY)
    print('\nSimple replace mode')
    enc = stb.encrypt_function(string_to_bin_list(text), string_to_bin_list(KEY))
    print('\nENCRYPTED: \n\t' + bin_list_to_string(enc))
    dec = stb.decrypt_function(enc, string_to_bin_list(KEY))
    print('\nDECRYPTED: \n\t' + bin_list_to_string(dec) + '\n')