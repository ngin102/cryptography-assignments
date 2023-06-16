from ntpath import join
import os, operator, random
#Samuel Brie - 7660408 & Nicholas Gin - 300107597
#This is the Attack code.


cur_path = os.path.dirname(__file__)
sbox = ['0110','0101', '1100', '1101', '0001', '1111', '1000', '1001', '1011', '1110', '0100', '0111', '0010', '0000', '0011', '1010']
rsbox =['1101','0100', '1100', '1110', '1010', '0001', '0000', '1011', '0110', '0111', '1111', '1000', '0010', '0011', '1001', '0101']
#sbox = ['1110','0100', '1101', '0001', '0010', '1111', '1011', '1000', '0011', '1010', '0110', '1100', '0101', '1001', '0000', '0111']
#rsbox = ['1110','0011', '0100', '1000', '0001', '1100', '1010', '1111', '0111', '1101', '1001', '0110', '1011', '0010', '0000', '0101']
perm = [1,5,9,13,2,6,10,14,3,7,11,15,4,8,12,16]
deltaP =  "0000101000000000"
targetP = "0100000000000100"
prob = 0.0234375

#Generate plaintext pairs satisfying deltaP
def generate():
    p = []
    pr = []
    for i in range (0, 9999, 2):
        p.append(random.randint(32, 126))  
        pr.append(p[i] ^ int(deltaP[:8], 2))
        p.append(random.randint(32, 126))  
        pr.append(p[i+1] ^ int(deltaP[8:16], 2))

    return p, pr

#KeyMixing, XOR function
def keyMixing(input, key):
    return format(operator.xor(int(input, 2), int(key, 2)), '016b')

#sBox function           
def sBox(input):   
    return sbox[int(input[:4], 2)] + sbox[int(input[4:8], 2)] + sbox[int(input[8:12], 2)] + sbox[int(input[12:16], 2)]

#Permutation
def permutation(input):
    result = [0] * 16
    for i in range(16):
        result[perm[i]-1] = input[i]
    return ''.join(result)

#Importing the keys
def importKeys(file):
    with open(file) as file:
        lines = file.readlines()
        keys = [line.rstrip() for line in lines]
    return keys


#Encrypting to get the resulting cypher text
def encrypt(p, keyList):
    cypher = []
    for i in range(0, len(p)-1, 2):
        #First byte
        temp = format(p[i], '08b') + format(p[i+1], '08b')
        for j in range(3):
    
            temp = keyMixing(temp, keyList[j]) 
    
            temp = sBox(temp)
        
            temp = permutation(temp) 
        
        temp = keyMixing(temp, keyList[3])

        temp = sBox(temp)
        binTemp = keyMixing(temp, keyList[4])

        cypher.append(binTemp[:4])   
        cypher.append(binTemp[4:8])
        cypher.append(binTemp[8:12])
        cypher.append(binTemp[12:16])
    return cypher

#This is the main function for the Attack
def attack(c, cr):
    #Based on our differential path, we know that we will get two resulting fragments of key so we make an array of 16x16
    keyProb = [0] * 256
    for i in range (0, len(c), 4):
        temp =""
        for j in range(16):
            for k in range(16): 
                #We iterate through all possible key combination. The code goes like this: We XOR the cypher/cypher' text with the subkey
                #Go through the reverse sbox and XOR then together to then compare them to the targetP. If we are good we increment the count
                #within the right array index.
                if((format(int(rsbox[int(c[i],2) ^ j], 2) ^ int(rsbox[int(cr[i],2) ^ j], 2), '04b')  == targetP[:4]) 
                and format(int(rsbox[int(c[i+3],2) ^ k], 2) ^ int(rsbox[int(cr[i+3],2) ^ k], 2), '04b')  == targetP[12:16]):
                    keyProb[int(format(j, '04b') + format(k, '04b'), 2)] += 1
    #We then divide everything to get a probability
    for b in range (len(keyProb)):
        keyProb[b] /= 10000
    return keyProb

keyList = importKeys(cur_path + "\\Keys.txt")

p, pr = generate()


c = encrypt(p, keyList)
cr = encrypt(pr, keyList)

ansTable = attack(c, cr)
answer = (sorted(ansTable, reverse=True)[0])

#Small if condition to verify our result, and print the answer
if (answer - 0.0234375) <= 0.004:
    wholeK = format(ansTable.index(answer), '08b')
    k14 = wholeK[:4]
    k1216 = wholeK[4:]

print("Your key at position K1...4 is: " + k14 + " and at k12...16 is: " + k1216)