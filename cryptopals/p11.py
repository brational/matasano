# prob 11

'''
Now that you have ECB and CBC working:

Write a function to generate a random AES key; that's just 16 random bytes.

Write a function that encrypts data under an unknown key --- that is, 
a function that generates a random key and encrypts under it.

The function should look like:

encryption_oracle(your-input)
=> [MEANINGLESS JIBBER JABBER]
Under the hood, have the function append 5-10 bytes (count chosen randomly) 
before the plaintext and 5-10 bytes after the plaintext.

Now, have the function choose to encrypt under ECB 1/2 the time, 
and under CBC the other half (just use random IVs each time for CBC). Use rand(2) to decide which to use.

Detect the block cipher mode the function is using each time. 
You should end up with a piece of code that, pointed at a block box that might be encrypting ECB or CBC, 
tells you which one is happening.
'''

import cutils as cu
import random
from Crypto.Cipher import AES

def DetectEncryptionType(msgIn, blockSize):
    numBlocks = len(msgIn) / blockSize
    
    blocks = []
    for k in xrange(0, numBlocks):            
        sub = msgIn[k*blockSize : (k+1)*blockSize]            
        blocks.append(sub)


    blockSet = set(blocks)        
    if len(blockSet) != numBlocks:        
        return 'ecb'
    else:
        return 'cbc'

def EncryptionOracle(msgIn):
    keySize = 16
    key = cu.RandAESkey(keySize)    
    initVec = cu.RandAESkey(keySize)
    randBefore = ''
    randAfter = ''
    beforeCt = random.randint(5,10)
    afterCt = random.randint(5,10)
    for idb in xrange(0, beforeCt):
        randBefore = randBefore + chr(random.randint(0,255))
    for ida in xrange(0, afterCt):
        randAfter = randAfter + chr(random.randint(0,255))

    padmsg = randBefore + msgIn + randAfter
    
    aesMode = random.randint(0,1)
    if len(padmsg) % keySize != 0:        
        thePad = cu.GetPad(padmsg, keySize)
        padmsg = padmsg + thePad

    if aesMode == 0:
        cipher = AES.new(key, AES.MODE_ECB)
        eMsg = cipher.encrypt(padmsg)
        return eMsg, 'ecb'
    elif aesMode == 1:
        cipher = AES.new(key, AES.MODE_CBC, initVec)
        eMsg = cipher.encrypt(padmsg)
        return eMsg, 'cbc'

def Main():
    blockLen = 16

    with open('testfile.txt', 'r') as txtfile:
        data=txtfile.read()

    trials = 100
    truths = ['']*trials
    guesses = ['']*trials
    numCorrect = 0
    for idx in xrange(0, trials):
        emsg, eType = EncryptionOracle(data)
        guess = DetectEncryptionType(emsg, blockLen)
        truths[idx] = eType
        guesses[idx] = guess        
        if eType == guess:
            print truths[idx] + ' || ' + guesses[idx] + ' || correct!'
            numCorrect = numCorrect + 1
        else:
            print truths[idx] + ' || ' + guesses[idx] + ' || wrong.'

    print "success rate: " + str(1.0 * numCorrect / trials)


Main()
