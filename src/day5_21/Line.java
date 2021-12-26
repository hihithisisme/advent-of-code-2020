package day5_21;

import java.util.ArrayList;
import java.util.List;

public class Line {
    public Point source;
    public Point destination;

    Line(String in) {
        final String[] split = in.split(" -> ");
        String s0 = split[0];
        String s1 = split[1];

        source = new Point(s0);
        destination = new Point(s1);
    }

    public boolean isStraightLine() {
        return (source.x == destination.x || source.y == destination.y);
    }

    public List<Point> getAllCoordinates() {
        List<Point> allCoordinates = new ArrayList<>();
        if (source.x == destination.x) {
            int constant = source.x;
            int more = Math.max(source.y, destination.y);
            int less = Math.min(source.y, destination.y);

            for (int i = less; i <= more; i++) {
                allCoordinates.add(new Point(constant, i));
            }
        } else if (source.y == destination.y) {
            int constant = source.y;
            int less = Math.min(source.x, destination.x);
            int more = Math.max(source.x, destination.x);

            for (int i = less; i <= more; i++) {
                allCoordinates.add(new Point(i, constant));
            }
        } else {
            int moreX = Math.max(source.x, destination.x);
            int lessX = Math.min(source.x, destination.x);
            int moreY = Math.max(source.y, destination.y);
            int lessY = Math.min(source.y, destination.y);

            if (source.x < destination.x && source.y < destination.y || source.x > destination.x && source.y > destination.y) {
                for (int i = 0; i <= moreX - lessX; i++) {
                    allCoordinates.add(new Point(lessX + i, lessY + i));
                }
            } else {
                for (int i = 0; i <= moreX - lessX; i++) {
                    allCoordinates.add(new Point(lessX + i, moreY - i));
                }
            }
        }

        return allCoordinates;
    }

    @Override
    public String toString() {
        return String.format("%d,%d -> %d,%d", source.x, source.y, destination.x, destination.y);
    }
}
