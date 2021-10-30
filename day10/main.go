package day10

import (
	"aoc/utils"
	"fmt"
	"github.com/spf13/cobra"
	"sync"
)

var Cmd = &cobra.Command{
	Use:   "10",
	Short: "Run day10 challenge",
	Run: func(cmd *cobra.Command, args []string) {
		main()
	},
}

func main() {
	in := asc(utils.ReadNumericInput("day10/input.txt"))
	in.ascendingSort()

	fmt.Printf("part one answer: %v\n", partOne(in))
	fmt.Printf("part two answer: %v\n", partTwo(in))
}

func partOne(in asc) int {
	prev := 0
	diff1 := 0
	diff3 := 0
	for _, i := range in {
		diff := i - prev
		switch diff {
		case 1:
			diff1++
		case 3:
			diff3++
		}

		prev = i
	}
	diff3++
	fmt.Printf("diff1: %v\ndiff3: %v\n", diff1, diff3)
	return diff3 * diff1
}

func partTwo(in asc) int {
	in = append([]int{0}, append(in, in[len(in)-1]+3)...)
	results := make(chan int)

	prev := 0
	prevIdx := 0
	wg := &sync.WaitGroup{}
	n := 0

	for idx, i := range in {
		if i-prev == 3 {
			wg.Add(1)
			n++

			go func(prevIdx, idx int) {
				tmpIn := asc(make([]int, idx-prevIdx))
				copy(tmpIn, in[prevIdx:idx+1])

				total := 0
				lock := &sync.Mutex{}

				tmpIn.recurse(&total, 0, lock)
				wg.Done()
				results <- total
			}(prevIdx, idx)

			prevIdx = idx
		}
		prev = i
	}

	wg.Wait()

	totalTotal := 1

	for i := 0; i < n; i++ {
		select {
		case r := <-results:
			totalTotal *= r
		}
	}
	return totalTotal
}

func (a asc) recurse(total *int, pointer int, lock *sync.Mutex) {
	wg := &sync.WaitGroup{}

	for ix := range a[pointer:] {
		idx := ix + pointer
		if idx == 0 || idx == len(a)-1 {
			continue
		}

		if a[idx+1]-a[idx-1] <= 3 {
			wg.Add(1)
			tmpA := asc(make([]int, len(a)))
			copy(tmpA, a)
			tmpA = append(tmpA[:idx], tmpA[idx+1:]...)

			go func(idx int) {
				tmpA.recurse(total, idx, lock)
				wg.Done()
			}(idx)
		}
	}

	wg.Wait()
	lock.Lock()
	*total++
	lock.Unlock()
}
