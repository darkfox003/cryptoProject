from CryptoUtility import *

def GenPrime(file, n):
    num = getNum(file, n)
    # print("Number from file :", num)
    if num % 2 == 0:
        num += 1
    while not IsPrime(num) or not IsPrime((num * 2) + 1):
        num += 2
    return ((num * 2) + 1)

def getNum(file, n):
    f = open(file, "rb")
    data = f.read()
    f.close()
    data = bytes_to_bits_binary(data)
    while data[0] == '0':
        data = data[1:]
    if len(data) < n:
        data = data + ('0' * (n - len(data)))
    else:
        data = data[:n]
    return int(data, 2)

def findPrime(start, bound):
    if start % 2 == 0:
        start += 1
    
    while (not IsPrime(start)):
        if (start > bound):
            print("Out of Bound")
            exit(0)

        start += 2
    return start