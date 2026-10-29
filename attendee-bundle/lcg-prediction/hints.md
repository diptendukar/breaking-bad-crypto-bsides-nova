# Hints — LCG prediction

- **Hint 1 (unlock ~6 min):** Pull several tokens with `/token?sid=…` and look at them as a
  sequence. They are *not* independent draws — each one is a fixed formula applied to the one
  before: `x_next = (a·x + c) mod m`. Your whole job is to find `a`, `c`, `m`. Then the "next
  random token" is just one more application of the formula.

- **Hint 2 (get the modulus `m`):** This is the clever step and `client.py` does it for you, but
  understand it. Take differences `d_i = s_{i+1} − s_i`. Because the `c` cancels in a subtraction,
  the diffs satisfy `d_{i+1} = a·d_i (mod m)` — a geometric chain. That makes
  `z_i = d_{i+2}·d_i − d_{i+1}²` equal to `a²d_i² − a²d_i² = 0 (mod m)`, i.e. every `z_i` is a
  multiple of `m`. `gcd` a few of them and you almost always land exactly on `m`.

- **Hint 3 (recover `a`):** Two consecutive steps give `s2 − s1 = a·(s1 − s0) (mod m)`. Solve for
  `a` — "dividing mod m" is multiplying by a modular inverse:
  ```python
  a = (s[2] - s[1]) * pow(s[1] - s[0], -1, m) % m
  ```

- **Hint 4 (recover `c`):** Now that you have `a`, use `s1 = a·s0 + c (mod m)`:
  ```python
  c = (s[1] - a * s[0]) % m
  ```
  Sanity-check: `(a*s[i] + c) % m` should reproduce `s[i+1]` for every `i`. If not, re-check which
  outputs you paired.

- **Hint 5 (predict + win):** You now own the generator. The next token — the admin reset token the
  server is about to mint — is `(a·s_last + c) % m`, where `s_last` is the most recent token you
  pulled on your `sid`. Submit that to `/flag`. (This line is already written for you.) Careful: the
  server advances *your* stream by one on `/flag`, so predict the output right after your last
  `/token`, not two ahead.
