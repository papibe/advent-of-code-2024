package main

type Queue[T any] struct {
	elements []T
}

func (q *Queue[T]) append(p T) {
	q.elements = append(q.elements, p)
}

func (q *Queue[T]) popleft() T {
	point := q.elements[0]
	q.elements = q.elements[1:]
	return point
}

func (q *Queue[T]) is_empty() bool {
	return len(q.elements) == 0
}

func NewQueue[T any]() *Queue[T] {
	return &Queue[T]{[]T{}}
}

// Visited Set
type Set[T comparable] struct {
	visited map[T]bool
}

func (v *Set[T]) add(p T) {
	v.visited[p] = true
}

func (v *Set[T]) remove(p T) {
	delete(v.visited, p)
}

func (v *Set[T]) contains(p T) bool {
	_, ok := v.visited[p]
	return ok
}

func (v *Set[T]) is_empty() bool {
	return len(v.visited) == 0
}

func (v *Set[T]) list_of_elemets() []T {
	keys := []T{}
	for point := range v.visited {
		keys = append(keys, point)
	}
	return keys
}

func (v *Set[T]) copy() *Set[T] {
	new_visited := NewSet[T]()
	for key, value := range v.visited {
		new_visited.visited[key] = value
	}
	return new_visited
}

func NewSet[T comparable]() *Set[T] {
	return &Set[T]{make(map[T]bool)}
}
