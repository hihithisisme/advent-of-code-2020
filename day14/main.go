package day14

import (
	"aoc/utils"
	"fmt"
	"github.com/spf13/cobra"
	"math"
	"strconv"
	"strings"
)

var Cmd = &cobra.Command{
	Use: "14",
	Run: func(cmd *cobra.Command, args []string) {
		main()
	},
}

/* So we take the latest value left in each mem element and add them up */
func main() {
	instructions := readInput("day14/input.txt")
	p := program{
		values:  map[int]bits{},
		bitmask: bits{},
	}

	for _, i := range instructions {
		p.stepForPartOne(i)
	}
	fmt.Printf("part one answer: %v\n", p.sum())

	p = program{
		values:  map[int]bits{},
		bitmask: bits{},
	}

	for _, i := range instructions {
		p.stepForPartTwo(i)
	}
	fmt.Printf("part two answer: %v\n", p.sum())

}

type bits struct {
	raw [36]int
}

func (b bits) toDecimal() int {
	total := 0.0
	for i, r := range b.raw {
		total += float64(r) * math.Pow(2, float64(35-i))
	}

	return int(total)
}

func (b bits) float(idx int) []bits {
	clone0 := bits{raw: [36]int{}}
	copy(clone0.raw[:], b.raw[:])

	clone1 := bits{raw: [36]int{}}
	copy(clone1.raw[:], b.raw[:])

	clone0.raw[idx] = 0
	clone1.raw[idx] = 1

	return []bits{clone0, clone1}
}

func newBitsFromDecimal(dec int) bits {
	remaining := float64(dec)
	b := bits{raw: [36]int{}}

	for i := 35; i >= 0; i-- {
		base := math.Pow(2, float64(i))
		if remaining >= base {
			remaining -= base
			b.raw[35-i] = 1
		} else {
			b.raw[35-i] = 0
		}
	}
	return b
}

func newBitMask(mask string) bits {
	b := bits{raw: [36]int{}}

	for i, s := range strings.Split(mask, "") {
		if s == "X" {
			b.raw[i] = -1
		} else {
			b.raw[i], _ = strconv.Atoi(s)
		}
	}

	return b
}

type program struct {
	values  map[int]bits
	bitmask bits
}

func (p *program) stepForPartOne(instr instruction) {
	if instr.address == -1 {
		p.bitmask = instr.value
	} else {
		resBits := bits{raw: [36]int{}}
		for i, r := range instr.value.raw {
			if p.bitmask.raw[i] == -1 {
				resBits.raw[i] = r
			} else {
				resBits.raw[i] = p.bitmask.raw[i]
			}
		}

		p.values[instr.address] = resBits
	}
}

func (p *program) stepForPartTwo(instr instruction) {
	if instr.address == -1 {
		p.bitmask = instr.value
	} else {
		valueBits := instr.value

		destBits := newBitsFromDecimal(instr.address)
		for i, r := range p.bitmask.raw {
			if r == 0 {
				continue
			} else if r == 1 {
				destBits.raw[i] = 1
			}
		}

		floatingDest := []bits{destBits}
		for i, r := range p.bitmask.raw {
			if r == -1 {
				tmpFloating := []bits{}
				for _, dest := range floatingDest {
					tmpFloating = append(tmpFloating, dest.float(i)...)
				}
				floatingDest = tmpFloating
			}
		}

		for _, dest := range floatingDest {
			p.values[dest.toDecimal()] = valueBits
		}
	}
}

func (p *program) sum() int {
	total := 0
	for _, b := range p.values {
		total += b.toDecimal()
	}
	return total
}

type instruction struct {
	value   bits
	address int
}

func readInput(filename string) []instruction {
	instructions := []instruction{}

	raw := utils.ReadFile(filename)
	for _, r := range raw {
		parts := strings.Split(r, " = ")
		if parts[0] == "mask" {
			instructions = append(instructions, instruction{
				value:   newBitMask(parts[1]),
				address: -1,
			})

		} else {
			val, _ := strconv.Atoi(parts[1])
			split := strings.Split(parts[0], "")
			addr, _ := strconv.Atoi(strings.Join(split[4:len(split)-1], ""))

			instructions = append(instructions, instruction{
				value:   newBitsFromDecimal(val),
				address: addr,
			})
		}
	}

	return instructions
}
