#set1_4.py

'''
One of the 60-character strings in this file has been encrypted by single-character XOR.

Find it.
'''


def score(checkstr, search1):

    searchList1 = []
    for letter in search1:
        searchList1.append(letter)

    sumHits = 0
    for idx in xrange(0, len(checkstr)):
        if checkstr[idx] in searchList1:
            sumHits = sumHits + 1

    return sumHits


def oneCharXOR(hexIn, alpha):

    raw = hexIn.decode('hex')

    orig = ''
    for idx in xrange(0, len(raw)):
        orig = orig + chr(ord(raw[idx]) ^ alpha)

    return orig



#begin main

lines = [line.rstrip('\n') for line in open('t4.txt')]

searchstr1 = 'etaoin shrdlu'
#alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

bestScore = 0
bestMsg = ''
for thisLine in lines:
    for num in xrange(0, 256):
        initMsg = oneCharXOR(thisLine, num)        

        lscore = score(initMsg, searchstr1)
        #print lscore

        if lscore > 10:
            print initMsg
            print lscore

        if lscore > bestScore:
            bestScore = lscore;
            bestMsg = initMsg

print '\nanswer: ' + bestMsg

