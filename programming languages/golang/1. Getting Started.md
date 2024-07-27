
## Code organization

Go programs are organized into packages. A package is a collection of source files in the same directory that are compiled together. Functions, types, variables, and constants defined in one source file are visible to all other source files within the same package.

A repository contains one or more modules. A module is a collection of related Go packages that are released together. A Go repository typically contains only one module, located at the root of the repository. A file named `go.mod` there declares the module path: the import path prefix for all packages within the module. The module contains the packages in the directory containing its `go.mod` file as well as subdirectories of that directory, up to the next subdirectory containing another `go.mod` file (if any).

Each module's path not only serves as an import path prefix for its packages, but also indicates where the `go` command should look to download it. For example, in order to download the module `golang.org/x/tools`, the `go` command would consult the repository indicated by `https://golang.org/x/tools` (described more [here](https://go.dev/cmd/go/#hdr-Remote_import_paths)).

An import path is a string used to import a package. A package's import path is its module path joined with its subdirectory within the module. For example, the module `github.com/google/go-cmp` contains a package in the directory `cmp/`. That package's import path is `github.com/google/go-cmp/cmp`. Packages in the standard library do not have a module path prefix.

## First Program

```bash
$ mkdir hello # Alternatively, clone it if it already exists in version control.
$ cd hello
$ go mod init example/user/hello
go: creating new go.mod: module example/user/hello
```


The first statement in a Go source file must be `package name`. Executable commands must always use `package main`.

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, world.")
}
```


Now you can build and install that program with the `go` tool:

```bash
$ go install example/user/hello
$
```
This command builds the `hello` command, producing an executable binary. It then installs that binary as `$HOME/go/bin/hello` (or, under Windows, `%USERPROFILE%\go\bin\hello.exe`).

The install directory is controlled by the `GOPATH` and `GOBIN` [environment variables](https://go.dev/cmd/go/#hdr-Environment_variables). If `GOBIN` is set, binaries are installed to that directory. If `GOPATH` is set, binaries are installed to the `bin` subdirectory of the first directory in the `GOPATH` list. Otherwise, binaries are installed to the `bin` subdirectory of the default `GOPATH` (`$HOME/go` or `%USERPROFILE%\go`).

You can use the `go env` command to portably set the default value for an environment variable for future `go` commands:

```bash
$ go env -w GOBIN=/somewhere/else/bin
$
```

To unset a variable previously set by `go env -w`, use `go env -u`:

```bash
$ go env -u GOBIN
$
```

Commands like `go install` apply within the context of the module containing the current working directory. If the working directory is not within the `example/user/hello` module, `go install` may fail.

### Importing packages from remote modules

An import path can describe how to obtain the package source code using a revision control system such as Git or Mercurial. The `go` tool uses this property to automatically fetch packages from remote repositories. For instance, to use `github.com/google/go-cmp/cmp` in your program:

```go
package main

import (
    "fmt"

    "example/user/hello/morestrings"
    "github.com/google/go-cmp/cmp"
)

func main() {
    fmt.Println(morestrings.ReverseRunes("!oG ,olleH"))
    fmt.Println(cmp.Diff("Hello World", "Hello Go"))
}
```

Now that you have a dependency on an external module, you need to download that module and record its version in your `go.mod` file. The `go mod tidy` command adds missing module requirements for imported packages and removes requirements on modules that aren't used anymore.

```bash
$ go mod tidy
go: finding module for package github.com/google/go-cmp/cmp
go: found github.com/google/go-cmp/cmp in github.com/google/go-cmp v0.5.4
$ go install example/user/hello
$ hello
Hello, Go!
  string(
-     "Hello World",
+     "Hello Go",
  )
$ cat go.mod
module example/user/hello

go 1.16

**require github.com/google/go-cmp v0.5.4**
$
```

Module dependencies are automatically downloaded to the `pkg/mod` subdirectory of the directory indicated by the `GOPATH` environment variable. The downloaded contents for a given version of a module are shared among all other modules that `require` that version, so the `go` command marks those files and directories as read-only. To remove all downloaded modules, you can pass the `-modcache` flag to `go clean`:

```bash
$ go clean -modcache
$
```
