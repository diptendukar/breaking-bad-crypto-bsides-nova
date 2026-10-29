# Hints — ECDSA nonce reuse

- **Hint 1 (unlock ~8 min):** Ask `/sign` for two *different* messages and compare the `r` values.
  If they're identical, the nonce `k` was reused — because `r = (k·G).x` depends only on `k`. Same
  `r` ⇒ same `k`. That's the entire vulnerability; everything else is algebra.

- **Hint 2:** Write the two signing equations with the *same* `k`:
  ```
  s1 = k⁻¹ (z1 + r·d)   mod n
  s2 = k⁻¹ (z2 + r·d)   mod n
  ```
  Subtract them. The `r·d` term is identical in both, so it cancels — leaving only `k` and known
  values. That's how you get `k` without knowing `d`.

- **Hint 3 (recover k):** `s1 - s2 = k⁻¹ (z1 - z2)`, so:
  ```python
  k = (z1 - z2) * ec.inv(s1 - s2, ec.N) % ec.N
  ```
  (`ec.inv(x, n)` is modular inverse — "division" mod n.)

- **Hint 4 (recover d):** Put `k` back into `s1·k = z1 + r·d` and solve for `d`:
  ```python
  d = (s1 * k - z1) * ec.inv(r, ec.N) % ec.N
  ```
  Check it: `ec.pub_from_priv(d)` should equal the `(Qx, Qy)` from `/pubkey`. If not, re-check
  which `z`/`s` go together.

- **Hint 5 (the forge):** This part is already written for you — but understand it. You now hold `d`,
  so you *are* the server. `ec.sign(d, MAGIC.encode(), some_random_k)` produces a signature that
  verifies under the server's public key. You can use *any* nonce for your own forgery (even a fresh
  random one — you're not leaking your key to anyone). Submit it to `/flag`.
