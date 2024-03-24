from Crypto.Util.number import getPrime, inverse
import time

bits = 512
pq_size = bits//2          
p = getPrime(pq_size)
q = getPrime(pq_size)
assert(p != q)
n = p * q
phi_n = (p - 1) * (q - 1)
e = 65537
assert(e < phi_n and phi_n % e != 0)
d = inverse(e, phi_n)

def rsa_classique(msg):
    s = pow(msg, d, n)
    return s

def crt_rsa(msg):
    dp = d % (p - 1)
    dq = d % (q - 1)
    iq = pow(q, -1, p)
    sp = pow(msg, dp, p)
    sq = pow(msg, dq, q)
    s = sq + q * (iq * (sp - sq) % p)
    return s

e_bc = 17

def  pgcd(a, b):
    if b == 0:
        return a
    else:
        c = a % b
        return pgcd(b, c)

def bellcore(sign, sign_f, n_bc):
    p_bc = pgcd((sign - sign_f), n_bc)
    q_bc = int(n_bc / p_bc)
    phi_n_bc = (p_bc - 1) * (q_bc - 1)
    assert(e_bc < phi_n_bc and phi_n_bc % e_bc != 0)
    d_bc = inverse(e_bc, phi_n_bc)
    return d_bc


if __name__ == "__main__":

    print("+----------+")
    print("|Exercice 1|")
    print("+----------+")
    msg = 12235688798115874651356845631123231354556841512544654114868978798796132313246
    if(rsa_classique(msg) == crt_rsa(msg)):
        print("True")

    print("Temps d'exécution pour RSA classique : ")
    start_time_rsa = time.time()
    for loop in range(1000):
        rsa_classique(msg)
    end_time_rsa = time.time()
    time_rsa = end_time_rsa - start_time_rsa
    print(time_rsa)

    print("Temps d'exécution pour CRT-RSA : ")
    start_time_crt_rsa = time.time()
    for loop in range(1000):
        crt_rsa(msg)
    end_time_crt_rsa = time.time()
    time_crt_rsa = end_time_crt_rsa - start_time_crt_rsa
    print(time_crt_rsa)
    
    print()

    print("+----------+")
    print("|Exercice 2|")
    print("+----------+")
    n_bc = 47775493107113604137
    sign = 4539922971077504169
    sign_f = 21327563041362669328
    d_bc = bellcore(sign, sign_f, n_bc)
    m_bc = pow(sign, e_bc, n_bc)
    s_bc = pow(m_bc, int(d_bc), n_bc)
    if(s_bc == sign): 
        print("Signature :",sign) 
        print("Signature trouvé avec la clé privée :",s_bc)
        print("True") 
        print("La clé privée =", d_bc) 