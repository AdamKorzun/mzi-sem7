import constants

def add_padding(data, k):
    if len(data) <= k:
        zeros_size = k - len(data)
        data2 = [0 for i in range(zeros_size)] + data
        return data2
        
class GOST:
    def __init__(self):
        self.TABLE_S = constants.t_s

    def encrypt(self, data, key):
        key = add_padding(key, 256)
        data = [1] + data
        m = ((len(data) // 64) + 1) * 64
        data = add_padding(data, m)
        res = []
        keys = [key[i:i + 32] for i in range(0, len(key), 32)]

        for i in range(0, m, 64):
            block_data = data[i:i+64]
            N1 = block_data[:32]
            N2 = block_data[32:]

            block_keys = []
            for i in range(32):
                block_keys.append(keys[i % 8])

            for i in range(32):
                pod_key = block_keys[i]
                N1, N2 = self.transform(N1, N2, pod_key)

            res += N1 + N2
        return res

    def transform(self, l_i_prev, r_i_prev, key):
        r_i = l_i_prev
        l_i = [0 for _ in range(32)]

        l_part = int("".join(str(i) for i in l_i_prev), 2)
        k_part = int("".join(str(i) for i in key), 2)

        l_and_key_mod = (l_part + k_part) % (2 ** 32)
        l = add_padding([int(i) for i in "{0:b}".format(l_and_key_mod)], 32)
        start_s_table = [l[i:i + 4] for i in range(0, 32, 4)]
        res = []
        for i in range(8):
            s_int = int("".join(str(i) for i in start_s_table[i]), 2)
            s_int = self.TABLE_S[i][s_int]
            start_s_table[i] = add_padding([int(i) for i in "{0:b}".format(s_int)], 4)
            res += start_s_table[i]
        funck = res[11:] + res[:11]
        for i in range(32):
            l_i[i] = r_i_prev[i] ^ funck[i]
        return l_i, r_i

    def decrypt(self, data, key):
        result_data = []
        key = add_padding(key, 256)
        keys = [key[i:i + 32] for i in range(0, len(key), 32)]

        for i in range(0, len(data), 64):
            block_data = data[i:i+64]
            N1 = block_data[:32]
            N2 = block_data[32:]

            block_keys = []
            for i in reversed(range(32)):
                block_keys.append(keys[i % 8])

            for i in range(32):
                pod_key = block_keys[i]
                N2, N1 = self.transform(N2, N1, pod_key)
            result_data += N1 + N2

        while result_data[0] != 1:
            result_data = result_data[1:]

        return result_data[1:]