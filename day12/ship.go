package day12

import (
	"fmt"
	"math"
)

type Instruction struct {
	command string
	value   int
}

type Location2D struct {
	north int
	east  int
}

func (l Location2D) Print() {
	if l.east >= 0 {
		fmt.Printf("east %v\t", l.east)
	} else {
		fmt.Printf("west %v\t", l.east*-1)
	}

	if l.north >= 0 {
		fmt.Printf("north %v\n", l.north)
	} else {
		fmt.Printf("south %v\n", l.north*-1)
	}
}

type Ship struct {
	instructions []Instruction
	pointer      int
	orientation  string
	location     Location2D
}

func (s *Ship) step() bool {
	if s.pointer >= len(s.instructions) {
		return false
	}

	instruction := s.instructions[s.pointer]
	if instruction.command == "F" {
		s.moveInDirection(s.orientation, instruction.value)
	} else if instruction.command == "R" || instruction.command == "L" {
		s.turn(instruction)
	} else {
		s.moveInDirection(instruction.command, instruction.value)
	}

	return true
}

func (s *Ship) turn(instruction Instruction) {
	interval := instruction.value / 90

	i := 0
	if instruction.command == "R" {
		for i = 0; i < interval; i++ {
			if i == 4 {
				i = 0
			}
		}
		order := []string{"north", "east", "south", "west"}
		s.orientation = order[i]
	} else if instruction.command == "L" {
		for i = 0; i < interval; i++ {
			if i == 4 {
				i = 0
			}
		}
		order := []string{"north", "west", "south", "east"}
		s.orientation = order[i]
	} else {
		panic("invalid turn instruction")
	}
}

func (s *Ship) moveInDirection(direction string, value int) {
	switch direction {
	case "N":
		s.location.north += value
	case "S":
		s.location.north -= value
	case "E":
		s.location.east += value
	case "W":
		s.location.east -= value
	default:
		panic("invalid direction")
	}
}

func (s Ship) getManhattanDistance() int {
	return int(math.Abs(float64(s.location.north)) + math.Abs(float64(s.location.east)))
}
