import random
from CryptoUtility import *
from CryptoP1 import *
from math import sqrt

def GenGenerator(p):
    rand = random.randint(2, p)
    #rand = FastExpo(rand, 2, p)
    if IsPrime(int((p - 1) / 2)):
        n = int((p - 1) / 2)
        if FastExpo(rand, n, p) != 1:
            return rand
        else:
            return -rand + p
    else:
        s = GenPrimeFactor(p - 1)
        while not CheckGenerator(rand, s, p):
            rand = random.randint(2, p)
            #rand = FastExpo(rand, 2, p)
        return rand


def CheckGenerator(g, s, p):
    if GCD(g, p) != 1:
        return False
    for i in s:
        if (FastExpo(g, (p - 1) // i, p) == 1):
            return False
    return True

def GenPrimeFactor(p):
    s = set()

    while (p % 2 == 0):
        s.add(2)
        p //= 2
    
    for i in range(3, int(sqrt(p)), 2):
        while (p % i == 0):
            s.add(i)
            p //= i

    if (p > 2):
        s.add(p)
    
    return s

def ElgamalKeyGen(p):
    g = GenGenerator(p)
    u = random.randint(2, p)
    y = FastExpo(g, u, p)
    print("Public key (p, g, y) : (" + str(p) + ", " + str(g) + ", " + str(y) + ")")
    print("Private key : " + str(u))
    return {"p" : p, "g" : g, "y" : y}, {"u" : u, "p" : p}

def ElgamalEncrypt(pk, txt):
    #res = StringToAscii(txt)
    cipher = []
    for ele in txt:
        k =  random.randint(2, pk["p"])
        while GCD(k, pk["p"] - 1) != 1:
            k = random.randint(2, pk["p"])
        #print(k, end=' ')
        cipher.append(GenAB(pk, k, ele))
    return cipher

def StringToAscii(txt):
    res = [ord(ele) for ele in txt]
    print(res)
    return res

def GenAB(pk, k, txt):
    a = FastExpo(pk["g"], k, pk["p"])
    b = (FastExpo(pk["y"], k, pk["p"]) * txt) % pk["p"]
    return {"a" : a, "b" : b}

def ElgamalDecrypt(sk, cipher):
    res = []
    exp = sk["p"] - 1 - sk["u"]
    for ele in cipher:
        res.append((FastExpo(ele["a"], exp, sk["p"]) * ele["b"]) % sk["p"])
    return res

def readPlainText(filename, p):
    blocksize = p.bit_length() - 1
    f = open(filename, "rb")
    data = f.read()
    f.close()
    print("Data : " + str(data))
    data = bytes_to_bits_binary(data)
    print("DataB : " + str(data))
    print(bits_to_bytes(data))
    block = []
    for i in range(0, len(data) + 1, blocksize):
        ele = data[i:i + blocksize]
        if len(ele) != blocksize:
            ele += '0' * (blocksize - len(ele))
        block.append(int(ele, 2))
    return block

def writePlainText(output, p):
    blocksize = p.bit_length() - 1
    res = ''
    for ele in output:
        b = bin(ele)[2:]
        if len(b) < blocksize:
            b = ('0' * (blocksize - len(b))) + b
        res += b
    return res

p = GenPrime("./Phase2/inp.txt", 30)
print(p.bit_length())
pk, sk = ElgamalKeyGen(p)
readF = readPlainText("./Phase2/sample.txt", p)
print(readF)
cipher = ElgamalEncrypt(pk, readF)
print("Cipher : ", end='')
print(cipher)
# # c = b''
# # for ele in cipher:
# #     c += int.to_bytes(ele["a"], 3)
# #     c += int.to_bytes(ele["b"], 3)
# # print(c)

plain = ElgamalDecrypt(sk, cipher)
print("Plain : ", end='')
print(plain)
res = writePlainText(plain, p)
print(res)
print(bits_to_bytes(res))
# b = ''
# for ele in plain:
#     bits = bin(ele)[2:]
#     if len(bits) < (p.bit_length() - 1):
#         bits = ('0' * ((p.bit_length() - 1) - len(bits))) + bits
#     b += bits
# print(b)
# print(bits_to_bytes(b))
