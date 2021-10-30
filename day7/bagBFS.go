package day7

import "container/list"

type BagBFS struct {
	allRules  []rule
	frontier  *list.List
	explored  map[bag]bool
	totalBags int
}

func NewBagBFS(allRules []rule, initialState bag) *BagBFS {
	bfs := &BagBFS{
		allRules:  allRules,
		frontier:  list.New(),
		explored:  map[bag]bool{},
		totalBags: 0,
	}

	bfs.frontier.PushFront(innerBag{qty: 1, bagID: initialState})
	bfs.explored[initialState] = true
	return bfs
}

func (b *BagBFS) pop() (bag, int) {
	element := b.frontier.Back()
	b.frontier.Remove(element)
	val := element.Value.(innerBag)
	return val.bagID, val.qty
}

func (b *BagBFS) push(bagID bag, qty int) {
	b.frontier.PushFront(innerBag{qty: qty, bagID: bagID})
	b.explored[bagID] = true
}

func (b *BagBFS) stepForPartOne() {
	currentState, _ := b.pop()
	for _, r := range b.allRules {
		if _, explored := b.explored[r.outerBagID]; !explored && r.canContain(currentState) {
			b.push(r.outerBagID, 1)
		}
	}
}

func (b *BagBFS) stepForPartTwo() {
	currentState, qty := b.pop()
	for _, r := range b.allRules {
		if r.outerBagID != currentState {
			continue
		}

		for _, ib := range r.innerBags {
			b.push(ib.bagID, ib.qty*qty)
			b.totalBags += ib.qty * qty
		}
	}
}
