
```go
package main

import (
	"fmt"
	"math/rand"
	"math"
)

func main() {
	fmt.Println("My favorite number is", rand.Intn(10))
	fmt.Println(math.pi)
}
```


## Exported names
In Go, a name is exported if it begins with a capital letter. For example, `Pizza` is an exported name, as is `Pi`, which is exported from the `math` package.

## Type declaration
```go
x int      //int
p *int     //pointer to int
a [3]int   //array[3] of int
```


## Variable declaration/initialization
```go
var i, j int = 1, 2
k := 3 //short hand notation, k becomes int
c, python, java := true, false, "no!"
```

## Return multiple results
```go
package main

import "fmt"

func swap(x, y string) (string, string) {
	return y, x
}

func main() {
	a, b := swap("hello", "world")
	fmt.Println(a, b)
}
```

## Named return values

Go's return values may be named. If so, they are treated as variables defined at the top of the function.

These names should be used to document the meaning of the return values.

A `return` statement without arguments returns the named return values. This is known as a "naked" return.
```go
package main

import "fmt"

func split(sum int) (x, y int) {
	x = sum * 4 / 9
	y = sum - x
	return
}

func main() {
	fmt.Println(split(17))
}
```

## Basic types

Go's basic types are

```
bool

string

int  int8  int16  int32  int64
uint uint8 uint16 uint32 uint64 uintptr

byte // alias for uint8

rune // alias for int32
     // represents a Unicode code point

float32 float64

complex64 complex128
```

## Zero values

Variables declared without an explicit initial value are given their _zero value_.

The zero value is:

```
-   `0` for numeric types,
-   `false` for the boolean type, and
-   `""` (the empty string) for strings.
```

## Type conversions

The expression `T(v)` converts the value `v` to the type `T`.
```go
i := 42
f := float64(i)
u := uint(f)
```

## Constants

Constants are declared like variables, but with the `const` keyword.
Constants can be character, string, boolean, or numeric values.
Constants cannot be declared using the `:=` syntax.

```bash
package main

import "fmt"

const Pi = 3.14

func main() {
	const World = "世界"
	fmt.Println("Hello", World)
	fmt.Println("Happy", Pi, "Day")

	const Truth = true
	fmt.Println("Go rules?", Truth)
}
```

## Numeric Constants

Numeric constants are high-precision _values_.
An untyped constant takes the type needed by its context.

```go
package main

import "fmt"

const (
	// Create a huge number by shifting a 1 bit left 100 places.
	// In other words, the binary number that is 1 followed by 100 zeroes.
	Big = 1 << 100
	// Shift it right again 99 places, so we end up with 1<<1, or 2.
	Small = Big >> 99
)

func needInt(x int) int { return x*10 + 1 }
func needFloat(x float64) float64 {
	return x * 0.1
}

func main() {
	fmt.Println(needInt(Small))
	fmt.Println(needFloat(Small))
	fmt.Println(needFloat(Big))
}
```

```
21
0.2
1.2676506002282295e+29
```