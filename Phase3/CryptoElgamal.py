from CryptoUtility import *
from CryptoP1 import *
from CryptoP2 import *
import Crypto.Random.random as Cryprand

def readPlainText(filename, p):
    blocksize = p.bit_length() - 1 
    f = open(filename, "rb")
    data = f.read()
    f.close()
    # print("Data : " + str(data))
    data = bytes_to_bits_binary(data)
    signature = sign(data)
    # print("DataB : " + str(data))
    # print(bits_to_bytes(data))
    block = []
    for i in range(0, len(data) + 1, blocksize):
        ele = data[i:i + blocksize]
        if len(ele) != blocksize:
            ele += '0' * (blocksize - len(ele))
        block.append(int(ele, 2))
    block.append(signature['r'])
    block.append(signature['s'])
    return block

def writePlainText(output, p, file, pkSender):
    blocksize = p.bit_length() - 1
    res = ''
    signature = {'r' : output[-2], 's' : output[-1]}
    output = output[:-2]
    for ele in output:
        b = bin(ele)[2:].zfill(blocksize)
        res += b
    res = res + '0' * (8 - (len(res) % 8))
    while res[-8:] == '0' * 8:
        res = res[:-8]
    verify(res, signature, pkSender)
    res = bits_to_bytes(res)
    f = open(file, "wb")
    f.write(res)
    f.close()

def sign(msg):
    pk = readPublicKeyWho('me')
    sk = readPrivateKey()
    k = Cryprand.randint(1, pk['p'] - 2)
    while (GCD(k, pk['p'] - 1) != 1):
        k = Cryprand.randint(1, pk['p'] - 2)
    r = FastExpo(pk['g'], k, pk['p'])
    ik = FindInverse(k, pk['p'] - 1)
    s = (ik * ((RWHash(msg, pk['p']) - ((sk['u'] * r) % (pk['p'] - 1))) % (pk['p'] - 1))) % (pk['p'] - 1) 
    return {'r' : r, 's' : s}

def verify(msg, signature, pk):
    test1 = FastExpo(pk['g'], RWHash(msg, pk['p']), pk['p'])
    yr = FastExpo(pk['y'], signature['r'], pk['p'])
    rs = FastExpo(signature['r'], signature['s'], pk['p'])
    test2 = (yr * rs) % pk['p']
    if test1 != test2:
        sel = input('This message has change, Do you want to continue read? (yes / no): ')
        if sel == 'no':
            exit(0)    

def RWHash(msg, p):
    outputSize = p.bit_length() - 1
    blockSize = outputSize * 5
    chunks = []
    res = len(msg)
    for i in range(0, len(msg), blockSize):
        chunk = msg[i:i + blockSize]
        if len(chunk) < blockSize:
            chunk += '1' * (blockSize - len(chunk))
        chunks.append(chunk)
    for chunk in chunks:
        for i in range(0, len(chunk), outputSize):
            sub = int(chunk[i:i+outputSize], 2)
            res = (res + (FastExpo(sub, (i + 1), p))) % p
    return res

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
        sender = input("Who sent : ")
        output = input("Output File : ")
        sk = readPrivateKey()
        pkSender = readPublicKeyWho(sender)
        NewCipher = inputCipher(cipher, sk["p"])
        plainText = ElgamalDecrypt(sk, NewCipher)
        writePlainText(plainText, sk["p"], output, pkSender)
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