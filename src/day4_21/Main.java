package day4_21;

import utils.Printer;
import utils.Reader;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Main {

    public static void main() throws Exception {
        final List<String> in = Reader.ReadFile("src/day4_21/input.txt");

        final int[] inputNums = readNumbers(in.get(0));
        final List<Bingo> bingos = readBingos(in.subList(2, in.size()));

        Printer.printAns(partOne(inputNums, bingos));
        Printer.printAns(partTwo(inputNums, bingos));
    }

    public static int partOne(int[] in, List<Bingo> bingos) {
        for (final int i : in) {
            for (final Bingo bingo : bingos) {
                bingo.setNum(i);
                if (bingo.checkWin()) {
                    return bingo.getScore() * i;
                }
            }
        }

        return -1;
    }

    public static int partTwo(int[] in, List<Bingo> bingos) throws Exception {
        for (final int i : in) {
            for (final Bingo bingo : bingos) {
                if (bingo.won) {
                    continue;
                }

                bingo.setNum(i);

                if (bingo.checkWin()) {
                    if (bingos.stream().mapToInt(bi -> bi.won ? 0 : 1).sum() == 1) {
                        return bingos.stream()
                                .filter(bi -> !bi.won)
                                .findFirst()
                                .orElseThrow(Exception::new)
                                .getScore() * i;
                    }

                    bingo.won = true;
                }
            }
        }

        return -1;
    }

    private static int[] readNumbers(String numbers) {
        final String[] split = numbers.split(",");
        return Arrays.stream(split)
                .mapToInt(Integer::parseInt)
                .toArray();
    }

    private static List<Bingo> readBingos(List<String> in) {
        List<String> bingoNumbers = new ArrayList<>();
        List<Bingo> bingos = new ArrayList<>();

        for (String s : in) {
            if (s.equals("")) {
                bingos.add(new Bingo(bingoNumbers));
                bingoNumbers = new ArrayList<>();
            } else {
                bingoNumbers.add(s);
            }
        }

        bingos.add(new Bingo(bingoNumbers));

        return bingos;
    }

}
