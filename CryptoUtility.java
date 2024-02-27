import java.util.Random;

public class CryptoUtility {

    static long GCD(long a, long b)
    {
        if (b == 0)
            return a;

        return GCD(b, a % b);
    }

    static long FastExpo(long base, long exp, long N)
    {
        long t = 1L;
        while (exp > 0) {
 
            if (exp % 2 != 0)
                t = (t * base) % N;
 
            base = (base * base) % N;
            //System.out.println(t + " " + base);
            exp /= 2;
        }

        return t % N;
    }

    /*
     * 11 -> 1011 -> 5 101 -> 2 -> 10 -> 1 -> 1 -> 0
     * t = 1 * 5 = 5 * 4 = 6 * 4 = 3
     * base = 5 * 5 = 4 * 4 = 2 * 2 = 4 * 4 = 2
     * 
     * 5 ^ 11 mod 7
     * 11 = 1011
     * 0 5                  1
     * 1 5 * 5 = 4 mod 7    1
     * 2 4 * 4 = 2 mod 7    0
     * 3 2 * 2 = 4 mod 7    1
     * 4 * 4 * 5 = 80 mod 7 = 3 mod 7
     */

    static boolean IsPrime(Long n)
    {
     
        Random rand = new Random(); 
         
        Long a = rand.nextLong(n - 3) + 2;
     
        Long e = (n - 1) / 2;

        int t = 100;
     
        while(t > 0)
        {

            if (GCD(a, n) > 1)
                return false;
     
            long result = FastExpo(a, e, n);
     
            if((result % n) == 1 || (result % n) == (n - 1))
            {
                a = rand.nextLong(n - 3) + 2;
                t -= 1;
            }
     
            else {
                //System.out.println(result);
                return false;
            }
                 
        }
         
        return true;
    }

    static long FindInverse(long A, long M)
    {
 
        long m0 = M;
        long b1 = 1, b2 = 0;
        
        //System.out.println(A + "\t" + M + "\t0\t" + b1 + "\t" + b2 );
            
        while (M > 1) {
            // q is quotient
            long q = A / M;
            
            // m is remainder now, process
            // same as Euclid's algo
            long t = M;
            M = A % M;
            A = t;
                
            // Update x and y
            t = b2;
            b2 = b1 - q * b2;
            b1 = t;
            //System.out.println(A + "\t" + M + "\t" + q + "\t" + b1 + "\t" + b2 );
        }
            
        // Make x positive
        if (b2 < 0)
            b2 = (b2 + m0) % m0;
 
        return b2;
    }

    static long Power(long base, long exp) {
        long res = base;

        for (int i = 0; i < exp; i++) {
            res *= base;
        }

        return res;
    }
}
