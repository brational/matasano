#set1_7.py

'''
AES in ECB mode
The Base64-encoded content in this file has been encrypted via AES-128 in ECB mode under the key

"YELLOW SUBMARINE".
(case-sensitive, without the quotes; exactly 16 characters; I like "YELLOW SUBMARINE" because it's exactly 16 bytes long, and now you do too).

Decrypt it. You know the key, after all.
'''

import base64
from Crypto.Cipher import AES

def GetPad(msg, padSize):
    
    padNeeded = len(msg) % padSize    
    pad = ''
    for k in xrange(0, padNeeded):
        pad = pad + '0'
    return pad

def RemovePad(msg, padToRemove):
    
    if len(padToRemove) == 0:
        return msg
    else:
        msg = msg[:-len(padToRemove)]
        return msg

def BreakAESecb(msg, key):

    padSize = len(key)
    thePad = GetPad(msg, padSize)

    msg = msg + thePad

    cipher = AES.new(key, AES.MODE_ECB)
    answer = cipher.decrypt(msg)
    answer = RemovePad(answer, thePad)
    return answer


def main():
    theKey = 'YELLOW SUBMARINE'

    with open('t7.txt', 'r') as txtfile:
        data=txtfile.read()

    data = base64.b64decode(data)    

    ans = BreakAESecb(data, theKey)

    print ans

main()