package day8

import (
	"fmt"
	"github.com/spf13/cobra"
)

var Cmd = &cobra.Command{
	Use:   "8",
	Short: "Run day8 challenge",
	Run: func(cmd *cobra.Command, args []string) {
		main()
	},
}

func main() {
	instructions := getInstructions()

	machine := NewMachine(instructions)
	machine.DetectLoop()
	fmt.Printf("part one answer: %v\n", machine.accumulator)

	for id, instruction := range instructions {
		if instruction.operation == "acc" {
			continue
		}

		tmpInstructions := make([]Instruction, len(instructions))
		copy(tmpInstructions, instructions)

		mutatedInstruction := instruction.copy()
		if mutatedInstruction.operation == "nop" {
			mutatedInstruction.operation = "jmp"
		} else if mutatedInstruction.operation == "jmp" {
			mutatedInstruction.operation = "nop"
		}

		tmpInstructions[id] = mutatedInstruction
		machine = NewMachine(tmpInstructions)
		if !machine.DetectLoop() {
			break
		}
	}
	fmt.Printf("part two answer: %v\n", machine.accumulator)
}
