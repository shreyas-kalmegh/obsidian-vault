# for, if, else, switch and defer

## For

Go has only one looping construct, the `for` loop.

The basic `for` loop has three components separated by semicolons:

-   the init statement: executed before the first iteration
-   the condition expression: evaluated before every iteration
-   the post statement: executed at the end of every iteration

The init statement will often be a short variable declaration, and the variables declared there are visible only in the scope of the `for` statement.

The loop will stop iterating once the boolean condition evaluates to `false`.

The init and post statements are optional.

Can also be used as while by dropping semicolon

```go
package main

import "fmt"

func main() {
	sum := 0
	for i := 0; i < 10; i++ {
		sum += i
	}
	fmt.Println(sum)
	
	// optional init and post
	sum := 1
	for ; sum < 1000; {
		sum += sum
	}
	fmt.Println(sum)
	
	// as a while
	sum := 1
	for sum < 1000 {
		sum += sum
	}
	fmt.Println(sum)
	
	// infinite loop
	for {
	}
}
```

## If

Go's `if` statements are like its `for` loops; the expression need not be surrounded by parentheses `( )` but the braces `{ }` are required.

Like `for`, the `if` statement can start with a short statement to execute before the condition.
Variables declared by the statement are only in scope until the end of the `if`.
Variables declared inside an `if` short statement are also available inside any of the `else` blocks.

```go
package main

import (
	"fmt"
	"math"
)

func sqrt(x float64) string {
	if x < 0 {
		return sqrt(-x) + "i"
	}
	return fmt.Sprint(math.Sqrt(x))
}
// init statement with if
func pow(x, n, lim float64) float64 {
	if v := math.Pow(x, n); v < lim {
		return v
	} else {
		fmt.Printf("%g >= %g\n", v, lim)
	}
	// can't use v here, though
	return lim
}

func main() {
	fmt.Println(sqrt(2), sqrt(-4))
	fmt.Println(pow(3, 2, 10))
}
```

## Switch

A `switch` statement is a shorter way to write a sequence of `if - else` statements. It runs the first case whose value is equal to the condition expression.
In effect, the `break` statement that is needed at the end of each case in those languages is provided automatically in Go. Another important difference is that Go's switch cases need not be constants, and the values involved need not be integers.

```go
package main

import (
	"fmt"
	"runtime"
)

func main() {
	fmt.Print("Go runs on ")
	switch os := runtime.GOOS; os {
	case "darwin":
		fmt.Println("OS X.")
	case "linux":
		fmt.Println("Linux.")
	default:
		// freebsd, openbsd,
		// plan9, windows...
		fmt.Printf("%s.\n", os)
	}
}
```

## Switch with no condition

Switch without a condition is the same as `switch true`.
This construct can be a clean way to write long if-then-else chains.

```go
package main

import (
	"fmt"
	"time"
)

func main() {
	t := time.Now()
	switch {
	case t.Hour() < 12:
		fmt.Println("Good morning!")
	case t.Hour() < 17:
		fmt.Println("Good afternoon.")
	default:
		fmt.Println("Good evening.")
	}
}
```

## Defer

A defer statement defers the execution of a function until the surrounding function returns.

The deferred call's arguments are evaluated immediately, but the function call is not executed until the surrounding function returns.

```go
package main

import "fmt"

func main() {
	defer fmt.Println("world")

	fmt.Println("hello")
}
```

Deferred function calls are pushed onto a stack. When a function returns, its deferred calls are executed in last-in-first-out order.

```go
package main

import "fmt"

func main() {
	fmt.Println("counting")

	for i := 0; i < 10; i++ {
		defer fmt.Println(i)
	}

	fmt.Println("done")
}
```

```
counting
done
9
8
.
.
```
