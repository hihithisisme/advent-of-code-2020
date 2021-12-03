package day16;

import utils.Reader;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.stream.Collectors;

public class Main {
    public static void main() throws IOException {
        List<String> in = Reader.ReadFile("src/day16/input.txt");

        List<Ticket> tickets = getTickets(in);
        List<Rule> rules = getRules(in);

        Ticket ownTicket = tickets.get(0);
        List<Ticket> nearbyTickets = tickets.subList(1, tickets.size());

        System.out.printf("part one answer: %d\n", partOne(rules, nearbyTickets));
        System.out.printf("part two answer: %d\n", partTwo(rules, nearbyTickets, ownTicket));

    }

    public static int partOne(List<Rule> rules, List<Ticket> tickets) {
        return tickets.stream()
                .flatMapToInt(t -> t.findInvalidFields(rules))
                .sum();
    }

    public static int partTwo(List<Rule> rules, List<Ticket> tickets, Ticket ownTicket) {
        final List<Ticket> validTickets = tickets.stream()
                .filter(t -> !t.isInvalid(rules))
                .collect(Collectors.toList());

        rules.forEach(r ->
                validTickets.forEach(r::eliminateValidIndices)
        );

        eliminateIndices(rules);

        return -1;
    }

    public static void eliminateIndices(List<Rule> rules) {
        rules.sort((Rule::comparePossibleIndices));

        HashMap<Integer, Rule> solution = new HashMap<>();

        /* backtracking algo */

//        for (int i = 0; i < rules.size(); i++) {
//            for (int j = 0; j < rules.get(i).getPossibleIndices().; j++) {
//
//            }
//        }

        rules.forEach(r -> System.out.printf("%s \t\t\t\t %s\n", r.toString(), r.getPossibleIndices()));

    }

    public static List<Rule> getRules(List<String> in) {
        List<Rule> rules = new ArrayList<>();
        for (String i : in) {
            if (i.equals("")) {
                break;
            }

            rules.add(new Rule(i));
        }

        return rules;
    }

    public static List<Ticket> getTickets(List<String> in) {
        boolean yourTicketFlag = false;
        boolean ticketsFlag = false;

        List<Ticket> allTickets = new ArrayList<>();
        for (String i : in) {
            if (yourTicketFlag) {
                allTickets.add(new Ticket(i));
                yourTicketFlag = false;
            }
            if (ticketsFlag) {
                allTickets.add(new Ticket(i));
            }

            if (i.equals("your ticket:")) {
                yourTicketFlag = true;
            } else if (i.equals("nearby tickets:")) {
                ticketsFlag = true;
            }
        }

        return allTickets;
    }
}
