package day5_21;

import lombok.Data;
import lombok.RequiredArgsConstructor;

import java.util.Arrays;

@Data
@RequiredArgsConstructor
public class Point {
    final public int x;
    final public int y;

    Point(String in) {
        final int[] split = Arrays.stream(in.split(",")).mapToInt(Integer::parseInt).toArray();
        x = split[0];
        y = split[1];
    }
}
