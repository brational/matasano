# prob 15

import cutils as cu


def Main():

    tests = []
    test0 = 'ICE ICE BABY'
    test1 = 'ICE ICE BABY\x04\x04\x04\x04'
    test2 = "ICE ICE BABY\x05\x05\x05\x05"
    test3 = "ICE ICE BABY\x01\x02\x03\x04"

    tests.append(test0)
    tests.append(test1)
    tests.append(test2)
    tests.append(test3)

    for test in tests:
        ans = cu.RemovePad_PKCS7(test)
        print ans


Main()