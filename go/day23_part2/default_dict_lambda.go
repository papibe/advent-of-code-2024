package main

// //////////////////////////////////////////////////////////////////////////////////////
// Default Dict Lmbda
// //////////////////////////////////////////////////////////////////////////////////////

type DefaultDictLambda[T comparable, U any, F func() U] struct {
	dict          map[T]U
	default_value F
}

func (dd *DefaultDictLambda[T, U, F]) insert(key T, value U) {
	dd.dict[key] = value
}

func (dd *DefaultDictLambda[T, U, F]) get(key T) U {
	value, ok := dd.dict[key]
	if ok {
		return value
	}
	dd.dict[key] = dd.default_value()
	return dd.dict[key]
}

func (dd *DefaultDictLambda[T, U, F]) len() int {
	return len(dd.dict)
}

func (dd *DefaultDictLambda[T, U, F]) keys() []T {
	dict_keys := []T{}
	for key := range dd.dict {
		dict_keys = append(dict_keys, key)
	}
	return dict_keys
}

func NewDefaultDictLambda[T comparable, U any, F func() U](default_value F) *DefaultDictLambda[T, U, F] {
	return &DefaultDictLambda[T, U, F]{make(map[T]U), default_value}
}
