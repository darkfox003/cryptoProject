from CryptoUtility import *

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

print(getNum("./Phase2/inp.txt", 30))