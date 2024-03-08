from math import pow
def test(a, p):
    s = set()
    for i in range(1, p):
        num = FastExpo(a, i, p)
        if num in s:
            print(str(a) + " " + str(i) + " " + str(FastExpo(a, i, p)))
        s.add(num)
    # print(s)
    print(len(s))
    print("done")

def FastExpo(base, exp, mod):
    t = 1
    while(exp > 0): 
 
        # for cases where exponent
        # is not an even value
        if (exp % 2 != 0):
            t = (t * base) % mod
 
        base = (base * base) % mod
        exp = int(exp / 2)
    return t % mod

def chekAlgo(b):
    print("\t", end='')
    for i in range(1, b):
        print(i, end='\t')
    print('')
    for i in range(2, b):
        print(i, end='\t')
        for j in range(1, b):
            print(FastExpo(i, j, b),end='\t')
        print('')
    print('')


# print(FastExpo(705, 25, 761))
# print(FastExpo(705, 46, 761))
#test(718, 761)
chekAlgo(29)
        