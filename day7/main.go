package day7

import (
	"aoc/utils"
	"fmt"
	"github.com/spf13/cobra"
	"strconv"
	"strings"
)

var Cmd = &cobra.Command{
	Use:   "7",
	Short: "Run day7 challenge",
	Run: func(cmd *cobra.Command, args []string) {
		main()
	},
}

func main() {
	rules := getRules()

	bfs := NewBagBFS(rules, bag("shiny gold"))
	for bfs.frontier.Len() != 0 {
		bfs.stepForPartOne()
	}
	fmt.Printf("answer part one: %v\n", len(bfs.explored)-1)

	bfs = NewBagBFS(rules, bag("shiny gold"))
	for bfs.frontier.Len() != 0 {
		bfs.stepForPartTwo()
	}
	fmt.Printf("answer part two: %v\n", bfs.totalBags)

}

func getRules() []rule {
	in := utils.ReadFile("day7/input.txt")
	rules := []rule{}
	for _, ruleString := range in {
		words := strings.Split(ruleString, " ")
		outerBag := bag(strings.Join(words[:2], " "))

		innerBagString := strings.Split(strings.Join(words[4:], " "), ", ")
		innerBags := []innerBag{}
		for _, ib := range innerBagString {
			bagString := strings.Split(ib, " ")

			var qty int
			var innerBagID bag
			if bagString[0] == "no" {
				qty = 0
				innerBagID = "other"
			} else {
				qty64, err := strconv.ParseInt(bagString[0], 10, 64)
				if err != nil {
					panic(fmt.Sprintf("what's the issue %+v", err))
				}
				qty = int(qty64)
				innerBagID = bag(strings.Join(bagString[1:3], " "))
			}

			innerBags = append(innerBags, innerBag{qty: qty, bagID: innerBagID})
		}

		rules = append(rules, rule{
			outerBagID: outerBag,
			innerBags:  innerBags,
		})
	}

	return rules
}
