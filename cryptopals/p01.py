

#hex 49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d

#base64 SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t


import base64

def hexToBase64(hexString):

	raw = hexString.decode('hex')
	b64string = base64.b64encode(raw)
	return b64string

hh = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'

ans = hexToBase64(hh)

print ans