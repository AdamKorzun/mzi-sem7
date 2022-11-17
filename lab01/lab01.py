from des import DES
from gost import GOST

des = DES()
gost = GOST()

def string_to_bin_list(st):
    return [int(i) for i in ''.join('{0:08b}'.format(ord(x), 'b') for x in st)]




def bin_list_to_string(input_list):
    res = ''

    if len(input_list) % 8:
        padding = [0 for _ in range(8 - len(input_list) % 8)]
        input_list = padding + input_list
    for i in range(0, len(input_list), 8):
        x = 0
        for j in range(i, i + 8):
            x = x * 2 + input_list[j]
        res += chr(x)
    return res


def des2(data, KEY1, KEY2):
    enc2 = des.encrypt( des.encrypt(data, KEY1), KEY2)
    dec2 = des.decrypt(des.decrypt(enc2, KEY2), KEY1)
    print(f'Encrypted: {bin_list_to_string(enc2)}')
    print(f'Decrypted: {bin_list_to_string(dec2)}')



def des3(data, KEY1, KEY2):
    enc = des.encrypt(des.encrypt(des.encrypt(data, KEY1), KEY1), KEY2)
    dec = des.decrypt(des.decrypt(des.decrypt(enc, KEY2), KEY1), KEY1)
    print(f'Encrypted: {bin_list_to_string(enc)}')
    print(f'Decrypted: {bin_list_to_string(dec)}')

   


if __name__ == '__main__':
    with open('text.txt', 'r') as f:
        data = f.read()


    KEY1 = 'WEQRTY'
    KEY2 = 'QWER24'
    KEY3 = 'AFDFGHJKL123456UYTREWQ235479'

    K1 = string_to_bin_list(KEY1)
    K2 = string_to_bin_list(KEY2)
    K3 = string_to_bin_list(KEY3)
    D = string_to_bin_list(data)

    enc = des.encrypt(D, K1)
    dec = des.decrypt(enc, K1)
    print('\n')
    print('DES (1):')
    print(f'Encrypted: {bin_list_to_string(enc)}')
    print(f'Decrypted: {bin_list_to_string(dec)}')

    print('DES (2):')
    des2(D, K1, K2)

    print('DES (3): ')
    des3(D, K1, K2)

    print('GOST: ')

    enc = gost.encrypt(D, K3)
    dec = gost.decrypt(enc, K3)
    print(f'Encrypted: {bin_list_to_string(enc)}')
    print(f'Decrypted: {bin_list_to_string(dec)}')

    print('\n')