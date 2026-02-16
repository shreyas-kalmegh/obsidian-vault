
Cargo is Rust’s build system and package manager. 
Cargo handles a lot of tasks for you, such as building your code, downloading the libraries your code depends on, and building those libraries. (We call the libraries that your code needs _dependencies_.)

### [Creating a Project with Cargo](https://doc.rust-lang.org/book/ch01-03-hello-cargo.html#creating-a-project-with-cargo)

```bash
cargo new hello_cargo
```


You’ll see that Cargo has generated two files and one directory for us: a _Cargo.toml_ file and a _src_ directory with a _main.rs_ file inside.

It has also initialized a new Git repository along with a _.gitignore_ file. Git files won’t be generated if you run `cargo new` within an existing Git repository; you can override this behavior by using `cargo new --vcs=git`.

```toml
[package] 
name = "hello_cargo" 
version = "0.1.0" 
edition = "2021" # See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html 
[dependencies]
```


This file is in the [_TOML_](https://toml.io/) (_Tom’s Obvious, Minimal Language_) format, which is Cargo’s configuration format.

The first line, `[package]`, is a section heading that indicates that the following statements are configuring a package.

The next three lines set the configuration information Cargo needs to compile your program: the name, the version, and the edition of Rust to use.

The last line, `[dependencies]`, is the start of a section for you to list any of your project’s dependencies. In Rust, packages of code are referred to as _crates_. 

Cargo expects your source files to live inside the _src_ directory. The top-level project directory is just for README files, license information, configuration files, and anything else not related to your code. Using Cargo helps you organize your projects. There’s a place for everything, and everything is in its place.

Building and running a cargo project

```bash
cargo build 
Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo) Finished dev [unoptimized + debuginfo] target(s) in 2.85 secs
```

This command creates an executable file in _target/debug/hello_cargo_ (or _target\debug\hello_cargo.exe_ on Windows) rather than in your current directory. Because the default build is a debug build, Cargo puts the binary in a directory named _debug_

We just built a project with `cargo build` and ran it with `./target/debug/hello_cargo`, but we can also use `cargo run` to compile the code and then run the resultant executable all in one command:

```bash
cargo run 
Finished dev [unoptimized + debuginfo] target(s) in 0.0 secs Running `target/debug/hello_cargo` 
Hello, world!
```

Cargo also provides a command called `cargo check`. This command quickly checks your code to make sure it compiles but doesn’t produce an executable:

```bash
cargo check 
Checking hello_cargo v0.1.0 (file:///projects/hello_cargo) Finished dev [unoptimized + debuginfo] target(s) in 0.32 secs
```

Why would you not want an executable? Often, `cargo check` is much faster than `cargo build` because it skips the step of producing an executable. If you’re continually checking your work while writing the code, using `cargo check` will speed up the process of letting you know if your project is still compiling! As such, many Rustaceans run `cargo check` periodically as they write their program to make sure it compiles. Then they run `cargo build` when they’re ready to use the executable.