import os, operator

#Samuel Brie - 7660408 & Nicholas Gin - 300107597
#This code gives us our differential table with numbers and probabilities as well as our differential paths

cur_path = os.path.dirname(__file__)
sbox = ['0110','0101', '1100', '1101', '0001', '1111', '1000', '1001', '1011', '1110', '0100', '0111', '0010', '0000', '0011', '1010']
#sbox = ['1110','0100', '1101', '0001', '0010', '1111', '1011', '1000', '0011', '1010', '0110', '1100', '0101', '1001', '0000', '0111']
perm = [1,5,9,13,2,6,10,14,3,7,11,15,4,8,12,16]

#Permuation
def permutation(input):
    result = [0] * 16
    for i in range(16):
        result[perm[i]-1] = input[i]
    return ''.join(result)

#We make the differential frequency table. Simple, XOR the deltaX with X and compare the result Y with the original Y
def makeTable():
    result = [[0 for col in range(16)] for row in range(16)]
    for i in range(16): #Input diff
        for j in range(16): #sbox iteration
            index = int(sbox[(i ^ j)],2) ^ int(sbox[j], 2)
            result[i][index] = result[i][index] + 1
    return result

#This recalculates the table by dividing by 16 to get probabilities and gives a smaller result to exclude 0 and 2(0.125)
def probTable(table):
    smallTable = []
    for i in range(16):
        for j in range(16):
            temp = table[i][j] / 16
            if(temp != 0 and temp != 0.125):
                smallTable.append([temp, [i, j]])
    return smallTable

#Calculate the best starting possible combo for the highest prob
def calcProb(table):
    inputPos = []
    v1 =0
    v2 = 0
    v3 =0 
    v4 =0 
    while v4 != len(table) -1:
        if v1 == len(table):
            v2 = v2 + 1
            v1 = 0
        if v2 == len(table):
            v3 = v3 + 1
            v2 = 0
        if v3 == len(table):
            v4 = v4 + 1
            v3 = 0
        inputPos.append([table[v4][0] * table[v3][0] * table[v2][0] * table[v1][0], table[v4][1] + table[v3][1] + table[v2][1] + table[v1][1]])
        v1 = v1 + 1

    return inputPos

#The behemoth of the calculation. This calculates all the possible paths with the highest probability possible        
def calcBestProb(input, probtable):
    allProbs = []
        #The input is the best combination found in the previous function. Table is the table generated with the different probabilities
    for i in range(1, len(input)):

        #Start an array that will become a matrix, we append the first value (probability)
        temp = []
        temp.append(input[i][0])
        current = input[i][0]
        binInput ="Delta X0: "
        for j in range(0, len(input[i][1]), 2):
            binInput = binInput + format(input[i][1][j], '04b')
        #We also append the first number making that probability, this is the differential input
        temp.append([binInput])
        binInput =""
        for j in range(1, len(input[i][1]), 2):
            binInput = binInput + format(input[i][1][j], '04b')
        #This is actually the differential output
        temp.append(["Delta Y0: "+binInput])
        for k in range (3):
            #Following the tutorial we follow the steps, permute
            binInput = permutation(binInput)
            temp.append(["Perm/Delta X" + str(k+1) + ": " + binInput])

            #We then make an array of indexes by finding the max value possible following the last permuation found in the probtables
            v = [int(binInput[:4], 2), int(binInput[4:8], 2), int(binInput[8:12], 2), int(binInput[12:16], 2)]
            index = [max(range(len(probtable[v[0]])), key=probtable[v[0]].__getitem__), 
            max(range(len(probtable[v[1]])), key=probtable[v[1]].__getitem__), 
            max(range(len(probtable[v[2]])), key=probtable[v[2]].__getitem__),
            max(range(len(probtable[v[3]])), key=probtable[v[3]].__getitem__)]
            binInput = "".join(format(x, '04b') for x in index)
            temp.append(["Delta Y" + str(k+1) + ": " + binInput])
            #Below we now multiply the new found probability to the current value.
            if k != 2:
                for m in range(len(index)):
                    current = current * (probtable[v[m]][index[m]])/16
        temp[0] = current
        allProbs.append(temp)

        #This gives us all the paths possible
    return allProbs


table = makeTable()
probtable = probTable(table)
condensedTable = calcProb(probtable)
sortedTable = sorted(condensedTable, key=operator.itemgetter(0), reverse = True)
input = []
#We exclude anything under prob 0.25 because the calculations are too long and won't generate a better result
for i in range (len(sortedTable)):
    if sortedTable[i][0] < 0.25:
        break
    input.append(sortedTable[i])
bestProb = calcBestProb(input, table)
#print(sortedTable[:4])
print(sorted(bestProb, key=operator.itemgetter(0), reverse = True))




