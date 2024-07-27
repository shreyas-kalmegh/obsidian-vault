## Methods

Go does not have classes. However, you can define methods on types.
A method is a function with a special _receiver_ argument.
The receiver appears in its own argument list between the `func` keyword and the method name.
In this example, the `Abs` method has a receiver of type `Vertex` named `v`.

```go
type Vertex struct {
	X, Y float64
}

func (v Vertex) Abs() float64 {
	return math.Sqrt(v.X*v.X + v.Y*v.Y)
}

func main() {
	v := Vertex{3, 4}
	fmt.Println(v.Abs())
}
```

## Methods are functions

Remember: a method is just a function with a receiver argument.
Here's `Abs` written as a regular function with no change in functionality.

```go
type Vertex struct {
	X, Y float64
}

func Abs(v Vertex) float64 {
	return math.Sqrt(v.X*v.X + v.Y*v.Y)
}
```

You can declare a method on non-struct types, too.
In this example we see a numeric type `MyFloat` with an `Abs` method.
You can only declare a method with a receiver whose type is defined in the same package as the method. You cannot declare a method with a receiver whose type is defined in another package (which includes the built-in types such as `int`).

```
type MyFloat float64

func (f MyFloat) Abs() float64 {
	if f < 0 {
		return float64(-f)
	}
	return float64(f)
}
```

## Pointer receivers

You can declare methods with pointer receivers.
Methods with pointer receivers can modify the value to which the receiver points (as `Scale` does here). Since methods often need to modify their receiver, pointer receivers are more common than value receivers.
With a value receiver, the `Scale` method operates on a copy of the original `Vertex` value. (This is the same behavior as for any other function argument.)

```go
type Vertex struct {
	X, Y float64
}
// value reciever
func (v Vertex) Abs() float64 {
	return math.Sqrt(v.X*v.X + v.Y*v.Y)
}
// pointer receiver
func (v *Vertex) Scale(f float64) {
	v.X = v.X * f
	v.Y = v.Y * f
}
```