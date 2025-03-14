// This example demonstrates a priority queue built using the heap interface.
package main

import (
	"container/heap"
)

// An Item is something we manage in a priority queue.
type Item[T any] struct {
	value    T   // The value of the item.
	priority int // The priority of the item in the queue.

	// The index is needed by update and is maintained by the heap.Interface methods.
	index int // The index of the item in the heap.
}

// A _PriorityQueue implements heap.Interface and holds Items.
type _PriorityQueue[T any] []*Item[T]

func (pq _PriorityQueue[T]) Len() int { return len(pq) }

func (pq _PriorityQueue[T]) Less(i, j int) bool {
	// We want Pop to give us the highest, not lowest, priority so we use greater than here.
	return pq[i].priority < pq[j].priority
}

func (pq _PriorityQueue[T]) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

func (pq *_PriorityQueue[T]) Push(x any) {
	n := len(*pq)
	item := x.(*Item[T])
	item.index = n
	*pq = append(*pq, item)
}

func (pq *_PriorityQueue[T]) Pop() any {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil  // don't stop the GC from reclaiming the item eventually
	item.index = -1 // for safety
	*pq = old[0 : n-1]
	return item
}

// update modifies the priority and value of an Item in the queue.
func (pq *_PriorityQueue[T]) update(item *Item[T], value T, priority int) {
	item.value = value
	item.priority = priority
	heap.Fix(pq, item.index)
}

type PriorityQueue[T any] struct {
	elements _PriorityQueue[T]
}

func NewPriorityQueue[T any]() *PriorityQueue[T] {
	pq := &PriorityQueue[T]{make(_PriorityQueue[T], 0)}
	heap.Init(&pq.elements)
	return pq
}

func (pq *PriorityQueue[T]) Len() int {
	return pq.elements.Len()
}

func (pq *PriorityQueue[T]) Less(i, j int) bool {
	return pq.elements[i].priority < pq.elements[j].priority
}

func (pq *PriorityQueue[T]) Swap(i, j int) {
	pq.elements[i], pq.elements[j] = pq.elements[j], pq.elements[i]
	pq.elements[i].index = i
	pq.elements[j].index = j
}

func (pq *PriorityQueue[T]) Pop() (T, int) {
	any_item := heap.Pop(&pq.elements)
	item := any_item.(*Item[T])
	return item.value, item.priority
}

func (pq *PriorityQueue[T]) Push(value T, priority int) {
	heap.Push(&pq.elements, &Item[T]{value: value, priority: priority})
}

func (pq *PriorityQueue[T]) IsEmpty() bool {
	return len(pq.elements) == 0
}
