# Hints — CBC padding oracle

- **Hint 1 (unlock ~10 min):** You are not attacking the block you want to read. You're attacking
  the block *in front of it*. Submit `forged_prev || target_block` and ask the oracle about the
  padding. What last byte of the decryption makes valid padding? `0x01`.

- **Hint 2:** The server decrypts your two blocks to `decrypt(target) XOR forged_prev`. You don't
  know `decrypt(target)` yet — that's the point. Sweep `forged_prev[15]` over all 256 values;
  exactly one (usually) makes the padding valid, i.e. makes the last byte `0x01`. Then:
  ```
  decrypt(target)[15] = forged_prev[15] XOR 0x01
  ```

- **Hint 3:** Go right-to-left. Once you know `decrypt(target)[15]`, set `forged_prev[15]` so that
  byte becomes `0x02`, then sweep `forged_prev[14]` for the second `0x02`. For pad value `p` at
  position `pos = 16 - p`:
  ```python
  for k in range(pos + 1, 16):
      forged[k] = inter[k] ^ p          # make the known tail decrypt to p
  for guess in range(256):
      forged[pos] = guess
      if padding_ok(bytes(forged) + target):
          inter[pos] = guess ^ p
          break
  ```

- **Hint 4 — the false positive (read this if block 1 has one wrong byte):** When `p == 1`, a hit
  can be a lie. If the real second-to-last decrypted byte is already `0x02`, then `.. 0x02 0x02`
  parses too, and you'll record the wrong last byte. **Guard it:** after a `p==1` hit, flip
  `forged[pos-1]` (XOR `0xFF`) and re-query. Still valid → it was a true `0x01`. Now invalid → you
  hit a longer padding; keep sweeping.

- **Hint 5 — from intermediate to plaintext:** `decrypt(target)` (call it `inter`) is not the
  plaintext yet. XOR the block's *real* previous block back in:
  `plaintext[j] = inter[j] XOR real_prev[j]`. For the first ciphertext block, `real_prev` is the IV.
