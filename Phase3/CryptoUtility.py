import Crypto.Random.random as Cryprand

def IsPrime(num):
    a = Cryprand.randint(2, num - 1)
 
    e = (num - 1) // 2
    t = 100

    while(t>0):
        result = FastExpo(a, e, num)

        if((result % num)== 1 or (result % num)==(num - 1)):
            a = Cryprand.randint(2, num)
            t -= 1
 
        else:
            return False
 
    return True

def FastExpo(base, exp, mod):
    t = 1
    while(exp > 0): 
        if (exp % 2 != 0):
            t = (t * base) % mod
 
        base = (base * base) % mod
        exp = exp // 2
    return t % mod


def GCD(a, b):
    if b == 0:
        return a
    return GCD(b, a % b)

def bytes_to_bits_binary(byte_data):
    bits_data = [bin(byte)[2:].zfill(8) for byte in byte_data]
    return ''.join(bits_data)

def bits_to_bytes(bit_string):
    if len(bit_string) % 8 != 0: 
        padded_bit_string = bit_string + '0' * (8 - (len(bit_string) % 8))
    else:
        padded_bit_string = bit_string
    chunks = [padded_bit_string[i:i+8] for i in range(0, len(padded_bit_string), 8)]
    byte_values = [int(chunk, 2) for chunk in chunks]
    while byte_values[len(byte_values) - 1] == 0:
        byte_values = byte_values[0:len(byte_values) - 1]
    # print(type(byte_values[len(byte_values) - 1]))
    return bytes(byte_values)

def bits_to_bytes_nopad(bit_string):
    if len(bit_string) % 8 != 0: 
        padded_bit_string = bit_string + '0' * (8 - (len(bit_string) % 8))
    else:
        padded_bit_string = bit_string
    chunks = [padded_bit_string[i:i+8] for i in range(0, len(padded_bit_string), 8)]
    byte_values = [int(chunk, 2) for chunk in chunks]
    return bytes(byte_values)

def Power(base, exp):
    res = base
    for i in range(exp):
        res *= base
    return res

def FindInverse(A, M):
    m0 = M
    b1 = 1
    b2 = 0

    while M > 1:
        q = A // M

        t = M
        M = A % M
        A = t

        t = b2
        b2 = b1 - q * b2
        b1 = t

    if b2 < 0:
        b2 = (b2 + m0) % m0

    return b2 % m0
