package day6_21;

import com.google.common.collect.ImmutableList;
import utils.Reader;

import java.io.IOException;
import java.math.BigInteger;
import java.util.HashMap;
import java.util.List;

public class Main {

    static int newAge = 9;
    static int normalAge = 7;
    static HashMap<ImmutableList, BigInteger> cache = new HashMap<>();

    public static void main() throws IOException {
        final List<Integer> in = Reader.ReadLineAsNumbers("src/day6_21/input.txt");

        System.out.printf("answer is: %s\n", recursionEntry(in, 80));
        System.out.printf("answer is: %s\n", recursionEntry(in, 256));
    }

    private static BigInteger recursionEntry(final List<Integer> in, final int limit) {
        return in.stream()
                .map(i -> i + 1)
                .map(i -> newFish(i, limit))
                .reduce(BigInteger.ZERO, BigInteger::add)
                .add(BigInteger.valueOf(in.size()));
    }

    private static BigInteger newFish(int key, int limit) {
        if (key <= limit) {
            return normalFish(key, limit);
        }
        return BigInteger.ZERO;
    }

    private static BigInteger normalFish(int key, int limit) {
        final ImmutableList<Integer> cacheKey = ImmutableList.of(key, limit);
        if (cache.containsKey(cacheKey)) {
            return cache.get(cacheKey);
        }

        BigInteger sum = BigInteger.ZERO;
        for (int i = key; i <= limit; i = i + normalAge) {
            sum = sum.add(BigInteger.ONE);
            sum = sum.add(newFish(newAge, limit - i));
        }
        cache.put(cacheKey, sum);
        return sum;
    }
}
