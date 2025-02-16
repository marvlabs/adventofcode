# Assembunny Module Documentation
=====================================

## Overview
-----------

The Assembunny module is a Python implementation of the Assembunny computer, a fictional computer architecture used in the Advent of Code 2016 challenges. The module provides a simulator for running Assembunny programs and includes various instructions and optimizations.

## Instructions
--------------

* `cpy x y`: Copies the value of `x` to `y`.
* `inc x`: Increments the value of `x` by 1.
* `dec x`: Decrements the value of `x` by 1.
* `jnz x y`: Jumps to the instruction `y` if `x` is not zero.
* `tgl x`: Toggles the instruction at position `x`.
* `out x`: Outputs the value of `x`.
* `add x y`: Adds `y` to `x`.
* `mul x y`: Multiplies `x` by `y`.
* `nop`: No operation.

## Registers
------------

* `a`: General-purpose register.
* `b`: General-purpose register.
* `c`: General-purpose register.
* `d`: General-purpose register.
* `IP`: Instruction pointer.
* `OUT`: Output register.

## Assembunny Class
------------------

### `__init__(program, do_optimize=True)`

Initializes the Assembunny computer with the given program.

* `program`: The Assembunny program to run - either as string or as array of list
* `do_optimize`: Whether to optimize the program before running it.

### `run(break_on_output=lambda:False)`

Runs the Assembunny program until it completes or the output register `OUT` fulfils the lambda.

* `break_on_output`: A function that returns `True` if the output register `OUT` is non-empty.

### `reset()`

Resets the Assembunny computer to its initial state.

### `get(reg)`

Returns the value of the given register.

* `reg`: The register to retrieve.

### `out(x)`

Outputs the value of `x`.

* `x`: The value to output.

### `add(x, y)`

Adds `y` to `x`.

* `x`: The register to add to.
* `y`: The value to add.

### `inc(x)`

Increments the value of `x` by 1.

* `x`: The register to increment.

### `dec(x)`

Decrements the value of `x` by 1.

* `x`: The register to decrement.

### `jnz(x, rel)`

Jumps to the instruction `rel` if `x` is not zero.

* `x`: The value to check.
* `rel`: The relative jump offset.

### `tgl(x)`

Toggles the instruction at position `x`.

* `x`: The position of the instruction to toggle.

### `cpy(x, y)`

Copies the value of `x` to `y`.

* `x`: The value to copy.
* `y`: The register to copy to.

### `mul(x, y)`

Multiplies `x` by `y`.

* `x`: The register to multiply.
* `y`: The value to multiply by.

### `nop()`

No operation.

## Example Usage
--------------

```python
from assembunny import Assembunny

# Define a sample program
prog = [
    ['cpy', 2, 'a'],
    ['cpy', 40,  'b'],
    ['inc', 'a'],
    ['dec', 'b'],
    ['jnz', 'b', -2],
]
# or
prog = '''cpy 2 a
cpy 5 d
cpy 8 c
inc a
dec c
jnz c -2
dec d
jnz d -5
'''

# Create an Assembunny computer and run the program
bunny = Assembunny(prog)
bunny.run()

# Print the final value of register 'a'
print(bunny.get('a'))
'''