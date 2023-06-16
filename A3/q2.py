# CSI4108 - Assignment 3 (Question 2)
# Nicholas Gin (300107597)

# Following code example on Page 693 of 6th Edition Textbook
# and Page 6 of Week3a(4108NumTheory) notes 
import random
def miller_rabin_test(n):
    # This function implements the Miller-Rabin Test. If it returns False, it is inconclusive that a given positive 
    # integer n is a composite number. If it returns True, it is conclusive that a given positive integer n is a
    # composite number.

    # Find k, q with k > 0, q odd s.t. n - 1 = (2**k) * q.
    q = n-1
    k = 0

    while (0 == (q % 2)):
        k += 1
        q = q // 2

    # Select random integer a in the range, 1 < a < (n - 1).
    a = random.randint(2, n - 2)
    a_q_mod_n = pow(a, q, n)

    # If (a**q) mod n is equal to 1, return False (inconclusive that n is composite)
    if (1 == a_q_mod_n):
        return False # Inconclusive that n is composite (probable prime)

    # For j = 0 to k - 1 do: if a**((2**j) * q) mod n is equal to n - 1, return False
    # (inconclusive if n is composite)
    e = q
    for j in range(k):
        if (n-1) == (pow(a, e, n)):
            return False # Inconclusive that n is composite (probable prime)
        e = 2*e

    return True # Conclusive that the number is composite

def k_trials(t, num):
    # Running Miller-Rabin Test for 5 trials.
    for i in range(t):
        if (miller_rabin_test(num) == True): 
            # If at least one of the trials determines the number is not a probable prime,
            # return True.
            return True # Conclusive that the number is composite
    return False # Inconclusive that the number is composite

def main():
    t = 5
    for i in range(pow(2, 13) + 1, pow(2, 14) - 1): # Range of 14 bit numbers that could possibly be prime.
        # Find the first number in this range that we can not conclude is composite
        if k_trials(t, i) == False:
            print("A probable prime is:", i)
            break
    # Should print out 8209 - which is in the table from https://primes.utm.edu/lists/small/10000.txt!

if __name__ == '__main__':
    main()

