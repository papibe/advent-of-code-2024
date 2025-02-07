package main

type Point struct {
	row int
	col int
}

type Map [][]int

type Queue struct {
	elements []Point
}

func (q *Queue) push(p Point) {
	q.elements = append(q.elements, p)
}

func (q *Queue) pop() Point {
	element := q.elements[0]
	q.elements = q.elements[1:]
	return element
}

func (q *Queue) is_empty() bool {
	return len(q.elements) == 0
}

func NewQueue() *Queue {
	return &Queue{[]Point{}}
}

// Visited Set
type VisitedSet struct {
	visited map[Point]bool
}

func (v *VisitedSet) add(p Point) {
	v.visited[p] = true
}

func (v *VisitedSet) contains(p Point) bool {
	_, ok := v.visited[p]
	return ok
}

func NewVisitedSet() *VisitedSet {
	return &VisitedSet{make(map[Point]bool)}
}
