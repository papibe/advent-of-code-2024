// This example demonstrates a priority queue built using the heap interface.
package main

import (
	"container/heap"
	"fmt"
)

// An Item is something we manage in a priority queue.
type Item_2 struct {
	value    string // The value of the item; arbitrary.
	priority int    // The priority of the item in the queue.

	// The index is needed by update and is maintained by the heap.Interface methods.
	index int // The index of the item in the heap.
}

// A PriorityQueue implements heap.Interface and holds Items.
type PriorityQueue_2 []*Item_2

func (pq PriorityQueue_2) Len() int { return len(pq) }

func (pq PriorityQueue_2) Less(i, j int) bool {
	// We want Pop to give us the highest, not lowest, priority so we use greater than here.
	return pq[i].priority < pq[j].priority
}

func (pq PriorityQueue_2) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

func (pq *PriorityQueue_2) Push(x any) {
	n := len(*pq)
	item := x.(*Item_2)
	item.index = n
	*pq = append(*pq, item)
}

func (pq *PriorityQueue_2) Pop() any {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil  // don't stop the GC from reclaiming the item eventually
	item.index = -1 // for safety
	*pq = old[0 : n-1]
	return item
}

// update modifies the priority and value of an Item in the queue.
func (pq *PriorityQueue_2) update(item *Item_2, value string, priority int) {
	item.value = value
	item.priority = priority
	heap.Fix(pq, item.index)
}

// This example creates a PriorityQueue with some items, adds and manipulates an item,
// and then removes the items in priority order.
func _main() {
	// Some items and their priorities.
	items := map[string]int{
		"banana": 3, "apple": 2, "pear": 5,
	}

	// Create a priority queue, put the items in it, and
	// establish the priority queue (heap) invariants.
	pq := make(PriorityQueue_2, 0)

	heap.Init(&pq)

	// i := 0
	for value, priority := range items {
		heap.Push(&pq, &Item_2{value: value, priority: priority})
		// pq[i] = &Item{
		// 	value:    value,
		// 	priority: priority,
		// 	index:    i,
		// }
		// i++
	}
	// heap.Init(&pq)

	heap.Push(&pq, &Item_2{value: "orange", priority: 1})

	heap.Push(&pq, &Item_2{value: "grape", priority: 0})

	// Take the items out; they arrive in decreasing priority order.
	for pq.Len() > 0 {
		item := heap.Pop(&pq).(*Item_2)
		fmt.Printf("%.2d:%s ", item.priority, item.value)
	}
	fmt.Println()
}
