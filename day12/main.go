package day12

import (
	"aoc/utils"
	"fmt"
	"github.com/spf13/cobra"
	"strconv"
	"strings"
)

var Cmd = &cobra.Command{
	Use: "12",
	Run: func(cmd *cobra.Command, args []string) {
		main()
	},
}

func main() {
	in := readInput("day12/input.txt")
	ship := NewShip(in)

	for ship.stepForPartOne() {
	}
	fmt.Printf("part one answer: %v\n", ship.getManhattanDistance())

	in = readInput("day12/input.txt")
	ship = NewShip(in)

	for ship.stepForPartTwo() {
	}
	fmt.Printf("part two answer: %v\n", ship.getManhattanDistance())
}

func readInput(filename string) []Instruction {
	raw := utils.ReadFile(filename)
	instructions := []Instruction{}

	for _, r := range raw {
		parts := strings.Split(r, "")
		command := parts[0]
		value, err := strconv.Atoi(strings.Join(parts[1:], ""))
		if err != nil {
			panic("invalid input?")
		}

		instructions = append(instructions, Instruction{
			command: command,
			value:   value,
		})
	}

	return instructions
}
