# CSI4108 - Assignment 4 (Question 1)
# Nicholas Gin (300107597)

import hashlib
import random
import hmac

# Inspired by algorithm on pg. 369 and pg. 370 of 6th edition textbook.

def generate_key():
    key = random.randint(pow(2, 511), pow(2, 1024) - 1)
    # Converting int to bytes using example from Python manual: https://docs.python.org/3/library/stdtypes.html#int.to_bytes
    key = key.to_bytes(key.bit_length() + 7, 'big')
    return key

def xor(a, b):
    iterator_of_tuples = zip(a, b)
    # Performing xor operation on each pair of items in the iterator of tuples produced by calling zip.
    return bytes(c ^ d for c, d in iterator_of_tuples)

def hmac_sha_512(k, m):
    # pg. 369 of the 6th edition textbook: if the length of k (the key) is greater than b
    # (the number of bits in a block, which for HMAC-SHA-512 is 1024 bits - or 128 bytes),
    # k is input to the hash function to produce an n-bit key.
    if len(k) > 128:
        k = hashlib.sha512(k).digest()

    # Pad k with zeroes so that it is b bits in length.
    # Note that the 6th edition textbook says to pad the left side of k with zeroes, but
    # the right side of k must be padded with zeroes if the results of my implementation
    # are to match the results of the hashlib library HMAC-SHA-512 function.
    padding_length = 128 - len(k)
    k_plus = k + (b'\x00' * padding_length)

    # opad is equal to 5c (in hex) repeated b/8 times (1024/8 times = 128 times)
    opad = b'\x5c' * 128
    # ipad is equal to 35 (in hex) repeated b/8 times (1024/8 times = 128 times)
    ipad = b'\x36' * 128
    
    output = hashlib.sha512( xor(k_plus, opad) + hashlib.sha512( xor(k_plus, ipad) + m ).digest() )
    return output.hexdigest()

def main():
    # Generate a key.
    key = generate_key()

    # The string that the HMAC will be computed on (given in the question).
    string_to_compute = b"I am using this input string to test my own implementation of HMAC-SHA-512."

    # Using my implementation of HMAC-SHA-512 on the string given in the question.
    my_hmac = hmac_sha_512(key, string_to_compute)
    print("Result of my HMAC-SHA-512 implementation:", my_hmac, "\n")

    # Using the implementation of HMAC-SHA-512 from the hashlib library on the string given in the question.
    library_hmac = hmac.new(key, string_to_compute, hashlib.sha512).hexdigest()
    print("Result of hashlib library HMAC-SHA-512 implementation:", library_hmac, "\n")

    # Confirming the correctness of my HMAC-SHA-512 implementation by comparing its result with the result of
    # HMAC-SHA-512 from the hashlib library.
    if (my_hmac == library_hmac):
        print("My HMAC-SHA-512 implementation produces the same result as the hashlib library HMAC-SHA-512 implementation.")

if __name__ == '__main__':
    main()