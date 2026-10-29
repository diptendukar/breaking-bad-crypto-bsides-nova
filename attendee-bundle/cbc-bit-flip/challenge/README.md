# Challenge — CBC bit-flipping ("become root")

Turn `role=user` into `role=root` and read the flag — **without ever knowing the key**.

## Setup
```
pip install requests
```
The **instructor** hosts the server on the LAN. Point your exploit at their address:
```
python client.py http://<instructor-ip>:5001
```

## The target
- `GET /token` gives you `base64( IV[16] || ciphertext )`. You start as `role=user`.
- Plaintext of block 0 is exactly: `role=user&uid=42`  ('user' at indices 5–8).
- `GET /flag?token=...` decrypts your token; if it starts with `role=root`, you get the flag.

## The idea (predict before you code)
In CBC, the first plaintext block is `P0 = decrypt(C0) XOR IV`. The server hands you the IV.
So if you flip a byte of the **IV**, the same byte of `P0` flips by the same amount — you edit
the decrypted message **without the key**. There's no MAC, so nothing notices.

Work out *which* IV bytes to flip, and by how much, to turn `user` into `root`. Fill in the TODO
in `client.py`. (`hints.md` if you're stuck.)

## After you win — the fix
Ask the instructor to restart with `--mac`. Re-run your exploit: it now fails
("integrity check failed"). Authenticating the ciphertext (Encrypt-then-MAC / AEAD) is the fix —
the malleability is still there, but tampering is detected before decryption is trusted.
