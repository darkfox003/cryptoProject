import java.io.FileInputStream;
import java.io.InputStream;

public class CryptoProject {
    public static void main(String[] args) {
        Long num = getNum("download.jpg", 30);
        System.out.println(num);   
        System.out.println(CryptoUtility.lehmann(num));
        System.out.println("Next Prime is : " + findPrime(num, (Long)Math.round(Math.pow(2, 30)) - 1));
        //System.out.println(CryptoUtility.lehmann(3532802839L));
    }

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

    static Long findPrime(Long start, Long bound) {
        while (!CryptoUtility.lehmann(start)) {
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
}