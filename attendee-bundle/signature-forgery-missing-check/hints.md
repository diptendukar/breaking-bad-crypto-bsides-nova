# Hints — ECDSA universal forgery (missing range check)

- **Hint 1 (unlock ~6 min):** You can't sign honestly — you don't have the vault's key. So stop
  trying to make a *correct* signature and start looking at the *verifier*. What does a real ECDSA
  verify do first, that this one skips? (Check `/demo_sign`: a real `r, s` are huge. What if yours
  weren't?)

- **Hint 2:** Real ECDSA verification begins with a **range check**: reject unless `1 ≤ r < n` and
  `1 ≤ s < n`. This server never does that. So values *outside* that range — like `0` — reach the
  math that was never meant to see them.

- **Hint 3 (the mechanism):** Verification computes `w = s⁻¹`, then `u1 = z·w`, `u2 = r·w`, then
  `X = u1·G + u2·Q`, and accepts if `X.x == r`. Set **`s = 0`**: the inverse collapses to `0`
  (the buggy library returns `0` instead of erroring), so `u1 = u2 = 0` and `X = 0·G + 0·Q` = the
  point at infinity, whose x-coordinate is treated as `0`.

- **Hint 4 (the forge):** Now pick **`r = 0`** to match: the check becomes `X.x == r` → `0 == 0` →
  **accepted.** So:
  ```python
  r = 0
  s = 0
  ```
  That pair verifies against *any* message and *any* public key. Submit the transfer.

- **Hint 5 (why it matters):** You forged a signature for a key you've never seen. The fix is the one
  line the library dropped: `if not (1 <= r < n and 1 <= s < n): reject`. Run the server with
  `--safe` and your `(0,0)` bounces — same attack, one check restored.
