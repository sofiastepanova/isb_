import java.util.Random;

 public class RandomBinarySequence {
     public static String generateRandomBinarySequence() {
         Random random = new Random();
         StringBuilder binaryString = new StringBuilder(128);

         for (int i = 0; i < 128; i++) {
             binaryString.append(random.nextBoolean() ? '1' : '0');
         }

         return binaryString.toString();
     }

     public static void main(String[] args) {
         String randomSequence = generateRandomBinarySequence();
         System.out.println(randomSequence);
     }
 }