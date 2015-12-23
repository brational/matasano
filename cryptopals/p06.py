#set1_6.py

#Break repeating-key XOR

import base64
import cutils as cu

class RptKeyXor:

    def FindKeySizes(self):
        epsilon = 3.0        
        for kSize in xrange(2, 40):
            meanDist = 0;
            
            substr1 = self.data[0 : kSize]
            substr2 = self.data[kSize : 2*kSize]
            substr3 = self.data[2*kSize : 3*kSize]
            substr4 = self.data[3*kSize : 4*kSize]

            hDist1 = cu.HammingDist(substr1, substr2)
            hDist2 = cu.HammingDist(substr1, substr3)
            hDist3 = cu.HammingDist(substr1, substr4)
            hDist4 = cu.HammingDist(substr2, substr3)
            hDist5 = cu.HammingDist(substr2, substr4)
            hDist6 = cu.HammingDist(substr3, substr4)

            hDist = hDist1 + hDist2 + hDist3 + hDist4 + hDist5 + hDist6
            hDist = 1.0 * hDist / kSize                        

            meanDist = 1.0 * hDist / 6  
            #print meanDist
            if meanDist < epsilon:
                print meanDist
                self.key_sizes.append(kSize)
                
        print self.key_sizes

    def GenerateBlocks(self):
        blockList = []

        subs = ''
        for idx in xrange(0, len(self.data)):
            keyid = idx % self.KEYSIZE
            if keyid == 0:
                subs = ''
                subs = subs + (self.data[idx])
            elif keyid == self.KEYSIZE - 1:
                subs = subs + (self.data[idx])
                blockList.append(subs)
            else:
                subs = subs + (self.data[idx])

        self.positionBlocks = []
        for pos in xrange(0, self.KEYSIZE):
            posString = ''
            for block in blockList:
                posString = posString + block[pos]
            self.positionBlocks.append(posString)    

    def FindKeyVals(self, search):

        resultKey = ''
        for line in self.positionBlocks:
            aKey = cu.FindSingleKeyXOR(line, search)
            resultKey = resultKey + aKey

        return resultKey


    def __init__(self):
        #test1 = 'this is a test'
        #test2 = 'wokka wokka!!!'
        #ans = self.HammingDist(msg1, msg2)
        #print ans

        searchStr = 'etaoin shrdlu'  
        self.key_sizes = []

        with open('t6.txt', 'r') as txtfile:
            self.data=txtfile.read()
        
        self.data = base64.b64decode(self.data)
                
        self.FindKeySizes()  
        keysDict = {}     
        for trial in self.key_sizes:
            self.KEYSIZE = trial 
            self.GenerateBlocks()
            
            theKey = self.FindKeyVals(searchStr)
            print theKey
    
            decryptedMsg = cu.RepeatKeyXOR(self.data, theKey)
            print decryptedMsg[:20]

            keysDict[trial] = theKey

        # after answer is discovered uncomment this section and run to view full msg
        #bestKeySize =  #insert result here
        #answer = cu.RepeatKeyXOR(self.data, keysDict[bestKeySize])
        #print answer


if __name__ == '__main__':
    RptKeyXor()