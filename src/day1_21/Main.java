package day1_21;

import utils.Printer;
import utils.Reader;

import java.io.IOException;

public class Main {
    public static void main() throws IOException {
        final int[] in = Reader.ReadFile("src/day1_21/input.txt").stream().mapToInt(Integer::parseInt).toArray();

        Printer.printAns(partOne(in));
        Printer.printAns(partTwo(in));
    }

    private static int partOne(final int[] in) {
        int count = 0;

        for (int i = 1; i < in.length; i++) {
            if (in[i] > in[i - 1]) {
                count++;
            }
        }

        return count;
    }

    private static int partTwo(final int[] in) {
        int count = 0;

        for (int i = 3; i < in.length; i++) {
            if (in[i] > in[i - 3]) {
                count++;
            }
        }

        return count;
    }
}
