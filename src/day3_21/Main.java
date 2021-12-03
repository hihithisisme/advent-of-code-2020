package day3_21;

import utils.Printer;
import utils.Reader;

import java.io.IOException;
import java.util.List;
import java.util.stream.Collectors;

public class Main {

    public static void main() throws IOException {
        final List<String> in = Reader.ReadFile("src/day3_21/input.txt");

        Printer.printAns(partOne(in));
        Printer.printAns(partTwo(in));
    }

    public static int partOne(List<String> in) {
        StringBuilder gamma = new StringBuilder();
        StringBuilder epsilon = new StringBuilder();

        for (int i = 0; i < in.get(0).length(); i++) {
            int count0 = countBits("0", i, in);
            int count1 = countBits("1", i, in);

            if (count0 > count1) {
                gamma.append("0");
                epsilon.append("1");
            } else if (count0 < count1) {
                epsilon.append("0");
                gamma.append("1");
            }
        }

        int gammaVal = getDecimalValue(gamma.toString());
        int epsilonVal = getDecimalValue(epsilon.toString());

        return gammaVal * epsilonVal;
    }

    public static int partTwo(List<String> in) {
        int o2Val = o2Value(0, in);
        int co2Val = co2Value(0, in);

        return o2Val * co2Val;
    }

    private static int o2Value(final int idx, final List<String> o2) {
        if (o2.size() == 1) {
            return getDecimalValue(o2.get(0));
        }

        int count0 = countBits("0", idx, o2);
        int count1 = countBits("1", idx, o2);

        String o2Add;
        if (count0 > count1) {
            o2Add = "0";
        } else {
            o2Add = "1";
        }

        List<String> newO2 = o2.stream()
                .filter(s -> Character.toString(s.charAt(idx)).equals(o2Add))
                .collect(Collectors.toList());

        return o2Value(idx + 1, newO2);
    }

    private static int co2Value(final int idx, final List<String> co2) {
        if (co2.size() == 1) {
            return getDecimalValue(co2.get(0));
        }

        int count0 = countBits("0", idx, co2);
        int count1 = countBits("1", idx, co2);

        String co2Add;
        if (count0 > count1) {
            co2Add = "1";
        } else {
            co2Add = "0";
        }

        List<String> newCO2 = co2.stream()
                .filter(s -> Character.toString(s.charAt(idx)).equals(co2Add))
                .collect(Collectors.toList());

        return co2Value(idx + 1, newCO2);
    }

    private static int countBits(String bit, int idx, List<String> in) {
        return Math.toIntExact(in.stream()
                .filter(s -> Character.toString(s.charAt(idx)).equals(bit))
                .count());
    }

    private static int getDecimalValue(final String o2) {
        return Integer.parseInt(o2, 2);
    }
}
