package day13

import (
	"aoc/src/utils"
	"fmt"
	"github.com/spf13/cobra"
	"math/big"
	"strconv"
	"strings"
)

var Cmd = &cobra.Command{
	Use: "13",
	Run: func(cmd *cobra.Command, args []string) {
		main()
	},
}

func main() {
	startTime, buses := readInput("src/day13/input.txt")

	fmt.Printf("part one answer: %v\n", partOne(startTime, buses))
	fmt.Printf("part two answer: %v\n", partTwo(buses))
}

func partOne(startTime int, buses []int) int {
	validBuses := []int{}
	for _, bus := range buses {
		if bus != -1 {
			validBuses = append(validBuses, bus)
		}
	}

	remainders := []int{}
	for _, bus := range validBuses {
		remainders = append(remainders, bus-(startTime%bus))
	}
	smallest := 99999
	smallestIdx := -1
	for idx, remainder := range remainders {
		if smallest > remainder {
			smallestIdx = idx
			smallest = remainder
		}
	}

	earliestBus := validBuses[smallestIdx]
	minToWait := remainders[smallestIdx]
	return earliestBus * minToWait
}

type Equation struct {
	remainder int
	mod       int
	coef      *big.Int
}

/* Chinese Remainder Theorem wtf*/
func partTwo(buses []int) string {
	var eqns []Equation

	prod := big.NewInt(1)
	for i, bus := range buses {
		if bus != -1 {
			eqns = append(eqns, Equation{
				remainder: (bus*100 - i) % bus,
				mod:       bus,
				coef:      big.NewInt(1),
			})
			prod.Mul(prod, big.NewInt(int64(bus)))
		}
	}

	for _, e := range eqns {
		e.coef.Div(prod, big.NewInt(int64(e.mod)))
	}

	total := big.NewInt(0)
	for _, e := range eqns {
		tmpInt := big.NewInt(1)
		tmpInt.Mod(e.coef, big.NewInt(int64(e.mod)))

		base := big.NewInt(0)
		base.Set(e.coef)

		for tmpInt.Cmp(big.NewInt(int64(e.remainder))) != 0 {
			tmpInt.Mod(e.coef.Add(e.coef, base), big.NewInt(int64(e.mod)))

		}
		total.Add(total, e.coef)
	}

	/* minimizing the answer */
	tmpInt := big.NewInt(1)
	tmpInt.Mul(prod, big.NewInt(2))
	for total.Cmp(prod) == 1 {
		total.Sub(total, prod)
	}

	return total.String()
}

func readInput(filename string) (startTime int, buses []int) {
	raw := utils.ReadFile(filename)
	startTime, _ = strconv.Atoi(raw[0])

	parts := strings.Split(raw[1], ",")
	var n int
	for _, bus := range parts {
		if bus == "x" {
			n = -1
		} else {
			n, _ = strconv.Atoi(bus)
		}
		buses = append(buses, n)
	}

	return
}
