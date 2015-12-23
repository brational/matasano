# prob 10

import cutils as cu
import base64

from Crypto.Cipher import AES

theKey = 'YELLOW SUBMARINE'
initVector = ''
for k in xrange(0,16):
    initVector = initVector + chr(0)

with open('t10.txt', 'r') as txtfile:
    data=txtfile.read()
    
eMsg = base64.b64decode(data)
ans = cu.cbcDecrypt(eMsg, theKey, initVector)

print ans

