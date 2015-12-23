#set1_2.py


'''
Write a function that takes two equal-length buffers and produces their XOR combination.

If your function works properly, then when you feed it the string:

1c0111001f010100061a024b53535009181c
... after hex decoding, and when XOR'd against:

686974207468652062756c6c277320657965
... should produce:

746865206b696420646f6e277420706c6179
'''


def eqLengthXOR(hexInA, hexInB):

    raw1 = hexInA.decode('hex')
    raw2 = hexInB.decode('hex')

    result = ''
    for idx in xrange(0, len(raw1)):
        result = result + chr(ord(raw1[idx]) ^ ord(raw2[idx]))

    return result.encode('hex')


#begin main

h1 = '1c0111001f010100061a024b53535009181c'
h2 = '686974207468652062756c6c277320657965'
ans = eqLengthXOR(h1,h2)
print ans


