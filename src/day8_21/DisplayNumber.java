package day8_21;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

public class DisplayNumber {
    public int display;
    public Set<String> segments = new HashSet<>();

    DisplayNumber(String s) {
        segments.addAll(Arrays.asList(s.split("")));

        switch (segments.size()) {
            case 2:
                display = 1;
                break;
            case 4:
                display = 4;
                break;
            case 3:
                display = 7;
                break;
            case 7:
                display = 8;
                break;
            default:
                display = -1;
        }
    }

//    DisplayNumber(String s, )

    @Override
    public String toString() {
        return String.format("%s | %d", segments.toString(), display);
    }

    public boolean isSolved() {
        return display != -1;
    }

    public int getNumOfSegments() {
        return segments.size();
    }

    public String getDifferenceInSegments(DisplayNumber subset) {
        return segments.stream()
                .filter(s -> !subset.segments.contains(s))
                .findFirst()
                .get();
    }

    public boolean equals(final DisplayNumber other) {
        return segments.equals(other.segments);
    }
}
