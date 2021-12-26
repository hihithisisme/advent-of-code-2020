package day7_21;

import utils.Printer;
import utils.Reader;

import java.io.IOException;
import java.util.Collections;
import java.util.IntSummaryStatistics;
import java.util.List;

public class Main {

    public static void main() throws IOException {
        final List<Integer> in = Reader.ReadLineAsNumbers("src/day7_21/input.txt");

        Collections.sort(in);

        System.out.printf("mean: %s\n", in.stream().mapToInt(Integer::intValue).summaryStatistics().toString());

        Printer.printAns(partOne(in));
        Printer.printAns(partTwo(in));
    }

    public static int partOne(List<Integer> in) {
        return getFuelUsage(in, getMedian(in));
    }

    public static int partTwo(List<Integer> in) {
        final int pos = findOptimalPos2(in);
        return getFuelUsage2(in, pos);
    }

    private static int findOptimalPos2(final List<Integer> in) {
        final IntSummaryStatistics summary = in.stream().mapToInt(Integer::intValue).summaryStatistics();

        int pos = summary.getMin();
        int minFuelUsage = Integer.MAX_VALUE;
        for (int i = summary.getMin(); i <= summary.getMax(); i++) {
            int fuelUsage = getFuelUsage2(in, i);
            if (fuelUsage < minFuelUsage) {
                pos = i;
                minFuelUsage = fuelUsage;
            }
        }

        return pos;
    }

    private static int getFuelUsage2(List<Integer> in, int pos) {
        return in.stream().mapToInt(i -> {
            int diff = Math.abs(i - pos);
            return (diff + 1) * diff / 2;
        }).sum();
    }

    private static int getFuelUsage(List<Integer> in, int pos) {
        return in.stream().mapToInt(i -> Math.abs(i - pos)).sum();
    }

    private static int getMedian(List<Integer> in) {
        if (in.size() % 2 == 0) {
            return in.get(in.size() / 2);

        } else {
            int l = (in.size() - 1) / 2;
            int h = (in.size() + 1) / 2;

            return Math.min(getFuelUsage(in, l), getFuelUsage(in, h));
        }
    }
}
