package day16;

import lombok.Value;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.stream.Collectors;

@Value
public class Rule {
    String label;
    List<int[]> qualifiers;
    HashMap<Integer, Boolean> possibleIndices = new HashMap<>();

    public Rule(String in) {
        label = in.split(":")[0];

        String[] qualifiersStrings = in.split(":")[1].substring(1).split(" or ");
        qualifiers = Arrays.stream(qualifiersStrings)
                .map(qualifier ->
                        Arrays.stream(qualifier.split("-"))
                                .mapToInt(Integer::parseInt)
                                .toArray()
                ).collect(Collectors.toList());
    }

    @Override
    public String toString() {
        return String.format("%s : %d-%d | %d-%d", this.label, this.qualifiers.get(0)[0], this.qualifiers.get(0)[1], this.qualifiers.get(1)[0], this.qualifiers.get(1)[1]);
    }

    public void eliminateValidIndices(Ticket ticket) {
        int[] fields = ticket.getFields().get().toArray();

        for (int i = 0; i < fields.length; i++) {

            boolean applies = appliesToField(fields[i]);
            if (!possibleIndices.containsKey(i) && applies) {
                possibleIndices.put(i, true);
            }
            if (!applies) {
                possibleIndices.put(i, false);
            }
        }
    }

    public int getNumOfPossibleIndices() {
        int count = 0;
        for (Boolean v : possibleIndices.values()) {
            if (v) {
                count++;
            }
        }
        return count;
    }

    public int comparePossibleIndices(Rule other) {
        if (this.getNumOfPossibleIndices() == other.getNumOfPossibleIndices()) {
            return 0;
        } else {
            return this.getNumOfPossibleIndices() < other.getNumOfPossibleIndices() ? -1 : 1;
        }
    }

    public boolean appliesToField(int field) {
        return qualifiers.stream()
                .anyMatch(q -> q[0] <= field && field <= q[1]);
    }

}
