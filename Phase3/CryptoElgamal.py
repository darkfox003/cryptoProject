from CryptoUtility import *
from CryptoP1 import *
from CryptoP2 import *
import Crypto.Random.random as Cryprand

def readMessage(filename):
    f = open(filename, "rb")
    data = f.read()
    f.close()
    data = bytes_to_bits_binary(data)
    return data

def writeMessage(filename, msg):
    data = bits_to_bytes(msg)
    f = open(filename, "wb")
    f.write(data)
    f.close()

def readSignature(filename, pkSender):
    f = open(filename, "rb")
    data = f.read()
    f.close()
    data = bytes_to_bits_binary(data)
    padlen = int(data[-8:], 2)
    data = data[:-8]
    for i in range(padlen):
        if data[-1] == '0':
            data = data[:-1]
    block = pkSender['p'].bit_length()
    s = data[-block:]
    data = data[:-block]
    r = data[-block:]
    data = data[:-block]
    return data, {'r' : int(r, 2), 's' : int(s, 2)}

def writeSignature(filename, msg, signature):
    allsig = signature["r"] + signature["s"]
    padlen = (8 - (len(allsig) % 8)) % 8
    if padlen != 0:
        allsig += '0' * padlen
    allsig += bin(padlen)[2:].zfill(8)
    msg_sig = msg + allsig
    msg_sig = bits_to_bytes(msg_sig)
    f = open(filename, "wb")
    f.write(msg_sig)
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
    return {'r' : bin(r)[2:].zfill(pk['p'].bit_length()), 's' : bin(s)[2:].zfill(pk['p'].bit_length())}

def verify(msg, signature, pk):
    test1 = FastExpo(pk['g'], RWHash(msg, pk['p']), pk['p'])
    yr = FastExpo(pk['y'], signature['r'], pk['p'])
    rs = FastExpo(signature['r'], signature['s'], pk['p'])
    test2 = (yr * rs) % pk['p']
    if test1 != test2:
        sel = input('This message has change, Do you want to continue read? (yes / no): ')
        if sel == 'no':
            exit(0)
    else :
        print("This message has not change")    

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
        res = circular_right_shift(res, 16, outputSize)
    return res

def main():
    mode = int(input("Input Mode (1:KeyGen, 2:Encrypt, 3:Decrypt, 4:AddPk, 5:sign, 6:verify) : "))
    if mode == 1:
        keyFile = input("What Key File : ")
        if keyFile == '':
            p = GenPrime("./Phase2/inp.txt", 100)
        else:
            p = GenPrime(keyFile, 400)
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
        pkfile = input("What File : ")
        f = open(pkfile, "r")
        data = f.read()
        f.close()
        data = data.split(' ')
        pk = {"p": data[0], "g": data[1], "y": data[2]}
        writePublicKey(owner, pk)
    elif mode == 5:
        msgFile = input("Message File : ")
        output = input("Output File : ")
        msg = readMessage(msgFile)
        signature = sign(msg)
        writeSignature(output, msg, signature)
    elif mode == 6:
        filename = input("Input File : ")
        sender = input("Who sent : ")
        output = input("Output File : ")
        pkSender = readPublicKeyWho(sender)
        msg, signature = readSignature(filename, pkSender)
        verify(msg, signature, pkSender)
        writeMessage(output, msg)
    else:
        print("Mode error!!")

if __name__ == '__main__':
    main()