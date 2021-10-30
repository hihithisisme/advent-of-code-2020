package utils

import "fmt"

func Print2D(arr [][]string) {
	for idx, i := range arr {
		fmt.Printf("%v:\t", idx)
		for _, i2 := range i {
			fmt.Printf("%v ", i2)
		}
		fmt.Printf("\n")
	}
}
