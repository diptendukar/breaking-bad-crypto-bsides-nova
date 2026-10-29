# Predicting an LCG — attendee brief

A password-reset service hands out "random" tokens. Predict the next one it will issue —
**with a little arithmetic, no brute force, no guessing.**

## Setup
```
pip install requests
```
Point your exploit at the instructor's server: `http://<instructor-ip>:5005`.
The crypto helper `lcg_toy.py` sits next to `client.py` — you `import` it; you don't edit it.

## The service
- `GET /token?sid=YOURNAME` → the next reset token on **your** stream (a big integer). Call it
  repeatedly to collect a sequence. Pick a **unique** `sid` so your stream is yours alone.
- `GET /flag?sid=YOURNAME&guess=N` → the server is about to mint the **admin** reset token on your
  stream. Tell it the value. Right answer → the flag. It never shows you the value; it only says
  yes or no. So you can't peek — you have to *predict*.

## The bug
The tokens are not random. They are consecutive outputs of a **Linear Congruential Generator**:
```
x_next = (a · x + c) mod m
```
`a`, `c`, `m` are the server's secret parameters; the seed is per-session. But an LCG is a pure
recurrence — given a handful of consecutive outputs you can recover `a`, `c`, and `m`, and from
there compute every future output. Including the next one.

## Work it out
`client.py` already recovers the modulus `m` for you (a neat gcd trick on the differences). From `m`
and a few consecutive outputs, two more lines of modular algebra give you `a` and `c` — derive them
from `s_next = (a·s + c) mod m` (division mod m is `pow(x, -1, m)`), or see `hints.md`.

## Your task
`client.py` already collects a run of tokens and recovers `m` for you (the `gcd` step). Fill in the
**two TODO lines** — recover `a`, then `c` — then it predicts the next token and submits it.

```
python client.py http://<instructor-ip>:5005
```
Goal: print the recovered `a`/`c`, then `{"ok": true, ... "flag": "flag{...}"}`.

> Real LCGs are everywhere: C's `rand()`, `java.util.Random`, old PHP `mt_rand` seeds. Anything
> built on them for security — session tokens, reset links, "random" keys — is predictable.
