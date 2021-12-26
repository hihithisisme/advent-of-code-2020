package day8_21;

import com.google.common.collect.ImmutableList;
import com.google.common.collect.MoreCollectors;
import utils.Printer;
import utils.Reader;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

public class Main {

    public static void main() throws Exception {
        final List<String> in = Reader.ReadFile("src/day8_21/input.txt");

        in.forEach(System.out::println);

        Printer.printAns(partOne(in));
        Printer.printAns(partTwo(in));
    }

    public static int partOne(List<String> in) {

        return in.stream()
                .mapToInt(s -> (int) parseEntryLine(s)
                        .get(1).stream()
                        .filter(DisplayNumber::isSolved)
                        .count()
                ).sum();

    }

    public static int partTwo(List<String> in) throws Exception {
        return in.stream()
                .mapToInt(s -> getOutputValue(parseEntryLine(s).get(0), parseEntryLine(s).get(1)))
                .sum();
        
    }

    public static ImmutableList<List<DisplayNumber>> parseEntryLine(String s) {
        final String[] parts = s.split(" \\| ");
        return ImmutableList.copyOf(Arrays.stream(parts)
                .map(p -> Arrays.stream(p.split(" "))
                        .map(DisplayNumber::new)
                        .collect(Collectors.toList()))
                .collect(Collectors.toList()));
    }

    private static int getOutputValue(List<DisplayNumber> inputSignals, List<DisplayNumber> outputSignals) {
        List<DisplayNumber> fiveSegments = filterByNumOfSegments(inputSignals, 5);
        List<DisplayNumber> sixSegments = filterByNumOfSegments(inputSignals, 6);

        DisplayNumber[] samples = new DisplayNumber[10];
        samples[1] = getSampleDisplay(inputSignals, 1);
        samples[4] = getSampleDisplay(inputSignals, 4);
        samples[7] = getSampleDisplay(inputSignals, 7);
        samples[8] = getSampleDisplay(inputSignals, 8);

        Map<String, String> segmentMapping = new HashMap<>();

        /* solve for A */
        segmentMapping.put("A", samples[7].getDifferenceInSegments(samples[1]));

        /* identify 6s, then solve for F, and then G */
        samples[6] = sixSegments.stream()
                .filter(dn -> !supersetOfSample1(samples[1], dn))
                .findAny()
                .get();
        samples[6].display = 6;

        segmentMapping.put("F", samples[8].getDifferenceInSegments(samples[6]));

        segmentMapping.put("G", samples[1].segments
                .stream()
                .filter(seg -> !seg.equals(segmentMapping.get("F")))
                .collect(MoreCollectors.onlyElement()));

        /* identify 3, then solve for B and then C */
        samples[3] = fiveSegments.stream()
                .filter(dn -> dn.segments.containsAll(
                        ImmutableList.of(segmentMapping.get("F"), segmentMapping.get("G"))))
                .findAny()
                .get();
        samples[3].display = 3;

        final Set<String> BC = samples[3].segments
                .stream()
                .filter(seg -> !seg.equals(segmentMapping.get("A")))
                .filter(seg -> !seg.equals(segmentMapping.get("F")))
                .filter(seg -> !seg.equals(segmentMapping.get("G")))
                .collect(Collectors.toSet());
        segmentMapping.put("B", BC.stream()
                .filter(seg -> samples[4].segments.contains(seg))
                .collect(MoreCollectors.onlyElement()));
        segmentMapping.put("C", BC.stream()
                .filter(seg -> !samples[4].segments.contains(seg))
                .collect(MoreCollectors.onlyElement()));

        /* solve for D using 4, then solve for E */
        segmentMapping.put("D", samples[4].segments
                .stream()
                .filter(seg -> !seg.equals(segmentMapping.get("B")))
                .filter(seg -> !seg.equals(segmentMapping.get("F")))
                .filter(seg -> !seg.equals(segmentMapping.get("G")))
                .collect(MoreCollectors.onlyElement()));

        final List<String> allSegments = Arrays.asList("abcdefg".split(""));
        segmentMapping.put("E", allSegments
                .stream()
                .filter(seg -> !segmentMapping.containsValue(seg))
                .collect(MoreCollectors.onlyElement()));

        /* identify a sample of the remaining numbers: 0, 2, 5, 9*/
        samples[0] = sixSegments.stream()
                .filter(dn -> !dn.equals(samples[6]))
                .filter(dn -> !dn.segments.contains(segmentMapping.get("B")))
                .findFirst()
                .get();
        samples[9] = sixSegments.stream()
                .filter(dn -> !dn.equals(samples[6]))
                .filter(dn -> !dn.equals(samples[0]))
                .findFirst()
                .get();
        samples[0].display = 0;
        samples[9].display = 9;

        samples[2] = fiveSegments.stream()
                .filter(dn -> dn.segments.contains(segmentMapping.get("E")))
                .findFirst()
                .get();
        samples[5] = fiveSegments.stream()
                .filter(dn -> dn.segments.contains(segmentMapping.get("D")))
                .findFirst()
                .get();
        samples[2].display = 2;
        samples[5].display = 5;

        /* generate the output value*/
        return Integer.parseInt(outputSignals.stream()
                .map(output -> Arrays.stream(samples)
                        .filter(output::equals)
                        .collect(MoreCollectors.onlyElement()))
                .map(dn -> Integer.toString(dn.display))
                .collect(Collectors.joining("")));
    }

    private static boolean supersetOfSample1(DisplayNumber sample1, DisplayNumber other) {
        return other.segments.containsAll(sample1.segments);
    }

    private static DisplayNumber getSampleDisplay(final List<DisplayNumber> inputSignals, final int displayValue) {
        return inputSignals.stream()
                .filter(s -> s.display == displayValue)
                .findAny()
                .get();
    }

    private static List<DisplayNumber> filterByNumOfSegments(final List<DisplayNumber> inputSignals, final int i) {
        return inputSignals.stream()
                .filter(s -> s.getNumOfSegments() == i)
                .collect(Collectors.toList());
    }





    /*
 AAAA
D    F
D    F
 BBBB
E    G
E    G
 CCCC

display     no. of segments
1           2 x
4           4 x
7           3 x
8           7 x

0           6 x
6           6 x
9           6 x

2           5
3           5 x
5           5

1. solve for A using 7 (3) vs 1 (2)
2. identify 6 (6) as the one that excludes one segment from 1 (2) -- the other two should have both
3. solve for F using 8 (7) vs 6 (6)
4. hence solve for G using F using 1 (2) as reference
5. identify 3 (5) as the only (5) with F and G
6. solve for B and C using 3 (5) excluding A, F, G -- B is the segment included in 4 (4); C is the segment left

7. solve for D using 4 (4) excluding B, F, G
8. solve for E as the last remaining segment
    *  */

}
