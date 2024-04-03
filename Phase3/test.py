from CryptoUtility import *
from CryptoElgamal import *

def isSafePrime(num):
    if IsPrime(num) and IsPrime((num - 1) // 2):
        print("True")
    else:
        print("False")

#isSafePrime(1960456983326939)
# print(RWHash('11010101011111000010101010111110000101010101010101010101010101', 17))
        
print(readPlainText('./Phase3/small.txt', 17))