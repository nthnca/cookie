# cookie

The goal of this project is to create a small little program that implements a very basic
programming language, but that could be used as a starting point for people interested in
learning to code, or learning to write a programming language.


## Basic syntax

Assign an integer, 1, to a variable, `v`.
```
v = l;
```

Define a function, `f`:
```
f = {
  [statements]
  ...
}
```

Call the method `f`, and assign the result to `a`.
```
a = f();
```

Some further notes:
- All variables are globally scoped. So have fun!  :-)
- You can't pass parameters to a function, but variables are globally scoped so you can
  just use a normal variable.
- A method *returns* the value that is assigned to `_r` when the method exits.
- There are just four built in functions:
  - print(): prints the value in variable `_1`.
  - add(): returns the result of adding the values in variable `_1` and `_2`.
  - if(): calls the function assigned to variable `_2`, if `_1` is non-zero.
  - loop(): repeatedly calls the function assigned to variable `_1` until that function
    returns a non-zero value.


In this language, all variables are of a global scope, and nothing is ever freed,
although variables can be re-used.

By convention we use the variables `_1`, `_2`, etc to pass data into a function.

## Examples

See the tests directory for examples.
