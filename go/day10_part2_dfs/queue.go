package main

type Point struct {
	row int
	col int
}

type Map [][]int

// Visited Set
type VisitedSet struct {
	visited map[Point]bool
}

func (v *VisitedSet) add(p Point) {
	v.visited[p] = true
}

func (v *VisitedSet) remove(p Point) {
	delete(v.visited, p)
}

func (v *VisitedSet) contains(p Point) bool {
	_, ok := v.visited[p]
	return ok
}

func NewVisitedSet() *VisitedSet {
	return &VisitedSet{make(map[Point]bool)}
}
