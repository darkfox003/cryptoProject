import Crypto.Random.random as Cryprand
from CryptoUtility import *
from CryptoP1 import *
from math import sqrt

def GenGenerator(p):
    rand = Cryprand.randint(2, p - 1)
    #rand = FastExpo(rand, 2, p)
    if IsPrime((p - 1) // 2):
        n = (p - 1) // 2
        if FastExpo(rand, n, p) != 1:
            return rand
        else:
            return -rand + p
    else:
        s = GenPrimeFactor(p - 1)
        while not CheckGenerator(rand, s, p):
            #rand = random.randint(2, p - 1)
            rand = (rand + 1) % p
            print(rand)
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
    u = Cryprand.randint(2, p - 1)
    y = FastExpo(g, u, p)
    print("Public key (p, g, y) : (" + str(p) + ", " + str(g) + ", " + str(y) + ")")
    #print("Private key : " + str(u))
    return {"p" : p, "g" : g, "y" : y}, {"u" : u, "p" : p}

def ElgamalEncrypt(pk, txt):
    #res = StringToAscii(txt)
    cipher = []
    for ele in txt:
        k =  Cryprand.randint(2, pk["p"] - 1)
        while GCD(k, pk["p"] - 1) != 1:
            k = Cryprand.randint(2, pk["p"] - 1)
        #print(k, end=' ')
        cipher.append(GenAB(pk, k, ele))
    return cipher

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
    # print("Data : " + str(data))
    data = bytes_to_bits_binary(data)
    # print("DataB : " + str(data))
    # print(bits_to_bytes(data))
    block = []
    for i in range(0, len(data) + 1, blocksize):
        ele = data[i:i + blocksize]
        if len(ele) != blocksize:
            ele += '0' * (blocksize - len(ele))
        block.append(int(ele, 2))
    return block

def writePlainText(output, p, file):
    blocksize = p.bit_length() - 1
    res = ''
    for ele in output:
        b = bin(ele)[2:].zfill(blocksize)
        res += b
    res = bits_to_bytes(res)
    f = open(file, "wb")
    f.write(res)
    f.close()

def outputCipher(cipher, p, file):
    blocksize = p.bit_length()
    f = open(file, "wb")
    res = ''
    for ele in cipher:
        a = (bin(ele["a"])[2:]).zfill(blocksize)
        b = (bin(ele["b"])[2:]).zfill(blocksize)
        res += a
        res += b
    res = bits_to_bytes(res)
    f.write(res)
    f.close()

def inputCipher(file, p):
    f = open(file, "rb")
    data = f.read()
    f.close()
    data = bytes_to_bits_binary(data)
    blocksize = p.bit_length()
    data = [data[i:i+blocksize] for i in range(0, len(data), blocksize)]
    res = []
    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            ele = {}
            ele["a"] = int(data[i], 2)
            ele["b"] = int(data[i + 1], 2)
            res.append(ele)
    return res

def readPublicKey():
    f = open("./Phase2/pk.txt", "r")
    data = f.read()
    f.close()
    data = data.split('\n')
    res = {}
    for ele in data:
        ele = ele.split(' ')
        if len(ele) > 1:
            res[ele[0]] = {"p": int(ele[1]), "g": int(ele[2]), "y": int(ele[3])} 
    return res

def readPublicKeyWho(who):
    pkList = readPublicKey()
    return pkList[who]

def readPrivateKey():
    f = open("./Phase2/sk.txt", "r")
    data = f.read().split(' ')
    f.close()
    return {"u" : int(data[0]), "p" : int(data[1])}

def writePublicKey(owner, pk):
    pkList = readPublicKey()
    pkList[owner] = pk
    out = ""
    for pk in pkList:
        out += pk + " " + str(pkList[pk]["p"]) + " " + str(pkList[pk]["g"]) + " " + str(pkList[pk]["y"]) + "\n"
    f = open("./Phase2/pk.txt", "w")
    f.write(out)
    f.close()

def writePrivateKey(sk):
    out = "" + str(sk["u"]) + " " + str(sk["p"])
    f = open("./Phase2/sk.txt", "w")
    f.write(out)
    f.close()

def main():
    mode = int(input("Input Mode (1:KeyGen, 2:Encrypt, 3:Decrypt, 4:AddPk) : "))
    if mode == 1:
        keyFile = input("What Key File : ")
        if keyFile == '':
            p = GenPrime("./Phase2/inp.txt", 50)
        else:
            p = GenPrime(keyFile, 50)
        pk, sk = ElgamalKeyGen(p)
        writePublicKey("me", pk)
        writePrivateKey(sk)
    elif mode == 2:
        file = input("What File : ")
        who = input("Send to : ")
        output = input("Output File : ")
        lfile = file.split('.')
        lfile = lfile[len(lfile) - 1]
        pkWho = readPublicKeyWho(who)
        readF = readPlainText(file, pkWho["p"])
        cipher = ElgamalEncrypt(pkWho, readF)
        if output == '':
            outputCipher(cipher, pkWho["p"], "output."+lfile)
        else:
            outputCipher(cipher, pkWho["p"], output)
    elif mode == 3:
        cipher = input("Cipher File : ")
        output = input("Output File : ")
        sk = readPrivateKey()
        NewCipher = inputCipher(cipher, sk["p"])
        plainText = ElgamalDecrypt(sk, NewCipher)
        writePlainText(plainText, sk["p"], output)
    elif mode == 4:
        owner = input("Who is owner : ")
        p = int(input("p : "))
        g = int(input("g : "))
        y = int(input("y : "))
        pk = {"p": p, "g": g, "y": y}
        writePublicKey(owner, pk)
    else:
        print("Mode error!!")

if __name__ == '__main__':
    main()
