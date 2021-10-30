package day9

import (
	"aoc/utils"
	"fmt"
	"github.com/spf13/cobra"
)

var Cmd = &cobra.Command{
	Use:   "9",
	Short: "Run day9 challenge",
	Run: func(cmd *cobra.Command, args []string) {
		main()
	},
}

func main() {
	xmas := NewXmas(25, utils.ReadNumericInput("day9/input.txt"))
	for xmas.step() {
	}

	weakness := xmas.input[xmas.pointer]
	fmt.Printf("part one answer: %+v\n", weakness)
	for i := 0; i < len(xmas.input); i++ {
		if res := xmas.findContiguousSum(i, weakness); res > 0 {
			fmt.Printf("part two answer: %+v\n", res)
			return
		}
	}
	fmt.Printf("something is wrong with program")
}
