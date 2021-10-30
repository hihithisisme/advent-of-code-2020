package day7

type bag string

type innerBag struct {
	qty   int
	bagID bag
}

type rule struct {
	outerBagID bag
	innerBags  []innerBag
}

func (r rule) canContain(innerBagID bag) bool {
	for _, ib := range r.innerBags {
		if ib.bagID == innerBagID {
			return true
		}
	}
	return false
}
