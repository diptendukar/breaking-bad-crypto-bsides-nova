#!/usr/bin/env python3
"""
Tiny, transparent Linear Congruential Generator  --  shared by the server and the solver.

Hand-rolled ON PURPOSE. The whole point of this module is that a "random" token stream is
really a *recurrence* you can reverse-engineer from a handful of samples. So the generator
is three lines of arithmetic you can read, not a library black box. Stdlib only.

    x_{n+1} = (a * x_n + c) mod m

`a` (multiplier), `c` (increment) and `m` (modulus) are the generator's parameters; `x_0` is
the seed. Given a few *consecutive* outputs you can recover a, c and m and then predict every
future output -- that is the attack (in solve.py). This file is just the generator.

Famous real LCGs (all fully predictable -- never use them for anything security-sensitive):
    glibc rand():   a=1103515245  c=12345      m=2**31
    MMIX (Knuth):   a=6364136223846793005  c=1442695040888963407  m=2**64
    java.util.Random: a=25214903917 c=11 m=2**48  (returns high bits only)
"""


class LCG:
    """x_{n+1} = (a*x_n + c) mod m.  next() advances the state and returns the new output."""

    def __init__(self, a: int, c: int, m: int, seed: int):
        self.a, self.c, self.m = a, c, m
        self.state = seed % m

    def next(self) -> int:
        self.state = (self.a * self.state + self.c) % self.m
        return self.state


def sample(a: int, c: int, m: int, seed: int, n: int):
    """Return the first n consecutive outputs of the LCG (the seed itself is not emitted)."""
    g = LCG(a, c, m, seed)
    return [g.next() for _ in range(n)]
