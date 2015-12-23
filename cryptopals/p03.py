#set1_3.py 

'''
Single-byte XOR cipher
The hex encoded string:

1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736
... has been XOR'd against a single character. Find the key, decrypt the message.

You can do this by hand. But don't: write code to do it for you.

How? Devise some method for "scoring" a piece of English plaintext. Character frequency is a good metric. 
Evaluate each output and choose the one with the best score. 
'''

   
def score(checkstr, search1, search2):

    searchList1 = []
    for letter in search1:
        searchList1.append(letter)

    searchList2 = []
    for letter in search2:
        searchList2.append(letter)

    sumHits = 0
    for idx in xrange(0, len(checkstr)):
        if checkstr[idx] in searchList1:
            sumHits = sumHits + 2
        elif checkstr[idx] in searchList2:
            sumHits = sumHits + 1

    return sumHits


def oneCharXOR(hexIn, alpha):

    raw = hexIn.decode('hex')

    orig = ''
    for idx in xrange(0, len(raw)):
        orig = orig + chr(ord(raw[idx]) ^ ord(alpha))

    return orig


# begin main

endstr = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
#searchstr = 'rstlneRSTLNE'
#searchstr = 'aeiou'
searchstr1 = 'etaoin'
searchstr2 = 'shrdlu'
alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

bestScore = 0
bestMsg = ''
for letter in alphabet:
    initMsg = oneCharXOR(endstr, letter)
    print initMsg

    lscore = score(initMsg, searchstr1, searchstr2)
    print lscore

    if lscore > bestScore:
        bestScore = lscore;
        bestMsg = initMsg

print bestMsg

