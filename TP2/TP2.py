from Crypto.Util.number import getPrime, inverse
import random
import hashlib

def gen_rsa_keypair(bits):
    global e
    pq_size = bits//2          
    p = getPrime(pq_size)
    q = getPrime(pq_size)
    assert(p != q)              
    n = p * q
    phi_n = (p - 1) * (q - 1) 
    e = 65537
    assert(e < phi_n and phi_n % e != 0)
    d = inverse(e, phi_n)
    return ((e, n), (d, n))

def rsa(msg, key):
    global c
    if(key[0] == e):
        assert(msg < key[1])
        c = pow(msg, key[0], key[1])
        return c
    else:
        assert(c < key[1])
        m = pow(c, key[0], key[1])
        return m

def rsa_enc(msg, key):
    msg_chif = rsa(int.from_bytes(msg.encode('utf-8'), 'big'), key)
    return msg_chif

def rsa_dec(msg_chif, key):
    tmp = rsa(msg_chif, key)
    msg_dechif = tmp.to_bytes((tmp.bit_length() + 7) // 8, 'big').decode('utf-8')
    return msg_dechif

def h(entier):
    hash_msg = int.from_bytes(hashlib.sha256(str(entier).encode('utf-8')).digest(), 'big')
    return hash_msg

def rsa_sign(msg, key):
    msg_a_sign = int.from_bytes(msg.encode('utf-8'), 'big') 
    s = pow(h(msg_a_sign), key[0], key[1])
    return s

def rsa_verify(msg_sign, key):
    v = pow(msg_sign, key[0], key[1])
    return v

if __name__ == '__main__':      # if __name__ == '__main__' => exécute seulement si c'est vrai
    
    print("+----------+")
    print("|Exercice 1|")
    print("+----------+")
    first_msg = 1312321548523165845123455445132
    key_pair = gen_rsa_keypair(512)
    first_pub_key = (key_pair[0][0], key_pair[0][1])
    second_priv_key = (key_pair[1][0], key_pair[1][1])
    first_enc = rsa(first_msg, first_pub_key)
    first_dec = rsa(first_enc, second_priv_key)
    print("Message :", first_msg)
    if(first_msg == first_dec):
        print("Message chiffré :", first_enc)
        print("Message déchiffré :", first_dec)
        print("True")
    else:
        print("False")
    
    print()
    
    print("+----------+")
    print("|Exercice 2|")
    print("+----------+")
    second_msg = "This message is very confidential."
    second_key_pair = gen_rsa_keypair(512)
    second_pub_key = (second_key_pair[0][0], second_key_pair[0][1])
    second_priv_key = (second_key_pair[1][0], second_key_pair[1][1])
    second_enc = rsa_enc(second_msg, second_pub_key)
    second_dec = rsa_dec(second_enc, second_priv_key)
    print("Message :", second_msg)
    if(second_msg == second_dec):
        print("Message chiffré :", second_enc)
        print("Message déchiffré :", second_dec)
        print("True")
    else:
        print("False")
    
    print()
    
    print("+----------+")
    print("|Exercice 3|")
    print("+----------+")
    msg = "I can understand the importance of this message."
    third_key_pair = gen_rsa_keypair(512)
    third_pub_key = (third_key_pair[0][0], third_key_pair[0][1])
    third_priv_key = (third_key_pair[1][0], third_key_pair[1][1])
    sign = rsa_sign(msg, third_pub_key)
    sign_verif = rsa_verify(sign, third_priv_key)
    hashed = h(int.from_bytes(msg.encode('utf-8'), 'big'))
    print("Message :", msg)
    if(hashed == sign_verif):
        print("Condensé du message : ", hashed)
        print("Message signé :", sign)
        print("Verification du message signé :", sign_verif)
        print("True")
    else:
        print("False")
    