package day5_21;

import utils.Printer;
import utils.Reader;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.stream.Collectors;

public class Main {

    public static void main() throws IOException {
        final List<String> in = Reader.ReadFile("src/day5_21/input.txt");

        final List<Line> lines = readAllLines(in);

        Printer.printAns(partOne(lines));
        Printer.printAns(partTwo(lines));

        Line line = new Line("1,1 -> 3,3");
        System.out.println(line.getAllCoordinates());
    }

    public static int partOne(List<Line> in) {
        final List<Line> lines = in.stream().filter(Line::isStraightLine).collect(Collectors.toList());

        HashMap<Point, Integer> map = new HashMap<>();
        lines.stream().map(Line::getAllCoordinates)
                .forEach(li -> li.forEach(c -> {
                    if (map.containsKey(c)) {
                        map.put(c, map.get(c) + 1);
                    } else {
                        map.put(c, 1);
                    }
                }));

        return ((int) map.values().stream().filter(v -> v >= 2).count());
    }

    public static int partTwo(List<Line> lines) {
        HashMap<Point, Integer> map = new HashMap<>();
        lines.stream().map(Line::getAllCoordinates)
                .forEach(li -> li.forEach(c -> {
                    if (map.containsKey(c)) {
                        map.put(c, map.get(c) + 1);
                    } else {
                        map.put(c, 1);
                    }
                }));

        return ((int) map.values().stream().filter(v -> v >= 2).count());
    }

    private static List<Line> readAllLines(List<String> in) {
        return in.stream().map(Line::new).collect(Collectors.toList());
    }
}
