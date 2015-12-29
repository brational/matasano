# prob 13

import cutils as cu
import random

def ParseCookie(stringIn):
    outs = {}
    key = ''
    val = ''
    next = 'key'
    for it in stringIn:        
        if it == '=':
            next = 'val'
        elif it == '&':
            next = 'key'
            outs[key] = val
            key = ''
            val = ''
        else:
            if next == 'key':
                key += it
            elif next == 'val':
                val += it

    outs[key] = val #store last one
    return outs

def encodeProfile(profileIn):    
    encodedP = 'email=' + profileIn['email'] + '&'
    encodedP += 'uid=' + str(profileIn['uid']) + '&'
    encodedP += 'role=' + profileIn['role']
    return encodedP

def profile_for(stringIn):
    clean = ''
    for k in stringIn:
        if k == '=' or k == '&':
            break
        else:
            clean += k
    prof = {}
    prof['email'] = clean
    prof['uid'] = random.randint(1,100)
    prof['role'] = 'user'

    return encodeProfile(prof)

def Oracle(key, profIn):
    encodedProf = profile_for(profIn)
    eMsg = cu.ecbEncrypt(encodedProf, key)
    return eMsg

def DecryptAndParse(msg):
    pass

def Main():

    #cookieString = 'foo=bar&baz=qux&zap=zazzle'
    #formatted = ParseCookie(cookieString)
    #print formatted

    theKey = cu.RandAESkey(16)

    msg = Oracle(theKey, "foo@bar.com")
    print msg
    print len(msg)

Main()