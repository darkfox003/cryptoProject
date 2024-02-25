import java.io.FileInputStream;
import java.io.InputStream;
import java.util.Arrays;
import java.util.Random;

public class CryptoProject {
    public static void main(String[] args) {
        long num = GenPrime("download.jpg", 30);
        System.out.println(Arrays.toString(GenRandomNowithinverse(num)));
    }

    static long GenPrime(String file, int n) {
        long num = getNum(file, n);
        System.out.println("Number from file : " + num);
        if (CryptoUtility.IsPrime(num)) {
            System.out.println(num + " is Prime");
        }
        else {
            System.out.println(num + " is not Prime");
            num = findPrime(num, (Long)Math.round(Math.pow(2, n)) - 1);
            System.out.println("Next Prime is : " + num);
        }
        return num;
    }
 
    //get number from file
    static long getNum(String file, int n) {
        try {
            InputStream in = new FileInputStream(file);
            byte[] bytes = in.readAllBytes();
            String res = "";
            for(byte b : bytes) {
                for (int i = 7; i >= 0; i--) {
                    // Extract each bit using bitwise AND operation
                    int bit = (b >> i) & 1;
                    // Append the bit to the StringBuilder
                    res += String.valueOf(bit);
                }
            }
            while (res.charAt(0) == '0')
                res = res.substring(1);
            res = res.substring(0, n);
            //System.out.println(res);
            in.close();
            return (Long.parseLong(res, 2));
            //System.out.println(Long.parseLong(res, 2));

        }
        catch(Exception e) {
            e.printStackTrace();
        }
        return 0;
    }

    //check prime
    static long findPrime(Long start, Long bound) {
        while (!CryptoUtility.IsPrime(start)) {
            if (start > bound) {
                break;
            }
            //System.out.println(start);
            if (start % 2 == 0)
                start ++;
            else 
                start += 2;
        }
        return start;
    }

    //generate number and find inverse
    static long[] GenRandomNowithinverse(long n) {
        Random rand = new Random();
        long randomNumber = rand.nextLong(n);
        while (CryptoUtility.GCD(randomNumber, n) != 1) {
            randomNumber = rand.nextLong(n);
        }

        return new long[]{randomNumber, CryptoUtility.FindInverse(randomNumber, n), n};
    }
}