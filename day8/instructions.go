package day8

import (
	"aoc/utils"
	"strconv"
	"strings"
)

type operation string

type Instruction struct {
	id        int
	operation operation
	value     int
}

func (i Instruction) copy() Instruction {
	return i
}

func getInstructions() []Instruction {
	raw := utils.ReadFile("day8/input.txt")

	var instructions []Instruction

	for id, instructionString := range raw {
		instructionParts := strings.Split(instructionString, " ")

		val, err := strconv.Atoi(instructionParts[1])
		if err != nil {
			panic("yaya")
		}

		instruction := Instruction{
			id:        id,
			operation: operation(instructionParts[0]),
			value:     val,
		}

		instructions = append(instructions, instruction)
	}

	return instructions
}
