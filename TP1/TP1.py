import random

sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]

def round(key, msg):
    return sbox[msg ^ key]

def enc(key, msg):
    tmp = round(key[0], msg)
    res = round(key[1], tmp)
    return res

xobs = [sbox.index(n) for n in range(0, 16)]

def back_round(key, c):
    return xobs[c] ^ key

def dec(key, ctxt):
    tmp = back_round(key[1], ctxt)
    res = back_round(key[0], tmp)
    return res

def enc_byte(key, msg):
    last = enc(key, (msg & 0b00001111))
    first = enc(key, ((msg & 0b11110000) >> 4))
    res = (first << 4) | last
    return res

def dec_byte(key, msg):
    last = dec(key, (msg & 0b00001111))
    first = dec(key, ((msg & 0b11110000) >> 4))
    res = (first << 4) | last
    return res

def enc_file(key, file):
    with open(file, "rb") as file_txt:
        with open(file + ".enc", 'w') as file_enc:
            for byte in file_txt.read():
                res = enc_byte(key, byte)
                file_enc.write(chr(res))
        file_enc.close()
    file_txt.close()

def dec_file(key, file):
    with open(file, 'r') as file_enc:
        with open(file + ".dec", 'w') as file_dec:
            for byte in file_enc.read():
                res = dec_byte(key, ord(byte))
                file_dec.write(chr(res))
        file_dec.close()
    file_enc.close()

def enc_file_cbc(key, file, vec_init):
    with open(file, "rb") as file_txt:
        with open(file + "_cbc.enc", 'w') as file_enc_cbc:
            for byte in file_txt.read():
                res = enc_byte(key, (byte ^ vec_init))
                vec_init = res
                file_enc_cbc.write(chr(res))
        file_enc_cbc.close()
    file_txt.close()

def dec_file_cbc(key, file, vec_init):
    with open(file, 'r') as file_enc_cbc:
        with open(file + ".dec", 'w') as file_dec_cbc:
            for byte in file_enc_cbc.read():
                res = dec_byte(key, ord(byte)) ^ vec_init
                vec_init = ord(byte)
                file_dec_cbc.write(chr(res))
        file_dec_cbc.close()
    file_enc_cbc.close()

def enc_file_cfb(key, file, vec_init):
    with open(file, 'rb') as file_txt:
        with open(file + "_cfb.enc", 'w') as file_enc_cfb:
            for byte in file_txt.read():
                res = enc_byte(key, vec_init) ^ byte
                vec_init = res
                file_enc_cfb.write(chr(res))
        file_enc_cfb.close()
    file_txt.close()

def dec_file_cfb(key, file, vec_init):
    with open(file, 'r') as file_enc_cfb:
        with open(file + ".dec", 'w') as file_dec_cfb:
            for byte in file_enc_cfb.read():
                res = enc_byte(key, vec_init) ^ ord(byte)
                vec_init = ord(byte)
                file_dec_cfb.write(chr(res))
        file_dec_cfb.close()
    file_enc_cfb.close()

def enc_file_ofb(key, file, vec_init):
    with open(file, 'rb') as file_txt:
        with open(file + "_ofb.enc", 'w') as file_enc_ofb:
            for byte in file_txt.read():
                tmp = enc_byte(key, vec_init)
                vec_init = tmp
                res = tmp ^ byte
                file_enc_ofb.write(chr(res))
        file_enc_ofb.close()
    file_txt.close()

def dec_file_ofb(key, file, vec_init):
    with open(file, 'r') as file_enc_ofb:
        with open(file + ".dec", 'w') as file_dec_ofb:
            for byte in file_enc_ofb.read():
                tmp = enc_byte(key, vec_init)
                res = tmp ^ ord(byte)
                vec_init = tmp
                file_dec_ofb.write(chr(res))
        file_dec_ofb.close()
    file_enc_ofb.close()

if __name__ == '__main__':

    print("+------------+")
    print("| Exercice 1 |")
    print("+------------+")
    first_key = (13, 12)
    first_msg = 5
    encr = enc(first_key, first_msg)
    decr = dec(first_key, encr)
    print("Message : ", first_msg)
    if(first_msg == decr):
        print("Message chiffré : ", encr)
        print("Message déchiffré : ", decr)
        print("True")
    else:
        print("False")
    
    print()

    print("+------------+")
    print("| Exercice 2 |")
    print("+------------+")
    second_key = (10, 6)
    second_msg = ord("r")
    encr_byte = enc_byte(second_key, second_msg)
    decr_byte = dec_byte(second_key, encr_byte)
    print("Message : ", second_msg)
    if(second_msg == decr_byte):
        print("Message chiffré : ", encr_byte)
        print("Message déchiffré : ", decr_byte)
        print("True")
    else:
        print("False")
    
    print()

    first_file = "exo2.txt"
    enc_file(second_key, first_file)
    print("Le fichier", first_file, "a été chiffré.")
    dec_file(second_key, first_file + ".enc")
    print("Le fichier", first_file, "a été déchiffré.")
    
    print()
    
    print("+------------+")
    print("| Exercice 3 |")
    print("+------------+")
    third_key = (9, 0)
    second_file = "test.txt"
    vec_init = random.randint(0, 15)
    
    enc_file_cbc(third_key, second_file, vec_init)
    print("Le fichier", second_file, "a été chiffré avec la méthode CBC.")
    dec_file_cbc(third_key, second_file + "_cbc.enc", vec_init)
    print("Le fichier", second_file, "a été déchiffré avec la méthode CBC.")
    print()
    
    enc_file_cfb(third_key, second_file, vec_init)
    print("Le fichier", second_file, "a été chiffré avec la méthode CFB.")
    dec_file_cfb(third_key, second_file + "_cfb.enc", vec_init)
    print("Le fichier", second_file, "a été déchiffré avec la méthode CFB.")
    print()
    
    enc_file_ofb(third_key, second_file, vec_init)
    print("Le fichier", second_file, "a été chiffré avec la méthode OFB.")
    dec_file_ofb(third_key, second_file + "_ofb.enc", vec_init)
    print("Le fichier", second_file, "a été déchiffré avec la méthode OFB.")
    