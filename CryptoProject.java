import java.io.FileInputStream;
import java.io.InputStream;
import java.util.Random;

public class CryptoProject {
    public static void main(String[] args) {
        System.out.println(CryptoUtility.modInverse(11, 39));
    }

    static void getNum(String file, int n) {
        try {
            InputStream in = new FileInputStream(file);
            int bytesR = -1;
            while ((bytesR = in.read()) != -1) {
                System.out.print(bytesR);
            }

            in.close();
        }
        catch(Exception e) {
            e.printStackTrace();
        }
    }
}