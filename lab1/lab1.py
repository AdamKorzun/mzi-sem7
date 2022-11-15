from des import DES
from gost import GOST

def string_to_bin_list(st):
    return [int(i) for i in ''.join('{0:08b}'.format(ord(x), 'b') for x in st)]


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


def get_double_des(data, KEY1, KEY2):
    des = DES()
    print('-'*30)
    enc1 = des.encrypt(data, KEY1)
    enc2 = des.encrypt(enc1, KEY2)

    dec1 = des.decrypt(enc2, KEY2)
    dec2 = des.decrypt(dec1, KEY1)
    
    print('KEY1 = {}, KEY2 = {}'.format(bin_list_to_string(KEY1), bin_list_to_string(KEY2)))
    print('\nEncrypted:\nEncrypted (key 1): \n\n\t{}'.format(bin_list_to_string(enc1)))
    print('\nEncrypted (key 2 after key1): \n\n\t{}'.format(bin_list_to_string(enc2)))
    print('\nDecrypted:\nDecrypted (key 2): \n\n\t{}'.format(bin_list_to_string(dec1)))
    print('\nDecrypted (key 2 after key 1): \n\n\t{}'.format(bin_list_to_string(dec2)))
    print('-'*30)


def get_triple_des(data, KEY1, KEY2):
    des = DES()
    print('-'*30)

    enc1 = des.encrypt(data, KEY1)
    dec2 = des.decrypt(enc1, KEY2)
    enc1_2 = des.encrypt(dec2, KEY1)

    dec1 = des.decrypt(enc1_2, KEY1)
    enc2 = des.encrypt(dec1, KEY2)
    dec1_2 = des.decrypt(enc2, KEY1)

    print('KEY1 = {}, KEY2 = {}'.format(bin_list_to_string(KEY1), bin_list_to_string(KEY2)))
    print('\nEncrypted (key 1):\n\t{}'.format(bin_list_to_string(enc1)))
    print('\nDecrypted (key 2): \n\t{}'.format(bin_list_to_string(dec2)))
    print('\nEncryption (key 1 after decryption key 2): \n\t{}'.format(bin_list_to_string(enc1_2)))
    print('\nDecryption (key 1): \n\t{}'.format(bin_list_to_string(dec1)))
    print('\nEncrypted (key 2): \n\t{}'.format(bin_list_to_string(enc2)))
    print('\nDecryption (key 1 after encryption key 2): \n\t{}'.format(bin_list_to_string(dec1_2)))
    print('-'*30)


def get_gost(data, KEY3):
    gost = GOST()
    print('-'*30)

    enc = gost.encrypt(data, KEY3)
    dec = gost.decrypt(enc, KEY3)
    print('KEY: {}'.format(bin_list_to_string(KEY3)))
    print('\nEncrypted: \n\t{}'.format(bin_list_to_string(enc)))
    print('\nDecrypted: \n\t{}'.format(bin_list_to_string(dec)))
    print('-'*30)


if __name__ == '__main__':
    file = open("text.txt", "r")
    data = file.read()
    file.close()
    # установка ключей
    KEY1 = 'ABOBA1'
    KEY2 = 'QWER24'
    KEY3 = 'ASDFGHJKL123456UYTREWQ235479'

    K1 = string_to_bin_list(KEY1)
    K2 = string_to_bin_list(KEY2)
    K3 = string_to_bin_list(KEY3)
    D = string_to_bin_list(data)
    print('\n\tDOUBLE DES:\n')
    get_double_des(D, K1, K2)

    print('\n\tTRIPLE DES:\n')
    get_triple_des(D, K1, K2)

    print('\n\tGOST:\n')
    get_gost(D, K3)
    print('\n')