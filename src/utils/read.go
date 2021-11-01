package utils

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func ReadFile(filename string) []string {

	file, err := os.Open(filename)
	if err != nil {
		panic(fmt.Sprintf("cannot open file %s\n%+v\n", filename, err))
	}

	defer file.Close()

	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)

	var res []string
	for scanner.Scan() {
		res = append(res, scanner.Text())
	}
	return res
}

func ReadNumericInput(filename string) []int {
	var res []int

	raw := ReadFile(filename)
	for _, r := range raw {
		val, err := strconv.Atoi(r)
		if err != nil {
			panic("invalid input")
		}

		res = append(res, val)
	}
	return res
}
