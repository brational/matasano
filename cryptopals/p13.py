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
        elif ord(it) < 16:
            print ord(it)
            next = 'done'
            outs[key] = val        
        else:
            if next == 'key':
                key += it
            elif next == 'val':
                val += it

    if next != 'done':
        outs[key] = val
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
    prof['uid'] = random.randint(10,99)
    prof['role'] = 'user'

    return encodeProfile(prof)

def Oracle(key, profIn):
    encodedProf = profile_for(profIn)
    eMsg = cu.ecbEncrypt(encodedProf, key)
    return eMsg

def IsAdmin(msg, key):
    dMsg = cu.ecbDecrypt(msg, key)
    print dMsg
    cookie = ParseCookie(dMsg)
    print cookie
    if cookie['role'] == 'admin':
        return True
    else:
        return False

def Main():

    #cookieString = 'foo=bar&baz=qux&zap=zazzle'
    #formatted = ParseCookie(cookieString)
    #print formatted

    theKey = cu.RandAESkey(16)

    m1 = Oracle(theKey, "foody@bar.com")    

    fakestr = 'm'*26 + 'admin' + chr(4)*11 
    m2 = Oracle(theKey, fakestr)        

    mm = m1[0:32] + m2[32:48]

    ans = IsAdmin(mm, theKey)
    print ans

Main()