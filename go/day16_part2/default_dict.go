package main

// //////////////////////////////////////////////////////////////////////////////////////
// Default Dict
// //////////////////////////////////////////////////////////////////////////////////////

type DefaultDict[T comparable, U any] struct {
	dict          map[T]U
	default_value U
}

func (dd *DefaultDict[T, U]) insert(key T, value U) {
	dd.dict[key] = value
}

func (dd *DefaultDict[T, U]) get(key T) U {
	value, ok := dd.dict[key]
	if ok {
		return value
	}
	return dd.default_value
}

func (dd *DefaultDict[T, U]) len() int {
	return len(dd.dict)
}

func NewDefaultDict[T comparable, U any](default_value U) *DefaultDict[T, U] {
	return &DefaultDict[T, U]{make(map[T]U), default_value}
}
