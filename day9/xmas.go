package day9

import (
	"aoc/utils"
)

type XmasEncryption struct {
	preambleN int
	input     []int
	pointer   int
}

func NewXmas(preambleN int, input []int) *XmasEncryption {
	return &XmasEncryption{
		preambleN: preambleN,
		input:     input,
		pointer:   0,
	}
}

func (x *XmasEncryption) step() bool {
	if x.pointer >= len(x.input) {
		panic("program is wrong; out of index")
	}

	if x.pointer < x.preambleN {
		x.pointer++
		return true
	}

	valid := x.check()
	if !valid {
		return valid
	}

	x.pointer++
	return valid
}

func (x *XmasEncryption) check() bool {
	window := x.input[x.pointer-x.preambleN : x.pointer]
	for idx, i := range window {
		for _, j := range window[idx:] {
			sum := i + j
			if sum == x.input[x.pointer] {
				return true
			}
		}
	}
	return false
}

func (x *XmasEncryption) findContiguousSum(startPointer int, weakness int) int {
	sum := 0
	min := 999999999999
	max := -1
	for _, i := range x.input[startPointer:] {
		sum += i
		min = utils.Min(min, i)
		max = utils.Max(max, i)
		if sum == weakness {
			return min + max
		}
		if sum > weakness {
			return -1
		}
	}
	return -2
}
