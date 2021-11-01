package utils;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;
import java.util.stream.Collectors;

public class Reader {
    public static List<String> ReadFile(String filename) throws IOException {
        FileInputStream fis = new FileInputStream(filename);
        Scanner sc = new Scanner(fis);

        List<String> res = new ArrayList<>();

        while (sc.hasNextLine()) {
            res.add(sc.nextLine());
        }

        return res;
    }

    public static List<Integer> ReadLineAsNumbers(String filename) throws IOException {
        FileInputStream fis = new FileInputStream(filename);
        Scanner sc = new Scanner(fis);

        String[] line = sc.nextLine().split(",");

        return Arrays.stream(line).map(Integer::parseInt).collect(Collectors.toList());
    }


}
