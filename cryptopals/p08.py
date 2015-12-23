#prob8 

'''
Detect AES in ECB mode
In this file are a bunch of hex-encoded ciphertexts.

One of them has been encrypted with ECB.

Detect it.

Remember that the problem with ECB is that it is stateless and deterministic; 
the same 16 byte plaintext block will always produce the same 16 byte ciphertext.
'''

import cutils as cu

def main():

    lines = [line.rstrip('\n') for line in open('t8.txt')]

    keepers = []
    for hexline in lines:

        line = hexline.decode('hex')

        numBlocks = len(line) / 16
        
        blocks = []
        for k in xrange(0, numBlocks):            
            sub = line[k*16 : (k+1)*16]            
            blocks.append(sub)


        blockSet = set(blocks)        
        if len(blockSet) != numBlocks:
            print len(blockSet)
            keepers.append(blockSet)


    print len(keepers)

    # for shits and giggles
    #theKey = 'YELLOW SUBMARINE'
    #themsg = ''
    #for bb in keepers[0]:
    #    themsg = themsg + bb
    #print themsg
    #guess = cu.BreakAESecb(themsg, theKey)
    #print guess


main()