# Hints — CBC bit-flipping

- **Hint 1 (unlock ~10 min):** You don't need the key. You need to change 4 bytes of the
  decrypted block 0. What part of the token feeds directly into block 0's decryption?
- **Hint 2:** `P0 = decrypt(C0) XOR IV`. The `decrypt(C0)` part you can't predict — but it's
  the *same* whether you touch the IV or not. So the *change* you make to `IV` is exactly the
  change that appears in `P0`.
- **Hint 3:** To turn plaintext byte `old` into `new` at index `j`: `IV[j] ^= (old ^ new)`.
  You know `old` (`role=user&uid=42`) and `new` (`role=root&uid=42`).
- **Hint 4:** `'user'` is at indices 5,6,7,8. Loop:
  ```python
  for j, old, new in zip(range(5, 9), b"user", b"root"):
      iv[j] ^= old ^ new
  ```
- **Stuck on plumbing?** `blob = bytearray(base64.urlsafe_b64decode(token))`,
  `iv, ct = blob[:16], blob[16:]`, then re-encode `bytes(iv)+bytes(ct)`.
