import picocli.CommandLine;

import java.io.IOException;

@CommandLine.Command(
        name = "Advent of Code 2020",
        description = "Type in day number to run the appropriate challenge"
)
public class Main {

    public static void main(String[] args) {
        new CommandLine(new Main()).execute(args);
    }

    @CommandLine.Command(name = "15")
    void day15() throws Exception {
        day15.Main.main();
    }

    @CommandLine.Command(name = "16")
    void day16() throws Exception {
        day16.Main.main();
    }

    @CommandLine.Command(name = "7")
    void day7() throws Exception {
        runGoCmd(7);
    }

    @CommandLine.Command(name = "8")
    void day8() throws Exception {
        runGoCmd(8);
    }

    @CommandLine.Command(name = "9")
    void day9() throws Exception {
        runGoCmd(9);
    }

    @CommandLine.Command(name = "10")
    void day10() throws Exception {
        runGoCmd(10);
    }

    @CommandLine.Command(name = "11")
    void day11() throws Exception {
        runGoCmd(11);
    }

    @CommandLine.Command(name = "12")
    void day12() throws Exception {
        runGoCmd(12);
    }

    @CommandLine.Command(name = "13")
    void day13() throws Exception {
        runGoCmd(12);
    }

    @CommandLine.Command(name = "14")
    void day14() throws Exception {
        runGoCmd(14);
    }

    private void runGoCmd(int day) throws IOException {
        ProcessBuilder builder = new ProcessBuilder("/usr/local/go/bin/go", "run", "src/main.go", Integer.toString(day));
        builder.inheritIO();
        builder.redirectErrorStream(true);
        builder.start();
    }
}
