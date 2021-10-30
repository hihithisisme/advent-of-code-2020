package day11

import (
	"aoc/utils"
	"fmt"
	"github.com/spf13/cobra"
	"strings"
)

const (
	floor    = "."
	empty    = "L"
	occupied = "#"
)

var Cmd = &cobra.Command{
	Use: "11",
	Run: func(cmd *cobra.Command, args []string) {
		main()
	},
}

func main() {
	raw := readInput("day11/input.txt")
	in := NewSeatLayout(raw)
	in2 := in.clone()

	for in.stepForPartOne() {
	}
	fmt.Printf("part one answer: %v\n", in.countOccupied())

	for in2.stepForPartTwo() {
	}
	fmt.Printf("part two answer: %v\n", in2.countOccupied())
}

type SeatLayout struct {
	Layout [][]string
	rowN   int
	colN   int
}

func NewSeatLayout(layout [][]string) SeatLayout {
	return SeatLayout{
		Layout: layout,
		rowN:   len(layout),
		colN:   len(layout[0]),
	}
}

func (s SeatLayout) clone() SeatLayout {
	duplicate := make([][]string, s.rowN)
	for idx := range s.Layout {
		duplicate[idx] = make([]string, s.colN)
		copy(duplicate[idx], s.Layout[idx])
	}

	return NewSeatLayout(duplicate)
}

func (s SeatLayout) isEqual(o SeatLayout) bool {
	for i := range s.Layout {
		for i2 := range s.Layout[i] {
			if s.Layout[i][i2] != o.Layout[i][i2] {
				return false
			}
		}
	}
	return true
}

func (s SeatLayout) Print() {
	utils.Print2D(s.Layout)
	fmt.Println()
}

func (s SeatLayout) countOccupied() int {
	total := 0

	for i := range s.Layout {
		for i2 := range s.Layout[i] {
			if s.Layout[i][i2] == occupied {
				total++
			}
		}
	}

	return total
}

func (s *SeatLayout) stepForPartOne() (changed bool) {
	original := s.clone()

	for i := range original.Layout {
		for i2 := range original.Layout[i] {
			if original.Layout[i][i2] == floor {
				continue
			}

			n := original.getNumOfSurroundingOccupiedSeats(i, i2)

			if n == 0 && s.Layout[i][i2] == empty {
				s.Layout[i][i2] = occupied
			} else if n >= 4 && s.Layout[i][i2] == occupied {
				s.Layout[i][i2] = empty
			}
		}
	}

	return !s.isEqual(original)
}

func (s *SeatLayout) stepForPartTwo() (changed bool) {
	original := s.clone()

	for i := range original.Layout {
		for i2 := range original.Layout[i] {
			if original.Layout[i][i2] == floor {
				continue
			}

			n := original.getNumOfVisibleOccupiedSeats(i, i2)

			if n == 0 && s.Layout[i][i2] == empty {
				s.Layout[i][i2] = occupied
			} else if n >= 5 && s.Layout[i][i2] == occupied {
				s.Layout[i][i2] = empty
			}
		}
	}

	return !s.isEqual(original)
}

func (s SeatLayout) getNumOfVisibleOccupiedSeats(i, i2 int) int {
	numOfOccupied := 0

	for d := -1; d <= 1; d++ {
		for d2 := -1; d2 <= 1; d2++ {

			if d == 0 && d2 == 0 {
				continue
			}

			if s.isFirstSeatInSightPathOccupied(i, i2, d, d2) {
				numOfOccupied++
			}
		}
	}

	return numOfOccupied
}

func (s SeatLayout) isFirstSeatInSightPathOccupied(i, i2, d, d2 int) bool {
	j, j2 := i+d, i2+d2

	for j >= 0 && j < s.rowN && j2 >= 0 && j2 < s.colN {
		if s.Layout[j][j2] == occupied {
			return true
		}

		if s.Layout[j][j2] == empty {
			return false
		}

		j += d
		j2 += d2
	}

	return false
}

func (s SeatLayout) getNumOfSurroundingOccupiedSeats(i, i2 int) int {
	minj := utils.Max(i-1, 0)
	maxj := utils.Min(i+1, s.rowN-1)
	minj2 := utils.Max(i2-1, 0)
	maxj2 := utils.Min(i2+1, s.colN-1)

	numOfOccupied := 0
	for j := minj; j <= maxj; j++ {
		for j2 := minj2; j2 <= maxj2; j2++ {
			if i == j && i2 == j2 {
				continue
			}
			if s.Layout[j][j2] == occupied {
				numOfOccupied++
			}
		}
	}

	return numOfOccupied
}

func readInput(filename string) (res [][]string) {
	raw := utils.ReadFile(filename)

	for _, r := range raw {
		res = append(res, strings.Split(r, ""))
	}
	return res
}
