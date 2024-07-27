# structs, slices, and maps


## Pointers

Go has pointers. A pointer holds the memory address of a value.

The type `*T` is a pointer to a `T` value. Its zero value is `nil`.

```go
var p *int
```

The `&` operator generates a pointer to its operand.

```go
i := 42
p = &i
```

The `*` operator denotes the pointer's underlying value.

```go
fmt.Println(*p) // read i through the pointer p
*p = 21         // set i through the pointer p
```

This is known as "dereferencing" or "indirecting".

Unlike C, Go has no pointer arithmetic.


## Structs

A `struct` is a collection of fields.
Struct fields are accessed using a dot.
Struct fields can be accessed through a struct pointer.

To access the field `X` of a struct when we have the struct pointer `p` we could write `(*p).X`. However, that notation is cumbersome, so the language permits us instead to write just `p.X`, without the explicit dereference.

```go
package main

import "fmt"

type Vertex struct {
	X int
	Y int
}

func main() {
	v := Vertex{1, 2}
	p := &v
	p.X = 1e9
	fmt.Println(v)
}
```

## Struct Literals

A struct literal denotes a newly allocated struct value by listing the values of its fields.
You can list just a subset of fields by using the `Name:` syntax. (And the order of named fields is irrelevant.)
The special prefix `&` returns a pointer to the struct value.

```go
package main

import "fmt"

type Vertex struct {
	X, Y int
}

var (
	v1 = Vertex{1, 2}  // has type Vertex
	v2 = Vertex{X: 1}  // Y:0 is implicit
	v3 = Vertex{}      // X:0 and Y:0
	p  = &Vertex{1, 2} // has type *Vertex
)

func main() {
	fmt.Println(v1, p, v2, v3)
}
```

## Arrays

The type `[n]T` is an array of `n` values of type `T`.
The expression

```go
var a [10]int
```

declares a variable `a` as an array of ten integers.
An array's length is part of its type, so arrays cannot be resized

```go
package main

import "fmt"

func main() {
	var a [2]string
	a[0] = "Hello"
	a[1] = "World"
	fmt.Println(a[0], a[1])
	fmt.Println(a)

	primes := [6]int{2, 3, 5, 7, 11, 13}
	fmt.Println(primes)
}
```

## Slices

An array has a fixed size. A slice, on the other hand, is a dynamically-sized, flexible view into the elements of an array. In practice, slices are much more common than arrays.
The type `[]T` is a slice with elements of type `T`.
A slice is formed by specifying two indices, a low and high bound, separated by a colon:

```go
a[low : high]
```

This selects a half-open range which includes the first element, but excludes the last one.
The following expression creates a slice which includes elements 1 through 3 of `a`:
```go
a[1:4]
```

## Slices are like references to arrays

A slice does not store any data, it just describes a section of an underlying array.
Changing the elements of a slice modifies the corresponding elements of its underlying array.
Other slices that share the same underlying array will see those changes.

The zero value of a slice is `nil`.
A nil slice has a length and capacity of 0 and has no underlying array.

```go
func main() {
	names := [4]string{
		"John",
		"Paul",
		"George",
		"Ringo",
	}
	fmt.Println(names)

	a := names[0:2]
	b := names[1:3]
	fmt.Println(a, b)

	b[0] = "XXX"
	fmt.Println(a, b)
	fmt.Println(names)
}
```

```
[John Paul George Ringo]
[John Paul] [Paul George]
[John XXX] [XXX George]
[John XXX George Ringo]
```

## Slice literals

A slice literal is like an array literal without the length.

This is an array literal:

```go
[3]bool{true, true, false}
```

And this creates the same array as above, then builds a slice that references it:

```go
[]bool{true, true, false}
```

## Slice defaults

When slicing, you may omit the high or low bounds to use their defaults instead.
The default is zero for the low bound and the length of the slice for the high bound.

## Slice length and capacity

A slice has both a _length_ and a _capacity_.
The length of a slice is the number of elements it contains.
The capacity of a slice is the number of elements in the underlying array, counting from the first element in the slice.
The length and capacity of a slice `s` can be obtained using the expressions `len(s)` and `cap(s)`.
You can extend a slice's length by re-slicing it, provided it has sufficient capacity.

```go
func main() {
	s := []int{2, 3, 5, 7, 11, 13}
	printSlice(s)

	// Slice the slice to give it zero length.
	s = s[:0]
	printSlice(s)

	// Extend its length.
	s = s[:4]
	printSlice(s)

	// Drop its first two values.
	s = s[2:]
	printSlice(s)
}

func printSlice(s []int) {
	fmt.Printf("len=%d cap=%d %v\n", len(s), cap(s), s)
}
```

