package day15;

import utils.Reader;

import java.util.HashMap;
import java.util.List;

public class Main {

    public static void main() throws Exception {
        List<Integer> in = Reader.ReadLineAsNumbers("src/day15/input.txt");

        System.out.printf("part one answer: %s\n", game(in, 2020));
        System.out.printf("part two answer: %s\n", game(in, 30000000));
    }

    private static int game(List<Integer> in, int stopIdx) {
        HashMap<Integer, Integer> map = new HashMap<>();

        int count = 0;
        int prev = -1;
        for (int i : in) {
            count++;
            if (prev != -1) {
                map.put(prev, count - 1);
            }

            prev = i;
        }

        int spoken = -1;
        while (count < stopIdx) {
            count++;
            if (!map.containsKey(prev)) {
                spoken = 0;
            } else {
                spoken = count - map.get(prev) - 1;
            }

            map.put(prev, count - 1);
            prev = spoken;
        }

        return spoken;
    }
}
