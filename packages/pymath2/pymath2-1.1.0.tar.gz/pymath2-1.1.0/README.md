# pymath

Perform math calculations either on the command line or in the Python repl. Imports all of the functions from the `math` and `statistics` modules and the combinatoric functions from the `itertools` module into the global namespace for convenience. Also includes some extra math functions defined in the [pymath](https://github.com/cjbassi/pymath/tree/master/pymath) folder.

## Installation

```shell
pip install [--user] pymath2
```

**Note**: `~/.local/bin` should be in your `$PATH` for `--user` installs.

## Usage

Run an expression from the command line:

```shell
> pymath 'factorial(5)+1'
121
```

Or perform multiple calculations in the Python repl:

```shell
> pymath

>>> extended_gcd(5, 2)
(1, 1, -2)
>>> list(primes(5))
[2, 3, 5, 7, 11]
>>>
```

List all available functions:

```shell
pymath -l
```
