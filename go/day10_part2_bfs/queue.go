package main

type Point struct {
	row int
	col int
}

type Map [][]int

type QueueKey struct {
	Point   Point
	visited VisitedSet
}

type Queue struct {
	elements []QueueKey
}

func (q *Queue) push(p QueueKey) {
	q.elements = append(q.elements, p)
}

func (q *Queue) pop() QueueKey {
	element := q.elements[0]
	q.elements = q.elements[1:]
	return element
}

func (q *Queue) is_empty() bool {
	return len(q.elements) == 0
}

func NewQueue() *Queue {
	return &Queue{[]QueueKey{}}
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

type Paths struct {
	sets map[*VisitedSet]bool
}

func (p *Paths) add(visited *VisitedSet) {
	p.sets[visited] = true
}