```
len=6 cap=6 [2 3 5 7 11 13]
len=0 cap=6 []
len=4 cap=6 [2 3 5 7]
len=2 cap=4 [5 7]
```

## Creating a slice with make

Slices can be created with the built-in `make` function; this is how you create dynamically-sized arrays.
The `make` function allocates a zeroed array and returns a slice that refers to that array:

```go
a := make([]int, 5)  // len(a)=5
```

To specify a capacity, pass a third argument to `make`:

```go
b := make([]int, 0, 5) // len(b)=0, cap(b)=5 []

b = b[:cap(b)] // len(b)=5, cap(b)=5 [0 0 0 0 0]
b = b[1:]      // len(b)=4, cap(b)=4  [0 0 0 0]
```

## Appending to a slice

It is common to append new elements to a slice, and so Go provides a built-in `append` function. The [documentation](https://go.dev/pkg/builtin/#append) of the built-in package describes `append`.

```go
func append(s []T, vs ...T) []T
```

The first parameter `s` of `append` is a slice of type `T`, and the rest are `T` values to append to the slice.

The resulting value of `append` is a slice containing all the elements of the original slice plus the provided values.

If the backing array of `s` is too small to fit all the given values a bigger array will be allocated. The returned slice will point to the newly allocated array.

## Range

The `range` form of the `for` loop iterates over a slice or map.

When ranging over a slice, two values are returned for each iteration. The first is the index, and the second is a copy of the element at that index.
You can skip the index or value by assigning to `_`.

```go
for i, _ := range pow
for _, value := range pow
```

If you only want the index, you can omit the second variable.

```go
for i := range pow
```

```go
var pow = []int{1, 2, 4, 8, 16, 32, 64, 128}

func main() {
	for i, v := range pow {
		fmt.Printf("2**%d = %d\n", i, v)
	}
}
```


## Maps

A map maps keys to values.
The zero value of a map is `nil`. A `nil` map has no keys, nor can keys be added.
The `make` function returns a map of the given type, initialized and ready for use

```go
type Vertex struct {
	Lat, Long float64
}

var m map[string]Vertex

// map literal
var ml = map[string]Vertex{
	"Bell Labs": Vertex{
		40.68433, -74.39967,
	},
	"Google": Vertex{
		37.42202, -122.08408,
	},
}

func main() {
	m = make(map[string]Vertex)
	m["Bell Labs"] = Vertex{
		40.68433, -74.39967,
	}
	fmt.Println(m["Bell Labs"])
	fmt.Println(ml)
}
```

## Map literals continued

If the top-level type is just a type name, you can omit it from the elements of the literal.

```go
type Vertex struct {
	Lat, Long float64
}

var m = map[string]Vertex{
	"Bell Labs": {40.68433, -74.39967},
	"Google":    {37.42202, -122.08408},
}
```

## Mutating Maps

Insert or update an element in map `m`:

```go
m[key] = elem
```

Retrieve an element:

```go
elem = m[key]
```

Delete an element:

```go
delete(m, key)
```

Test that a key is present with a two-value assignment:

```go
elem, ok := m[key]
```

If `key` is in `m`, `ok` is `true`. If not, `ok` is `false`.
If `key` is not in the map, then `elem` is the zero value for the map's element type.

## Function values

Functions are values too. They can be passed around just like other values.
Function values may be used as function arguments and return values.

```go
func compute(fn func(float64, float64) float64) float64 {
	return fn(3, 4)
}

func main() {
	hypot := func(x, y float64) float64 {
		return math.Sqrt(x*x + y*y)
	}
	fmt.Println(hypot(5, 12))

	fmt.Println(compute(hypot))
	fmt.Println(compute(math.Pow))
}
```

## Function closures

Go functions may be closures. A closure is a function value that references variables from outside its body. The function may access and assign to the referenced variables; in this sense the function is "bound" to the variables.

For example, the `adder` function returns a closure. Each closure is bound to its own `sum` variable

```go
func adder() func(int) int {
	sum := 0
	return func(x int) int {
		sum += x
		return sum
	}
}

func main() {
	pos, neg := adder(), adder()
	for i := 0; i < 10; i++ {
		fmt.Println(
			pos(i),
			neg(-2*i),
		)
	}
}
```

