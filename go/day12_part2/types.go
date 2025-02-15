package main

type Garden []string

type Point struct {
	row int
	col int
}

type Region map[Point]bool

type Regions []Region

func (r *Region) add(p Point) {
	(*r)[p] = true
}

func (r *Region) contains(p Point) bool {
	_, ok := (*r)[p]
	return ok
}

func NewRegion() *Region {
	region_map := make(map[Point]bool)
	region := (Region)(region_map)
	return &region
}

type Edge struct {
	point Point
	dir   Point
}

type Edges []Edge

type Queue struct {
	elements []Point
}

func (q *Queue) push(p Point) {
	q.elements = append(q.elements, p)
}

func (q *Queue) pop() Point {
	point := q.elements[0]
	q.elements = q.elements[1:]
	return point
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

func (v *VisitedSet) copy() *VisitedSet {
	new_visited := NewVisitedSet()
	for key, value := range v.visited {
		new_visited.visited[key] = value
	}
	return new_visited
}

func NewVisitedSet() *VisitedSet {
	return &VisitedSet{make(map[Point]bool)}
}
