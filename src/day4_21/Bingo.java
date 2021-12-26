package day4_21;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class Bingo {
    public List<int[]> numbers;
    public int size;
    public boolean won;

    Bingo(List<String> in) {
        numbers = in.stream()
                .map(s -> Arrays.stream(s.split(" "))
                        .filter(si -> !si.equals(""))
                        .mapToInt(Integer::parseInt)
                        .toArray())
                .collect(Collectors.toList());

        size = in.size();
        won = false;
    }

    public void setNum(int num) {
        for (int idx = 0; idx < numbers.size(); idx++) {
            numbers.set(idx, Arrays.stream(numbers.get(idx))
                    .map(i -> i == num ? -1 : i)
                    .toArray());
        }
    }

    public int getScore() {
        return numbers.stream()
                .flatMapToInt(row -> Arrays.stream(row)
                        .filter(i -> i != -1))
                .sum();
    }

    public boolean checkWin() {
        for (final int[] row : numbers) {
            if (Arrays.stream(row).allMatch(i -> i == -1)) {
                return true;
            }
        }

        for (int i = 0; i < size; i++) {
            boolean win = true;
            for (final int[] row : numbers) {
                if (row[i] != -1) {
                    win = false;
                    break;
                }
            }
            if (win) {
                return true;
            }
        }
        return false;
    }
}
