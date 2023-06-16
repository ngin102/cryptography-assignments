# CSI4108 - Assignment 4 (Question 2)
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
    m = 522346828557612
    p, q, g = DSA_generate_domain_parameters()
    
    # Generate a value of k (generating a value of k in the same way as in the code example)
    k = randint(2, q-1)

    x, y = DSA_generate_keypair(p, q, g)
    r, s, Hm_int = DSA_sign(m, p, q, k, g, x)

    print('Signature (r, s):', '(' + str(r) + ', ' + str(s) + ')')
    print('Running verification on signature (r, s); if (r, s) is verified, Valid will be outputted on next line:')
    verified = DSA_verify(r, s, q, Hm_int, g, p, y)
    print(verified)

if __name__ == '__main__':
    main()