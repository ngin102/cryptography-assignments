# CSI4108 - Assignment 4 (Question 3)
# Nicholas Gin (300107597)

import hashlib

# Following code examples from pg. 706-709 of 6th edition textbook

# Generate a 160 bit q and a 1024 bit p, both prime, such that q divides p-1
def DSA_generate_domain_parameters():
    g = 1
    while (1 == g):
        # First find a q
        q = 1
        while (q < 2^159): q = random_prime(2^160)
        # Next find a p
        p = 1
        while (not is_prime(p)):
            p = (2^863 + randint(1, 2^861)*2)*q + 1
        F = GF(p)
        h = randint(2, p-1)
        g = (F(h)^((p-1)/q)).lift()
    return (p, q, g)

# Generate a user's private and public key given domain parameters p, q, and g
def DSA_generate_keypair(p, q, g):
    x = randint(2, q-1)
    F = GF(p)
    y = F(g)^x
    y = y.lift()
    return (x, y)

# Perform the DSA signing algorithm
def DSA_sign(m, p, q, k, g, x):
    F = GF(p)
    r = F(g)^k
    r = r.lift() % q
    kinv = xgcd(k,q)[1] % q
    Hm = hashlib.sha1(str(m).encode('ASCII'))
    Hm_int = int(Hm.hexdigest(), 16)
    s = (Hm_int + x*r)*kinv % q
    return (r, s, Hm_int)

# Verify a signature
def DSA_verify(r, s, q, Hm_int, g, p, y):
    w = xgcd(s, q)[1]
    u1 = Hm_int * w % q
    u2 = r* w % q
    F = GF(p)
    validity = ( (F(g)^u1 * F(y)^u2).lift() % q ) == r

    if (validity):
        return 'Valid'
    else:
        return 'Invalid'

def main():
    p, q, g = DSA_generate_domain_parameters()
    x, y = DSA_generate_keypair(p, q, g)

    # Generate a value of k that will be re-used later.
    k = randint(2, q-1)

    r1, s1, Hm_int1 = DSA_sign(522346828557612, p, q, k, g, x)
    print('Signature on m from question 2 (r1, s1):', '(' + str(r1) + ', ' + str(s1) + ')')
    print('Running verification on signature (r1, s1); if (r1, s1) is verified, Valid will be outputted on next line:')
    verified = DSA_verify(r1, s1, q, Hm_int1, g, p, y)
    print(verified, '\n')

    r2, s2, Hm_int2 = DSA_sign(8161474912883, p, q, k, g, x)
    print('Signature on m from question 3 (r2, s2):', '(' + str(r2) + ', ' + str(s2) + ')')
    print('Running verification on signature (r2, s2); if (r2, s2) is verified, Valid will be outputted on next line:')
    verified2 = DSA_verify(r2, s2, q, Hm_int2, g, p, y)
    print(verified2, '\n')

    # The following steps below to calculate k and x are from the Week11(4108DigSig) course notes (pg. 16)

    print('Showing that we can calculate k, if k is not unique.')
    print('k generated by random int generator:', k)    
    calculated_k = ( (Hm_int1 - Hm_int2)/ (s1 - s2) ) % q
    print('k calculated based on signatures (r1, s1) and (r2, s2):', calculated_k)
    if (k == calculated_k):
        print('The generated k and calculated k are the same values.', '\n')
        
    print('Showing that we can complete compromise security by computing private key, x, if k is not unique.')
    print('x (originally generated):', x) 
    calculated_x = ( ( (calculated_k * s1) - Hm_int1 ) / r1 ) % q
    print('x calculated based on signatures (r1, s1 and (r2, s2):', calculated_x)
    if (k == calculated_k):
        print('We successfully determined the private key, x.')

if __name__ == '__main__':
    main()