# CSI4108 - Assignment 3 (Question 3a)
# Nicholas Gin (300107597)

import time
def RSA():
    # RSA algorithm from pages 5-6 of Week7b(4108PKCToECC) course notes

    # Choose two prime numbers (ensuring that they are 1024 bit)
    p = int(random_prime((2**1024) - 1, (2**1023) + 1))
    q = int(random_prime((2**1024) - 1, (2**1023) + 1))

    # Let n = p * q
    n = p * q

    # Compute phi(n) = (p - 1) * (q - 1)
    phi = (p - 1) * (q - 1)

    # e has already been selected in the question
    # (the public exponent)
    e = 65537
 
    # Compute d such that 1 < d < phi(n) and e * d is congruent to 1 mod phi(n)
    # (the private exponent)
    d = int(inverse_mod (e, phi))
    # The public key is {e, nt}.
    # The private key is {d}.

    # The message to be encrypted (as given in the question)
    m = 466921883457309
    c = pow(m, e, n)

    return c, d, p, q, n

def decrypt(c, d, n):
    # Decryption formula from pages 5-6 of Week7b(4108PKCToECC) course notes
    decrypted_c = (c**d) % n
    return decrypted_c

def CRT_setup(p, q):
    # CRT_setup coded based on CRT Examples 2 and 3 from Week3b(4108NumTheory) course notes
    m1 = p
    m2 = q

    mm1 = m2
    mm2 = m1

    mm1_mod_m1 = mm1 % m1
    mm2_mod_m2 = mm2 % m2

    i1 = int(inverse_mod(mm1_mod_m1, m1))
    i2 = int(inverse_mod(mm2_mod_m2, m2))

    c1 = mm1 * i1
    c2 = mm2 * i2
    return c1, c2

def CRT(c, c1, c2, p, q, d, n):
    # CRT coded based on CRT Examples 2 and 3 from Week3b(4108NumTheory) course notes
    # Integers in the tuple
    t1 = int(pow(c % p, d % (p-1), p))
    t2 = int(pow(c % q, d % (q-1), q))
    decrypted_c_crt = (t1 * c1 + t2 * c2) % n

    return decrypted_c_crt

def main():
    ciphertext, d, p, q, n = RSA()
    print ("Ciphertext:", ciphertext, "\n")

    start = time.time()
    decrypted_c = decrypt(ciphertext, d, n)
    end = time.time()

    c1, c2 = CRT_setup(p, q)

    start2 = time.time()
    decrypted_c_crt = CRT(ciphertext, c1, c2, p, q, d, n)
    end2 = time.time()

    print ("Decrypted Ciphertext (Regular):", decrypted_c)
    print ("Duration:", end - start, "s", "\n")
    print ("Decrypted Ciphertext (CRT):", decrypted_c_crt)
    print ("Duration:", end2 - start2, "s", "\n")

if __name__ == '__main__':
    main()
