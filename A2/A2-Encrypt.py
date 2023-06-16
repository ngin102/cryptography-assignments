import os, operator
#Samuel Brie - 7660408 & Nicholas Gin - 300107597
cur_path = os.path.dirname(__file__)
sbox = ['0110','0101', '1100', '1101', '0001', '1111', '1000', '1001', '1011', '1110', '0100', '0111', '0010', '0000', '0011', '1010']
perm = [1,5,9,13,2,6,10,14,3,7,11,15,4,8,12,16]

def readTxt(file):
    #Read our file
    file = open(file, 'r', encoding="utf-8")

    #Read whole file to a string
    data = file.read()

    #close file
    file.close()

    #list of binary
    return  [format(ord(x), '08b') for x in data] 
#Importing the keys
def importKeys(file):
    with open(file) as file:
        lines = file.readlines()
        keys = [line.rstrip() for line in lines]
    return keys

#Writing with an utf-8 encoding
def write(file, final):
    with open(file, 'w', encoding="utf-8") as f:
        f.write(final)
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


#We read the encrypt and re write it in result
binList = readTxt(cur_path + "\\Encrypt.txt")
keyList = importKeys(cur_path + "\\Keys.txt")
final =""
for i in range(0, len(binList)-1, 2):
    #First byte
    temp = binList[i] + binList[i+1]
    for j in range(3):
 
        temp = keyMixing(temp, keyList[j]) 
   
        temp = sBox(temp)
     
        temp = permutation(temp) 
    
    temp = keyMixing(temp, keyList[3]) 
    temp = sBox(temp)
    binTemp = keyMixing(temp, keyList[4]) 
  
    final = final + chr(int(binTemp[:8], 2)) + chr(int(binTemp[8:], 2))


write(cur_path + "\\Result.txt", final) 
    #output = permutation(output)