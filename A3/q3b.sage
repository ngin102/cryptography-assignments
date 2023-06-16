# CSI4108 - Assignment 3b (Question 3a)
# Nicholas Gin (300107597)

import random
import time
def ECDH():
    start = time.time()
    # Following code example from pg. 703 of 6th edition textbook and Page 4 from Week9b(4108AsymmetricKeying) 
    # Generating a random 256 bit prime number
    p = random_prime((2**256) - 1, (2**255) + 1)

    F = GF(p)
    E = EllipticCurve(F, 5, 10)
    G = E.gen(0)
    q = E.order()

    # Alice computes a secret value n_a in 2...q-1
    n_a = randint(2, q-1)

    # Alice computes a public value p_a
    p_a = n_a * G

    # Bob computes a secret value n_b in 2...q-1
    n_b = randint(2, q-1)

    # Bob computes a public value p_b 
    p_b = n_b * G

    # Alice computes the shared value (k_a)
    k_a = n_a * p_b

    # Bob also computes the shared value (k_b)
    k_b = n_b * p_a
    
    end = time.time()

    print("A's shared value (EDCH):", k_a, "\n")
    print("B's shared value (EDCH):", k_b, "\n")

    if (k_a == k_b):
        print("Using ECDH: A and B have jointly created a key for encryption.")

    duration = end - start
    print("Duration:", duration, "s", "\n")


def DH():
    # Following code example from pg. 699 of the textbook and Page 3 of Week9b(4108AsymmetricKeying) course notes.
    # To be equivalent security to ECC, private key must be 256 bits, and the public key must be 3072 bits.

    start2 = time.time()

    # p is a safety prime of length 3072 bits, which was randomly generated from this link: https://2ton.com.au/getprimes/random/3072?callback=safePrimes.
    p = 5706506157234918077697620794757832850164288054563798372894135938213062275647987966122258633068750422765412656757031356726396953590532832612651778614105809511849586196710555382454189104759450958990285411479790481437352705776283272319456652683323538937260497193311000143689192179068902276345990720987654551508067515625028369857940338694384788165882274696075459273470422106697305318790147893846253129820012898648351508015551223745278890520359947507571241894368485838392269925693850703541149126528910198218181190191838684380991993129190323795286186174306283659413109320618812927148957617563530654213183595845271455134532824868900351704125087594416973833865080689714103518378681020386961497325886960688753954478128513240575141476060693006117221793647116462273346529910629485419839082883251938529554425411985690411396844560536638031658795868520645186250402436980640601282094386585717214831113366241935827438075825235610782477184663
    
    g = primitive_root(p)
    
    x_a = random.randint((2**255), (2**256) - 1) # Alice's private value
    y_a = pow(g, x_a, p) # Alice's public value

    x_b = random.randint((2**255), (2**256) - 1) # Bob's private value
    y_b = pow(g, x_b, p) # Bob's public value

    # Shared value:
    a_shared = pow(y_b, x_a)
    b_shared = pow(y_a, x_b)

    end2 = time.time()

    print("A's shared value (DH):", a_shared, "\n")
    print("B's shared value (DH):", b_shared, "\n")

    if (a_shared == b_shared):
        print("Using DH: A and B have jointly created a key for encryption.")

    duration2 = end2 - start2
    print("Duration:", duration2, "s")


def main():
    ECDH()
    DH()

if __name__ == '__main__':
    main()

