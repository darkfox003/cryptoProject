import java.util.Random;

public class CryptoUtility {

    static int x;
    static int y;

    static int gcd(int a, int b)
    {
        if (b == 0)
            return a;

        return gcd(b, a % b);
    }

    static long fastExpo(long base, long exp, long N)
    {
        long t = 1L;
        while (exp > 0) {
 
            if (exp % 2 != 0)
                t = (t * base) % N;
 
            base = (base * base) % N;
            exp /= 2;
        }

        return t % N;
    }

      static boolean lehmann(Long n)
    {
     
        Random rand = new Random(); 
         
        Long a = rand.nextLong(n - 3) + 2;
     
        Long e = (n - 1) / 2;

        int t = 100;
     
        while(t > 0)
        {
     
            long result = fastExpo(a, e, n);
     
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

    static int gcdExtended(int A, int M)
    {
 
        int m0 = M;
        int b1 = 1, b2 = 0;
        
        System.out.println(A + "\t" + M + "\t0\t" + b1 + "\t" + b2);
        if (M == 1)
            return 0;
            
        while (M > 1) {
            // q is quotient
            int q = A / M;
            
            // m is remainder now, process
            // same as Euclid's algo
            int t = M;
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
            b2 += m0;
 
        return b2;
    }

    static int modInverse(int A, int M)
    {
        if (gcd(A, M) != 1) {
            System.out.println("Inverse doesn't exist");
            return -1;
        }
        return gcdExtended(A, M);
    }
}
