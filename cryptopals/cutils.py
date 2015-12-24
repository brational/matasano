#cutils.py

'''
utils file for useful functions
'''

import base64
from Crypto.Cipher import AES
import random


def hexToBase64(hexString):

    raw = hexString.decode('hex')
    b64string = base64.b64encode(raw)
    return b64string


def eqXOR(hexInA, hexInB):

    raw1 = hexInA.decode('hex')
    raw2 = hexInB.decode('hex')

    result = StringXOR(raw1, raw2)

    return result.encode('hex')

def StringXOR(msg1, msg2):

    result = ''
    for idx in xrange(0, len(msg1)):
        result = result + chr(ord(msg1[idx]) ^ ord(msg2[idx]))

    return result

def RepeatKeyXOR(msg, key):

    repeatSegments = len(key)

    result = ''
    for idx in xrange(0, len(msg)):
        keyid = idx % repeatSegments
        result = result + chr(ord(msg[idx]) ^ ord(key[keyid]))        

    return result


def HammingDist(str1, str2):

    if len(str1) != len(str2):
        print 'error: strings not equal length'
        return

    sumOffs = 0
    for idx in xrange(0, len(str1)):
        bits = bin(ord(str1[idx]) ^ ord(str2[idx]))[2:]
        for bit in bits:
            sumOffs = sumOffs + int(bit)

    return sumOffs

def oneCharXOR(rawIn, alpha):

    orig = ''
    for idx in xrange(0, len(rawIn)):
        orig = orig + chr(ord(rawIn[idx]) ^ alpha)

    return orig

def ScoreString(checkstr, search):

    searchList = []
    for letter in search:
        searchList.append(letter)    

    sumHits = 0
    for idx in xrange(0, len(checkstr)):
        if checkstr[idx] in searchList:
            sumHits = sumHits + 2    

    return sumHits

def FindSingleKeyXOR(msgIn, searchIn):

    bestScore = 0
    bestNum = -1
    for num in xrange(0, 256):
        invMsg = oneCharXOR(msgIn, num)        

        lscore = ScoreString(invMsg, searchIn)        

        if lscore > bestScore:
            bestScore = lscore;
            bestNum = num

    return chr(bestNum)

def GetPad(msg, blockSize):
    
    remainder = len(msg) % blockSize    
    if remainder == 0:
        return ''
    else:
        padNeeded = blockSize - remainder
        pad = ''
        for k in xrange(0, padNeeded):
            pad = pad + 'c'
        return pad

def ApplyPad(msg, blockSize):
    thePad = GetPad(msg, blockSize)
    return msg + thePad

def RemovePad(msg, padToRemove):
    
    if len(padToRemove) == 0:
        return msg
    else:
        msg = msg[:-len(padToRemove)]
        return msg

def ecbEncrypt(msg, key):

    blockSize = len(key)
    thePad = GetPad(msg, blockSize)
    msg = msg + thePad

    cipher = AES.new(key, AES.MODE_ECB)
    eMsg = cipher.encrypt(msg)
    
    return eMsg

def ecbDecrypt(msg, key):

    blockSize = len(key)
    thePad = GetPad(msg, blockSize)
    
    msg = msg + thePad
    
    cipher = AES.new(key, AES.MODE_ECB)
    answer = cipher.decrypt(msg)
    answer = RemovePad(answer, thePad)
    return answer

def cbcEncrypt(msg, key, iv):

    blockSize = len(key)
    msg = ApplyPad(msg, blockSize)

    numBlocks = len(msg) / blockSize

    eMsg = ''
    prevSub = iv
    for k in xrange(0, numBlocks):
        sub = msg[k*blockSize : (k+1)*blockSize]        
        chain = StringXOR(prevSub, sub)
        thisCipher = ecbEncrypt(chain, key)        
        prevSub = thisCipher
        eMsg = eMsg + thisCipher

    return eMsg

def cbcDecrypt(msg, key, iv):

    blockSize = len(key)
    thePad = GetPad(msg, blockSize)
    msg = ApplyPad(msg, blockSize)

    numBlocks = len(msg) / blockSize
    
    dMsg = ''
    prevSub = iv
    for k in xrange(0, numBlocks):
        sub = msg[k*blockSize : (k+1)*blockSize]        
        deCipher = ecbDecrypt(sub, key)
        deChain = StringXOR(deCipher, prevSub)
        prevSub = sub
        dMsg = dMsg + deChain

    dMsg = RemovePad(dMsg, thePad)
    return dMsg

def RandAESkey(keyLen):
    randKey = ''
    for k in xrange(0, keyLen):
        bb = random.randint(0, 255)
        randKey = randKey + chr(bb)

    return randKey

def EncryptionOracle(msgIn):
    keySize = 16
    key = RandAESkey(keySize)    
    initVec = RandAESkey(keySize)
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
        thePad = GetPad(padmsg, keySize)
        padmsg = padmsg + thePad

    if aesMode == 0:
        cipher = AES.new(key, AES.MODE_ECB)
        eMsg = cipher.encrypt(padmsg)
        return eMsg, 'ecb'
    elif aesMode == 1:
        cipher = AES.new(key, AES.MODE_CBC, initVec)
        eMsg = cipher.encrypt(padmsg)
        return eMsg, 'cbc'
    
