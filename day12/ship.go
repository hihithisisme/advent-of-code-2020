package day12

import (
	"fmt"
	"math"
)

type Instruction struct {
	command string
	value   int
}

func (i Instruction) Print() {
	fmt.Printf("%s%v\n", i.command, i.value)
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

type Waypoint struct {
	locationFromShip Location2D
}

func (w *Waypoint) moveInDirection(direction string, value int) {
	switch direction {
	case "N":
		w.locationFromShip.north += value
	case "S":
		w.locationFromShip.north -= value
	case "E":
		w.locationFromShip.east += value
	case "W":
		w.locationFromShip.east -= value
	default:
		fmt.Printf("direction: %s\n", direction)
		panic("invalid direction")
	}
}

func (w *Waypoint) rotate(instruction Instruction) {
	interval := instruction.value / 90 % 4

	if interval == 0 {
		return
	} else if interval == 2 {
		w.locationFromShip.north *= -1
		w.locationFromShip.east *= -1
		return
	} else {
		w.locationFromShip.north, w.locationFromShip.east = w.locationFromShip.east, w.locationFromShip.north
		if interval == 1 {
			if instruction.command == "R" {
				w.locationFromShip.north *= -1
			} else if instruction.command == "L" {
				w.locationFromShip.east *= -1
			} else {
				panic("invalid rotate instruction")
			}

		} else if interval == 3 {
			if instruction.command == "R" {
				w.locationFromShip.east *= -1
			} else if instruction.command == "L" {
				w.locationFromShip.north *= -1
			} else {
				panic("invalid rotate instruction")
			}
		}
	}
}

type Ship struct {
	instructions []Instruction
	pointer      int
	orientation  string
	location     Location2D
	waypoint     *Waypoint
}

func NewShip(instructions []Instruction) Ship {
	return Ship{
		instructions: instructions,
		pointer:      0,
		orientation:  "E",
		location: Location2D{
			north: 0,
			east:  0,
		},
		waypoint: &Waypoint{locationFromShip: Location2D{
			north: 1,
			east:  10,
		}},
	}
}

func (s *Ship) stepForPartOne() bool {
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

	s.pointer++
	return true
}

func (s *Ship) stepForPartTwo() bool {
	if s.pointer >= len(s.instructions) {
		return false
	}

	instruction := s.instructions[s.pointer]
	if instruction.command == "F" {
		s.moveTowardsWaypoint(instruction.value)
	} else if instruction.command == "R" || instruction.command == "L" {
		s.waypoint.rotate(instruction)
	} else {
		s.waypoint.moveInDirection(instruction.command, instruction.value)
	}

	s.pointer++
	return true
}

func (s *Ship) turn(instruction Instruction) {
	interval := instruction.value / 90

	var order []string
	if instruction.command == "R" {
		order = []string{"N", "E", "S", "W"}

	} else if instruction.command == "L" {
		order = []string{"N", "W", "S", "E"}
	} else {
		panic("invalid turn instruction")
	}

	idx := 0
	for idx < len(order) {
		if order[idx] == s.orientation {
			break
		}
		idx++
	}
	for count := 0; count < interval; count++ {
		idx++
		if idx == 4 {
			idx = 0
		}
	}
	s.orientation = order[idx]
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
		fmt.Printf("direction: %s\n", direction)
		panic("invalid direction")
	}
}

func (s *Ship) moveTowardsWaypoint(value int) {
	s.location.north += s.waypoint.locationFromShip.north * value
	s.location.east += s.waypoint.locationFromShip.east * value
}

func (s Ship) getManhattanDistance() int {
	return int(math.Abs(float64(s.location.north)) + math.Abs(float64(s.location.east)))
}
