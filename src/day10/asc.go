package day10

import "sort"

type asc []int

func (a asc) Less(i, j int) bool {
	return a[i] < a[j]
}

func (a asc) Swap(i, j int) {
	a[i], a[j] = a[j], a[i]
}

func (a asc) Len() int {
	return len(a)
}

func (a *asc) ascendingSort() {
	sort.Sort(a)
}
