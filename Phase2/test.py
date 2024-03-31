from math import pow
from CryptoElgamal import *
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

from PIL import Image

def compare_images(image1_path, image2_path):
    try:
        # Open the images
        with Image.open(image1_path) as img1, Image.open(image2_path) as img2:
            # Convert images to bytes
            img1_bytes = img1.tobytes()
            img2_bytes = img2.tobytes()

            # Compare byte by byte
            if img1_bytes == img2_bytes:
                print("Images are identical.")
            else:
                print("Images are different.")

    except Exception as e:
        print("An error occurred:", e)

# Example usage
image1_path = "download.jpg"
image2_path = "res.jpg"
compare_images(image1_path, image2_path)


# p, s = ElgamalKeyGen(296255883173063500756876664533391692597)
# print(FastExpo(705, 25, 761))
# print(FastExpo(705, 46, 761))
#test(718, 761)
# chekAlgo(29)
# b = b'hello555'
# print(b.decode('utf-8'))