# CSI4108 - Assignment 3 (Question 1 Part 2)
# Nicholas Gin (300107597)

import random

# Following steps described on Page 292 of 6th Edition Textbook
q = 89 # Given in the question
alpha = 13 # Given in the question

def generate_keys():
    # Assuming that User A will only use this function once to generate their private and public keys; 
    # then they will store these keys after they are returned by the function.
    x_a = random.randint(2, q-2) # A's private key (generate a random integer x_a, such that 1 < x_a < q - 1)
    y_a = pow(alpha, x_a, q) #  y_a = (alpha**x_a) mod q
    a_public_key = [q, alpha, y_a] # A's public key
    return x_a, a_public_key # Return A's private and public keys

def encrypt(a_public_key, M): # Takes A's public key (a_public_key) and the message (M) as parameters.
    # Since m1 = 56 is already an integer M in the range 0 <= M <= q - 1, m1 is represented by its actual value, 56.
    k = 37 # Given in the question
    K = pow(a_public_key[2], k, q) # Compute a one time key K = ((y_a)**k) mod q.
    # Encrypted M as a pair of integers (C1, c2) where C1 = (alpha**k) mod q, and C2 = K*M mod q.
    C1 = pow(alpha, k, q) 
    C2 = (K * M) % q
    # Return C1 and C2.
    return [C1, C2]

def recover(x_a, C1, C2): # Takes  A’s private key, C1 and C2 as parameters.
    K = pow(C1, x_a, q) # Recover the one-time key by computing K = ((C1)**x_a) mod q.
    M = (C2 * (pow(K, -1, q))) % q  # Finally, recover M by computing (C2 * (K**-1)) mod q.
    # Return M.
    return M

def main():
    a_private_key, a_public_key = generate_keys()
    encrypted_pair = encrypt(a_public_key, 56)
    M = recover(a_private_key, encrypted_pair[0], encrypted_pair[1]) 

    M2 = (pow(61, -1, q) * 88 * M) % q
    
    print("Original, unencrypted Message:", M)
    print("Generated keys for Alice:", a_private_key, "(private key),", a_public_key, "(public key)")
    print("Message encrypted as a pair of integers (C1,1, C2,1):", encrypted_pair)
    print("Recovered Message (M1):", M)
    print("M2 (assuming that (C2,2) = 88):", M2)


if __name__ == '__main__':
    main()
