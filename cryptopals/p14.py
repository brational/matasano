# prob 14

# prob 12

'''
Byte-at-a-time ECB decryption (Simple)
Copy your oracle function to a new function that encrypts buffers under ECB mode using a consistent but unknown key (for instance, assign a single random key, once, to a global variable).

Now take that same function and have it append to the plaintext, BEFORE ENCRYPTING, the following string:

Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK
Spoiler alert.
Do not decode this string now. Don't do it.
'''

import cutils as cu
import base64
import random

class ECBdecryption:

    def FeedOracle(self, msgIn):    
        msgOut = cu.ecbEncrypt(self.thePrefix + msgIn, self.theKey)
        return msgOut

    def FindBlockSize(self):
        block_sizes = {}
        minDist = 10000.0    
        for kSize in xrange(1, 40):
            dummy = 'A'*kSize
            moreDummy = 'b'*200
            cipher = self.FeedOracle(dummy + moreDummy)          
            
            meanDist = 0;
             
            substr1 = cipher[0 : kSize]
            substr2 = cipher[kSize : 2*kSize]
            substr3 = cipher[2*kSize : 3*kSize]
            substr4 = cipher[3*kSize : 4*kSize]

            hDist1 = cu.HammingDist(substr1, substr2)
            hDist2 = cu.HammingDist(substr1, substr3)
            hDist3 = cu.HammingDist(substr1, substr4)
            hDist4 = cu.HammingDist(substr2, substr3)
            hDist5 = cu.HammingDist(substr2, substr4)
            hDist6 = cu.HammingDist(substr3, substr4)

            hDist = hDist1 + hDist2 + hDist3 + hDist4 + hDist5 + hDist6
            hDist = 1.0 * hDist / kSize                        

            meanDist = 1.0 * hDist / 6              
            #print str(kSize) + ' , ' + str(meanDist)
            if meanDist < minDist:   
                minDist = meanDist                         
                block_sizes[kSize] = minDist
                    
        #print block_sizes
        return min(block_sizes, key = block_sizes.get)

    def GenerateLastBytes(self, bytesDict, blockSize, prefixSize):
        
        dummy = 'A'*(blockSize - prefixSize - 1)
        for bb in xrange(0, 256):
            cipher = self.FeedOracle(dummy + chr(bb))        
            bytesDict[cipher] = chr(bb)

    def GetRandPrefix(self):
        prefixSize = random.randint(1,16)
        return cu.RandBytes(prefixSize)

    def FindPrefixSize(self, unknown):
        prevCipher = self.FeedOracle(unknown)
        for dd in xrange(1, 16):
            dummy = 'A'*dd
            cipher = self.FeedOracle(dummy + unknown)
            compare = cu.StringXOR(prevCipher, cipher)            
            if compare[:16] == chr(0)*16:                
                return 16 - (dd - 1)
          
            prevCipher = cipher


    def __init__(self):
        
        # make "unknown" key
        self.theKey = cu.RandAESkey(16)

        tbd64 = 'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'

        tbd = base64.b64decode(tbd64)

        # # find "unknown" key size 
        # blockSize = self.FindBlockSize()
        # print blockSize
       
        # # detect which AES mode
        # dummy = 'A'*blockSize*20
        # modeCheck = self.FeedOracle(dummy)
        # aesMode = cu.DetectEncryptionType(modeCheck, blockSize) 
        # print aesMode

        blockSize = 16     
        self.thePrefix = self.GetRandPrefix()   
        print len(self.thePrefix)

        prefSize = self.FindPrefixSize(tbd)
        print prefSize
        # generate last byte dict
        bytesDict = {}
        self.GenerateLastBytes(bytesDict, blockSize, prefSize)
        #print bytesDict

        answer = ''
        dummy = 'A'*(blockSize - prefSize - 1)
        for pos in xrange(0, len(tbd)):
            searchstr = tbd[pos:]
            cipher = self.FeedOracle(dummy + searchstr)
            firstBlock = cipher[:16]            
            lastByte = bytesDict[firstBlock]
            answer = answer + lastByte

        print answer
        

if __name__ == '__main__':
    ECBdecryption()
