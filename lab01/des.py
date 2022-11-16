from collections import Counter
import constants

def add_padding(data, k):
    if len(data) <= k:
        zeros_size = k - len(data)
        data2 = [0 for i in range(zeros_size)] + data
        return data2
        
class DES:
    def __init__(self):
        self.IP = constants.ip
        self.E = constants.e 
        self.S = constants.s
        self.P = constants.p
        self.C = constants.c
        self.D = constants.d
        self.shift = constants.shift
        self.KP = constants.kp
        self.final_IP = constants.f_ip

    def encrypt(self, data, key):
        res = []
        data = [1] + data
        m = ((len(data) // 64) + 1) * 64
        data = add_padding(data, m)
        for block in range(0, m, 64):
            res += self.encrypt_64(data[block:block+64], key)
        return res

    def encrypt_64(self, data, key):
        len_block = 64
        key =add_padding(key, 56)
        data_IP = []
        for i in range(len_block):
            data_IP.append(data[self.IP[i] - 1])
        left = data_IP[:len_block//2]
        right = data_IP[len_block//2:]
        for i in range(16):
            k_i = self.generate_k48(key, i)
            left, right = self.feistel_transform(left, right, k_i)
        new_data = left + right
        ans = [new_data[self.final_IP[i] - 1] for i in range(len_block)]
        return ans

    def generate_k48(self, k_56, iteration):
        k_64 = []
        for i in range(8):
            k_64 += k_56[i * 7:i * 7 + 7]
            if Counter(k_56[i * 7:i * 7 + 7])[1] % 2 == 0:
                k_64 += [1]
            else:
                k_64 += [0]
        cd_56 = [0 for i in range(56)]
        for i in range(28):
            cd_56[i] = k_64[self.C[i] - 1]
        j = 0
        for i in range(28, 56):
            cd_56[i] = k_64[self.D[j] - 1]
            j += 1
        k_48 = [0 for i in range(48)]
        for i in range(48):
            k_48[i] = cd_56[self.KP[i] - 1]
        self.C = self.C[self.shift[iteration]:] + self.C[:self.shift[iteration]]
        self.D = self.D[self.shift[iteration]:] + self.D[:self.shift[iteration]]
        return k_48

    def feistel_transform(self, left, right, k):
        L_i = right
        right_48_bit = [right[self.E[i] - 1] for i in range(48)]
        f_right = [right_48_bit[i] ^ k[i] for i in range(48)]
        s_boxes_32 = []
        for i in range(8):
            b_i = f_right[i * 6:i * 6 + 6]
            a = int(str(b_i[0]) + str(b_i[-1]), 2)
            str_b = ''.join([str(i) for i in b_i])
            b = int(str_b[1:-1], 2)
            s = self.S[i]
            b_4 = bin(s[a][b])[2:]
            if len(b_4) < 4:
                b_4 = '0' * (4 - len(b_4)) + b_4
            s_boxes_32 += [int(i) for i in b_4]
        function_r_k = [s_boxes_32[self.P[i] - 1] for i in range(32)]
        R_i = [left[i] ^ function_r_k[i] for i in range(32)]
        return L_i, R_i

    def decrypt(self, data, key):
        n = len(data)
        res = []
        for i in range(0, n, 64):
            res += self.decrypt_64(data[i:i+64], key)
        while res[0] != 1:
            res = res[1:]
        return res[1:]

    def decrypt_64(self, data, key):
        key = add_padding(key, 56)
        len_n = 64
        data_IP = [data[self.IP[i] - 1] for i in range(len_n)]
        l_i = data_IP[:len_n//2]
        r_i = data_IP[len_n//2:]

        keys = []
        for i in range(16):
            k_i = self.generate_k48(key, i)
            keys.append(k_i)
        for i in reversed(range(16)):
            l_i, r_i = self.feistel_transform_dec(l_i, r_i, keys[i])
        data_IP = l_i + r_i
        ans = [data_IP[self.final_IP[i] - 1] for i in range(len_n)]
        return ans

    def feistel_transform_dec(self, left, right, k):
        R_i = left
        right_48_bit = [left[self.E[i] - 1] for i in range(48)]
        f_right = [right_48_bit[i] ^ k[i] for i in range(48)]
        s_boxes_32 = []
        for i in range(8):
            b_i = f_right[i * 6:i * 6 + 6]
            a = int(str(b_i[0]) + str(b_i[-1]), 2)
            str_b = ''.join([str(i) for i in b_i])
            b = int(str_b[1:-1], 2)
            s = self.S[i]
            b_4 = bin(s[a][b])[2:]
            if len(b_4) < 4:
                b_4 = '0' * (4 - len(b_4)) + b_4
            s_boxes_32 += [int(i) for i in b_4]
        function_r_k = [s_boxes_32[self.P[i] - 1] for i in range(32)]
        L_i = [right[i] ^ function_r_k[i] for i in range(32)]
        return L_i, R_i