package main

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

func (v *Set[T]) len() int {
	return len(v.visited)
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
