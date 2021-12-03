package day16;

import lombok.AllArgsConstructor;
import lombok.Value;

import java.util.Arrays;
import java.util.List;
import java.util.function.Supplier;
import java.util.stream.IntStream;

@Value
@AllArgsConstructor
public class Ticket {
    Supplier<IntStream> fields;

    public Ticket(String in) {
        this.fields = () -> Arrays.stream(in.split(","))
                .mapToInt(Integer::parseInt);

    }

    private boolean fieldIsDefInvalid(int field, List<Rule> rules) {
        return rules.stream().noneMatch(r ->
                        r.appliesToField(field)
//                r.getQualifiers()
//                        .stream()
//                        .anyMatch(q -> q[0] <= field && field <= q[1])
        );
    }

    public IntStream findInvalidFields(List<Rule> rules) {
        return this.fields.get()
                .filter(f -> this.fieldIsDefInvalid(f, rules));
    }

    public boolean isInvalid(List<Rule> rules) {
        return this.fields.get()
                .anyMatch(f -> this.fieldIsDefInvalid(f, rules));
    }
}
