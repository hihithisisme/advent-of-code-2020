package day2_21;

import utils.Printer;
import utils.Reader;

import java.io.IOException;
import java.util.List;

public class Main {
    public static void main() throws IOException {
        final List<String> in = Reader.ReadFile("src/day2_21/input.txt");

        Printer.printAns(partOne(in));
        Printer.printAns(partTwo(in));
    }

    public static int partTwo(List<String> in) {
        int distance = 0;
        int depth = 0;
        int aim = 0;

        for (final String s : in) {
            String[] split = s.split(" ");
            String command = split[0];
            int unit = Integer.parseInt(split[1]);

            switch (command) {
                case "forward":
                    distance = distance + unit;
                    depth = depth + aim * unit;
                    break;
                case "down":
                    aim = aim + unit;
                    break;
                case "up":
                    aim = aim - unit;
                    break;
            }
        }

        return distance * depth;

    }

    public static int partOne(List<String> in) {
        int distance = 0;
        int depth = 0;

        for (final String s : in) {
            String[] split = s.split(" ");
            String command = split[0];
            int unit = Integer.parseInt(split[1]);

            switch (command) {
                case "forward":
                    distance = distance + unit;
                    break;
                case "down":
                    depth = depth + unit;
                    break;
                case "up":
                    depth = depth - unit;
                    break;
            }
        }

        return distance * depth;
    }
}
